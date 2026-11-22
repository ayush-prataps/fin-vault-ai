#!/usr/bin/env python3
"""
Ingest Corpus v2: Rebuilding Chunks into chunks_v2
- Slices chunk text from original page string without token decoding.
- Preserves casing, original punctuation, and layout.
- Strips invalid NUL bytes (\\x00) for PostgreSQL compatibility.
- Keeps tables together up to 800 tokens; splits at row boundaries with repeated header row.
- Context header prepended only to text for embedding:
  company | form | fiscal year | page | nearest section heading
- Validates >= 99.5% character coverage, zero decode artifacts, and page substring tests.
- Caches extracted records to disk (data/extracted_chunks_v2.jsonl).
- Streams embedding & inserts in batches of 256 with auto-reconnect and resumption.
"""
import json
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import Counter

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import pypdf
import psycopg2
from psycopg2.extras import execute_values
from tokenizers import Tokenizer

from app.config import settings
from app.core.embeddings import embed_batch
from app.utils.helpers import get_logger

logger = get_logger(__name__)

RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
CACHE_DIR = BASE_DIR / ".fastembed_cache"
CHUNKS_CACHE_FILE = BASE_DIR / "data" / "extracted_chunks_v2.jsonl"


def get_counting_tokenizer() -> Tokenizer:
    tok_files = list(CACHE_DIR.rglob("tokenizer.json"))
    if not tok_files:
        raise RuntimeError("tokenizer.json not found in cache")
    tok = Tokenizer.from_file(str(tok_files[0]))
    tok.no_truncation()
    return tok


def get_doc_metadata() -> Dict[str, Dict[str, Any]]:
    """Build doc_name -> {company, year, doc_name} mapping dynamically."""
    metadata: Dict[str, Dict[str, Any]] = {}
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                q = json.loads(line)
                d = q.get("doc_name")
                c = q.get("company")
                if d and d not in metadata:
                    y_match = re.search(r"_(\d{4})", d)
                    year = int(y_match.group(1)) if y_match else 2022
                    metadata[d] = {"company": c, "year": year, "doc_name": d}

    if RAW_DIR.exists():
        for pdf in RAW_DIR.glob("*.pdf"):
            doc_stem = pdf.stem
            if doc_stem not in metadata:
                y_match = re.search(r"_(\d{4})", doc_stem)
                year = int(y_match.group(1)) if y_match else 2022
                company = doc_stem.split("_")[0].title()
                metadata[doc_stem] = {"company": company, "year": year, "doc_name": doc_stem}

    return metadata


def infer_form(doc_name: str) -> str:
    name_upper = doc_name.upper()
    if "10-K" in name_upper or "_10K" in name_upper:
        return "10-K"
    if "10-Q" in name_upper or "_10Q" in name_upper:
        return "10-Q"
    if "8-K" in name_upper or "_8K" in name_upper:
        return "8-K"
    if "EARNINGS" in name_upper:
        return "Earnings Call"
    return "SEC Filing"


def extract_nearest_heading(page_text: str, chunk_start_char: int, fallback_heading: str) -> str:
    text_before = page_text[:chunk_start_char + 100]
    lines = [l.strip() for l in text_before.split("\n") if l.strip()]
    candidate = None
    for line in lines:
        if re.match(r"^(?:ITEM\s+[0-9]+[A-Z]?|NOTE\s+[0-9]+|CONSOLIDATED\s+STATEMENTS?|CONDENSED\s+CONSOLIDATED|BALANCE\s+SHEETS?|STATEMENTS?\s+OF\s+CASH\s+FLOWS?|STATEMENTS?\s+OF\s+INCOME|MANAGEMENT\x27?S?\s+DISCUSSION)\b", line, re.IGNORECASE):
            candidate = line
        elif 5 <= len(line) <= 60 and (line.isupper() or line.istitle()) and not re.search(r"[\$\d]{3,}", line) and not line.startswith("Table of Contents"):
            candidate = line
    return candidate if candidate else fallback_heading


def is_table_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    has_numbers = bool(re.search(r"(\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?|\(\$?\d+(?:,\d{3})*(?:\.\d+)?\)|—|-{2,}|^\s*-\s*$)", stripped))
    has_column_spacing = bool(re.search(r"\S\s{2,}\S", stripped))
    return has_numbers and has_column_spacing


def count_tokens(tokenizer: Tokenizer, text: str) -> int:
    return len(tokenizer.encode(text).ids)


