#!/usr/bin/env python3
"""
Section C.2: Reranker Benchmark & Evaluation on Dev Split (75 questions)
- Checks what FastEmbed supports for reranking (LateInteractionTextEmbedding / ColBERT).
- Measures RAM consumption and per-query latency.
- Reranks top 25 candidates down to top 10 on chunks_v2.
- Evaluates Page Hit@10 and Token Recall@10 with paired counts versus Vector-Only.
"""
import json
import os
import re
import resource
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Set
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import psycopg2
from app.config import settings
from app.core.embeddings import embed_text
from app.aliases import infer_company, infer_year
from eval.evaluate_chunks_v2 import compute_token_recall, is_token_recall_hit, is_page_hit
from eval.run_retrieval_fusion_rrf import search_vector

DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
SPLIT_PATH = BASE_DIR / "eval" / "results" / "split_75_75.json"
RESULTS_DIR = BASE_DIR / "eval" / "results"


def get_ram_mb() -> float:
    # On macOS ru_maxrss is in bytes
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)


def colbert_maxsim(query_emb: np.ndarray, doc_embs: List[np.ndarray]) -> List[float]:
    """Compute ColBERT MaxSim operator for a query against multiple document token embeddings."""
    scores = []
    for d in doc_embs:
        # query_emb: (L_q, D), d: (L_d, D)
        sim = np.dot(query_emb, d.T)  # (L_q, L_d)
        max_sim = np.max(sim, axis=1)  # max across doc tokens for each query token
        scores.append(float(np.sum(max_sim)))
    return scores


