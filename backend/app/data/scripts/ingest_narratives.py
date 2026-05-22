#!/usr/bin/env python3
"""
Ingest narrative financial data (earnings transcripts) into pgvector-backed PostgreSQL.

This script:
1. Fetches SEC filings with narrative disclosure text
2. Chunks narrative text
3. Generates embeddings
4. Stores in PostgreSQL with pgvector embeddings
5. Registers in PostgreSQL

Phase 2: Hybrid Narrative Retrieval
"""
import sys
import os
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional, Iterable

import pandas as pd

# Add backend to path (go up 4 levels from backend/app/data/scripts/)
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.config import settings, DATA_OUTPUT_DIR
from app.data.pipeline.sec_data_fetcher import SECDataFetcher
from app.data.adapter import (
    chunk_text,
    clear_narrative_documents,
    ensure_narrative_store_ready,
    embed_and_store_narrative,
)
from app.core.embeddings import embed_text
from app.utils.helpers import get_logger

logger = get_logger(__name__)

HIGH_SIGNAL_SECTIONS = {
    "business": re.compile(r"\bitem\s*1\s*[\.:\-]?\s*business\b", re.IGNORECASE),
    "risk_factors": re.compile(r"\bitem\s*1a\s*[\.:\-]?\s*risk\s+factors\b", re.IGNORECASE),
    "md&a": re.compile(
        r"\bitem\s*7\s*[\.:\-]?\s*management(?:['’]s|\s+s|s)?\s+discussion\s+and\s+analysis\b",
        re.IGNORECASE,
    ),
}

ITEM_HEADING_PATTERN = re.compile(r"\bitem\s*\d+[a-z]?\b", re.IGNORECASE)


def _normalize_section_title(section_name: str) -> str:
    if section_name == "business":
        return "Item 1. Business"
    if section_name == "risk_factors":
        return "Item 1A. Risk Factors"
    return "Item 7. Management's Discussion and Analysis"


def extract_high_signal_sections(plain_text: str) -> list[tuple[str, str]]:
    """Extract high-signal 10-K sections from plain text using heading anchors."""
    text = re.sub(r"\s+", " ", plain_text or "").strip()
    if len(text) < 500:
        return []

    extracted: list[tuple[str, str]] = []

    def find_section_end(start_index: int) -> int:
        search_from = start_index + 50
        while True:
            next_heading = ITEM_HEADING_PATTERN.search(text, search_from)
            if not next_heading:
                return len(text)
            if next_heading.start() - start_index < 3000:
                search_from = next_heading.end()
                continue
            return next_heading.start()

    for section_name, pattern in HIGH_SIGNAL_SECTIONS.items():
        best_section: Optional[str] = None
        best_word_count = 0

        for match in pattern.finditer(text):
            start = match.start()
            toc_window = text[max(0, start - 1200): min(len(text), start + 1200)].lower()
            if "table of contents" in toc_window:
                continue

            end = find_section_end(start)
            section_text = text[start:end].strip()
            word_count = len(section_text.split())
            if word_count < 250:
                continue

            if word_count > best_word_count:
                best_word_count = word_count
                best_section = section_text

        if best_section:
            extracted.append((_normalize_section_title(section_name), best_section))

    deduped: list[tuple[str, str]] = []
    seen_signatures = set()
    for section_title, section_text in sorted(extracted, key=lambda item: len(item[1]), reverse=True):
        signature = section_text[:2000].lower()
        if signature in seen_signatures:
            continue
        seen_signatures.add(signature)
        deduped.append((section_title, section_text))

    return deduped


def is_noisy_chunk(text: str) -> bool:
    """Heuristic filter to remove low-signal narrative chunks."""
    cleaned = (text or "").strip()
    if not cleaned:
        return True

    words = cleaned.split()
    if len(words) < 45:
        return True

    alpha_chars = sum(1 for ch in cleaned if ch.isalpha())
    digit_chars = sum(1 for ch in cleaned if ch.isdigit())
    total_chars = max(len(cleaned), 1)
    alpha_ratio = alpha_chars / total_chars
    digit_ratio = digit_chars / total_chars

    if alpha_ratio < 0.55 or digit_ratio > 0.35:
        return True

    lower = cleaned.lower()
    noisy_markers = [
        "us-gaap",
        "xbrl",
        "xmlns",
        "schema",
        "contextref",
        "defref",
        "linkbase",
    ]
    marker_hits = sum(marker in lower for marker in noisy_markers)
    if marker_hits >= 2:
        return True

    return False


