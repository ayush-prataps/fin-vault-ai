#!/usr/bin/env python3
"""
Naive Baseline Ingestion Script (Section D Ablation)
- Ignores page and table structure completely.
- Concatenates full document text.
- Fixed-size token windows (400 tokens, 50 token overlap).
- Page assigned by chunk start offset.
- Same embedding model (BAAI/bge-small-en-v1.5).
- Ingests into separate table chunks_naive with streaming inserts and auto-reconnect.
"""
import json
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import pypdf
import psycopg2
from psycopg2.extras import execute_values

from app.config import settings
from app.core.embeddings import embed_batch
from scripts.ingest_chunks_v2 import get_doc_metadata, get_db_connection, get_counting_tokenizer

RAW_DIR = BASE_DIR / "data" / "raw"
NAIVE_CACHE_FILE = BASE_DIR / "data" / "extracted_chunks_naive.jsonl"


def build_naive_chunks(
    doc_name: str,
    meta: Dict[str, Any],
    tokenizer: Any,
    chunk_tokens: int = 400,
    overlap_tokens: int = 50,
) -> List[Dict[str, Any]]:
    pdf_path = RAW_DIR / f"{doc_name}.pdf"
    if not pdf_path.exists():
        return []

    reader = pypdf.PdfReader(str(pdf_path))
    page_texts = []
    page_char_offsets: List[Tuple[int, int, int]] = []
    current_char = 0

    for page_idx, page in enumerate(reader.pages):
        try:
            ptxt = (page.extract_text() or "").replace("\x00", "")
        except Exception:
            ptxt = ""
        start = current_char
        end = current_char + len(ptxt)
        page_char_offsets.append((start, end, page_idx))
        page_texts.append(ptxt)
        current_char = end + 1

    full_doc_text = "\n".join(page_texts)
    if not full_doc_text.strip():
        return []

    encoding = tokenizer.encode(full_doc_text)
    token_ids = encoding.ids
    offsets = encoding.offsets

    if not token_ids:
        return []

    step = chunk_tokens - overlap_tokens
    chunks: List[Dict[str, Any]] = []
    chunk_idx = 0

    for start_t in range(0, len(token_ids), step):
        end_t = min(start_t + chunk_tokens, len(token_ids))
        start_char = offsets[start_t][0]
        end_char = offsets[end_t - 1][1]

        chunk_text = full_doc_text[start_char:end_char].strip().replace("\x00", "")
        if not chunk_text:
            continue

        assigned_page = 0
        for p_start, p_end, p_idx in page_char_offsets:
            if p_start <= start_char <= p_end:
                assigned_page = p_idx
                break

        chunks.append({
            "company": meta["company"].replace("\x00", ""),
            "doc_name": meta["doc_name"].replace("\x00", ""),
            "year": meta["year"],
            "page": assigned_page,
            "chunk_index": chunk_idx,
            "text": chunk_text,
        })
        chunk_idx += 1

    return chunks


def ingest_naive(batch_size: int = 256):
    print("=== FinVault AI: Ingesting Naive Baseline into chunks_naive ===")
    t0 = time.time()

    tokenizer = get_counting_tokenizer()
    doc_metadata = get_doc_metadata()
    print(f"Loaded metadata for {len(doc_metadata)} documents.")

    if NAIVE_CACHE_FILE.exists():
        print(f"Loading pre-extracted naive chunks from {NAIVE_CACHE_FILE}...")
        all_records = []
        with open(NAIVE_CACHE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    all_records.append(json.loads(line))
        print(f"Loaded {len(all_records)} chunks from cache.")
    else:
        print("Extracting naive fixed-window chunks...")
        all_records = []
        for doc_name, meta in sorted(doc_metadata.items()):
            doc_chunks = build_naive_chunks(doc_name, meta, tokenizer)
            all_records.extend(doc_chunks)
        print(f"Generated {len(all_records)} naive chunks across {len(doc_metadata)} documents.")
        with open(NAIVE_CACHE_FILE, "w", encoding="utf-8") as f:
            for r in all_records:
                f.write(json.dumps(r) + "\n")
        print("Cached naive chunks to disk.")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks_naive (
        id SERIAL PRIMARY KEY,
        company VARCHAR(100) NOT NULL,
        doc_name VARCHAR(255) NOT NULL,
        year INTEGER NOT NULL,
        page INTEGER NOT NULL,
        chunk_index INTEGER NOT NULL,
        text TEXT NOT NULL,
        embedding VECTOR(384)
    );
    """)
    conn.commit()

    cur.execute("SELECT count(*) FROM chunks_naive;")
    existing_count = cur.fetchone()[0]

    total = len(all_records)
    if existing_count == total:
        print(f"chunks_naive already contains all {total} chunks.")
    else:
        if existing_count > 0:
            print(f"Resuming naive ingestion from chunk {existing_count}/{total}...")
        else:
            print(f"Starting naive ingestion of {total} chunks...")

        insert_sql = """
            INSERT INTO chunks_naive (company, doc_name, year, page, chunk_index, text, embedding)
            VALUES %s
        """

        t_emb_start = time.time()
        for i in range(existing_count, total, batch_size):
            batch_records = all_records[i:i + batch_size]
            batch_texts = [r["text"] for r in batch_records]

            batch_embs = embed_batch(batch_texts)
            if not batch_embs:
                raise RuntimeError(f"Embedding batch {i} failed!")

            rows_to_insert = [
                (
                    r["company"],
                    r["doc_name"],
                    r["year"],
                    r["page"],
                    r["chunk_index"],
                    r["text"],
                    emb,
                )
                for r, emb in zip(batch_records, batch_embs)
            ]

            inserted = False
            for attempt in range(5):
                try:
                    execute_values(cur, insert_sql, rows_to_insert, template="(%s, %s, %s, %s, %s, %s, %s::vector)", page_size=256)
                    conn.commit()
                    inserted = True
                    break
                except Exception as exc:
                    time.sleep(2)
                    try:
                        conn = get_db_connection()
                        cur = conn.cursor()
                    except Exception:
                        pass

            if not inserted:
                raise RuntimeError(f"Failed to insert naive batch {i} after 5 attempts!")

            elapsed = time.time() - t_emb_start
            chunks_done = (i - existing_count) + len(batch_records)
            pct = min(100.0, (i + len(batch_records)) / total * 100)
            rate = chunks_done / elapsed if elapsed > 0 else 0
            rem_sec = (total - (i + len(batch_records))) / rate if rate > 0 else 0
            if (i // batch_size) % 20 == 0 or (i + len(batch_records)) >= total:
                print(f"  [{pct:5.1f}%] Inserted {i + len(batch_records)}/{total} naive chunks ({elapsed:.1f}s, {rate:.1f} chk/s, ~{rem_sec/60:.1f}m left)", flush=True)

    print("Building HNSW index on chunks_naive(embedding)...", flush=True)
    t_idx_start = time.time()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_naive_embedding_hnsw ON chunks_naive USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);")
    conn.commit()
    print(f"HNSW index built in {time.time() - t_idx_start:.1f}s.", flush=True)

    conn.close()
    print(f"Naive baseline ingestion complete in {time.time() - t0:.1f}s.")


if __name__ == "__main__":
    ingest_naive()
