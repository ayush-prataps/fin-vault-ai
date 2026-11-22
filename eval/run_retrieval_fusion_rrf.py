#!/usr/bin/env python3
"""
Section C.1: Postgres Full-Text Search + Vector Fusion with Reciprocal Rank Fusion (RRF)
Evaluated on Dev Split (75 questions) on chunks_v2.
Compares Vector-Only vs Hybrid (Vector + Full-Text RRF).
Reports:
- Page Hit@10
- Token Recall@10 (normalized alphanumeric tokens, threshold 0.8)
- Paired counts (both right, only vector, only hybrid, both wrong, net change)
"""
import json
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Set

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import psycopg2
from app.config import settings
from app.core.embeddings import embed_text
from app.aliases import infer_company, infer_year
from eval.evaluate_chunks_v2 import compute_token_recall, is_token_recall_hit, is_page_hit

DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
SPLIT_PATH = BASE_DIR / "eval" / "results" / "split_75_75.json"
RESULTS_DIR = BASE_DIR / "eval" / "results"


def search_vector(cur, table_name: str, query_vector: List[float], company: str = None, year: int = None, limit: int = 50):
    conditions = []
    params = [query_vector]
    if company:
        conditions.append("LOWER(company) = LOWER(%s)")
        params.append(company)
    if year:
        conditions.append("year = %s")
        params.append(year)
    where_clause = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = f"""
        SELECT id, company, doc_name, year, page, chunk_index, text,
               1 - (embedding <=> %s::vector) AS score
        FROM {table_name}
        {where_clause}
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """
    params.extend([query_vector, limit])
    cur.execute(sql, params)
    return cur.fetchall()


def search_fts(cur, table_name: str, query_text: str, company: str = None, year: int = None, limit: int = 50):
    # Clean query for tsquery
    cleaned_q = re.sub(r"[^\w\s]", " ", query_text)
    words = [w for w in cleaned_q.split() if len(w) > 2]
    if not words:
        return []

    conditions = ["to_tsvector('english', text) @@ plainto_tsquery('english', %s)"]
    params = [query_text]
    if company:
        conditions.append("LOWER(company) = LOWER(%s)")
        params.append(company)
    if year:
        conditions.append("year = %s")
        params.append(year)

    where_clause = "WHERE " + " AND ".join(conditions)
    sql = f"""
        SELECT id, company, doc_name, year, page, chunk_index, text,
               ts_rank_cd(to_tsvector('english', text), plainto_tsquery('english', %s)) AS score
        FROM {table_name}
        {where_clause}
        ORDER BY score DESC
        LIMIT %s
    """
    params.extend([query_text, limit])
    try:
        cur.execute(sql, params)
        return cur.fetchall()
    except Exception:
        cur.connection.rollback()
        return []


def rrf_fusion(vector_results, fts_results, k: int = 60, top_n: int = 10) -> List[Dict[str, Any]]:
    # Map chunk id to metadata
    items = {}
    rrf_scores = {}

    # Rank dense results (1-based)
    for rank, r in enumerate(vector_results, 1):
        cid = r[0]
        items[cid] = {
            "id": r[0], "company": r[1], "doc_name": r[2], "year": r[3],
            "page": r[4], "chunk_index": r[5], "text": r[6], "dense_score": float(r[7])
        }
        rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank))

    # Rank sparse results (1-based)
    for rank, r in enumerate(fts_results, 1):
        cid = r[0]
        if cid not in items:
            items[cid] = {
                "id": r[0], "company": r[1], "doc_name": r[2], "year": r[3],
                "page": r[4], "chunk_index": r[5], "text": r[6], "dense_score": 0.0
            }
        rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (k + rank))

    # Sort items by RRF score descending
    sorted_ids = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)
    fused = []
    for cid in sorted_ids[:top_n]:
        item = dict(items[cid])
        item["rrf_score"] = rrf_scores[cid]
        fused.append(item)
    return fused