def filter_narrative_chunks(chunks: list[str]) -> list[str]:
    """Drop low-signal chunks and exact duplicates while preserving order."""
    filtered: list[str] = []
    seen = set()

    for chunk in chunks:
        normalized = re.sub(r"\s+", " ", chunk).strip()
        if is_noisy_chunk(normalized):
            continue

        signature = normalized[:500].lower()
        if signature in seen:
            continue

        seen.add(signature)
        filtered.append(normalized)

    return filtered

class _HtmlTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data:
            self.parts.append(data)

    def get_text(self) -> str:
        text = " ".join(self.parts)
        text = re.sub(r"\s+", " ", text)
        return text.strip()


def strip_html(text: str) -> str:
    """Convert SEC HTML filings into embeddable plain text."""
    if not text:
        return ""

    extractor = _HtmlTextExtractor()
    extractor.feed(text)
    plain_text = extractor.get_text()
    plain_text = re.sub(r"\s{2,}", " ", plain_text)
    return plain_text.strip()


def discover_bulk_download_companies(bulk_download_dir: Optional[Path] = None) -> list[dict]:
    """Load company metadata from bulk download outputs."""
    bulk_dir = Path(bulk_download_dir or DATA_OUTPUT_DIR / "bulk_download")
    summary_files = sorted(bulk_dir.glob("summary_*.csv"))
    if not summary_files:
        return []

    summary_df = pd.read_csv(summary_files[0])
    companies = []
    for _, row in summary_df.iterrows():
        ticker = str(row.get("Ticker", "")).strip().upper()
        company = str(row.get("Company", "")).strip()
        cik = row.get("CIK")
        if not ticker or not company or pd.isna(cik):
            continue

        companies.append(
            {
                "ticker": ticker,
                "company": company,
                "cik": str(int(cik)),
            }
        )

    return companies


def load_real_narratives(
    tickers: Optional[Iterable[str]] = None,
    filings_per_company: int = 1,
    form_type: str = "10-K",
) -> list[dict]:
    """Fetch real SEC filing text for companies already present in bulk downloads."""
    fetcher = SECDataFetcher()
    target_tickers = {ticker.upper() for ticker in tickers} if tickers else None
    narratives: list[dict] = []

    for company in discover_bulk_download_companies():
        ticker = company["ticker"]
        if target_tickers and ticker not in target_tickers:
            continue

        filings = fetcher.list_recent_filings(company["cik"], form_type=form_type, limit=filings_per_company)
        for filing in filings:
            filing_text = fetcher.get_filing_text(
                cik=company["cik"],
                accession_number_nodash=filing["accession_number_nodash"],
                primary_document=filing["primary_document"],
            )
            if not filing_text:
                logger.warning("No filing text available for %s %s", ticker, filing["accession_number"])
                continue

            plain_text = strip_html(filing_text)
            if len(plain_text) < 200:
                logger.warning("Skipping short filing text for %s %s", ticker, filing["accession_number"])
                continue

            high_signal_sections = extract_high_signal_sections(plain_text)
            if not high_signal_sections:
                logger.warning(
                    "No high-signal sections found for %s %s; skipping filing",
                    ticker,
                    filing["accession_number"],
                )
                continue

            for section_title, section_text in high_signal_sections:
                narratives.append(
                    {
                        "ticker": ticker,
                        "company": company["company"],
                        "year": int(str(filing.get("report_date") or filing.get("filing_date") or "0")[:4] or 0),
                        "form": filing["form"],
                        "filing_date": filing.get("filing_date"),
                        "report_date": filing.get("report_date"),
                        "doc_type": "sec_filing",
                        "section_title": section_title,
                        "source_file": filing["primary_document"],
                        "text": section_text,
                    }
                )

    return narratives


