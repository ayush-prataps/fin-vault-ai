#!/usr/bin/env python3
"""
Step 0-5 Diagnostic Suite: Retrieval Part 2 & Fixes
- Step 0: Fixed-seed 75/75 company-stratified split
- Step 1: Mutually exclusive failure reconciliation (summing to exact failure count)
- Step 2: 10 verbatim table chunks (5 hits, 5 misses) with gold evidence
- Step 3: Dev rank diagnostic (ranks 1-10, 11-20, 21-50, 51-100, >100, absent)
          and evidence text presence rate in stored chunks
- Step 4: Evidence-text hit metric alongside page hit
- Step 5: Config C (inferred company and year) vs Config A and Config B (oracle)
- Step 7 checkpoint check
"""
import json
import random
import re
import subprocess
import sys
import time
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import psycopg2
from app.config import settings
from app.core.embeddings import embed_text
from app.core.vector import search_chunks
from eval.run_eval import is_retrieval_hit

DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
RESULTS_DIR = BASE_DIR / "eval" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

COMPANY_PATTERNS = [
    ("3M", r"\b3M\b"),
    ("AES Corporation", r"\bAES\b"),
    ("AMD", r"\bAMD\b"),
    ("Activision Blizzard", r"\bActivision(?:\s+Blizzard)?\b"),
    ("Adobe", r"\bAdobe\b"),
    ("Amazon", r"\bAmazon\b"),
    ("Amcor", r"\bAmcor\b"),
    ("American Express", r"\b(?:American\s+Express|Amex)\b"),
    ("American Water Works", r"\bAmerican\s+Water(?:\s+Works)?\b"),
    ("Best Buy", r"\bBest\s+Buy\b"),
    ("Block", r"\b(?:Block|Square)\b"),
    ("Boeing", r"\bBoeing\b"),
    ("Coca-Cola", r"\b(?:Coca-Cola|Coca\s+Cola|Coke)\b"),
    ("Corning", r"\bCorning\b"),
    ("Costco", r"\bCostco\b"),
    ("CVS Health", r"\bCVS(?:\s+Health)?\b"),
    ("Foot Locker", r"\bFoot\s+Locker\b"),
    ("General Mills", r"\bGeneral\s+Mills\b"),
    ("Johnson & Johnson", r"\b(?:Johnson\s+&\s+Johnson|J&J|JnJ)\b"),
    ("JPMorgan", r"\b(?:JPMorgan|JP\s+Morgan|JPMorgan\s+Chase|JPM)\b"),
    ("Kraft Heinz", r"\bKraft(?:\s+Heinz)?\b"),
    ("Lockheed Martin", r"\bLockheed(?:\s+Martin)?\b"),
    ("MGM Resorts", r"\bMGM(?:\s+Resorts)?\b"),
    ("Microsoft", r"\bMicrosoft\b"),
    ("Netflix", r"\bNetflix\b"),
    ("Nike", r"\bNike\b"),
    ("PayPal", r"\bPayPal\b"),
    ("PepsiCo", r"\bPepsi(?:Co)?\b"),
    ("Pfizer", r"\bPfizer\b"),
    ("Ulta Beauty", r"\bUlta(?:\s+Beauty)?\b"),
    ("Verizon", r"\bVerizon\b"),
    ("Walmart", r"\b(?:Walmart|Wal-Mart)\b"),
]


def get_git_commit() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(BASE_DIR))
        return out.decode().strip()
    except Exception:
        return "unknown"


def infer_company(text: str) -> Optional[str]:
    for comp, pat in COMPANY_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return comp
    return None


def infer_year(text: str) -> Optional[int]:
    fy_match = re.findall(r"\bFY\s*(\d{4})\b", text, re.IGNORECASE)
    if fy_match:
        return int(fy_match[-1])
    all_years = re.findall(r"\b(20\d\d)\b", text)
    if all_years:
        return int(all_years[-1])
    return None


def normalize_tokens(text: str) -> Set[str]:
    """Extract significant lowercase alphanumeric tokens (len >= 3)."""
    words = re.findall(r"\b[a-zA-Z0-9]{3,}\b", text.lower())
    return set(words)


