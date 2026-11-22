#!/usr/bin/env python3
"""
Section D: Naive Baseline Ablation Evaluation on Dev Split (75 questions)
- Evaluates retrieval on chunks_naive (fixed-size token windows, no page/table awareness).
- Compares against chunks_v2 (best config).
- Reports:
  - Page Hit@10
  - Token Recall@10
  - Paired counts (both right, only naive, only v2, both wrong, net difference).
"""
import json
import re
import subprocess
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
from eval.evaluate_chunks_v2 import compute_token_recall, is_token_recall_hit, is_page_hit, search_table

DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
SPLIT_PATH = BASE_DIR / "eval" / "results" / "split_75_75.json"
RESULTS_DIR = BASE_DIR / "eval" / "results"


def run_naive_eval():
    with open(SPLIT_PATH) as f:
        split = json.load(f)
    dev_ids = set(split["dev_ids"])

    dev_questions = []
    with open(DATA_PATH) as f:
        for line in f:
            q = json.loads(line)
            if q["financebench_id"] in dev_ids:
                dev_questions.append(q)

    print(f"Loaded {len(dev_questions)} dev questions for Naive Baseline evaluation.")
    conn = psycopg2.connect(settings.database_url)

    print("Pre-embedding dev questions...")
    query_embeddings = {q["financebench_id"]: embed_text(q["question"]) for q in dev_questions}

    configs = ["Config A (Vanilla)", "Config C (Inferred)", "Oracle (Gold Co+Yr)"]
    tables = [("chunks_naive", "Naive Baseline"), ("chunks_v2", "Chunker v2")]

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
                else:
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

                if q_page_hit: page_hits += 1
                if q_token_hit: token_hits += 1
                per_q[fb_id] = {"page_hit": q_page_hit, "token_hit": q_token_hit}

            eval_results[tbl_name][cfg] = {
                "page_hit_10": page_hits,
                "token_hit_10": token_hits,
                "total": len(dev_questions),
                "per_question": per_q
            }

    paired_summary = {}
    for cfg in configs:
        naive_q = eval_results["chunks_naive"][cfg]["per_question"]
        v2_q = eval_results["chunks_v2"][cfg]["per_question"]

        p_both = sum(1 for qid in naive_q if naive_q[qid]["page_hit"] and v2_q[qid]["page_hit"])
        p_only_naive = sum(1 for qid in naive_q if naive_q[qid]["page_hit"] and not v2_q[qid]["page_hit"])
        p_only_v2 = sum(1 for qid in naive_q if not naive_q[qid]["page_hit"] and v2_q[qid]["page_hit"])
        p_neither = sum(1 for qid in naive_q if not naive_q[qid]["page_hit"] and not v2_q[qid]["page_hit"])

        t_both = sum(1 for qid in naive_q if naive_q[qid]["token_hit"] and v2_q[qid]["token_hit"])
        t_only_naive = sum(1 for qid in naive_q if naive_q[qid]["token_hit"] and not v2_q[qid]["token_hit"])
        t_only_v2 = sum(1 for qid in naive_q if not naive_q[qid]["token_hit"] and v2_q[qid]["token_hit"])
        t_neither = sum(1 for qid in naive_q if not naive_q[qid]["token_hit"] and not v2_q[qid]["token_hit"])

        paired_summary[cfg] = {
            "page_hit": {
                "naive": eval_results["chunks_naive"][cfg]["page_hit_10"],
                "v2": eval_results["chunks_v2"][cfg]["page_hit_10"],
                "both_right": p_both,
                "only_naive": p_only_naive,
                "only_v2": p_only_v2,
                "both_wrong": p_neither,
                "net_change": p_only_v2 - p_only_naive
            },
            "token_hit": {
                "naive": eval_results["chunks_naive"][cfg]["token_hit_10"],
                "v2": eval_results["chunks_v2"][cfg]["token_hit_10"],
                "both_right": t_both,
                "only_naive": t_only_naive,
                "only_v2": t_only_v2,
                "both_wrong": t_neither,
                "net_change": t_only_v2 - t_only_naive
            }
        }

    print("\n=== NAIVE BASELINE VS CHUNKS_V2 ON DEV (n=75) ===")
    print(f"{'Config':<22} | {'Metric':<14} | {'Naive Baseline':<16} | {'Chunker v2':<16} | {'Paired (both / only_naive / only_v2 / neither)':<42}")
    print("-" * 120)
    for cfg in configs:
        p_res = paired_summary[cfg]["page_hit"]
        t_res = paired_summary[cfg]["token_hit"]
        p_naive_str = f"{p_res['naive']}/75 ({p_res['naive']/75*100:.1f}%)"
        p_v2_str = f"{p_res['v2']}/75 ({p_res['v2']/75*100:.1f}%)"
        p_pair = f"{p_res['both_right']} / {p_res['only_naive']} / {p_res['only_v2']} / {p_res['both_wrong']} (net {p_res['net_change']:+d})"

        t_naive_str = f"{t_res['naive']}/75 ({t_res['naive']/75*100:.1f}%)"
        t_v2_str = f"{t_res['v2']}/75 ({t_res['v2']/75*100:.1f}%)"
        t_pair = f"{t_res['both_right']} / {t_res['only_naive']} / {t_res['only_v2']} / {t_res['both_wrong']} (net {t_res['net_change']:+d})"

        print(f"{cfg:<22} | {'Page Hit@10':<14} | {p_naive_str:<16} | {p_v2_str:<16} | {p_pair:<42}")
        print(f"{cfg:<22} | {'Token Recall@10':<14} | {t_naive_str:<16} | {t_v2_str:<16} | {t_pair:<42}")

    git_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    output_payload = {
        "metadata": {
            "model": "BAAI/bge-small-en-v1.5",
            "split_seed": 42,
            "dev_question_count": len(dev_questions),
            "git_commit": git_commit,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "eval_results": eval_results,
        "paired_summary": paired_summary
    }
    with open(RESULTS_DIR / "naive_baseline_comparison.json", "w") as f:
        json.dump(output_payload, f, indent=2)

    conn.close()

if __name__ == "__main__":
    run_naive_eval()