def ingest_narrative(
    ticker: str,
    company: str,
    year: int,
    text: str,
    section_title: str,
    source_file: str,
    collection_name: str = "financial_narratives"
) -> int:
    """
    Ingest a single SEC filing narrative into PostgreSQL.
    
    Args:
        ticker: Stock ticker
        company: Company name
        year: Fiscal year
        text: Filing text to chunk and embed
        section_title: Filing title or section heading
        source_file: Filing source filename
        collection_name: Narrative store name (retained for compatibility)
        
    Returns:
        Number of chunks successfully ingested
    """
    ingested = 0

    if text and len(text.strip()) > 100:
        chunks = chunk_text(text, chunk_size=500, overlap=80)
        chunks = filter_narrative_chunks(chunks)
        for idx, chunk in enumerate(chunks):
            try:
                embed_and_store_narrative(
                    text=chunk,
                    collection_name=collection_name,
                    company=company,
                    ticker=ticker,
                    year=year,
                    doc_type="sec_filing",
                    embeddings_model_fn=embed_text,
                    chunk_id=idx,
                    total_chunks=len(chunks),
                    section_title=section_title,
                    source_file=source_file,
                )
                ingested += 1
            except Exception as exc:
                logger.error(f"Failed to ingest chunk {idx}: {exc}")
    
    return ingested


def main():
    """Main ingestion workflow."""
    tickers_arg = sys.argv[1:]
    print("\n" + "="*70)
    print("Phase 2: SEC Filing Narrative Ingestion into pgvector")
    print("="*70 + "\n")
    
    # Step 1: Ensure pgvector storage is ready
    print("📝 Step 1: Preparing pgvector narrative storage...")
    if not ensure_narrative_store_ready():
        print("❌ Failed to prepare pgvector narrative storage")
        return False
    print("✅ pgvector storage ready\n")

    print("🧹 Step 1b: Clearing existing narrative documents for a clean rebuild...")
    if not clear_narrative_documents():
        print("❌ Failed to clear existing narrative documents")
        return False
    print("✅ Cleared old narrative documents\n")
    
    # Step 2: Load real SEC narrative data
    print("📚 Step 2: Loading SEC filing narratives...")
    narratives = load_real_narratives(tickers=tickers_arg or None)
    if not narratives:
        print("❌ No SEC filing narratives were found")
        print("   Run the bulk download pipeline first, or verify SEC connectivity and CIK metadata")
        return False

    print(f"✅ Loaded {len(narratives)} filing narratives\n")
    
    # Step 3: Ingest narratives
    print("🔄 Step 3: Ingesting narratives into PostgreSQL...")
    total_chunks = 0
    
    for narrative in narratives:
        ingest_key = f"{narrative['ticker']}_{narrative['year']}_{narrative['form']}"
        print(f"\n  Ingesting {ingest_key}...")
        
        chunks_ingested = ingest_narrative(
            ticker=narrative['ticker'],
            company=narrative['company'],
            year=narrative['year'],
            text=narrative['text'],
            section_title=narrative['section_title'],
            source_file=narrative['source_file']
        )
        
        total_chunks += chunks_ingested
        print(f"    ✅ {chunks_ingested} chunks ingested")
    
    print(f"\n✅ Ingestion complete: {total_chunks} chunks total\n")
    
    # Step 4: Verify with a test search
    print("🔍 Step 4: Verifying with test search...")
    try:
        from app.core.retrieval import retrieve_narrative_context
        from app.core.embeddings import embed_text
        
        test_query = "What is Apple's AI strategy?"
        test_embedding = embed_text(test_query)
        
        results = retrieve_narrative_context(
            query_embedding=test_embedding,
            tickers=["AAPL"],
            limit=3
        )
        
        if results:
            print(f"✅ Found {len(results)} relevant narrative chunks for test query\n")
            for i, chunk in enumerate(results, 1):
                print(f"   [{i}] {chunk['doc_type']} - {chunk['ticker']} FY{chunk['year']}")
                print(f"       Score: {chunk['score']:.3f}")
                print(f"       Section: {chunk['section_title']}\n")
        else:
            print("⚠️  No results found - pgvector store may be empty\n")
        
    except Exception as exc:
        logger.error(f"Verification failed: {exc}")
    
    print("="*70)
    print("Phase 2 Narrative Ingestion Complete")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
