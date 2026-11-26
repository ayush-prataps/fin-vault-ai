"""
FinanceBench Evaluation Harness for FinVault AI.

Evaluates retrieval hit rate (k=5, k=10) and answer accuracy against gold
SEC filing evidence from the FinanceBench dataset.

Compares:
  Config A: Naive baseline (top-k vector search without ticker filter)
  Config B: Pipeline (top-k vector search with company ticker filter)
"""

import json
import logging
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure backend directory is in sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.config import settings
from app.core.embeddings import embed_text
from app.core.llm import call_llm
from app.core.retrieval import build_rag_prompt
from app.core.vector import search_chunks

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("eval")


def get_git_commit() -> str:
    """Return current git commit hash."""
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(BASE_DIR))
        return out.decode().strip()
    except Exception:
        return "unknown"


def call_with_retry(fn, *args, max_retries: int = 8, initial_delay: float = 3.0, **kwargs):
    """Execute function with exponential backoff on rate limits."""
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            err_msg = str(exc).lower()
            if "rate_limit" in err_msg or "429" in err_msg or "too many requests" in err_msg:
                logger.warning(f"Rate limit hit (attempt {attempt + 1}/{max_retries}), sleeping {delay:.1f}s: {exc}")
                time.sleep(delay)
                delay *= 2.0
            elif attempt == max_retries - 1:
                raise
            else:
                logger.warning(f"Error on attempt {attempt + 1}/{max_retries}: {exc}. Retrying in {delay:.1f}s...")
                time.sleep(delay)


def is_retrieval_hit(chunk: Dict[str, Any], gold_evidence_list: List[Dict[str, Any]]) -> bool:
    """
    Check if a retrieved chunk matches any gold evidence item.
    Match condition: doc_name and 0-indexed page number match.
    """
    chunk_doc = (chunk.get("doc_name") or "").strip().upper()
    chunk_page = chunk.get("page")

    for ev in gold_evidence_list:
        ev_doc = (ev.get("doc_name") or "").strip().upper()
        ev_page = ev.get("evidence_page_num")
        if chunk_doc == ev_doc and chunk_page == ev_page:
            return True
    return False


def check_abstention(answer_text: str) -> bool:
    """Return True if model explicitly abstained from answering."""
    text_lower = answer_text.lower()
    phrases = [
        "cannot answer this question",
        "i cannot answer",
        "not provided in the",
        "not mentioned in the provided",
        "excerpts do not contain",
        "does not contain information",
        "does not provide information",
    ]
    return any(p in text_lower for p in phrases)


def try_numeric_match(gold_answer: str, pred_answer: str) -> Optional[bool]:
    """
    Tolerance-based match for pure numeric / percentage answers.
    Returns True if match within 2% or unit match, False if numeric but failed, None if not purely numeric.
    """
    gold_cleaned = gold_answer.strip().replace(",", "")
    # Check if gold answer is essentially a single numeric value (e.g. $1577.00, 4.2%, $8.70, $12645.00)
    num_match = re.search(r"^[\$€£]?\s*(-?\d+(?:\.\d+)?)\s*(%|million|billion)?$", gold_cleaned, re.IGNORECASE)
    if not num_match:
        return None

    gold_val = float(num_match.group(1))
    gold_unit = (num_match.group(2) or "").lower()

    # Search for candidate numbers in predicted answer
    candidates = re.findall(r"[\$€£]?\s*(-?[\d,]+(?:\.\d+)?)\s*(%|million|billion)?", pred_answer, re.IGNORECASE)
    if not candidates:
        return False

    for num_str, unit_str in candidates:
        try:
            val = float(num_str.replace(",", ""))
            unit = unit_str.lower()
            # If units match or no unit specified
            if unit == gold_unit or not gold_unit:
                denom = max(abs(gold_val), 1e-6)
                if abs(val - gold_val) / denom <= 0.02:
                    return True
            # Check million vs billion conversion (e.g., 8738 million vs 8.7 billion)
            if gold_unit == "billion" and unit == "million" and abs(val / 1000.0 - gold_val) <= 0.05:
                return True
            if gold_unit == "million" and unit == "billion" and abs(val * 1000.0 - gold_val) <= 50.0:
                return True
        except ValueError:
            continue

    return False


