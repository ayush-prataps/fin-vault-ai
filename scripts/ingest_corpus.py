#!/usr/bin/env python3
"""
Corpus Ingestion Script
Extracts text from filing PDFs, chunks with page-awareness and table preservation,
generates embeddings, and stores in PostgreSQL chunks table.
"""
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

import pypdf
import psycopg2
from psycopg2.extras import execute_values
from transformers import AutoTokenizer

from app.config import settings
from app.core.embeddings import embed_batch
from app.core.schema import init_schema
from app.utils.helpers import get_logger

logger = get_logger(__name__)

RAW_DIR = backend_dir / "data" / "raw"
TOKENIZER_NAME = settings.embedding_model or "BAAI/bge-small-en-v1.5"

DOC_METADATA = {
    "3M_2018_10K": {"company": "3M", "year": 2018, "doc_name": "3M_2018_10K"},
    "3M_2022_10K": {"company": "3M", "year": 2022, "doc_name": "3M_2022_10K"},
    "3M_2023Q2_10Q": {"company": "3M", "year": 2023, "doc_name": "3M_2023Q2_10Q"},
    "AMD_2015_10K": {"company": "AMD", "year": 2015, "doc_name": "AMD_2015_10K"},
    "AMD_2022_10K": {"company": "AMD", "year": 2022, "doc_name": "AMD_2022_10K"},
    "AMERICANEXPRESS_2022_10K": {"company": "American Express", "year": 2022, "doc_name": "AMERICANEXPRESS_2022_10K"},
    "BOEING_2018_10K": {"company": "Boeing", "year": 2018, "doc_name": "BOEING_2018_10K"},
    "BOEING_2022_10K": {"company": "Boeing", "year": 2022, "doc_name": "BOEING_2022_10K"},
}


def _is_table_line(line: str) -> bool:
    """Check if a line looks like tabular financial data (numbers, currency, dashes)."""
    stripped = line.strip()
    if not stripped:
        return False
    # Check for presence of numbers with financial formatting
    has_numbers = bool(re.search(r"(\$?\d{1,3}(,\d{3})*(\.\d+)?|\(\d+\)|-\s*$)", stripped))
    has_spaces = bool(re.search(r"\s{2,}", stripped))
    return has_numbers and has_spaces


def chunk_page_text(
    text: str,
    tokenizer: Any,
    chunk_size: int = 400,
    overlap: int = 50,
) -> List[str]:
    """
    Chunk page text using a real tokenizer while keeping tables intact where possible.
    """
    cleaned = text.replace("\x00", "").strip()
    if not cleaned:
        return []

    tokens = tokenizer.encode(cleaned, add_special_tokens=False)
    # If the page fits in chunk_size, return it whole
    if len(tokens) <= chunk_size + 50:
        return [cleaned]

    # Split into structural blocks (paragraphs / tables)
    lines = cleaned.split("\n")
    blocks: List[str] = []
    current_block: List[str] = []
    in_table = False

    for line in lines:
        is_table = _is_table_line(line)
        if is_table != in_table and current_block:
            blocks.append("\n".join(current_block))
            current_block = [line]
            in_table = is_table
        else:
            current_block.append(line)
            in_table = is_table

    if current_block:
        blocks.append("\n".join(current_block))

    # Assemble blocks into chunks up to chunk_size tokens
    chunks: List[str] = []
    current_chunk_tokens: List[int] = []
    current_chunk_text: List[str] = []

    for block in blocks:
        block_tokens = tokenizer.encode(block, add_special_tokens=False)
        if not block_tokens:
            continue

        if len(current_chunk_tokens) + len(block_tokens) <= chunk_size:
            current_chunk_tokens.extend(block_tokens)
            current_chunk_text.append(block)
        else:
            if current_chunk_text:
                chunks.append("\n".join(current_chunk_text).strip())

            # If a single block exceeds chunk_size, slice it with overlap
            if len(block_tokens) > chunk_size:
                start = 0
                while start < len(block_tokens):
                    end = min(start + chunk_size, len(block_tokens))
                    sub_text = tokenizer.decode(block_tokens[start:end], skip_special_tokens=True)
                    if sub_text.strip():
                        chunks.append(sub_text.strip())
                    start = end - overlap if end - overlap > start else end
                current_chunk_tokens = []
                current_chunk_text = []
            else:
                # Start new chunk with current block
                current_chunk_tokens = list(block_tokens)
                current_chunk_text = [block]

    if current_chunk_text:
        chunks.append("\n".join(current_chunk_text).strip())

    return [c for c in chunks if len(c.strip()) > 30]


