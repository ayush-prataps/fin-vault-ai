#!/usr/bin/env python3
"""
Final Held-Out Test Split Evaluation (75 questions)
- Evaluates frozen configuration on held-out test split (split_75_75.json seed 42).
- Configurations:
  1. Config A: Vanilla (unfiltered)
  2. Config C: Inferred Metadata (company & year inferred from question text)
  3. Oracle: Gold Company + Gold Fiscal Year
- Metrics:
  - Page Hit@10 (primary)
  - Token Recall@10 (threshold >= 0.8, normalized alphanumeric tokens)
  - 95% Wilson score confidence intervals for all metrics
- Paired counts and statistical interval checks.
- Output: eval/results/held_out_evaluation.json
"""
import json
import math
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


def wilson_score_interval(k: int, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Calculate Wilson score interval for binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    # z for 95% confidence is ~1.95996
    z = 1.959963984540054
    p = k / n
    denominator = 1.0 + (z**2) / n
    centre_adjusted_probability = p + (z**2) / (2 * n)
    adjusted_std_dev = math.sqrt((p * (1 - p) + (z**2) / (4 * n)) / n)
    lower_bound = (centre_adjusted_probability - z * adjusted_std_dev) / denominator
    upper_bound = (centre_adjusted_probability + z * adjusted_std_dev) / denominator
    return (max(0.0, lower_bound), min(1.0, upper_bound))


def run_held_out_eval():
    with open(SPLIT_PATH) as f:
        split = json.load(f)
    test_ids = set(split["test_ids"])

    test_questions = []
    with open(DATA_PATH) as f:
        for line in f:
            q = json.loads(line)
            if q["financebench_id"] in test_ids:
                test_questions.append(q)

    print(f"Loaded {len(test_questions)} held-out test questions.")
    conn = psycopg2.connect(settings.database_url)

    print("Pre-embedding test questions...")
    query_embeddings = {q["financebench_id"]: embed_text(q["question"]) for q in test_questions}

    configs = ["Config A (Vanilla)", "Config C (Inferred)", "Oracle (Gold Co+Yr)"]
    eval_results = {}

    for cfg in configs:
        page_hits = 0
        token_hits = 0
        per_q = {}

        for q in test_questions:
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
                table_name="chunks_v2",
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
                "token_hit": q_token_hit,
                "inferred_company": infer_company(q["question"]) if cfg == "Config C (Inferred)" else None,
                "inferred_year": infer_year(q["question"]) if cfg == "Config C (Inferred)" else None,
                "gold_company": q.get("company"),
                "gold_pages": list(gold_pages)
            }

        p_low, p_high = wilson_score_interval(page_hits, len(test_questions))
        t_low, t_high = wilson_score_interval(token_hits, len(test_questions))

        eval_results[cfg] = {
            "page_hit_10": page_hits,
            "page_hit_rate": page_hits / len(test_questions),
            "page_hit_95_ci": [p_low, p_high],
            "token_hit_10": token_hits,
            "token_hit_rate": token_hits / len(test_questions),
            "token_hit_95_ci": [t_low, t_high],
            "total": len(test_questions),
            "per_question": per_q
        }

    # Paired comparisons
    paired_summary = {}
    pairs = [
        ("Config C vs Config A", "Config C (Inferred)", "Config A (Vanilla)"),
        ("Oracle vs Config C", "Oracle (Gold Co+Yr)", "Config C (Inferred)"),
        ("Oracle vs Config A", "Oracle (Gold Co+Yr)", "Config A (Vanilla)")
    ]

    for label, cfg1, cfg2 in pairs:
        q1 = eval_results[cfg1]["per_question"]
        q2 = eval_results[cfg2]["per_question"]

        p_both = sum(1 for qid in q1 if q1[qid]["page_hit"] and q2[qid]["page_hit"])
        p_only1 = sum(1 for qid in q1 if q1[qid]["page_hit"] and not q2[qid]["page_hit"])
        p_only2 = sum(1 for qid in q1 if not q1[qid]["page_hit"] and q2[qid]["page_hit"])
        p_neither = sum(1 for qid in q1 if not q1[qid]["page_hit"] and not q2[qid]["page_hit"])

        t_both = sum(1 for qid in q1 if q1[qid]["token_hit"] and q2[qid]["token_hit"])
        t_only1 = sum(1 for qid in q1 if q1[qid]["token_hit"] and not q2[qid]["token_hit"])
        t_only2 = sum(1 for qid in q1 if not q1[qid]["token_hit"] and q2[qid]["token_hit"])
        t_neither = sum(1 for qid in q1 if not q1[qid]["token_hit"] and not q2[qid]["token_hit"])

        paired_summary[label] = {
            "page_hit": {
                "both": p_both,
                f"only_{cfg1}": p_only1,
                f"only_{cfg2}": p_only2,
                "neither": p_neither,
                "net_diff": p_only1 - p_only2
            },
            "token_hit": {
                "both": t_both,
                f"only_{cfg1}": t_only1,
                f"only_{cfg2}": t_only2,
                "neither": t_neither,
                "net_diff": t_only1 - t_only2
            }
        }

    # Check extraction accuracy on held-out test split
    co_hits = 0
    yr_hits = 0
    both_hits = 0
    for q in test_questions:
        inf_co = infer_company(q["question"])
        inf_yr = infer_year(q["question"])
        gold_co = q.get("company")
        y_m = re.search(r"_(\d{4})", q.get("doc_name", ""))
        gold_yr = int(y_m.group(1)) if y_m else None

        c_ok = (inf_co == gold_co)
        y_ok = (inf_yr == gold_yr)
        if c_ok: co_hits += 1
        if y_ok: yr_hits += 1
        if c_ok and y_ok: both_hits += 1

    extraction_stats = {
        "company_accuracy": f"{co_hits}/{len(test_questions)} ({co_hits/len(test_questions)*100:.1f}%)",
        "year_accuracy": f"{yr_hits}/{len(test_questions)} ({yr_hits/len(test_questions)*100:.1f}%)",
        "both_accuracy": f"{both_hits}/{len(test_questions)} ({both_hits/len(test_questions)*100:.1f}%)",
    }

    print("\n=== HELD-OUT TEST EVALUATION (n=75, seed=42) ===")
    print(f"{'Config':<22} | {'Page Hit@10 (k/n)':<18} | {'95% CI':<18} | {'Token Recall@10 (k/n)':<22} | {'95% CI':<18}")
    print("-" * 105)
    for cfg in configs:
        res = eval_results[cfg]
        p_str = f"{res['page_hit_10']}/75 ({res['page_hit_rate']*100:.1f}%)"
        p_ci = f"[{res['page_hit_95_ci'][0]*100:.1f}%, {res['page_hit_95_ci'][1]*100:.1f}%]"
        t_str = f"{res['token_hit_10']}/75 ({res['token_hit_rate']*100:.1f}%)"
        t_ci = f"[{res['token_hit_95_ci'][0]*100:.1f}%, {res['token_hit_95_ci'][1]*100:.1f}%]"
        print(f"{cfg:<22} | {p_str:<18} | {p_ci:<18} | {t_str:<22} | {t_ci:<18}")

    print("\n--- Paired Comparisons ---")
    for label, summary in paired_summary.items():
        p_pair = summary["page_hit"]
        t_pair = summary["token_hit"]
        print(f"{label} Page Hit: Net {p_pair['net_diff']:+d} (Both {p_pair['both']}, Only1 {list(p_pair.values())[1]}, Only2 {list(p_pair.values())[2]}, Neither {p_pair['neither']})")
        print(f"{label} Token Hit: Net {t_pair['net_diff']:+d} (Both {t_pair['both']}, Only1 {list(t_pair.values())[1]}, Only2 {list(t_pair.values())[2]}, Neither {t_pair['neither']})")

    print("\n--- Test Extraction Accuracy ---")
    print(extraction_stats)

    git_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    output_payload = {
        "metadata": {
            "model": "BAAI/bge-small-en-v1.5",
            "table": "chunks_v2",
            "split_seed": 42,
            "test_question_count": len(test_questions),
            "top_k": 10,
            "token_recall_threshold": 0.8,
            "git_commit": git_commit,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "eval_results": eval_results,
        "paired_summary": paired_summary,
        "extraction_stats": extraction_stats
    }

    with open(RESULTS_DIR / "held_out_evaluation.json", "w") as f:
        json.dump(output_payload, f, indent=2)

    conn.close()

if __name__ == "__main__":
    run_held_out_eval()