def llm_judge(
    question: str,
    gold_answer: str,
    justification: str,
    pred_answer: str,
    model: str,
) -> Tuple[int, str]:
    """
    Use LLM as a judge with strict rubric to score predicted answer against ground truth.
    Returns (score: 0 or 1, reason: str).
    """
    prompt = f"""You are a financial QA evaluation judge. Determine whether the PREDICTED ANSWER is correct compared to the GOLD ANSWER and JUSTIFICATION from an SEC filing.

QUESTION:
{question}

GOLD ANSWER:
{gold_answer}

GOLD JUSTIFICATION:
{justification}

PREDICTED ANSWER:
{pred_answer}

RUBRIC:
1. Score 1 (CORRECT) if:
   - The predicted answer provides the correct factual answer matching the gold answer.
   - Key numeric figures match within reasonable rounding or unit expression.
   - For qualitative questions (reasons, segments, categories, legal battles, trends), key concepts match the gold answer.
   - If the gold answer states that performance is not measured by that metric or not reported, and the predicted answer correctly states that, it is CORRECT.
2. Score 0 (INCORRECT) if:
   - The predicted answer is factually wrong, contradicts the gold answer, or hallucinates numbers/facts.
   - The predicted answer abstains ("I cannot answer...") when the gold answer shows it is answerable.
   - The predicted answer answers incorrectly instead of abstaining.

Return ONLY a valid JSON object:
{{"score": 1, "reason": "brief 1-sentence reason"}} or {{"score": 0, "reason": "brief 1-sentence reason"}}"""

    try:
        res = call_with_retry(call_llm, prompt=prompt, model=model)
        raw_text = res.get("output", "").strip()
        # Parse JSON from response
        json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            score = int(data.get("score", 0))
            reason = str(data.get("reason", ""))
            return score, reason
    except Exception as exc:
        logger.error(f"LLM judge failed: {exc}")

    return 0, "Judge parse failed"