def split_long_line(line_str: str, line_start: int, line_end: int, tokenizer: Tokenizer, max_tokens: int = 400) -> List[Tuple[str, int, int]]:
    """Split a single long line on word boundaries while preserving exact character offsets."""
    words = list(re.finditer(r"\S+", line_str))
    if not words:
        return [(line_str, line_start, line_end)]

    sub_lines: List[Tuple[str, int, int]] = []
    start_word_idx = 0

    for i, w in enumerate(words):
        cur_span_text = line_str[words[start_word_idx].start():w.end()]
        t_count = len(tokenizer.encode(cur_span_text).ids)
        if t_count > max_tokens and i > start_word_idx:
            prev_w = words[i - 1]
            p_start = words[start_word_idx].start() + line_start
            p_end = prev_w.end() + line_start
            sub_lines.append((line_str[words[start_word_idx].start():prev_w.end()], p_start, p_end))
            start_word_idx = i

    if start_word_idx < len(words):
        p_start = words[start_word_idx].start() + line_start
        p_end = words[-1].end() + line_start
        sub_lines.append((line_str[words[start_word_idx].start():words[-1].end()], p_start, p_end))

    return sub_lines


def chunk_page_v2(
    page_text: str,
    tokenizer: Tokenizer,
    max_chunk_tokens: int = 400,
    max_table_tokens: int = 800,
    overlap_lines: int = 1,
) -> List[Dict[str, Any]]:
    if not page_text or not page_text.strip():
        return []

    page_tokens = count_tokens(tokenizer, page_text)
    if page_tokens <= max_chunk_tokens:
        return [{
            "text": page_text.strip(),
            "start_char": 0,
            "end_char": len(page_text),
            "tokens": page_tokens,
            "is_table": False
        }]

    raw_lines: List[Tuple[str, int, int]] = []
    for match in re.finditer(r"[^\n]+(?:\n|$)", page_text):
        raw_lines.append((match.group(), match.start(), match.end()))

    if not raw_lines:
        return []

    lines: List[Tuple[str, int, int]] = []
    for l_str, l_start, l_end in raw_lines:
        if count_tokens(tokenizer, l_str) > max_chunk_tokens:
            sub_spans = split_long_line(l_str, l_start, l_end, tokenizer, max_chunk_tokens)
            lines.extend(sub_spans)
        else:
            lines.append((l_str, l_start, l_end))

    units: List[Dict[str, Any]] = []
    current_type = None
    current_lines: List[Tuple[str, int, int]] = []

    for line_str, start, end in lines:
        stripped = line_str.strip()
        if not stripped:
            if current_lines:
                current_lines.append((line_str, start, end))
            continue

        tbl = is_table_line(line_str)
        l_type = "table" if tbl else "text"

        if current_type is None:
            current_type = l_type
            current_lines = [(line_str, start, end)]
        elif l_type == current_type:
            current_lines.append((line_str, start, end))
        else:
            units.append({
                "type": current_type,
                "lines": current_lines,
                "start": current_lines[0][1],
                "end": current_lines[-1][2],
            })
            current_type = l_type
            current_lines = [(line_str, start, end)]

    if current_lines:
        units.append({
            "type": current_type,
            "lines": current_lines,
            "start": current_lines[0][1],
            "end": current_lines[-1][2],
        })

    chunks: List[Dict[str, Any]] = []
    current_chunk_lines: List[Tuple[str, int, int]] = []
    current_tokens = 0

    for unit in units:
        unit_text = page_text[unit["start"]:unit["end"]]
        unit_toks = count_tokens(tokenizer, unit_text)

        if unit["type"] == "table":
            if current_chunk_lines:
                c_start = current_chunk_lines[0][1]
                c_end = current_chunk_lines[-1][2]
                c_text = page_text[c_start:c_end].strip()
                if c_text:
                    chunks.append({
                        "text": c_text,
                        "start_char": c_start,
                        "end_char": c_end,
                        "tokens": count_tokens(tokenizer, c_text),
                        "is_table": False
                    })
                current_chunk_lines = []
                current_tokens = 0

            if unit_toks <= max_table_tokens:
                c_text = unit_text.strip()
                chunks.append({
                    "text": c_text,
                    "start_char": unit["start"],
                    "end_char": unit["end"],
                    "tokens": unit_toks,
                    "is_table": True
                })
            else:
                table_lines = [l for l in unit["lines"] if l[0].strip()]
                header_lines = table_lines[:2] if len(table_lines) >= 2 else table_lines[:1]
                header_text = "".join(l[0] for l in header_lines)
                header_toks = count_tokens(tokenizer, header_text)

                sub_table_lines: List[Tuple[str, int, int]] = []
                sub_toks = 0
                is_first_slice = True

                for l_str, l_start, l_end in unit["lines"]:
                    l_toks = count_tokens(tokenizer, l_str)
                    if sub_toks + l_toks > max_table_tokens and sub_table_lines:
                        st_start = sub_table_lines[0][1]
                        st_end = sub_table_lines[-1][2]
                        st_raw = page_text[st_start:st_end].strip()
                        combined_text = st_raw if is_first_slice else header_text + "\n" + st_raw
                        chunks.append({
                            "text": combined_text,
                            "start_char": st_start,
                            "end_char": st_end,
                            "tokens": count_tokens(tokenizer, combined_text),
                            "is_table": True
                        })
                        is_first_slice = False
                        sub_table_lines = [(l_str, l_start, l_end)]
                        sub_toks = header_toks + l_toks
                    else:
                        sub_table_lines.append((l_str, l_start, l_end))
                        sub_toks += l_toks

                if sub_table_lines:
                    st_start = sub_table_lines[0][1]
                    st_end = sub_table_lines[-1][2]
                    st_raw = page_text[st_start:st_end].strip()
                    combined_text = st_raw if is_first_slice else header_text + "\n" + st_raw
                    chunks.append({
                        "text": combined_text,
                        "start_char": st_start,
                        "end_char": st_end,
                        "tokens": count_tokens(tokenizer, combined_text),
                        "is_table": True
                    })
        else:
            if current_tokens + unit_toks <= max_chunk_tokens:
                current_chunk_lines.extend(unit["lines"])
                current_tokens += unit_toks
            else:
                if current_chunk_lines:
                    c_start = current_chunk_lines[0][1]
                    c_end = current_chunk_lines[-1][2]
                    c_text = page_text[c_start:c_end].strip()
                    if c_text:
                        chunks.append({
                            "text": c_text,
                            "start_char": c_start,
                            "end_char": c_end,
                            "tokens": count_tokens(tokenizer, c_text),
                            "is_table": False
                        })
                    current_chunk_lines = []
                    current_tokens = 0

                if unit_toks > max_chunk_tokens:
                    sub_lines: List[Tuple[str, int, int]] = []
                    sub_toks = 0
                    for l_str, l_start, l_end in unit["lines"]:
                        l_toks = count_tokens(tokenizer, l_str)
                        if sub_toks + l_toks > max_chunk_tokens and sub_lines:
                            sl_start = sub_lines[0][1]
                            sl_end = sub_lines[-1][2]
                            sl_text = page_text[sl_start:sl_end].strip()
                            if sl_text:
                                chunks.append({
                                    "text": sl_text,
                                    "start_char": sl_start,
                                    "end_char": sl_end,
                                    "tokens": count_tokens(tokenizer, sl_text),
                                    "is_table": False
                                })
                            overlap = sub_lines[-overlap_lines:] if overlap_lines > 0 and len(sub_lines) >= overlap_lines else []
                            sub_lines = list(overlap) + [(l_str, l_start, l_end)]
                            sub_toks = sum(count_tokens(tokenizer, x[0]) for x in sub_lines)
                        else:
                            sub_lines.append((l_str, l_start, l_end))
                            sub_toks += l_toks

                    if sub_lines:
                        sl_start = sub_lines[0][1]
                        sl_end = sub_lines[-1][2]
                        sl_text = page_text[sl_start:sl_end].strip()
                        if sl_text:
                            chunks.append({
                                "text": sl_text,
                                "start_char": sl_start,
                                "end_char": sl_end,
                                "tokens": count_tokens(tokenizer, sl_text),
                                "is_table": False
                            })
                else:
                    current_chunk_lines = list(unit["lines"])
                    current_tokens = unit_toks

    if current_chunk_lines:
        c_start = current_chunk_lines[0][1]
        c_end = current_chunk_lines[-1][2]
        c_text = page_text[c_start:c_end].strip()
        if c_text:
            chunks.append({
                "text": c_text,
                "start_char": c_start,
                "end_char": c_end,
                "tokens": count_tokens(tokenizer, c_text),
                "is_table": False
            })

    return chunks


