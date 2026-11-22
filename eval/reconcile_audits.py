#!/usr/bin/env python3
"""
Evidence Audit Reconciliation for Dev Split (91 items).
Measures exact, whitespace-stripped, case-folded whitespace-stripped,
alphanumeric-only case-folded, numeric-token recall >= 0.8, and word-token recall >= 0.8
against:
(i) raw pypdf page text
(ii) stored chunks of the gold page (single chunk and concatenated chunks)
"""
import json
import re
import difflib
import sys
from pathlib import Path
from collections import Counter
import pypdf
import psycopg2

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
SPLIT_PATH = BASE_DIR / "eval" / "results" / "split_75_75.json"

from app.config import settings

def strip_ws(text: str) -> str:
    return re.sub(r"\s+", "", text)

def case_fold_strip_ws(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())

def alnum_case_fold(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())

def extract_numeric_tokens(text: str):
    # Extract digit sequences or numbers (e.g. 34,229 -> 34229 or decimals)
    # Strip commas from numbers
    cleaned = re.sub(r",(\d{3})", r"\1", text)
    tokens = re.findall(r"\b\d+(?:\.\d+)?\b", cleaned)
    return tokens

def numeric_recall(gold_text: str, target_text: str) -> float:
    gold_nums = extract_numeric_tokens(gold_text)
    if not gold_nums:
        return 1.0  # no numbers to match
    target_nums = set(extract_numeric_tokens(target_text))
    # Count how many gold numeric tokens appear in target
    matched = sum(1 for n in gold_nums if n in target_nums)
    return matched / len(gold_nums)

def extract_word_tokens(text: str):
    return re.findall(r"\b[a-z0-9]+\b", text.lower())

def word_recall(gold_text: str, target_text: str) -> float:
    gold_words = extract_word_tokens(gold_text)
    if not gold_words:
        return 1.0
    target_words = set(extract_word_tokens(target_text))
    matched = sum(1 for w in gold_words if w in target_words)
    return matched / len(gold_words)

