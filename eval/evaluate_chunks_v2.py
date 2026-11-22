#!/usr/bin/env python3
"""
Evaluate chunks_v2 vs chunks on Dev Split (75 questions).
Computes:
- Page Hit@10
- Token Recall Hit@10 (normalized alphanumeric tokens, threshold 0.8)
For:
- Config A (vanilla, no filters)
- Config C (inferred company + year)
- Oracle (gold company + gold year)
Reports paired counts (both right, only old, only new, both wrong).
Measures evidence presence across the 91 dev evidence items in chunks_v2.
"""
import json
import re
import sys
import time
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any, Tuple, Set

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import psycopg2
from app.config import settings
from app.core.embeddings import embed_text
from app.aliases import infer_company, infer_year

DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
SPLIT_PATH = BASE_DIR / "eval" / "results" / "split_75_75.json"
RESULTS_DIR = BASE_DIR / "eval" / "results"


def get_alphanumeric_tokens(text: str) -> Set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def compute_token_recall(chunk_text: str, evidence_text: str) -> float:
    ev_tokens = get_alphanumeric_tokens(evidence_text)
    if not ev_tokens:
        return 1.0
    chunk_tokens = get_alphanumeric_tokens(chunk_text)
    overlap = len(ev_tokens & chunk_tokens)
    return overlap / len(ev_tokens)


def is_token_recall_hit(chunk_text: str, chunk_doc: str, target_doc: str, evidence_list: List[Dict[str, Any]], threshold: float = 0.8) -> bool:
    if (chunk_doc or "").strip().upper() != (target_doc or "").strip().upper():
        return False
    for ev in evidence_list:
        ev_text = ev.get("evidence_text", "")
        recall = compute_token_recall(chunk_text, ev_text)
        if recall >= threshold:
            return True
    return False


def is_page_hit(chunk_doc: str, chunk_page: int, target_doc: str, gold_pages: Set[int]) -> bool:
    if (chunk_doc or "").strip().upper() != (target_doc or "").strip().upper():
        return False
    return chunk_page in gold_pages


def search_table(
    table_name: str,
    query_vector: List[float],
    company: str = None,
    year: int = None,
    limit: int = 10,
    conn = None
) -> List[Dict[str, Any]]:
    cur = conn.cursor()
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
    rows = cur.fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "company": r[1],
            "doc_name": r[2],
            "year": r[3],
            "page": r[4],
            "chunk_index": r[5],
            "text": r[6],
            "score": float(r[7]),
        })
    return results