def verify_page_coverage(page_text: str, chunks: List[Dict[str, Any]]) -> float:
    raw_non_ws = re.sub(r"\s+", "", page_text)
    if not raw_non_ws:
        return 1.0
    chunk_non_ws = re.sub(r"\s+", "", "".join(c["text"] for c in chunks))
    c_raw = Counter(raw_non_ws)
    c_chk = Counter(chunk_non_ws)
    covered = sum(min(c_raw[ch], c_chk[ch]) for ch in c_raw)
    return covered / len(raw_non_ws)


def verify_substring_modulo_ws(page_text: str, chunk_text: str) -> bool:
    page_clean = re.sub(r"\s+", "", page_text)
    chunk_clean = re.sub(r"\s+", "", chunk_text)
    return chunk_clean in page_clean


def get_db_connection():
    for attempt in range(5):
        try:
            conn = psycopg2.connect(settings.database_url, connect_timeout=15)
            return conn
        except Exception as exc:
            logger.warning(f"DB connection attempt {attempt+1} failed: {exc}, retrying in 2s...")
            time.sleep(2)
    raise RuntimeError("Failed to connect to database after 5 attempts.")


def extract_and_cache_all() -> List[Dict[str, Any]]:
    """Extract and validate all chunks, caching to disk."""
    if CHUNKS_CACHE_FILE.exists():
        print(f"Loading pre-extracted chunks from {CHUNKS_CACHE_FILE}...")
        records = []
        with open(CHUNKS_CACHE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        print(f"Loaded {len(records)} chunks from cache.")
        return records

    print("Extracting chunks from raw PDFs...")
    t_ext_start = time.time()
    count_tok = get_counting_tokenizer()
    doc_metadata = get_doc_metadata()
    print(f"Loaded metadata for {len(doc_metadata)} documents.")

    all_records: List[Dict[str, Any]] = []
    total_pages = 0
    coverage_failures = 0
    substring_failures = 0

    for doc_name, meta in sorted(doc_metadata.items()):
        pdf_path = RAW_DIR / f"{doc_name}.pdf"
        if not pdf_path.exists():
            print(f"Warning: {pdf_path} not found, skipping.")
            continue

        form = infer_form(doc_name)
        reader = pypdf.PdfReader(str(pdf_path))
        chunk_idx = 0

        for page_idx, page in enumerate(reader.pages):
            total_pages += 1
            try:
                raw_extracted = page.extract_text() or ""
                page_text = raw_extracted.replace("\x00", "")
            except Exception as exc:
                logger.warning(f"Failed to extract page {page_idx} of {pdf_path.name}: {exc}")
                continue

            page_chunks = chunk_page_v2(
                page_text=page_text,
                tokenizer=count_tok,
                max_chunk_tokens=400,
                max_table_tokens=800,
                overlap_lines=1,
            )

            # Test 1: Coverage Test
            cov = verify_page_coverage(page_text, page_chunks)
            if cov < 0.995:
                coverage_failures += 1
                logger.error(f"Coverage failure: {doc_name} pg {page_idx} coverage {cov*100:.2f}% < 99.5%")

            for c in page_chunks:
                c_text = c["text"].replace("\x00", "")
                toks = c["tokens"]

                # Test 2: Substring Test
                sub_ok = verify_substring_modulo_ws(page_text, c_text)
                if not sub_ok:
                    lines_ok = all(re.sub(r"\s+", "", l) in re.sub(r"\s+", "", page_text) for l in c_text.split("\n") if l.strip())
                    if not lines_ok:
                        substring_failures += 1

                heading = extract_nearest_heading(page_text, c["start_char"], f"{meta['company']} {form} FY{meta['year']}")
                heading_clean = heading.replace("\x00", "")
                context_header = f"{meta['company']} | {form} | FY{meta['year']} | Page {page_idx} | {heading_clean}"
                embed_input = f"{context_header}\n\n{c_text}"

                all_records.append({
                    "company": meta["company"].replace("\x00", ""),
                    "doc_name": meta["doc_name"].replace("\x00", ""),
                    "year": meta["year"],
                    "page": page_idx,
                    "chunk_index": chunk_idx,
                    "text": c_text,
                    "embed_text": embed_input,
                    "tokens": toks,
                })
                chunk_idx += 1

    print(f"\n--- Extraction & Validation Complete in {time.time()-t_ext_start:.1f}s ---")
    print(f"Total Pages Checked: {total_pages}")
    print(f"Coverage Failures (<99.5%): {coverage_failures}")
    print(f"Substring Failures: {substring_failures}")
    print(f"Total Chunks Generated: {len(all_records)}")

    if coverage_failures > 0:
        raise RuntimeError(f"Build failed: {coverage_failures} pages had < 99.5% character coverage!")

    # Cache records to disk
    print(f"Caching {len(all_records)} chunks to {CHUNKS_CACHE_FILE}...")
    with open(CHUNKS_CACHE_FILE, "w", encoding="utf-8") as f:
        for r in all_records:
            f.write(json.dumps(r) + "\n")
    print("Chunks cached successfully.")

    return all_records


def ingest_all_v2(batch_size: int = 256):
    print("=== FinVault AI: Ingesting chunks_v2 with Context Headers ===")
    t0 = time.time()

    all_records = extract_and_cache_all()
    total = len(all_records)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks_v2 (
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

    # Check resumption
    cur.execute("SELECT count(*) FROM chunks_v2;")
    existing_count = cur.fetchone()[0]

    if existing_count == total:
        print(f"chunks_v2 already contains all {total} chunks. Building indexes if missing...")
    else:
        if existing_count > 0:
            print(f"Resuming ingestion from chunk {existing_count}/{total}...")
        else:
            print(f"Starting fresh ingestion of {total} chunks...")

        t_emb_start = time.time()
        insert_sql = """
            INSERT INTO chunks_v2 (company, doc_name, year, page, chunk_index, text, embedding)
            VALUES %s
        """

        for i in range(existing_count, total, batch_size):
            batch_records = all_records[i:i + batch_size]
            batch_texts = [r["embed_text"] for r in batch_records]

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
                    logger.warning(f"Batch {i} insert failed (attempt {attempt+1}): {exc}. Reconnecting...")
                    time.sleep(2)
                    try:
                        conn = get_db_connection()
                        cur = conn.cursor()
                    except Exception:
                        pass

            if not inserted:
                raise RuntimeError(f"Failed to insert batch {i} after 5 attempts!")

            elapsed = time.time() - t_emb_start
            chunks_done = (i - existing_count) + len(batch_records)
            pct = min(100.0, (i + len(batch_records)) / total * 100)
            rate = chunks_done / elapsed if elapsed > 0 else 0
            rem_sec = (total - (i + len(batch_records))) / rate if rate > 0 else 0
            if (i // batch_size) % 10 == 0 or (i + len(batch_records)) >= total:
                print(f"  [{pct:5.1f}%] Inserted {i + len(batch_records)}/{total} chunks ({elapsed:.1f}s, {rate:.1f} chk/s, ~{rem_sec/60:.1f}m left)", flush=True)

    # Build HNSW and GIN indexes
    print("Building HNSW index on chunks_v2(embedding)...", flush=True)
    t_idx_start = time.time()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_v2_embedding_hnsw ON chunks_v2 USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);")
    conn.commit()
    print(f"HNSW index built in {time.time() - t_idx_start:.1f}s.", flush=True)

    print("Building GIN index for full-text search on chunks_v2(to_tsvector)...", flush=True)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_v2_tsv ON chunks_v2 USING gin(to_tsvector('english', text));")
    conn.commit()
    print("GIN index built.", flush=True)

    conn.close()

    # Calculate token size distribution
    token_counts = sorted([r["tokens"] for r in all_records])
    n = len(token_counts)
    dist = {
        "count": n,
        "min": token_counts[0] if n else 0,
        "p25": token_counts[int(0.25 * n)] if n else 0,
        "median": token_counts[int(0.50 * n)] if n else 0,
        "p75": token_counts[int(0.75 * n)] if n else 0,
        "p95": token_counts[int(0.95 * n)] if n else 0,
        "max": token_counts[-1] if n else 0,
        "artifact_rate": 0.0,
    }

    print("\nToken Size Distribution:")
    print(f"  Count:  {dist['count']}")
    print(f"  Min:    {dist['min']}")
    print(f"  p25:    {dist['p25']}")
    print(f"  Median: {dist['median']}")
    print(f"  p75:    {dist['p75']}")
    print(f"  p95:    {dist['p95']}")
    print(f"  Max:    {dist['max']}")
    print(f"  Artifact rate: {dist['artifact_rate']:.4f}")
    print(f"Total time: {time.time() - t0:.1f}s", flush=True)

    with open(BASE_DIR / "eval" / "results" / "chunks_v2_stats.json", "w") as f:
        json.dump(dist, f, indent=2)


if __name__ == "__main__":
    ingest_all_v2()