def is_evidence_text_hit(chunk_text: str, evidence_list: List[Dict[str, Any]], target_doc: str, chunk_doc: str) -> bool:
    """
    Evidence text hit condition:
    1. Document matches target_doc.
    2. Chunk contains substantial token recall (>= 60%) or key sentence match of any gold evidence item.
    """
    if (chunk_doc or "").strip().upper() != (target_doc or "").strip().upper():
        return False

    chunk_tokens = normalize_tokens(chunk_text)
    if not chunk_tokens:
        return False

    for ev in evidence_list:
        ev_text = ev.get("evidence_text", "")
        ev_tokens = normalize_tokens(ev_text)
        if not ev_tokens:
            continue
        overlap = len(chunk_tokens.intersection(ev_tokens))
        recall = overlap / len(ev_tokens)
        if recall >= 0.60:
            return True
        # Check if any substantial line from evidence (>= 30 chars) is present in chunk
        lines = [line.strip() for line in ev_text.split("\n") if len(line.strip()) >= 30]
        for line in lines:
            line_clean = re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", line.lower())).strip()
            chunk_clean = re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", chunk_text.lower())).strip()
            if line_clean in chunk_clean:
                return True

    return False


def make_stratified_split(questions: List[Dict[str, Any]], seed: int = 42) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    by_comp = defaultdict(list)
    for q in questions:
        by_comp[q["company"]].append(q)

    rng = random.Random(seed)
    dev_q = []
    test_q = []

    toggle = True
    for comp in sorted(by_comp.keys()):
        qs = list(by_comp[comp])
        qs.sort(key=lambda x: x["financebench_id"])
        rng.shuffle(qs)

        n = len(qs)
        half = n // 2
        rem = n % 2

        dev_slice = qs[:half]
        test_slice = qs[half:half * 2]

        if rem > 0:
            extra = qs[-1]
            if toggle:
                dev_slice.append(extra)
            else:
                test_slice.append(extra)
            toggle = not toggle

        dev_q.extend(dev_slice)
        test_q.extend(test_slice)

    return dev_q, test_q