def process_pdf(
    pdf_path: Path,
    metadata: Dict[str, Any],
    tokenizer: Any,
    chunk_size: int = 400,
    overlap: int = 50,
) -> List[Dict[str, Any]]:
    """Extract and chunk a single PDF with page awareness."""
    reader = pypdf.PdfReader(pdf_path)
    records: List[Dict[str, Any]] = []

    chunk_idx = 0
    for page_idx, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text() or ""
        except Exception as exc:
            logger.warning(f"Failed to extract page {page_idx} of {pdf_path.name}: {exc}")
            continue

        page_chunks = chunk_page_text(
            text=page_text,
            tokenizer=tokenizer,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for chunk_text in page_chunks:
            records.append({
                "company": metadata["company"],
                "doc_name": metadata["doc_name"],
                "year": metadata["year"],
                "page": page_idx,
                "chunk_index": chunk_idx,
                "text": chunk_text,
            })
            chunk_idx += 1

    return records


def ingest_all(chunk_size: int = 400, overlap: int = 50):
    """Main ingestion pipeline."""
    print("=== FinVault AI: Ingesting Real SEC Filings ===")
    t0 = time.time()

    # 1. Ensure schema is ready
    if not init_schema():
        print("Error: Database schema initialization failed.", file=sys.stderr)
        sys.exit(1)

    # 2. Load tokenizer
    print(f"Loading tokenizer: {TOKENIZER_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)

    # 3. Process all PDFs
    all_chunks: List[Dict[str, Any]] = []
    for doc_name, meta in sorted(DOC_METADATA.items()):
        pdf_path = RAW_DIR / f"{doc_name}.pdf"
        if not pdf_path.exists():
            print(f"Warning: {pdf_path} not found, skipping.")
            continue

        print(f"Parsing {doc_name}.pdf ({meta['company']}, FY{meta['year']})...")
        doc_chunks = process_pdf(
            pdf_path=pdf_path,
            metadata=meta,
            tokenizer=tokenizer,
            chunk_size=chunk_size,
            overlap=overlap,
        )
        print(f"  -> Generated {len(doc_chunks)} page-aware chunks")
        all_chunks.extend(doc_chunks)

    print(f"\nTotal chunks to embed and store: {len(all_chunks)}")

    # 4. Generate embeddings in batches
    print("Generating embeddings with BAAI/bge-small-en-v1.5...")
    batch_size = 64
    texts = [c["text"] for c in all_chunks]
    embeddings: List[List[float]] = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        emb_batch = embed_batch(batch)
        if not emb_batch:
            raise RuntimeError(f"Embedding batch {i} failed")
        embeddings.extend(emb_batch)
        if (i // batch_size) % 5 == 0 or i + batch_size >= len(texts):
            print(f"  Embedded {min(i + batch_size, len(texts))}/{len(texts)} chunks...")

    # Attach embeddings to records
    for c, emb in zip(all_chunks, embeddings):
        c["embedding"] = "[" + ",".join(f"{float(v):.8f}" for v in emb) + "]"

    # 5. Store in PostgreSQL
    print("\nInserting chunks into Neon PostgreSQL...")
    conn = psycopg2.connect(settings.database_url)
    with conn.cursor() as cur:
        # Clear previous chunks for a clean slate
        cur.execute("TRUNCATE TABLE chunks RESTART IDENTITY;")

        insert_query = """
            INSERT INTO chunks (company, doc_name, year, page, chunk_index, text, embedding)
            VALUES %s
        """
        values = [
            (
                c["company"],
                c["doc_name"],
                c["year"],
                c["page"],
                c["chunk_index"],
                c["text"].replace("\x00", ""),
                c["embedding"],
            )
            for c in all_chunks
        ]
        execute_values(cur, insert_query, values, page_size=500)
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM chunks;")
        total_in_db = cur.fetchone()[0]

    conn.close()

    elapsed = time.time() - t0
    print(f"\nSUCCESS: Ingested {total_in_db} chunks in {elapsed:.1f}s")


if __name__ == "__main__":
    ingest_all()