def run_evaluation():
    with open(SPLIT_PATH) as f:
        split = json.load(f)
    dev_ids = set(split["dev_ids"])

    dev_questions = []
    with open(DATA_PATH) as f:
        for line in f:
            q = json.loads(line)
            if q["financebench_id"] in dev_ids:
                dev_questions.append(q)

    print(f"Loaded {len(dev_questions)} dev questions.")

    conn = psycopg2.connect(settings.database_url)

    # Pre-embed dev queries
    print("Embedding dev questions...")
    query_embeddings = {}
    for q in dev_questions:
        fb_id = q["financebench_id"]
        emb = embed_text(q["question"])
        query_embeddings[fb_id] = emb

    configs = ["Config A (Vanilla)", "Config C (Inferred)", "Oracle (Gold Co+Yr)"]
    tables = [("chunks", "Old (chunks)"), ("chunks_v2", "New (chunks_v2)")]

    eval_results = {}

    for tbl_name, tbl_label in tables:
        eval_results[tbl_name] = {}
        for cfg in configs:
            page_hits = 0
            token_hits = 0
            per_q = {}

            for q in dev_questions:
                fb_id = q["financebench_id"]
                emb = query_embeddings[fb_id]
                target_doc = q.get("doc_name", "")
                gold_evidence = q.get("evidence", [])
                gold_pages = {int(ev["evidence_page_num"]) for ev in gold_evidence if "evidence_page_num" in ev}

                if cfg == "Config A (Vanilla)":
                    filter_co = None
                    filter_yr = None
                elif cfg == "Config C (Inferred)":
                    filter_co = infer_company(q["question"])
                    filter_yr = infer_year(q["question"])
                else:  # Oracle
                    filter_co = q.get("company")
                    y_m = re.search(r"_(\d{4})", target_doc)
                    filter_yr = int(y_m.group(1)) if y_m else None

                chunks = search_table(
                    table_name=tbl_name,
                    query_vector=emb,
                    company=filter_co,
                    year=filter_yr,
                    limit=10,
                    conn=conn
                )

                q_page_hit = any(is_page_hit(c["doc_name"], c["page"], target_doc, gold_pages) for c in chunks)
                q_token_hit = any(is_token_recall_hit(c["text"], c["doc_name"], target_doc, gold_evidence, threshold=0.8) for c in chunks)

                if q_page_hit:
                    page_hits += 1
                if q_token_hit:
                    token_hits += 1

                per_q[fb_id] = {
                    "page_hit": q_page_hit,
                    "token_hit": q_token_hit
                }

            eval_results[tbl_name][cfg] = {
                "page_hit_10": page_hits,
                "token_hit_10": token_hits,
                "total": len(dev_questions),
                "page_hit_rate": page_hits / len(dev_questions),
                "token_hit_rate": token_hits / len(dev_questions),
                "per_question": per_q
            }

    # Paired comparisons
    paired_summary = {}
    n = len(dev_questions)
    for cfg in configs:
        old_q = eval_results["chunks"][cfg]["per_question"]
        new_q = eval_results["chunks_v2"][cfg]["per_question"]

        page_both = sum(1 for qid in old_q if old_q[qid]["page_hit"] and new_q[qid]["page_hit"])
        page_only_old = sum(1 for qid in old_q if old_q[qid]["page_hit"] and not new_q[qid]["page_hit"])
        page_only_new = sum(1 for qid in old_q if not old_q[qid]["page_hit"] and new_q[qid]["page_hit"])
        page_neither = sum(1 for qid in old_q if not old_q[qid]["page_hit"] and not new_q[qid]["page_hit"])

        token_both = sum(1 for qid in old_q if old_q[qid]["token_hit"] and new_q[qid]["token_hit"])
        token_only_old = sum(1 for qid in old_q if old_q[qid]["token_hit"] and not new_q[qid]["token_hit"])
        token_only_new = sum(1 for qid in old_q if not old_q[qid]["token_hit"] and new_q[qid]["token_hit"])
        token_neither = sum(1 for qid in old_q if not old_q[qid]["token_hit"] and not new_q[qid]["token_hit"])

        paired_summary[cfg] = {
            "page_hit": {
                "old": eval_results["chunks"][cfg]["page_hit_10"],
                "new": eval_results["chunks_v2"][cfg]["page_hit_10"],
                "both_right": page_both,
                "only_old": page_only_old,
                "only_new": page_only_new,
                "both_wrong": page_neither,
                "net_change": page_only_new - page_only_old
            },
            "token_hit": {
                "old": eval_results["chunks"][cfg]["token_hit_10"],
                "new": eval_results["chunks_v2"][cfg]["token_hit_10"],
                "both_right": token_both,
                "only_old": token_only_old,
                "only_new": token_only_new,
                "both_wrong": token_neither,
                "net_change": token_only_new - token_only_old
            }
        }

    # Evidence Presence in chunks_v2 across 91 dev evidence items
    print("\nAuditing Evidence Presence in chunks_v2 for 91 dev evidence items...")
    cur = conn.cursor()
    cur.execute("SELECT doc_name, page, text FROM chunks_v2 ORDER BY doc_name, page, chunk_index;")
    chunks_v2_db = {}
    for doc, pg, txt in cur.fetchall():
        key = (doc, pg)
        if key not in chunks_v2_db:
            chunks_v2_db[key] = []
        chunks_v2_db[key].append(txt)

    v2_ev_single_alnum = 0
    v2_ev_concat_alnum = 0
    v2_ev_single_num = 0
    v2_ev_single_word = 0
    v2_ev_single_token_recall_08 = 0
    total_ev = 0

    for q in dev_questions:
        target_doc = q.get("doc_name", "")
        for ev in q.get("evidence", []):
            total_ev += 1
            pg = int(ev.get("evidence_page_num"))
            ev_text = ev.get("evidence_text", "")
            chks = chunks_v2_db.get((target_doc, pg), [])
            concat_text = "\n".join(chks)

            # Alphanumeric substring
            alnum_ev = re.sub(r"[^a-z0-9]", "", ev_text.lower())
            if any(alnum_ev in re.sub(r"[^a-z0-9]", "", c.lower()) for c in chks):
                v2_ev_single_alnum += 1
            if alnum_ev in re.sub(r"[^a-z0-9]", "", concat_text.lower()):
                v2_ev_concat_alnum += 1

            # Token recall 0.8
            if any(compute_token_recall(c, ev_text) >= 0.8 for c in chks):
                v2_ev_single_token_recall_08 += 1

    evidence_presence_summary = {
        "total_dev_evidence_items": total_ev,
        "single_chunk_alnum_substring": v2_ev_single_alnum,
        "single_chunk_alnum_substring_rate": v2_ev_single_alnum / total_ev if total_ev else 0,
        "concat_chunks_alnum_substring": v2_ev_concat_alnum,
        "concat_chunks_alnum_substring_rate": v2_ev_concat_alnum / total_ev if total_ev else 0,
        "single_chunk_token_recall_08": v2_ev_single_token_recall_08,
        "single_chunk_token_recall_08_rate": v2_ev_single_token_recall_08 / total_ev if total_ev else 0,
    }

    print("\n=== RESULTS TABLE ON DEV (n=75) ===")
    print(f"{'Config':<25} | {'Metric':<14} | {'Old chunks':<14} | {'New chunks_v2':<14} | {'Paired (both / only_old / only_new / neither)':<35}")
    print("-" * 110)
    for cfg in configs:
        p_res = paired_summary[cfg]["page_hit"]
        t_res = paired_summary[cfg]["token_hit"]
        p_old_str = f"{p_res['old']}/75 ({p_res['old']/75*100:.1f}%)"
        p_new_str = f"{p_res['new']}/75 ({p_res['new']/75*100:.1f}%)"
        p_pair = f"{p_res['both_right']} / {p_res['only_old']} / {p_res['only_new']} / {p_res['both_wrong']} (net {p_res['net_change']:+d})"

        t_old_str = f"{t_res['old']}/75 ({t_res['old']/75*100:.1f}%)"
        t_new_str = f"{t_res['new']}/75 ({t_res['new']/75*100:.1f}%)"
        t_pair = f"{t_res['both_right']} / {t_res['only_old']} / {t_res['only_new']} / {t_res['both_wrong']} (net {t_res['net_change']:+d})"

        print(f"{cfg:<25} | {'Page Hit@10':<14} | {p_old_str:<14} | {p_new_str:<14} | {p_pair:<35}")
        print(f"{cfg:<25} | {'Token Recall@10':<14} | {t_old_str:<14} | {t_new_str:<14} | {t_pair:<35}")

    print("\n=== EVIDENCE PRESENCE IN chunks_v2 (n=91) ===")
    print(f"Single Chunk Alnum Substring: {v2_ev_single_alnum}/91 ({v2_ev_single_alnum/91*100:.1f}%) (Old was 41/91, 45.1%)")
    print(f"Concat Chunks Alnum Substring: {v2_ev_concat_alnum}/91 ({v2_ev_concat_alnum/91*100:.1f}%) (Old was 60/91, 65.9%)")
    print(f"Single Chunk Token Recall >= 0.8: {v2_ev_single_token_recall_08}/91 ({v2_ev_single_token_recall_08/91*100:.1f}%)")

    final_payload = {
        "metadata": {
            "model": "BAAI/bge-small-en-v1.5",
            "split_seed": 42,
            "dev_question_count": len(dev_questions),
            "git_commit": "c6414c1",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "eval_results": eval_results,
        "paired_summary": paired_summary,
        "evidence_presence": evidence_presence_summary
    }

    with open(RESULTS_DIR / "chunks_v2_comparison.json", "w") as f:
        json.dump(final_payload, f, indent=2)

    conn.close()

if __name__ == "__main__":
    run_evaluation()