def evaluate_fusion(table_name: str = "chunks_v2"):
    with open(SPLIT_PATH) as f:
        split = json.load(f)
    dev_ids = set(split["dev_ids"])

    dev_questions = []
    with open(DATA_PATH) as f:
        for line in f:
            q = json.loads(line)
            if q["financebench_id"] in dev_ids:
                dev_questions.append(q)

    print(f"Loaded {len(dev_questions)} dev questions for RRF fusion evaluation.")
    conn = psycopg2.connect(settings.database_url)
    cur = conn.cursor()

    # Pre-embed questions
    print("Pre-embedding dev questions...")
    query_embeddings = {q["financebench_id"]: embed_text(q["question"]) for q in dev_questions}

    configs = ["Config A (Vanilla)", "Config C (Inferred)", "Oracle (Gold Co+Yr)"]
    methods = ["Vector-Only", "Hybrid (Vector+FTS RRF)"]

    results = {}
    for cfg in configs:
        results[cfg] = {m: {"page_hit_10": 0, "token_hit_10": 0, "per_q": {}} for m in methods}

        for q in dev_questions:
            fb_id = q["financebench_id"]
            q_text = q["question"]
            emb = query_embeddings[fb_id]
            target_doc = q.get("doc_name", "")
            gold_evidence = q.get("evidence", [])
            gold_pages = {int(ev["evidence_page_num"]) for ev in gold_evidence if "evidence_page_num" in ev}

            if cfg == "Config A (Vanilla)":
                filter_co = None
                filter_yr = None
            elif cfg == "Config C (Inferred)":
                filter_co = infer_company(q_text)
                filter_yr = infer_year(q_text)
            else:
                filter_co = q.get("company")
                y_m = re.search(r"_(\d{4})", target_doc)
                filter_yr = int(y_m.group(1)) if y_m else None

            # 1. Vector only
            v_rows = search_vector(cur, table_name, emb, filter_co, filter_yr, limit=50)
            v_top10 = [{
                "id": r[0], "company": r[1], "doc_name": r[2], "year": r[3],
                "page": r[4], "chunk_index": r[5], "text": r[6], "score": float(r[7])
            } for r in v_rows[:10]]

            v_page_hit = any(is_page_hit(c["doc_name"], c["page"], target_doc, gold_pages) for c in v_top10)
            v_token_hit = any(is_token_recall_hit(c["text"], c["doc_name"], target_doc, gold_evidence, threshold=0.8) for c in v_top10)

            if v_page_hit: results[cfg]["Vector-Only"]["page_hit_10"] += 1
            if v_token_hit: results[cfg]["Vector-Only"]["token_hit_10"] += 1
            results[cfg]["Vector-Only"]["per_q"][fb_id] = {"page_hit": v_page_hit, "token_hit": v_token_hit}

            # 2. Hybrid RRF
            fts_rows = search_fts(cur, table_name, q_text, filter_co, filter_yr, limit=50)
            h_top10 = rrf_fusion(v_rows, fts_rows, k=60, top_n=10)

            h_page_hit = any(is_page_hit(c["doc_name"], c["page"], target_doc, gold_pages) for c in h_top10)
            h_token_hit = any(is_token_recall_hit(c["text"], c["doc_name"], target_doc, gold_evidence, threshold=0.8) for c in h_top10)

            if h_page_hit: results[cfg]["Hybrid (Vector+FTS RRF)"]["page_hit_10"] += 1
            if h_token_hit: results[cfg]["Hybrid (Vector+FTS RRF)"]["token_hit_10"] += 1
            results[cfg]["Hybrid (Vector+FTS RRF)"]["per_q"][fb_id] = {"page_hit": h_page_hit, "token_hit": h_token_hit}

    # Paired comparisons
    paired_summary = {}
    n = len(dev_questions)
    for cfg in configs:
        vec_q = results[cfg]["Vector-Only"]["per_q"]
        hyb_q = results[cfg]["Hybrid (Vector+FTS RRF)"]["per_q"]

        page_both = sum(1 for qid in vec_q if vec_q[qid]["page_hit"] and hyb_q[qid]["page_hit"])
        page_only_vec = sum(1 for qid in vec_q if vec_q[qid]["page_hit"] and not hyb_q[qid]["page_hit"])
        page_only_hyb = sum(1 for qid in vec_q if not vec_q[qid]["page_hit"] and hyb_q[qid]["page_hit"])
        page_neither = sum(1 for qid in vec_q if not vec_q[qid]["page_hit"] and not hyb_q[qid]["page_hit"])

        token_both = sum(1 for qid in vec_q if vec_q[qid]["token_hit"] and hyb_q[qid]["token_hit"])
        token_only_vec = sum(1 for qid in vec_q if vec_q[qid]["token_hit"] and not hyb_q[qid]["token_hit"])
        token_only_hyb = sum(1 for qid in vec_q if not vec_q[qid]["token_hit"] and hyb_q[qid]["token_hit"])
        token_neither = sum(1 for qid in vec_q if not vec_q[qid]["token_hit"] and not hyb_q[qid]["token_hit"])

        paired_summary[cfg] = {
            "page_hit": {
                "vector_only": results[cfg]["Vector-Only"]["page_hit_10"],
                "hybrid_rrf": results[cfg]["Hybrid (Vector+FTS RRF)"]["page_hit_10"],
                "both_right": page_both,
                "only_vector": page_only_vec,
                "only_hybrid": page_only_hyb,
                "both_wrong": page_neither,
                "net_change": page_only_hyb - page_only_vec
            },
            "token_hit": {
                "vector_only": results[cfg]["Vector-Only"]["token_hit_10"],
                "hybrid_rrf": results[cfg]["Hybrid (Vector+FTS RRF)"]["token_hit_10"],
                "both_right": token_both,
                "only_vector": token_only_vec,
                "only_hybrid": token_only_hyb,
                "both_wrong": token_neither,
                "net_change": token_only_hyb - token_only_vec
            }
        }

    print("\n=== HYBRID RRF FUSION RESULTS ON DEV (n=75) ===")
    print(f"{'Config':<22} | {'Metric':<14} | {'Vector-Only':<16} | {'Hybrid RRF':<16} | {'Paired (both / only_vec / only_hyb / neither)':<38}")
    print("-" * 115)
    for cfg in configs:
        p_res = paired_summary[cfg]["page_hit"]
        t_res = paired_summary[cfg]["token_hit"]
        p_vec_str = f"{p_res['vector_only']}/75 ({p_res['vector_only']/75*100:.1f}%)"
        p_hyb_str = f"{p_res['hybrid_rrf']}/75 ({p_res['hybrid_rrf']/75*100:.1f}%)"
        p_pair = f"{p_res['both_right']} / {p_res['only_vector']} / {p_res['only_hybrid']} / {p_res['both_wrong']} (net {p_res['net_change']:+d})"

        t_vec_str = f"{t_res['vector_only']}/75 ({t_res['vector_only']/75*100:.1f}%)"
        t_hyb_str = f"{t_res['hybrid_rrf']}/75 ({t_res['hybrid_rrf']/75*100:.1f}%)"
        t_pair = f"{t_res['both_right']} / {t_res['only_vector']} / {t_res['only_hybrid']} / {t_res['both_wrong']} (net {t_res['net_change']:+d})"

        print(f"{cfg:<22} | {'Page Hit@10':<14} | {p_vec_str:<16} | {p_hyb_str:<16} | {p_pair:<38}")
        print(f"{cfg:<22} | {'Token Recall@10':<14} | {t_vec_str:<16} | {t_hyb_str:<16} | {t_pair:<38}")

    output_payload = {
        "metadata": {
            "model": "BAAI/bge-small-en-v1.5",
            "table": table_name,
            "fusion": "Reciprocal Rank Fusion (RRF, k=60)",
            "split_seed": 42,
            "dev_question_count": len(dev_questions),
            "git_commit": "c6414c1",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "results": results,
        "paired_summary": paired_summary
    }
    with open(RESULTS_DIR / "hybrid_rrf_results.json", "w") as f:
        json.dump(output_payload, f, indent=2)

    conn.close()

if __name__ == "__main__":
    evaluate_fusion()
