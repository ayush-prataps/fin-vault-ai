#!/usr/bin/env python3
"""
Step 1: Read-only diagnostic script for FinanceBench retrieval.
Computes:
1. Document-level and page-level hit rates at k=5 and k=10 (Config A and B).
2. Page indexing audit across 5 distinct companies with printed page vs 0-indexed page.
3. Multi-page evidence breakdown and scoring behavior.
4. 10 table-heavy chunks verbatim.
5. Top 3 failure causes with exact counts.
Saves results to eval/results/diagnosis_step1.json.
"""
import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import pypdf
import psycopg2
from app.config import settings
from app.core.embeddings import embed_text
from app.core.vector import search_chunks
from eval.run_eval import is_retrieval_hit

DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
RAW_DIR = BASE_DIR / "data" / "raw"
RESULTS_DIR = BASE_DIR / "eval" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def run_diagnosis():
    print("=== Step 1: Retrieval Diagnosis (Read-Only) ===")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        questions = [json.loads(line) for line in f if line.strip()]

    total_q = len(questions)
    print(f"Loaded {total_q} questions from {DATA_PATH.name}")

    # 1. Document and Page-Level Retrieval Benchmark
    print("\nRunning retrieval over all 150 questions (Config A & Config B)...")
    
    # Counts
    doc_hits_a_5 = 0
    doc_hits_a_10 = 0
    page_hits_a_5 = 0
    page_hits_a_10 = 0

    doc_hits_b_5 = 0
    doc_hits_b_10 = 0
    page_hits_b_5 = 0
    page_hits_b_10 = 0

    # Multi-page strict all-hits
    page_all_hits_b_5 = 0
    page_all_hits_b_10 = 0

    failures_a_10 = []
    failures_b_10 = []

    t0 = time.time()
    for idx, q in enumerate(questions, 1):
        q_id = q.get("financebench_id", f"q_{idx}")
        company = q.get("company")
        target_doc = (q.get("doc_name") or "").strip().upper()
        evidence_list = q.get("evidence", [])
        gold_pages = {e.get("evidence_page_num") for e in evidence_list}

        q_emb = embed_text(q.get("question", ""))

        # Config A: Unfiltered
        chunks_a_10 = search_chunks(query_embedding=q_emb, company=None, top_k=10)
        chunks_a_5 = chunks_a_10[:5]

        doc_hit_a_5 = any((c.get("doc_name") or "").strip().upper() == target_doc for c in chunks_a_5)
        doc_hit_a_10 = any((c.get("doc_name") or "").strip().upper() == target_doc for c in chunks_a_10)
        page_hit_a_5 = any(is_retrieval_hit(c, evidence_list) for c in chunks_a_5)
        page_hit_a_10 = any(is_retrieval_hit(c, evidence_list) for c in chunks_a_10)

        if doc_hit_a_5: doc_hits_a_5 += 1
        if doc_hit_a_10: doc_hits_a_10 += 1
        if page_hit_a_5: page_hits_a_5 += 1
        if page_hit_a_10: page_hits_a_10 += 1

        if not page_hit_a_10:
            failures_a_10.append({
                "id": q_id,
                "company": company,
                "target_doc": target_doc,
                "gold_pages": list(gold_pages),
                "doc_hit": doc_hit_a_10,
                "retrieved_docs": [(c.get("doc_name"), c.get("page")) for c in chunks_a_10],
            })

        # Config B: Filtered by Company
        chunks_b_10 = search_chunks(query_embedding=q_emb, company=company, top_k=10)
        chunks_b_5 = chunks_b_10[:5]

        doc_hit_b_5 = any((c.get("doc_name") or "").strip().upper() == target_doc for c in chunks_b_5)
        doc_hit_b_10 = any((c.get("doc_name") or "").strip().upper() == target_doc for c in chunks_b_10)
        page_hit_b_5 = any(is_retrieval_hit(c, evidence_list) for c in chunks_b_5)
        page_hit_b_10 = any(is_retrieval_hit(c, evidence_list) for c in chunks_b_10)

        if doc_hit_b_5: doc_hits_b_5 += 1
        if doc_hit_b_10: doc_hits_b_10 += 1
        if page_hit_b_5: page_hits_b_5 += 1
        if page_hit_b_10: page_hits_b_10 += 1

        # Check all gold pages retrieved
        retrieved_b_pages_5 = {c.get("page") for c in chunks_b_5 if (c.get("doc_name") or "").strip().upper() == target_doc}
        retrieved_b_pages_10 = {c.get("page") for c in chunks_b_10 if (c.get("doc_name") or "").strip().upper() == target_doc}
        if gold_pages.issubset(retrieved_b_pages_5):
            page_all_hits_b_5 += 1
        if gold_pages.issubset(retrieved_b_pages_10):
            page_all_hits_b_10 += 1

        if not page_hit_b_10:
            failures_b_10.append({
                "id": q_id,
                "company": company,
                "target_doc": target_doc,
                "gold_pages": list(gold_pages),
                "doc_hit": doc_hit_b_10,
                "retrieved_docs": [(c.get("doc_name"), c.get("page")) for c in chunks_b_10],
            })

        if idx % 50 == 0 or idx == total_q:
            print(f"  Processed {idx}/{total_q} questions...")

    elapsed = time.time() - t0
    print(f"Retrieval benchmarking finished in {elapsed:.1f}s")

    # 2. Page Numbering & Indexing Audit (5 concrete examples across 5 companies)
    sample_cases = [
        ("3M", "3M_2018_10K", "financebench_id_03029"),
        ("AMD", "AMD_2022_10K", "financebench_id_00995"),
        ("American Express", "AMERICANEXPRESS_2022_10K", "financebench_id_01028"),
        ("Boeing", "BOEING_2018_10K", "financebench_id_10285"),
        ("Best Buy", "BESTBUY_2023_10K", "financebench_id_01538"),
    ]
    page_audit_results = []
    print("\nAuditing page indexing on 5 examples...")
    for comp, doc, q_id in sample_cases:
        matching_q = next((q for q in questions if q.get("financebench_id") == q_id), None)
        if not matching_q:
            continue
        ev = matching_q.get("evidence", [])[0]
        gold_page = ev.get("evidence_page_num")
        ev_text = ev.get("evidence_text", "")

        pdf_file = RAW_DIR / f"{doc}.pdf"
        reader = pypdf.PdfReader(str(pdf_file))
        
        # Check text on reader.pages[gold_page]
        p_text = reader.pages[gold_page].extract_text() or ""
        
        # Try to find printed page number in text (usually at bottom or top)
        printed_nums = re.findall(r"\b(?:page\s*)?(\d{1,3})\b", p_text[-300:], re.IGNORECASE)
        printed_page = printed_nums[-1] if printed_nums else "not detected"

        # Check chunk in DB
        with psycopg2.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT page, chunk_index, text FROM chunks WHERE doc_name = %s AND page = %s LIMIT 1;",
                    (doc, gold_page)
                )
                db_row = cur.fetchone()

        db_chunk_found = bool(db_row)
        sample_db_text = db_row[2][:120].replace("\n", " ") if db_row else "none"

        # Evidence phrase match verification
        words = ev_text.split()
        probe_phrase = " ".join(words[:5]) if len(words) >= 5 else ev_text[:30]
        phrase_in_pypdf_page = probe_phrase in p_text

        page_audit_results.append({
            "question_id": q_id,
            "company": comp,
            "doc_name": doc,
            "gold_evidence_page_num": gold_page,
            "pypdf_page_index": gold_page,
            "phrase_verified_on_page": phrase_in_pypdf_page,
            "probe_phrase": probe_phrase,
            "printed_page_num_on_sheet": printed_page,
            "db_chunk_exists_for_page": db_chunk_found,
            "sample_chunk_text": sample_db_text,
        })

    # 3. Multi-page evidence breakdown
    evidence_lens = [len(q.get("evidence", [])) for q in questions]
    single_page_q = sum(1 for l in evidence_lens if l == 1)
    multi_page_q = sum(1 for l in evidence_lens if l > 1)
    max_ev_pages = max(evidence_lens) if evidence_lens else 0

    # 4. 10 Chunks from Table-Heavy Pages (verbatim)
    print("\nFetching 10 verbatim chunks from table-heavy pages...")
    table_chunks = []
    with psycopg2.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT company, doc_name, page, chunk_index, text
                FROM chunks
                WHERE text ~ '(\\$[0-9]+.*[0-9]+.*[0-9]+)'
                  AND text ~ '(Millions|thousands|Total|Balance|Assets|Liabilities)'
                ORDER BY LENGTH(text) DESC
                LIMIT 10;
            """)
            rows = cur.fetchall()
            for r in rows:
                table_chunks.append({
                    "company": r[0],
                    "doc_name": r[1],
                    "page": r[2],
                    "chunk_index": r[3],
                    "text": r[4]
                })

    # 5. Failure Analysis (Config B: company filter)
    # Categorize failures at k=10
    wrong_doc_count = 0
    wrong_page_count = 0
    multi_page_miss_count = 0

    for f in failures_b_10:
        if not f["doc_hit"]:
            # Even within company, retrieved wrong year/filing (e.g. 2022 instead of 2018)
            wrong_doc_count += 1
        else:
            # Retrieved target document, but missed the target page
            if len(f["gold_pages"]) > 1:
                multi_page_miss_count += 1
            else:
                wrong_page_count += 1

    report_data = {
        "total_questions": total_q,
        "metrics": {
            "config_a_unfiltered": {
                "doc_hit_k5": doc_hits_a_5,
                "doc_hit_k5_pct": round(doc_hits_a_5 / total_q * 100, 2),
                "doc_hit_k10": doc_hits_a_10,
                "doc_hit_k10_pct": round(doc_hits_a_10 / total_q * 100, 2),
                "page_hit_k5": page_hits_a_5,
                "page_hit_k5_pct": round(page_hits_a_5 / total_q * 100, 2),
                "page_hit_k10": page_hits_a_10,
                "page_hit_k10_pct": round(page_hits_a_10 / total_q * 100, 2),
            },
            "config_b_company_filtered": {
                "doc_hit_k5": doc_hits_b_5,
                "doc_hit_k5_pct": round(doc_hits_b_5 / total_q * 100, 2),
                "doc_hit_k10": doc_hits_b_10,
                "doc_hit_k10_pct": round(doc_hits_b_10 / total_q * 100, 2),
                "page_hit_k5": page_hits_b_5,
                "page_hit_k5_pct": round(page_hits_b_5 / total_q * 100, 2),
                "page_hit_k10": page_hits_b_10,
                "page_hit_k10_pct": round(page_hits_b_10 / total_q * 100, 2),
                "page_all_hits_k5": page_all_hits_b_5,
                "page_all_hits_k5_pct": round(page_all_hits_b_5 / total_q * 100, 2),
                "page_all_hits_k10": page_all_hits_b_10,
                "page_all_hits_k10_pct": round(page_all_hits_b_10 / total_q * 100, 2),
            }
        },
        "page_indexing_audit": page_audit_results,
        "multi_page_breakdown": {
            "single_page_questions": single_page_q,
            "multi_page_questions": multi_page_q,
            "max_evidence_pages": max_ev_pages
        },
        "failure_causes_config_b_k10": {
            "wrong_document_within_company": wrong_doc_count,
            "wrong_page_single_target": wrong_page_count,
            "wrong_page_multi_target": multi_page_miss_count,
            "total_failures": len(failures_b_10)
        },
        "sample_table_chunks": table_chunks
    }

    out_file = RESULTS_DIR / "diagnosis_step1.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    print(f"\nDiagnosis complete. Results saved to {out_file}")
    return report_data


if __name__ == "__main__":
    run_diagnosis()