def main():
    with open(SPLIT_PATH) as f:
        split = json.load(f)
    dev_ids = set(split["dev_ids"])

    conn = psycopg2.connect(settings.database_url)
    cur = conn.cursor()

    # Load dev evidence items
    dev_evidence = []
    with open(DATA_PATH) as f:
        for line in f:
            q = json.loads(line)
            if q["financebench_id"] in dev_ids:
                for ev in q.get("evidence", []):
                    dev_evidence.append({
                        "fb_id": q["financebench_id"],
                        "company": q.get("company"),
                        "doc_name": ev.get("doc_name") or q.get("doc_name"),
                        "page_num": int(ev.get("evidence_page_num")),
                        "evidence_text": ev.get("evidence_text", "")
                    })

    print(f"Total dev evidence items: {len(dev_evidence)}")

    # Cache raw pypdf pages: (doc_name, page_num) -> text
    raw_pages = {}
    # Fetch stored chunks from db: (doc_name, page_num) -> list of texts
    cur.execute("SELECT doc_name, page, text FROM chunks ORDER BY doc_name, page, chunk_index;")
    db_chunks = {}
    for doc, pg, txt in cur.fetchall():
        key = (doc, pg)
        if key not in db_chunks:
            db_chunks[key] = []
        db_chunks[key].append(txt)

    results = {
        "raw_pypdf": Counter(),
        "stored_single": Counter(),
        "stored_concat": Counter()
    }

    category_d_cases = []
    dropped_by_chunker = []

    for item in dev_evidence:
        doc = item["doc_name"]
        pg = item["page_num"]
        ev = item["evidence_text"]

        # Raw pypdf text
        if (doc, pg) not in raw_pages:
            pdf_path = RAW_DIR / f"{doc}.pdf"
            if not pdf_path.exists():
                print(f"Missing PDF: {pdf_path}")
                raw_text = ""
            else:
                reader = pypdf.PdfReader(str(pdf_path))
                if pg < len(reader.pages):
                    raw_text = reader.pages[pg].extract_text() or ""
                else:
                    raw_text = ""
            raw_pages[(doc, pg)] = raw_text

        raw = raw_pages[(doc, pg)]
        chunks = db_chunks.get((doc, pg), [])
        concat_chunks = "\n".join(chunks)

        # Check raw pypdf
        r_exact = ev in raw
        r_ws = strip_ws(ev) in strip_ws(raw)
        r_cf_ws = case_fold_strip_ws(ev) in case_fold_strip_ws(raw)
        r_alnum = alnum_case_fold(ev) in alnum_case_fold(raw)
        r_num = numeric_recall(ev, raw) >= 0.8
        r_word = word_recall(ev, raw) >= 0.8

        if r_exact: results["raw_pypdf"]["exact"] += 1
        if r_ws: results["raw_pypdf"]["ws"] += 1
        if r_cf_ws: results["raw_pypdf"]["cf_ws"] += 1
        if r_alnum: results["raw_pypdf"]["alnum"] += 1
        if r_num: results["raw_pypdf"]["num_0.8"] += 1
        if r_word: results["raw_pypdf"]["word_0.8"] += 1

        # Check stored single chunk
        s_exact = any(ev in c for c in chunks)
        s_ws = any(strip_ws(ev) in strip_ws(c) for c in chunks)
        s_cf_ws = any(case_fold_strip_ws(ev) in case_fold_strip_ws(c) for c in chunks)
        s_alnum = any(alnum_case_fold(ev) in alnum_case_fold(c) for c in chunks)
        s_num = any(numeric_recall(ev, c) >= 0.8 for c in chunks)
        s_word = any(word_recall(ev, c) >= 0.8 for c in chunks)

        if s_exact: results["stored_single"]["exact"] += 1
        if s_ws: results["stored_single"]["ws"] += 1
        if s_cf_ws: results["stored_single"]["cf_ws"] += 1
        if s_alnum: results["stored_single"]["alnum"] += 1
        if s_num: results["stored_single"]["num_0.8"] += 1
        if s_word: results["stored_single"]["word_0.8"] += 1

        # Check stored concat chunks
        c_exact = ev in concat_chunks
        c_ws = strip_ws(ev) in strip_ws(concat_chunks)
        c_cf_ws = case_fold_strip_ws(ev) in case_fold_strip_ws(concat_chunks)
        c_alnum = alnum_case_fold(ev) in alnum_case_fold(concat_chunks)
        c_num = numeric_recall(ev, concat_chunks) >= 0.8
        c_word = word_recall(ev, concat_chunks) >= 0.8

        if c_exact: results["stored_concat"]["exact"] += 1
        if c_ws: results["stored_concat"]["ws"] += 1
        if c_cf_ws: results["stored_concat"]["cf_ws"] += 1
        if c_alnum: results["stored_concat"]["alnum"] += 1
        if c_num: results["stored_concat"]["num_0.8"] += 1
        if c_word: results["stored_concat"]["word_0.8"] += 1

        # Check category (d): evidence not in raw page text even whitespace-insensitively
        # Now under case-folding and alphanumeric normalization:
        if not r_alnum:
            category_d_cases.append({
                "fb_id": item["fb_id"],
                "doc_name": doc,
                "page": pg,
                "evidence_text": ev,
                "raw_text": raw
            })

        # Check dropped by chunker: present in raw pypdf (alnum) but NOT in concat chunks (alnum)
        if r_alnum and not c_alnum:
            dropped_by_chunker.append({
                "fb_id": item["fb_id"],
                "doc_name": doc,
                "page": pg,
                "evidence_text": ev,
                "raw_len": len(raw),
                "chunks_len": len(concat_chunks),
                "num_chunks": len(chunks)
            })

    print("\n--- RECONCILIATION TABLE (91 Dev Evidence Items) ---")
    header = f"{'Normalization Level':<35} | {'(i) Raw PyPDF':<18} | {'(ii) Stored Single':<18} | {'(iii) Stored Concat':<18}"
    print(header)
    print("-" * len(header))
    levels = [
        ("Exact", "exact"),
        ("Whitespace-stripped", "ws"),
        ("Case-folded + Whitespace-stripped", "cf_ws"),
        ("Alphanumeric-only Case-folded", "alnum"),
        ("Numeric-token Recall (>=0.8)", "num_0.8"),
        ("Word-token Recall (>=0.8)", "word_0.8"),
    ]
    for name, key in levels:
        r_val = results["raw_pypdf"][key]
        s_val = results["stored_single"][key]
        c_val = results["stored_concat"][key]
        print(f"{name:<35} | {r_val:>3}/91 ({r_val/91*100:>5.1f}%) | {s_val:>3}/91 ({s_val/91*100:>5.1f}%) | {c_val:>3}/91 ({c_val/91*100:>5.1f}%)")

    print(f"\nCategory (d) failures under alnum normalization: {len(category_d_cases)}")
    print(f"Evidence dropped by chunker (in raw alnum, not in concat chunks alnum): {len(dropped_by_chunker)}")
    for d in dropped_by_chunker:
        print(f"  Dropped: {d['fb_id']} {d['doc_name']} pg {d['page']} (raw len {d['raw_len']}, concat chunks len {d['chunks_len']}, {d['num_chunks']} chunks)")

    # Save details to json
    output_data = {
        "counts": {
            k: dict(v) for k, v in results.items()
        },
        "category_d_count": len(category_d_cases),
        "dropped_by_chunker": dropped_by_chunker,
        "category_d_examples": category_d_cases[:5]
    }
    with open(BASE_DIR / "eval" / "results" / "evidence_audit_reconciliation.json", "w") as f:
        json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    main()