def run_reranker_eval():
    from fastembed import LateInteractionTextEmbedding

    print("=== FinVault AI: Section C.2 Reranker Evaluation ===")
    ram_start = get_ram_mb()
    print(f"Base RAM: {ram_start:.2f} MB")

    # FastEmbed supports LateInteractionTextEmbedding (ColBERT)
    model_name = "answerdotai/answerai-colbert-small-v1"
    print(f"Loading FastEmbed LateInteraction model: {model_name}...")
    t_load_start = time.time()
    colbert = LateInteractionTextEmbedding(model_name)
    load_time = time.time() - t_load_start
    ram_after_load = get_ram_mb()
    ram_increase = ram_after_load - ram_start
    print(f"Model loaded in {load_time:.2f}s. RAM after load: {ram_after_load:.2f} MB (increase: {ram_increase:.2f} MB)")

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
    cur = conn.cursor()

    print("Pre-embedding dev questions with dense model...")
    query_embeddings = {q["financebench_id"]: embed_text(q["question"]) for q in dev_questions}

    configs = ["Config A (Vanilla)", "Config C (Inferred)", "Oracle (Gold Co+Yr)"]
    methods = ["Vector-Only", "ColBERT-Reranked"]

    results = {}
    rerank_latencies = []

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

            # Retrieve top 25 candidates
            rows = search_vector(cur, "chunks_v2", emb, filter_co, filter_yr, limit=25)
            candidates = [{
                "id": r[0], "company": r[1], "doc_name": r[2], "year": r[3],
                "page": r[4], "chunk_index": r[5], "text": r[6], "score": float(r[7])
            } for r in rows]

            # 1. Vector-only top 10
            v_top10 = candidates[:10]
            v_page_hit = any(is_page_hit(c["doc_name"], c["page"], target_doc, gold_pages) for c in v_top10)
            v_token_hit = any(is_token_recall_hit(c["text"], c["doc_name"], target_doc, gold_evidence, threshold=0.8) for c in v_top10)

            if v_page_hit: results[cfg]["Vector-Only"]["page_hit_10"] += 1
            if v_token_hit: results[cfg]["Vector-Only"]["token_hit_10"] += 1
            results[cfg]["Vector-Only"]["per_q"][fb_id] = {"page_hit": v_page_hit, "token_hit": v_token_hit}

            # 2. Rerank top 25 down to top 10 using ColBERT MaxSim
            if candidates:
                t0 = time.time()
                q_emb = list(colbert.query_embed(q_text))[0]
                doc_embs = list(colbert.embed([c["text"] for c in candidates]))
                scores = colbert_maxsim(q_emb, doc_embs)
                t_rerank = time.time() - t0
                rerank_latencies.append(t_rerank)

                # Sort by rerank score descending
                ranked_indices = np.argsort(scores)[::-1]
                r_top10 = [candidates[idx] for idx in ranked_indices[:10]]
            else:
                r_top10 = []

            r_page_hit = any(is_page_hit(c["doc_name"], c["page"], target_doc, gold_pages) for c in r_top10)
            r_token_hit = any(is_token_recall_hit(c["text"], c["doc_name"], target_doc, gold_evidence, threshold=0.8) for c in r_top10)

            if r_page_hit: results[cfg]["ColBERT-Reranked"]["page_hit_10"] += 1
            if r_token_hit: results[cfg]["ColBERT-Reranked"]["token_hit_10"] += 1
            results[cfg]["ColBERT-Reranked"]["per_q"][fb_id] = {"page_hit": r_page_hit, "token_hit": r_token_hit}

    # Paired comparisons
    paired_summary = {}
    for cfg in configs:
        vec_q = results[cfg]["Vector-Only"]["per_q"]
        rrk_q = results[cfg]["ColBERT-Reranked"]["per_q"]

        page_both = sum(1 for qid in vec_q if vec_q[qid]["page_hit"] and rrk_q[qid]["page_hit"])
        page_only_vec = sum(1 for qid in vec_q if vec_q[qid]["page_hit"] and not rrk_q[qid]["page_hit"])
        page_only_rrk = sum(1 for qid in vec_q if not vec_q[qid]["page_hit"] and rrk_q[qid]["page_hit"])
        page_neither = sum(1 for qid in vec_q if not vec_q[qid]["page_hit"] and not rrk_q[qid]["page_hit"])

        token_both = sum(1 for qid in vec_q if vec_q[qid]["token_hit"] and rrk_q[qid]["token_hit"])
        token_only_vec = sum(1 for qid in vec_q if vec_q[qid]["token_hit"] and not rrk_q[qid]["token_hit"])
        token_only_rrk = sum(1 for qid in vec_q if not vec_q[qid]["token_hit"] and rrk_q[qid]["token_hit"])
        token_neither = sum(1 for qid in vec_q if not vec_q[qid]["token_hit"] and not rrk_q[qid]["token_hit"])

        paired_summary[cfg] = {
            "page_hit": {
                "vector_only": results[cfg]["Vector-Only"]["page_hit_10"],
                "reranked": results[cfg]["ColBERT-Reranked"]["page_hit_10"],
                "both_right": page_both,
                "only_vector": page_only_vec,
                "only_reranked": page_only_rrk,
                "both_wrong": page_neither,
                "net_change": page_only_rrk - page_only_vec
            },
            "token_hit": {
                "vector_only": results[cfg]["Vector-Only"]["token_hit_10"],
                "reranked": results[cfg]["ColBERT-Reranked"]["token_hit_10"],
                "both_right": token_both,
                "only_vector": token_only_vec,
                "only_reranked": token_only_rrk,
                "both_wrong": token_neither,
                "net_change": token_only_rrk - token_only_vec
            }
        }

    mean_latency = float(np.mean(rerank_latencies)) if rerank_latencies else 0.0
    p95_latency = float(np.percentile(rerank_latencies, 95)) if rerank_latencies else 0.0

    print("\n=== RERANKER RESULTS ON DEV (n=75) ===")
    print(f"Reranker Model: {model_name}")
    print(f"RAM increase: {ram_increase:.2f} MB (Peak RSS: {get_ram_mb():.2f} MB)")
    print(f"Per-query latency (top 25): Mean = {mean_latency*1000:.1f}ms, p95 = {p95_latency*1000:.1f}ms")
    print("-" * 115)
    print(f"{'Config':<22} | {'Metric':<14} | {'Vector-Only':<16} | {'Reranked (top 25->10)':<22} | {'Paired (both / only_vec / only_rrk / neither)':<38}")
    print("-" * 115)
    for cfg in configs:
        p_res = paired_summary[cfg]["page_hit"]
        t_res = paired_summary[cfg]["token_hit"]
        p_vec_str = f"{p_res['vector_only']}/75 ({p_res['vector_only']/75*100:.1f}%)"
        p_rrk_str = f"{p_res['reranked']}/75 ({p_res['reranked']/75*100:.1f}%)"
        p_pair = f"{p_res['both_right']} / {p_res['only_vector']} / {p_res['only_reranked']} / {p_res['both_wrong']} (net {p_res['net_change']:+d})"

        t_vec_str = f"{t_res['vector_only']}/75 ({t_res['vector_only']/75*100:.1f}%)"
        t_rrk_str = f"{t_res['reranked']}/75 ({t_res['reranked']/75*100:.1f}%)"
        t_pair = f"{t_res['both_right']} / {t_res['only_vector']} / {t_res['only_reranked']} / {t_res['both_wrong']} (net {t_res['net_change']:+d})"

        print(f"{cfg:<22} | {'Page Hit@10':<14} | {p_vec_str:<16} | {p_rrk_str:<22} | {p_pair:<38}")
        print(f"{cfg:<22} | {'Token Recall@10':<14} | {t_vec_str:<16} | {t_rrk_str:<22} | {t_pair:<38}")

    final_payload = {
        "metadata": {
            "model": "BAAI/bge-small-en-v1.5",
            "reranker": model_name,
            "rerank_top_k": 25,
            "ram_increase_mb": ram_increase,
            "mean_latency_ms": mean_latency * 1000,
            "p95_latency_ms": p95_latency * 1000,
            "split_seed": 42,
            "dev_question_count": len(dev_questions),
            "git_commit": "c6414c1",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "results": results,
        "paired_summary": paired_summary
    }

    with open(RESULTS_DIR / "reranker_results.json", "w") as f:
        json.dump(final_payload, f, indent=2)

    conn.close()

if __name__ == "__main__":
    run_reranker_eval()