def run_evaluation() -> Dict[str, Any]:
    dataset_path = BASE_DIR / "data" / "financebench_filtered.jsonl"
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        questions = [json.loads(line) for line in f if line.strip()]

    total_q = len(questions)
    logger.info(f"Loaded {total_q} questions from {dataset_path.name}")

    git_commit = get_git_commit()
    target_model = settings.llm_model
    if not target_model:
        raise ValueError("LLM_MODEL is not configured")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    # Metrics storage
    # Config A: Baseline (no company filter)
    # Config B: Pipeline (with company filter)
    config_a_hits_5 = 0
    config_a_hits_10 = 0
    config_b_hits_5 = 0
    config_b_hits_10 = 0

    pipeline_correct = 0
    pipeline_abstained = 0
    pipeline_incorrect = 0
    api_models_seen = set()

    question_results: List[Dict[str, Any]] = []

    for idx, q in enumerate(questions, 1):
        q_id = q.get("financebench_id", f"q_{idx}")
        company = q.get("company")
        doc_name = q.get("doc_name")
        query_text = q.get("question")
        gold_answer = q.get("answer", "")
        justification = q.get("justification", "") or ""
        evidence_list = q.get("evidence", [])

        logger.info(f"[{idx}/{total_q}] Eval: {company} - {q_id}")

        # 1. Embed query
        q_emb = embed_text(query_text)

        # 2. Config A: Search top 10 without ticker filter
        chunks_a_10 = search_chunks(query_embedding=q_emb, company=None, top_k=10)
        chunks_a_5 = chunks_a_10[:5]
        hit_a_5 = any(is_retrieval_hit(c, evidence_list) for c in chunks_a_5)
        hit_a_10 = any(is_retrieval_hit(c, evidence_list) for c in chunks_a_10)
        if hit_a_5:
            config_a_hits_5 += 1
        if hit_a_10:
            config_a_hits_10 += 1

        # 3. Config B: Search top 10 with ticker filter
        chunks_b_10 = search_chunks(query_embedding=q_emb, company=company, top_k=10)
        chunks_b_5 = chunks_b_10[:5]
        hit_b_5 = any(is_retrieval_hit(c, evidence_list) for c in chunks_b_5)
        hit_b_10 = any(is_retrieval_hit(c, evidence_list) for c in chunks_b_10)
        if hit_b_5:
            config_b_hits_5 += 1
        if hit_b_10:
            config_b_hits_10 += 1

        # 4. Generate Answer using Config B top 5
        rag_prompt = build_rag_prompt(query_text, chunks_b_5)
        llm_resp = call_with_retry(call_llm, prompt=rag_prompt, model=target_model)
        api_model = llm_resp["model"]
        pred_answer = llm_resp.get("output", "").strip()
        tokens_used = llm_resp.get("tokens_used", 0)
        prompt_tokens = llm_resp.get("prompt_tokens", 0)
        completion_tokens = llm_resp.get("completion_tokens", 0)
        latency_ms = llm_resp.get("latency_ms", 0)

        # Pacing delay between LLM calls to respect API rate limits
        time.sleep(2.0)

        # 5. Check abstention
        abstained = check_abstention(pred_answer)

        # 6. Evaluate Accuracy
        score = 0
        eval_method = "llm_judge"
        judge_reason = ""

        if abstained:
            score = 0
            eval_method = "abstention"
            judge_reason = "Model abstained from answering."
            pipeline_abstained += 1
        else:
            # Try numeric match first
            num_match = try_numeric_match(gold_answer, pred_answer)
            if num_match is True:
                score = 1
                eval_method = "numeric_tolerance"
                judge_reason = "Numeric exact/tolerance match passed."
            else:
                # LLM Judge
                j_score, j_reason = llm_judge(
                    question=query_text,
                    gold_answer=gold_answer,
                    justification=justification,
                    pred_answer=pred_answer,
                    model=target_model,
                )
                score = j_score
                judge_reason = j_reason
                time.sleep(2.0)

        if score == 1:
            pipeline_correct += 1
        else:
            if not abstained:
                pipeline_incorrect += 1

        # Citations summary
        citations_summary = [
            {
                "n": c_idx + 1,
                "company": c.get("company"),
                "doc_name": c.get("doc_name"),
                "year": c.get("year"),
                "page": c.get("page"),
                "similarity_score": c.get("similarity_score"),
                "is_gold_hit": is_retrieval_hit(c, evidence_list),
            }
            for c_idx, c in enumerate(chunks_b_5)
        ]

        api_models_seen.add(api_model)
        q_res = {
            "id": q_id,
            "company": company,
            "doc_name": doc_name,
            "question": query_text,
            "gold_answer": gold_answer,
            "predicted_answer": pred_answer,
            "api_model": api_model,
            "score": score,
            "abstained": abstained,
            "eval_method": eval_method,
            "judge_reason": judge_reason,
            "hit_a_5": hit_a_5,
            "hit_a_10": hit_a_10,
            "hit_b_5": hit_b_5,
            "hit_b_10": hit_b_10,
            "tokens_used": tokens_used,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "latency_ms": latency_ms,
            "citations": citations_summary,
        }
        question_results.append(q_res)

    # Calculate aggregate rates
    rate_a_5 = round(config_a_hits_5 / total_q, 4)
    rate_a_10 = round(config_a_hits_10 / total_q, 4)
    rate_b_5 = round(config_b_hits_5 / total_q, 4)
    rate_b_10 = round(config_b_hits_10 / total_q, 4)

    accuracy_rate = round(pipeline_correct / total_q, 4)
    abstention_rate = round(pipeline_abstained / total_q, 4)
    incorrect_rate = round(pipeline_incorrect / total_q, 4)

    # Select 20 questions for manual human review (all failures + sample of correct)
    failures = [q for q in question_results if q["score"] == 0]
    successes = [q for q in question_results if q["score"] == 1]
    needed_successes = max(0, 20 - len(failures))
    review_sample = failures + successes[:needed_successes]
    flagged_ids = [q["id"] for q in review_sample[:20]]

    # Failed questions breakdown
    failed_questions = [
        {
            "id": q["id"],
            "company": q["company"],
            "question": q["question"],
            "gold_answer": q["gold_answer"],
            "predicted_answer": q["predicted_answer"],
            "abstained": q["abstained"],
            "judge_reason": q["judge_reason"],
            "citations": q["citations"],
        }
        for q in failures
    ]

    reported_model = sorted(api_models_seen)[0] if len(api_models_seen) == 1 else sorted(api_models_seen)
    summary = {
        "git_commit": git_commit,
        "timestamp": timestamp,
        "model": reported_model,
        "api_models_returned": sorted(api_models_seen),
        "chunk_size": 400,
        "total_questions": total_q,
        "retrieval": {
            "config_a_baseline_no_filter": {
                "hit_rate_at_5": rate_a_5,
                "hit_count_at_5": config_a_hits_5,
                "hit_rate_at_10": rate_a_10,
                "hit_count_at_10": config_a_hits_10,
            },
            "config_b_pipeline_with_filter": {
                "hit_rate_at_5": rate_b_5,
                "hit_count_at_5": config_b_hits_5,
                "hit_rate_at_10": rate_b_10,
                "hit_count_at_10": config_b_hits_10,
            },
        },
        "generation": {
            "accuracy": accuracy_rate,
            "correct_count": pipeline_correct,
            "abstention_rate": abstention_rate,
            "abstained_count": pipeline_abstained,
            "incorrect_rate": incorrect_rate,
            "incorrect_count": pipeline_incorrect,
        },
        "manual_review_20_flagged_ids": flagged_ids,
        "failed_questions": failed_questions,
        "all_questions": question_results,
    }

    # Save to results file
    results_dir = BASE_DIR / "eval" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    results_file = results_dir / f"{timestamp}.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Results written to {results_file}")

    # Print summary table
    print("\n" + "=" * 60)
    print("FINANCEBENCH EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Commit:           {git_commit}")
    print(f"Model (API):      {reported_model}")
    print(f"Total Questions:  {total_q}")
    print("-" * 60)
    print("RETRIEVAL HIT RATE (evidence page in top-k):")
    print(f"  Config A (No filter):   k=5: {rate_a_5 * 100:.1f}% ({config_a_hits_5}/{total_q}) | k=10: {rate_a_10 * 100:.1f}% ({config_a_hits_10}/{total_q})")
    print(f"  Config B (With filter): k=5: {rate_b_5 * 100:.1f}% ({config_b_hits_5}/{total_q}) | k=10: {rate_b_10 * 100:.1f}% ({config_b_hits_10}/{total_q})")
    print("-" * 60)
    print("GENERATION ACCURACY (Config B top-5):")
    print(f"  Accuracy:         {accuracy_rate * 100:.1f}% ({pipeline_correct}/{total_q})")
    print(f"  Abstention Rate:  {abstention_rate * 100:.1f}% ({pipeline_abstained}/{total_q})")
    print(f"  Incorrect Rate:   {incorrect_rate * 100:.1f}% ({pipeline_incorrect}/{total_q})")
    print("-" * 60)
    print(f"Flagged for human review: {len(flagged_ids)} questions")
    print(f"Full results JSON: {results_file}")
    print("=" * 60 + "\n")

    return summary


if __name__ == "__main__":
    run_evaluation()
