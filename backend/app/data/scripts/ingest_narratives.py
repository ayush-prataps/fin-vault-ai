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

            narratives.append(
                {
                    "ticker": ticker,
                    "company": company["company"],
                    "year": int(str(filing.get("report_date") or filing.get("filing_date") or "0")[:4] or 0),
                    "form": filing["form"],
                    "filing_date": filing.get("filing_date"),
                    "report_date": filing.get("report_date"),
                    "doc_type": "sec_filing",
                    "section_title": filing.get("primary_doc_description") or filing.get("primary_document"),
                    "source_file": filing["primary_document"],
                    "text": plain_text,
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