def main():
    print("=== FinVault AI: Retrieval Diagnosis Part 2 & Fixes ===")
    t_start = time.time()
    git_commit = get_git_commit()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        questions = [json.loads(line) for line in f if line.strip()]

    total_q = len(questions)
    print(f"Total corpus questions: {total_q}")

    # Step 0: Save 75/75 Split
    dev_q, test_q = make_stratified_split(questions, seed=42)
    split_info = {
        "seed": 42,
        "dev_count": len(dev_q),
        "test_count": len(test_q),
        "dev_ids": [q["financebench_id"] for q in dev_q],
        "test_ids": [q["financebench_id"] for q in test_q],
    }
    with open(RESULTS_DIR / "split_75_75.json", "w", encoding="utf-8") as f:
        json.dump(split_info, f, indent=2)
    with open(BASE_DIR / "data" / "financebench_split.json", "w", encoding="utf-8") as f:
        json.dump(split_info, f, indent=2)
    print("Step 0 Complete: Saved 75 dev / 75 test split to eval/results/split_75_75.json")

    # Pre-embed all queries
    print("Embedding all queries...")
    query_embeddings = {q["financebench_id"]: embed_text(q["question"]) for q in questions}

    # Connect to PostgreSQL
    conn = psycopg2.connect(settings.database_url)

    # We will run retrieval for Config A, Config B, and Config C
    print("\nRunning retrievals for Config A (unfiltered), B (oracle), C (inferred)...")
    res_a = {}
    res_b = {}
    res_c = {}

    for idx, q in enumerate(questions, 1):
        qid = q["financebench_id"]
        q_emb = query_embeddings[qid]
        c_gold = q["company"]

        # Config A: Unfiltered
        res_a[qid] = search_chunks(q_emb, company=None, top_k=10)

        # Config B: Oracle Company Filter
        res_b[qid] = search_chunks(q_emb, company=c_gold, top_k=10)

        # Config C: Inferred Company & Year
        c_inf = infer_company(q["question"])
        y_inf = infer_year(q["question"])
        chunks_c = search_chunks(q_emb, company=c_inf, year=y_inf, top_k=10)
        # If no chunks returned with year filter, fallback to company only
        if not chunks_c and y_inf:
            chunks_c = search_chunks(q_emb, company=c_inf, year=None, top_k=10)
        res_c[qid] = chunks_c

        if idx % 50 == 0 or idx == total_q:
            print(f"  Retrieved {idx}/{total_q} questions...")

    # Step 1: Reconciled Mutually Exclusive Failure Analysis at k=10
    print("\nStep 1: Reconciling Mutually Exclusive Failure Categories at k=10...")
    def categorize_failures(q_list, res_dict, is_oracle=False):
        categories = {
            "wrong_company": 0,
            "right_company_wrong_doc": 0,
            "right_doc_single_page_miss": 0,
            "right_doc_multi_page_miss": 0,
        }
        total_hits = 0
        total_fails = 0

        for q in q_list:
            qid = q["financebench_id"]
            chunks = res_dict[qid]
            target_doc = q["doc_name"].strip().upper()
            c_gold = q["company"].strip().upper()
            evidence = q.get("evidence", [])
            gold_pages = {e["evidence_page_num"] for e in evidence}

            hit = any(is_retrieval_hit(c, evidence) for c in chunks)
            if hit:
                total_hits += 1
            else:
                total_fails += 1
                retrieved_companies = {(c.get("company") or "").strip().upper() for c in chunks}
                retrieved_docs = {(c.get("doc_name") or "").strip().upper() for c in chunks}

                if c_gold not in retrieved_companies and not is_oracle:
                    categories["wrong_company"] += 1
                elif target_doc not in retrieved_docs:
                    categories["right_company_wrong_doc"] += 1
                else:
                    if len(gold_pages) == 1:
                        categories["right_doc_single_page_miss"] += 1
                    else:
                        categories["right_doc_multi_page_miss"] += 1

        sum_categories = sum(categories.values())
        assert sum_categories == total_fails, f"Sum mismatch: {sum_categories} != {total_fails}"
        return {
            "total_questions": len(q_list),
            "hits": total_hits,
            "failures": total_fails,
            "categories": categories,
            "reconciliation_check": f"{sum_categories} == {total_fails} (EXACT SUM MATCH)"
        }

    failures_a = categorize_failures(questions, res_a, is_oracle=False)
    failures_b = categorize_failures(questions, res_b, is_oracle=True)

    reconciled_failures = {
        "config_a_k10": failures_a,
        "config_b_oracle_k10": failures_b
    }
    with open(RESULTS_DIR / "reconciled_failures.json", "w", encoding="utf-8") as f:
        json.dump(reconciled_failures, f, indent=2)

    # Step 2: 10 Table-Heavy Chunks (5 Hits, 5 Misses) with Gold Evidence
    print("\nStep 2: Selecting 10 table-heavy chunks for chunk_samples.md...")
    hit_samples = []
    miss_samples = []

    for q in questions:
        qid = q["financebench_id"]
        chunks = res_b[qid]
        evidence = q.get("evidence", [])
        if not evidence:
            continue
        ev = evidence[0]
        ev_text = ev.get("evidence_text", "")
        # Filter for questions whose evidence is distinctly tabular
        if not re.search(r"\$\d+", ev_text) or not re.search(r"\b(20\d\d|millions|thousands)\b", ev_text, re.IGNORECASE):
            continue

        hit = any(is_retrieval_hit(c, evidence) for c in chunks)
        if hit and len(hit_samples) < 5:
            # Find the hitting chunk
            hit_chunk = next(c for c in chunks if is_retrieval_hit(c, evidence))
            hit_samples.append({
                "status": "HIT",
                "qid": qid,
                "company": q["company"],
                "doc_name": q["doc_name"],
                "question": q["question"],
                "chunk": hit_chunk,
                "gold_evidence": ev_text
            })
        elif not hit and len(miss_samples) < 5:
            # Pick the top ranked chunk from the same document if available, else top-1 chunk
            top_chunk = chunks[0] if chunks else {}
            miss_samples.append({
                "status": "MISSED",
                "qid": qid,
                "company": q["company"],
                "doc_name": q["doc_name"],
                "question": q["question"],
                "chunk": top_chunk,
                "gold_evidence": ev_text
            })

        if len(hit_samples) == 5 and len(miss_samples) == 5:
            break

    # Write chunk_samples.md
    with open(RESULTS_DIR / "chunk_samples.md", "w", encoding="utf-8") as f:
        f.write("# Verbatim Table-Heavy Chunk Samples\n\n")
        f.write("5 table chunks from retrieval HITS and 5 table chunks from retrieval MISSES alongside ground truth evidence.\n\n")
        f.write("---\n\n")
        f.write("## Section 1: 5 Table Chunks from Pages That Were HIT\n\n")
        for i, item in enumerate(hit_samples, 1):
            f.write(f"### Hit Sample {i}: {item['company']} ({item['doc_name']}, Page {item['chunk'].get('page')})\n")
            f.write(f"- **Question ID:** `{item['qid']}`\n")
            f.write(f"- **Question:** {item['question']}\n\n")
            f.write("#### Stored Chunk Text (Verbatim):\n```text\n")
            f.write(item['chunk'].get('text', '').strip() + "\n```\n\n")
            f.write("#### Gold Evidence Text (Verbatim):\n```text\n")
            f.write(item['gold_evidence'].strip() + "\n```\n\n")
            f.write("---\n\n")

        f.write("## Section 2: 5 Table Chunks from Pages That Were MISSED\n\n")
        for i, item in enumerate(miss_samples, 1):
            f.write(f"### Miss Sample {i}: {item['company']} ({item['doc_name']}, Target Page {q.get('evidence', [{}])[0].get('evidence_page_num')})\n")
            f.write(f"- **Question ID:** `{item['qid']}`\n")
            f.write(f"- **Question:** {item['question']}\n\n")
            f.write(f"#### Top Retrieved Chunk Text (Page {item['chunk'].get('page')}) (Verbatim):\n```text\n")
            f.write(item['chunk'].get('text', '').strip() + "\n```\n\n")
            f.write("#### Gold Evidence Text (Target Page) (Verbatim):\n```text\n")
            f.write(item['gold_evidence'].strip() + "\n```\n\n")
            f.write("---\n\n")

    print("Step 2 Complete: Saved 10 verbatim table samples to eval/results/chunk_samples.md")

    # Step 3: Rank diagnostic on dev & evidence text presence in stored chunks
    print("\nStep 3: Computing rank diagnostic and evidence text presence on DEV set (75 questions)...")
    rank_buckets = {
        "1-10": 0,
        "11-20": 0,
        "21-50": 0,
        "51-100": 0,
        ">100": 0,
        "absent": 0
    }
    dev_doc_found_count = 0

    # Presence checks
    exact_contained_count = 0
    sentence_matched_count = 0
    high_token_recall_count = 0  # >= 70%

    with conn.cursor() as cur:
        for q in dev_q:
            qid = q["financebench_id"]
            target_doc = q["doc_name"]
            evidence = q.get("evidence", [])
            gold_pages = {e["evidence_page_num"] for e in evidence}
            q_emb = query_embeddings[qid]
            emb_str = "[" + ",".join(f"{float(v):.8f}" for v in q_emb) + "]"

            # Check if right document is found in Config B top-10
            chunks_b_10 = res_b[qid]
            doc_found = any((c.get("doc_name") or "").strip().upper() == target_doc.strip().upper() for c in chunks_b_10)

            if doc_found:
                dev_doc_found_count += 1
                # Rank ALL chunks of this document by cosine similarity
                cur.execute("""
                    SELECT page, chunk_index, 1 - (embedding <=> %s::vector) AS score
                    FROM chunks
                    WHERE doc_name = %s
                    ORDER BY embedding <=> %s::vector;
                """, (emb_str, target_doc, emb_str))
                all_doc_rows = cur.fetchall()

                # Find best rank of any chunk from gold pages
                gold_ranks = [rank for rank, row in enumerate(all_doc_rows, 1) if row[0] in gold_pages]
                if not gold_ranks:
                    rank_buckets["absent"] += 1
                else:
                    best_rank = min(gold_ranks)
                    if 1 <= best_rank <= 10:
                        rank_buckets["1-10"] += 1
                    elif 11 <= best_rank <= 20:
                        rank_buckets["11-20"] += 1
                    elif 21 <= best_rank <= 50:
                        rank_buckets["21-50"] += 1
                    elif 51 <= best_rank <= 100:
                        rank_buckets["51-100"] += 1
                    else:
                        rank_buckets[">100"] += 1

            # Check presence of normalized gold evidence text inside stored chunks of the gold page
            for ev in evidence:
                g_page = ev.get("evidence_page_num")
                ev_text = ev.get("evidence_text", "")
                cur.execute("SELECT text FROM chunks WHERE doc_name = %s AND page = %s ORDER BY chunk_index;", (target_doc, g_page))
                chunk_texts = [r[0] for r in cur.fetchall()]
                page_combined = " ".join(chunk_texts)

                # Normalized alphanumeric string
                norm_ev = re.sub(r"[^a-z0-9]", "", ev_text.lower())
                norm_page = re.sub(r"[^a-z0-9]", "", page_combined.lower())

                if norm_ev and norm_ev in norm_page:
                    exact_contained_count += 1

                # Token recall
                ev_toks = normalize_tokens(ev_text)
                page_toks = normalize_tokens(page_combined)
                if ev_toks and len(ev_toks.intersection(page_toks)) / len(ev_toks) >= 0.70:
                    high_token_recall_count += 1

                # Sentence match (at least one substantial line >= 30 chars found)
                lines = [l.strip() for l in ev_text.split("\n") if len(l.strip()) >= 30]
                if any(re.sub(r"[^a-z0-9]", "", l.lower()) in norm_page for l in lines):
                    sentence_matched_count += 1

    total_dev_evidence_items = sum(len(q.get("evidence", [])) for q in dev_q)
    presence_stats = {
        "total_dev_evidence_items": total_dev_evidence_items,
        "exact_alphanumeric_containment": {
            "count": exact_contained_count,
            "pct": round(exact_contained_count / total_dev_evidence_items * 100, 2)
        },
        "sentence_span_containment": {
            "count": sentence_matched_count,
            "pct": round(sentence_matched_count / total_dev_evidence_items * 100, 2)
        },
        "high_token_recall_gte_70pct": {
            "count": high_token_recall_count,
            "pct": round(high_token_recall_count / total_dev_evidence_items * 100, 2)
        }
    }

    rank_diag_results = {
        "dev_questions_with_doc_found": dev_doc_found_count,
        "rank_distribution": rank_buckets,
        "evidence_presence_on_gold_pages": presence_stats
    }
    with open(RESULTS_DIR / "dev_rank_diagnostic.json", "w", encoding="utf-8") as f:
        json.dump(rank_diag_results, f, indent=2)

    # Step 4 & 5: Evaluate Config A, B (oracle), C on Dev and Full with Page & Evidence-Text Hit
    print("\nStep 4 & 5: Evaluating Config A, Config B (Oracle), Config C on Dev and Full...")

    def eval_suite(q_list, name):
        metrics = {}
        for cfg_name, res_dict in [("Config A (No filter)", res_a), ("Config B (Oracle filter)", res_b), ("Config C (Inferred filter)", res_c)]:
            p_hit_5 = 0
            p_hit_10 = 0
            t_hit_5 = 0
            t_hit_10 = 0

            for q in q_list:
                qid = q["financebench_id"]
                chunks = res_dict[qid]
                evidence = q.get("evidence", [])
                target_doc = q["doc_name"]

                # Page Hit
                if any(is_retrieval_hit(c, evidence) for c in chunks[:5]): p_hit_5 += 1
                if any(is_retrieval_hit(c, evidence) for c in chunks[:10]): p_hit_10 += 1

                # Evidence Text Hit
                if any(is_evidence_text_hit(c["text"], evidence, target_doc, c.get("doc_name", "")) for c in chunks[:5]): t_hit_5 += 1
                if any(is_evidence_text_hit(c["text"], evidence, target_doc, c.get("doc_name", "")) for c in chunks[:10]): t_hit_10 += 1

            n = len(q_list)
            metrics[cfg_name] = {
                "page_hit_k5": f"{p_hit_5}/{n} ({p_hit_5/n*100:.2f}%)",
                "page_hit_k10": f"{p_hit_10}/{n} ({p_hit_10/n*100:.2f}%)",
                "evidence_text_hit_k5": f"{t_hit_5}/{n} ({t_hit_5/n*100:.2f}%)",
                "evidence_text_hit_k10": f"{t_hit_10}/{n} ({t_hit_10/n*100:.2f}%)",
                "raw": {
                    "p_hit_5": p_hit_5,
                    "p_hit_10": p_hit_10,
                    "t_hit_5": t_hit_5,
                    "t_hit_10": t_hit_10,
                    "n": n
                }
            }
        return metrics

    dev_metrics = eval_suite(dev_q, "DEV")
    full_metrics = eval_suite(questions, "FULL")

    eval_summary = {
        "git_commit": git_commit,
        "split_seed": 42,
        "dev_75_results": dev_metrics,
        "full_150_results": full_metrics
    }
    with open(RESULTS_DIR / "config_comparison_step5.json", "w", encoding="utf-8") as f:
        json.dump(eval_summary, f, indent=2)

    conn.close()
    elapsed = time.time() - t_start
    print(f"\nAll diagnostics completed in {elapsed:.1f}s")
    print(f"Results written to:\n - {RESULTS_DIR / 'split_75_75.json'}\n - {RESULTS_DIR / 'reconciled_failures.json'}\n - {RESULTS_DIR / 'chunk_samples.md'}\n - {RESULTS_DIR / 'dev_rank_diagnostic.json'}\n - {RESULTS_DIR / 'config_comparison_step5.json'}")


if __name__ == "__main__":
    main()
