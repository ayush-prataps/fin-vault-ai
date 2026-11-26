#!/usr/bin/env python3
"""
Answer-level evaluation harness for FinVault AI's frozen RAG pipeline.

Features:
- Resumable per-question JSONL caching for both generation and LLM judge verdicts
  (keyed by LLM_MODEL and config hash).
- Header-aware rate-limit pacing and exponential backoff for OpenAI-compatible APIs.
- Deterministic numeric tolerance matching + fixed-rubric LLM judge.
- Computes 95% Wilson score confidence intervals on all metrics and conditional
  accuracy broken down by retrieval Page Hit@k vs Retrieval Miss.
- Generates human review markdown/JSON files for:
  - 20 sampled LLM judge verdicts
  - 30 sampled answers' (claim, cited chunk text) citation support pairs
- Supports --split dev, --split test, and --split abstention --abstention-file <path>.
"""
import argparse
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import psycopg2
from app.config import settings
from app.core.llm import call_llm
from app.core.retrieval import PROMPT_TEMPLATES, build_rag_prompt, retrieve_chunks_with_meta
from eval.evaluate_chunks_v2 import is_page_hit, is_token_recall_hit

DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
SPLIT_PATH = BASE_DIR / "eval" / "results" / "split_75_75.json"
ALIASES_PATH = BASE_DIR / "config" / "aliases.json"
RESULTS_DIR = BASE_DIR / "eval" / "results"
CACHE_DIR = RESULTS_DIR / "cache"

DEFAULT_JUDGE_MODEL = None  # Defaults to configured LLM_MODEL unless overridden via --judge-model

JUDGE_RUBRIC_TEMPLATE = """You are an impartial financial QA evaluation judge. Compare the PREDICTED ANSWER against the GOLD ANSWER and GOLD JUSTIFICATION from an SEC filing.

QUESTION:
{question}

GOLD ANSWER:
{gold_answer}

GOLD JUSTIFICATION:
{justification}

PREDICTED ANSWER:
{pred_answer}

RUBRIC:
Score 1 (CORRECT) if ALL of the following hold:
- The predicted answer directly agrees with the core conclusion of the gold answer (same yes/no direction, same drivers/causes, same identified entities/segments/categories, or correctly identifies when the filing explicitly reports a metric is zero, none, or not measured).
- Key numeric values or percentages match within reasonable rounding or unit expression (e.g., $1.6B vs $1,600M, 1.7% vs 1.7 percentage points).
- It does not contradict the gold answer or hallucinate key facts.

Score 0 (WRONG) if ANY of the following hold:
- The predicted answer reaches the wrong conclusion, identifies the wrong entity/segment/fiscal period, or misses the essential answer.
- Key numbers differ materially (>2% or wrong sign/unit).
- The predicted answer refuses or abstains when the question is answerable, OR invents claims contradicted by the gold answer.

Respond ONLY with valid JSON:
{{"verdict": "correct" | "wrong", "reason": "<one concise sentence explaining the verdict>"}}"""


def get_git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=str(BASE_DIR)).decode().strip()
    except Exception:
        return "unknown"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_config_payload(
    prompt_version: str,
    top_k: int,
    generator_model: str,
    judge_model: str,
) -> Dict[str, Any]:
    aliases_hash = sha256_text(ALIASES_PATH.read_text(encoding="utf-8")) if ALIASES_PATH.exists() else ""
    payload = {
        "prompt_version": prompt_version,
        "prompt_template": PROMPT_TEMPLATES[prompt_version],
        "llm_base_url": (os.getenv("LLM_BASE_URL", settings.llm_base_url) or "").strip(),
        "generator_model": generator_model,
        "temperature": 0.0,
        "max_tokens": settings.llm_max_tokens,
        "timeout_seconds": settings.llm_timeout_seconds,
        "retriever": {
            "table": "chunks_v2",
            "embedding_model": settings.embedding_model,
            "metadata_mode": "inferred_config_c_with_missing_year_fallback",
            "aliases_sha256": aliases_hash,
            "top_k": top_k,
        },
        "judge_model": judge_model,
        "judge_rubric_sha256": sha256_text(JUDGE_RUBRIC_TEMPLATE),
    }
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    payload["config_hash"] = sha256_text(canonical)
    return payload


def wilson_interval(k: int, n: int) -> Dict[str, Any]:
    """Compute rate and 95% Wilson score confidence interval."""
    if n == 0:
        return {"k": 0, "n": 0, "rate": 0.0, "ci_95": [0.0, 0.0], "formatted": "0/0 (0.0%) [0.0%, 0.0%]"}
    z = 1.959963984540054
    p = k / n
    denom = 1.0 + (z**2) / n
    center = p + (z**2) / (2.0 * n)
    margin = z * math.sqrt((p * (1.0 - p) + (z**2) / (4.0 * n)) / n)
    low = max(0.0, (center - margin) / denom)
    high = min(1.0, (center + margin) / denom)
    return {
        "k": k,
        "n": n,
        "rate": round(p, 6),
        "ci_95": [round(low, 6), round(high, 6)],
        "formatted": f"{k}/{n} ({p * 100:.1f}%) [{low * 100:.1f}%, {high * 100:.1f}%]",
    }


def parse_reset_seconds(reset_str: Optional[str]) -> float:
    """Parse header duration strings such as '53.631s', '1m26.4s', '142ms' into seconds."""
    if not reset_str:
        return 0.0
    total = 0.0
    for val, unit in re.findall(r"(\d+(?:\.\d+)?)(ms|s|m|h)", str(reset_str)):
        num = float(val)
        if unit == "ms":
            total += num / 1000.0
        elif unit == "s":
            total += num
        elif unit == "m":
            total += num * 60.0
        elif unit == "h":
            total += num * 3600.0
    return total


class LLMPacer:
    """Per-model optional token-bucket pacer with exponential backoff on rate limits."""

    def __init__(self, tpm_limit: int = 8000):
        self.tpm_limit = tpm_limit
        self.state: Dict[str, Dict[str, Any]] = {}

    def _estimate_tokens(self, prompt: str) -> int:
        return max(400, int(len(prompt) / 2.6) + 350)

    def _wait_if_needed(self, model: str, needed_tokens: int) -> None:
        st = self.state.get(model)
        if not st:
            return
        elapsed = time.time() - st["updated_at"]
        refill = elapsed * (self.tpm_limit / 60.0)
        est_remaining = min(float(self.tpm_limit), st["remaining_tokens"] + refill)
        if est_remaining < needed_tokens:
            deficit = needed_tokens - est_remaining
            wait_s = (deficit / self.tpm_limit) * 60.0 + 1.5
            max_reset = max(0.0, st["reset_seconds"] - elapsed) + 0.5
            sleep_s = min(max(wait_s, 1.0), max(max_reset, 2.0))
            print(f"    [pacer:{model}] est_rem={est_remaining:.0f} < need={needed_tokens}, sleeping {sleep_s:.1f}s")
            time.sleep(sleep_s)

    def call(self, prompt: str, model: str, max_retries: int = 8) -> Dict[str, Any]:
        needed = min(self.tpm_limit - 200, self._estimate_tokens(prompt))
        self._wait_if_needed(model, needed)

        delay = 8.0
        for attempt in range(max_retries):
            try:
                res = call_llm(prompt=prompt, model=model, use_cache=False)
                rem_raw = res.get("ratelimit_remaining_tokens")
                rst_raw = res.get("ratelimit_reset_tokens")
                if rem_raw is not None:
                    self.state[model] = {
                        "remaining_tokens": float(rem_raw),
                        "reset_seconds": parse_reset_seconds(rst_raw),
                        "updated_at": time.time(),
                    }
                return res
            except Exception as exc:
                msg = str(exc).lower()
                if "tokens per day" in msg or "tpd" in msg or "requests per day" in msg or "rpd" in msg:
                    raise RuntimeError(f"Daily API quota reached for {model}: {exc}") from exc
                if "429" in msg or "rate_limit" in msg or "too many requests" in msg or "rate limit" in msg:
                    m_wait = re.search(r"try again in\s+(\d+(?:\.\d+)?)\s*(ms|s|m)", msg)
                    if m_wait:
                        wait_s = parse_reset_seconds(m_wait.group(1) + m_wait.group(2)) + 2.0
                    else:
                        wait_s = delay
                    print(f"    [backoff:{model}] 429 hit (attempt {attempt + 1}/{max_retries}), sleeping {wait_s:.1f}s")
                    time.sleep(wait_s)
                    self.state.pop(model, None)
                    delay = min(delay * 1.8, 90.0)
                    continue
                if attempt == max_retries - 1:
                    raise
                print(f"    [retry:{model}] transient error (attempt {attempt + 1}/{max_retries}): {exc}; sleeping {delay:.1f}s")
                time.sleep(delay)
                delay = min(delay * 2.0, 60.0)

        raise RuntimeError(f"Exhausted {max_retries} retries calling {model}")


def check_abstention(answer_text: str) -> bool:
    """Return True if the model explicitly abstained rather than giving a substantive answer."""
    text = (answer_text or "").strip()
    if not text:
        return True
    lower = text.lower()

    strong_phrases = [
        "i cannot answer this question",
        "cannot answer this question",
        "i cannot answer based on",
        "cannot answer based on",
        "excerpts do not contain enough information",
        "context does not contain enough information",
        "do not contain enough information to answer",
        "does not contain enough information to answer",
        "do not contain sufficient information",
        "does not contain sufficient information",
        "insufficient information to answer",
        "unable to answer this question",
    ]
    if any(p in lower for p in strong_phrases):
        return True

    # Check if the opening sentence declines to answer due to missing context
    first_sentence = re.split(r"(?<=[.!?])\s+", lower, maxsplit=1)[0]
    opening_phrases = [
        "cannot determine",
        "unable to determine",
        "not provided in the",
        "not mentioned in the provided",
        "not disclosed in the provided",
        "not stated in the provided",
        "is not stated in",
        "is not disclosed in",
        "is not provided in",
        "do not contain information",
        "does not contain information",
        "does not provide information",
        "do not provide information",
        "does not explicitly state",
        "do not explicitly state",
        "does not state",
        "do not state",
        "does not specify",
        "do not specify",
        "no information about",
    ]
    if any(p in first_sentence for p in opening_phrases):
        return True

    return False


_SCALE_MAP = {
    "": 1.0,
    "k": 1e3,
    "thousand": 1e3,
    "thousands": 1e3,
    "m": 1e6,
    "mm": 1e6,
    "mn": 1e6,
    "million": 1e6,
    "millions": 1e6,
    "b": 1e9,
    "bn": 1e9,
    "billion": 1e9,
    "billions": 1e9,
}


def _detect_question_scale(question: str) -> float:
    q_low = question.lower()
    if re.search(r"\b(?:in\s+usd\s+billions|in\s+billions)\b", q_low):
        return 1e9
    if re.search(r"\b(?:in\s+usd\s+millions|in\s+millions)\b", q_low):
        return 1e6
    if re.search(r"\b(?:in\s+usd\s+thousands|in\s+thousands)\b", q_low):
        return 1e3
    return 1.0


def _mask_years_and_citations(text: str) -> str:
    # Remove bracketed citations like [1], [1, 2]
    cleaned = re.sub(r"\[[\d,\s]+\]", " ", text)
    # Remove FY/quarter identifiers and date years
    cleaned = re.sub(r"\bFY\s*(?:19|20)?\d{2}\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bQ[1-4]\s*(?:19|20)?\d{2}\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(
        r"\b(?:19|20)\d{2}\b(?!(?:\.\d|\s*(?:%|percent|million|millions|billion|billions|thousand|thousands)))",
        " ",
        cleaned,
    )
    return cleaned


def try_numeric_match(question: str, gold_answer: str, pred_answer: str) -> Optional[bool]:
    """
    Tolerance-based numeric matching for pure numeric / currency / percentage gold answers.
    Returns:
      True: pure numeric gold answer and prediction matches within tolerance.
      False: pure numeric gold answer and prediction does not match.
      None: gold answer is not pure numeric (route to LLM judge).
    """
    gold_clean = gold_answer.strip().replace(",", "")
    # Handle accounting parentheses e.g. ($15.00) -> -$15.00
    paren_m = re.match(r"^\((.*)\)$", gold_clean)
    if paren_m:
        gold_clean = "-" + paren_m.group(1)

    m = re.match(
        r"^\s*([+-]?)\s*[\$€£]?\s*([+-]?\d+(?:\.\d+)?)\s*(%|million|millions|billion|billions|thousand|thousands|x|times|days)?\s*$",
        gold_clean,
        re.IGNORECASE,
    )
    if not m:
        return None

    sign_prefix, num_str, unit_raw = m.groups()
    gold_val = float(num_str)
    if sign_prefix == "-" and gold_val > 0:
        gold_val = -gold_val
    decimals = len(num_str.split(".")[1]) if "." in num_str else 0
    gold_unit = (unit_raw or "").lower()

    is_pct = gold_unit == "%"
    has_currency = any(sym in gold_answer for sym in ("$", "€", "£"))
    q_scale = _detect_question_scale(question) if gold_unit == "" else 1.0
    gold_scale = _SCALE_MAP.get(gold_unit, 1.0) if gold_unit in _SCALE_MAP else 1.0
    if gold_unit == "" and not is_pct and (has_currency or q_scale > 1.0):
        gold_scale = q_scale
    gold_abs = gold_val * gold_scale

    pred_masked = _mask_years_and_citations(pred_answer)
    pattern = re.compile(
        r"(?P<open_paren>\()?(?P<sign>[+-])?\s*(?P<curr>[\$€£])?\s*(?P<num>\d[\d,]*(?:\.\d+)?)(?P<close_paren>\))?\s*(?P<unit>%|percentage\s+points?|percent|millions?|billions?|thousands?|mm|mn|bn|[MBK](?=\b)|x|times)?",
        re.IGNORECASE,
    )

    q_low = question.lower()
    allow_pct_ratio = (
        gold_unit == ""
        and abs(gold_val) < 1.0
        and any(w in q_low for w in ("margin", "roa", "roe", "ratio", "rate", "cagr", "growth", "yield", "return"))
    )

    for cm in pattern.finditer(pred_masked):
        raw_num = cm.group("num").replace(",", "")
        if not raw_num:
            continue
        val = float(raw_num)
        if cm.group("sign") == "-" or (cm.group("open_paren") and cm.group("close_paren")):
            val = -abs(val)

        unit = (cm.group("unit") or "").lower().strip()
        if unit.startswith("percent"):
            unit = "%"

        if is_pct:
            if unit != "%":
                continue
            target = gold_val
            tol = max(0.02 * abs(target), 0.5 * (10 ** (-decimals)) if decimals > 0 else 0.0)
            if abs(target) < 1e-9:
                if abs(val) <= 1e-6:
                    return True
            elif abs(val - target) <= tol:
                return True
            continue

        # Gold is non-percentage
        if unit == "%":
            if allow_pct_ratio:
                val_ratio = val / 100.0
                tol = max(0.02 * abs(gold_val), 0.5 * (10 ** (-decimals)) if decimals > 0 else 0.0)
                if abs(val_ratio - gold_val) <= tol:
                    return True
            continue

        if unit in ("x", "times"):
            pred_abs = val
            candidate_targets = [gold_val]
        else:
            unit_scale = _SCALE_MAP.get(unit, 1.0)
            if unit == "" and (cm.group("curr") or q_scale > 1.0):
                # Prediction could be in question scale (omitting "million") OR raw matching gold_val
                candidate_scales = [1.0, q_scale]
            else:
                candidate_scales = [unit_scale]

            if abs(gold_val) < 1e-9:
                if abs(val) <= 1e-6:
                    return True
                continue

            matched = False
            for sc in candidate_scales:
                pred_abs = val * sc
                # Compare against scaled gold_abs AND unscaled gold_val if scales align
                for tgt in (gold_abs, gold_val) if (unit == "" and q_scale > 1.0) else (gold_abs,):
                    if tgt == 0:
                        continue
                    half_ulp = 0.5 * (10 ** (-decimals)) * (tgt / gold_val if gold_val != 0 else 1.0)
                    use_ulp = decimals > 0 and (abs(gold_val) < 1.0 or "round" in q_low)
                    tol = max(0.02 * abs(tgt), half_ulp if use_ulp else 0.0)
                    if abs(pred_abs - tgt) <= tol:
                        return True
            if matched:
                return True
            continue

        # x / times comparison
        if abs(gold_val) < 1e-9:
            if abs(val) <= 1e-6:
                return True
        else:
            tol = max(0.02 * abs(gold_val), 0.5 * (10 ** (-decimals)) if decimals > 0 and abs(gold_val) < 1.0 else 0.0)
            if abs(val - gold_val) <= tol:
                return True

    return False


def judge_answer(
    pacer: LLMPacer,
    judge_cache: Dict[str, Dict[str, Any]],
    judge_cache_path: Path,
    fb_id: str,
    question: str,
    gold_answer: str,
    justification: str,
    pred_answer: str,
    judge_model: str,
) -> Dict[str, Any]:
    """Run LLM judge with fixed rubric and cache verdict keyed by answer/gold hashes."""
    rubric_hash = sha256_text(JUDGE_RUBRIC_TEMPLATE)[:12]
    key = sha256_text(f"{fb_id}|{gold_answer}|{pred_answer}|{judge_model}|{rubric_hash}")
    if key in judge_cache:
        return judge_cache[key]

    prompt = JUDGE_RUBRIC_TEMPLATE.format(
        question=question,
        gold_answer=gold_answer,
        justification=justification or "N/A",
        pred_answer=pred_answer,
    )
    res = pacer.call(prompt=prompt, model=judge_model)
    raw = (res.get("output") or "").strip()
    verdict = "wrong"
    reason = "Judge output parse failed"

    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(0))
            v_str = str(data.get("verdict", "")).strip().lower()
            if v_str in ("correct", "1", "true"):
                verdict = "correct"
            else:
                verdict = "wrong"
            reason = str(data.get("reason", "")).strip()
        except json.JSONDecodeError:
            pass

    entry = {
        "cache_key": key,
        "financebench_id": fb_id,
        "verdict": verdict,
        "reason": reason,
        "judge_model": res["model"],
        "tokens_used": res["tokens_used"],
        "raw_output": raw,
    }
    judge_cache[key] = entry
    with open(judge_cache_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return entry


def load_cache(cache_path: Path, key_field: str = "financebench_id") -> Dict[str, Dict[str, Any]]:
    cache: Dict[str, Dict[str, Any]] = {}
    if not cache_path.exists():
        return cache
    with open(cache_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                k = rec.get(key_field)
                if k:
                    cache[k] = rec
            except json.JSONDecodeError:
                continue
    return cache


def extract_claim_citation_pairs(pred_answer: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Split an answer into claims and pair each referenced [n] citation with its chunk text.
    Never auto-scores support; leaves evaluation strictly to human reviewers.
    """
    # Merge standalone trailing citation markers like ".\n\n[10]" onto previous text
    text = re.sub(r"\n+\s*(\[[\d,\s]+\])\s*$", r" \1", pred_answer.strip())
    raw_lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    claims: List[str] = []
    for ln in raw_lines:
        # Clean markdown list prefix
        ln_clean = re.sub(r"^(?:[-*]|\d+\.)\s+", "", ln).strip()
        # Split non-bullet paragraphs into sentences after bracket+punctuation or punctuation
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\*\(\[])", ln_clean)
        for p in parts:
            p = p.strip()
            if not p:
                continue
            # Merge orphan citation-only fragment onto previous claim
            if re.fullmatch(r"(\[[\d,\s]+\]\.?)+", p) and claims:
                claims[-1] = claims[-1].rstrip(".") + " " + p
                continue
            # Skip short bold-only section headers ending with ":"
            if p.endswith(":") and len(p) < 80 and not re.search(r"\[\d+\]", p):
                continue
            claims.append(p)

    pairs: List[Dict[str, Any]] = []
    max_idx = len(chunks)
    for claim in claims:
        cite_nums: List[int] = []
        for grp in re.findall(r"\[([\d,\s]+)\]", claim):
            for num_s in grp.split(","):
                num_s = num_s.strip()
                if num_s.isdigit():
                    idx = int(num_s)
                    if 1 <= idx <= max_idx and idx not in cite_nums:
                        cite_nums.append(idx)

        if cite_nums:
            for c_idx in cite_nums:
                ch = chunks[c_idx - 1]
                pairs.append({
                    "claim": claim,
                    "citation_num": c_idx,
                    "doc_name": ch.get("doc_name"),
                    "year": ch.get("year"),
                    "page": ch.get("page"),
                    "cited_chunk_text": ch.get("text", ""),
                })
        elif len(claim) > 20:
            pairs.append({
                "claim": claim,
                "citation_num": None,
                "doc_name": None,
                "year": None,
                "page": None,
                "cited_chunk_text": "[NO CITATION EMITTED FOR CLAIM]",
            })

    return pairs


def generate_review_files(records: List[Dict[str, Any]], tag: str, seed: int = 42) -> Dict[str, str]:
    """Write 20 sampled LLM judge verdicts and 30 sampled citation-support pairs for human review."""
    rng = random.Random(seed)
    paths: Dict[str, str] = {}

    # 1. Sample 20 LLM judge verdicts (stratified by correct vs wrong if available)
    judge_recs = [r for r in records if r["eval_method"] == "llm_judge"]
    j_correct = [r for r in judge_recs if r["verdict"] == "correct"]
    j_wrong = [r for r in judge_recs if r["verdict"] == "wrong"]
    rng.shuffle(j_correct)
    rng.shuffle(j_wrong)

    target_n = min(20, len(judge_recs))
    n_wrong = min(len(j_wrong), max(1, round(target_n * len(j_wrong) / max(1, len(judge_recs)))))
    n_correct = min(len(j_correct), target_n - n_wrong)
    # Top up if one bucket was short
    sampled_judge = j_wrong[:n_wrong] + j_correct[:n_correct]
    remaining = j_wrong[n_wrong:] + j_correct[n_correct:]
    while len(sampled_judge) < target_n and remaining:
        sampled_judge.append(remaining.pop(0))

    judge_md_path = RESULTS_DIR / f"judge_verdicts_review_20_{tag}.md"
    judge_json_path = RESULTS_DIR / f"judge_verdicts_review_20_{tag}.json"
    with open(judge_json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "sampled_count": len(sampled_judge),
                "total_judge_verdicts": len(judge_recs),
                "seed": seed,
                "items": [
                    {
                        "financebench_id": r["financebench_id"],
                        "company": r["company"],
                        "doc_name": r["doc_name"],
                        "question": r["question"],
                        "gold_answer": r["gold_answer"],
                        "justification": r["justification"],
                        "predicted_answer": r["predicted_answer"],
                        "judge_verdict": r["verdict"],
                        "judge_reason": r["judge_reason"],
                        "judge_model": r["judge_model"],
                        "human_agreement": None,
                    }
                    for r in sampled_judge
                ],
            },
            f,
            indent=2,
        )

    md_lines = [
        f"# LLM Judge Verdict Review ({len(sampled_judge)} Sampled Verdicts, {tag})",
        "",
        f"Total LLM judge verdicts: {len(judge_recs)} (wrong: {len(j_wrong)}, correct: {len(j_correct)}).",
        "Mark `[x]` for Agree or Disagree during manual inspection.",
        "",
    ]
    for i, r in enumerate(sampled_judge, 1):
        md_lines.extend([
            f"## {i}. `{r['financebench_id']}` ({r['company']} | `{r['doc_name']}`)",
            f"- **Question:** {r['question']}",
            f"- **Gold Answer:** {r['gold_answer']}",
            f"- **Gold Justification:** {r['justification'] or 'N/A'}",
            f"- **Predicted Answer:**\n\n> " + r["predicted_answer"].replace("\n", "\n> "),
            f"- **Judge Verdict:** `{r['verdict']}` ({r['judge_model']})",
            f"- **Judge Reason:** {r['judge_reason']}",
            "- **Human Check:** `[ ] Agree`  `[ ] Disagree`  Notes: ______________________",
            "",
        ])
    judge_md_path.write_text("\n".join(md_lines), encoding="utf-8")
    paths["judge_review_md"] = str(judge_md_path)
    paths["judge_review_json"] = str(judge_json_path)

    # 2. Sample 30 non-abstained answers for citation support (NO auto-scoring)
    non_abstained = [r for r in records if r["verdict"] != "abstained"]
    pool = list(non_abstained)
    rng.shuffle(pool)
    sampled_cite = pool[: min(30, len(pool))]

    cite_md_path = RESULTS_DIR / f"citation_support_review_30_{tag}.md"
    cite_json_path = RESULTS_DIR / f"citation_support_review_30_{tag}.json"
    cite_items = []
    cite_md = [
        f"# Citation Support Review ({len(sampled_cite)} Sampled Non-Abstained Answers, {tag})",
        "",
        "Mark whether each cited chunk supports its paired claim. Not auto-scored.",
        "",
    ]
    for i, r in enumerate(sampled_cite, 1):
        pairs = extract_claim_citation_pairs(r["predicted_answer"], r["retrieved_chunks"])
        cite_items.append({
            "financebench_id": r["financebench_id"],
            "company": r["company"],
            "question": r["question"],
            "predicted_answer": r["predicted_answer"],
            "pairs": pairs,
        })
        cite_md.extend([
            f"## {i}. `{r['financebench_id']}` ({r['company']})",
            f"- **Question:** {r['question']}",
            f"- **Predicted Answer:**\n\n> " + r["predicted_answer"].replace("\n", "\n> "),
            "",
        ])
        for p_idx, p in enumerate(pairs, 1):
            src = f"[{p['citation_num']}] {p['doc_name']} FY{p['year']} p.{p['page']}" if p["citation_num"] else "NO CITATION"
            cite_md.extend([
                f"### Pair {i}.{p_idx} ({src})",
                f"- **Claim:** {p['claim']}",
                f"- **Cited Chunk Text:**\n```text\n{p['cited_chunk_text']}\n```",
                "- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________",
                "",
            ])

    with open(cite_json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "sampled_answers": len(sampled_cite),
                "total_non_abstained": len(non_abstained),
                "total_pairs": sum(len(x["pairs"]) for x in cite_items),
                "seed": seed,
                "items": cite_items,
            },
            f,
            indent=2,
        )
    cite_md_path.write_text("\n".join(cite_md), encoding="utf-8")
    paths["citation_review_md"] = str(cite_md_path)
    paths["citation_review_json"] = str(cite_json_path)
    return paths


def compute_metrics_summary(records: List[Dict[str, Any]], is_abstention_set: bool = False) -> Dict[str, Any]:
    n = len(records)
    if is_abstention_set:
        abstained = sum(1 for r in records if r["verdict"] == "abstained")
        false_answers = n - abstained
        return {
            "total_questions": n,
            "abstention_rate": wilson_interval(abstained, n),
            "false_answer_rate": wilson_interval(false_answers, n),
        }

    correct = sum(1 for r in records if r["verdict"] == "correct")
    wrong = sum(1 for r in records if r["verdict"] == "wrong")
    abstained = sum(1 for r in records if r["verdict"] == "abstained")
    attempted = correct + wrong

    page_hits = [r for r in records if r["retrieval_page_hit"]]
    page_misses = [r for r in records if not r["retrieval_page_hit"]]
    tok_hits = [r for r in records if r["retrieval_token_hit"]]

    num_recs = [r for r in records if r["eval_method"] == "numeric_tolerance"]
    judge_recs = [r for r in records if r["eval_method"] == "llm_judge"]

    return {
        "total_questions": n,
        "overall": {
            "correct": wilson_interval(correct, n),
            "wrong": wilson_interval(wrong, n),
            "abstained": wilson_interval(abstained, n),
            "accuracy_among_attempted": wilson_interval(correct, attempted),
        },
        "retrieval": {
            "page_hit": wilson_interval(len(page_hits), n),
            "token_recall_hit_0_8": wilson_interval(len(tok_hits), n),
        },
        "conditional_on_page_hit": {
            "hit_count": len(page_hits),
            "correct": wilson_interval(sum(1 for r in page_hits if r["verdict"] == "correct"), len(page_hits)),
            "wrong": wilson_interval(sum(1 for r in page_hits if r["verdict"] == "wrong"), len(page_hits)),
            "abstained": wilson_interval(sum(1 for r in page_hits if r["verdict"] == "abstained"), len(page_hits)),
        },
        "conditional_on_page_miss": {
            "miss_count": len(page_misses),
            "correct": wilson_interval(sum(1 for r in page_misses if r["verdict"] == "correct"), len(page_misses)),
            "wrong": wilson_interval(sum(1 for r in page_misses if r["verdict"] == "wrong"), len(page_misses)),
            "abstained": wilson_interval(sum(1 for r in page_misses if r["verdict"] == "abstained"), len(page_misses)),
        },
        "by_scoring_method": {
            "numeric_total_attempted": wilson_interval(sum(1 for r in num_recs if r["verdict"] == "correct"), len(num_recs)),
            "llm_judge_total_attempted": wilson_interval(sum(1 for r in judge_recs if r["verdict"] == "correct"), len(judge_recs)),
        },
    }


def load_questions(split: str, abstention_file: Optional[str]) -> List[Dict[str, Any]]:
    if split == "abstention":
        if not abstention_file:
            raise ValueError("--abstention-file is required when --split abstention")
        p = Path(abstention_file)
        if not p.exists():
            raise FileNotFoundError(f"Abstention file not found: {p}")
        raw_text = p.read_text(encoding="utf-8").strip()
        if raw_text.startswith("["):
            items = json.loads(raw_text)
        else:
            items = [json.loads(ln) for ln in raw_text.splitlines() if ln.strip()]
        normalized = []
        for idx, item in enumerate(items, 1):
            normalized.append({
                "financebench_id": item.get("id") or item.get("financebench_id") or f"abst_{idx:03d}",
                "question": item.get("question") or item.get("query"),
                "category": item.get("category") or item.get("type") or "unanswerable",
                "reason": item.get("reason") or "",
                "company": item.get("company"),
                "doc_name": item.get("doc_name", ""),
                "answer": "",
                "justification": "",
                "evidence": [],
            })
        return normalized

    with open(SPLIT_PATH, "r", encoding="utf-8") as f:
        split_data = json.load(f)
    target_ids = set(split_data["dev_ids"] if split == "dev" else split_data["test_ids"])

    questions = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            q = json.loads(line)
            if q["financebench_id"] in target_ids:
                questions.append(q)
    return questions


def run_eval(args: argparse.Namespace) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    generator_model = (args.model or os.getenv("LLM_MODEL", settings.llm_model) or settings.deepseek_model or "").strip()
    if not generator_model:
        raise ValueError("LLM_MODEL is not configured")
    judge_model = (args.judge_model or generator_model).strip()
    cfg = build_config_payload(args.prompt_version, args.top_k, generator_model, judge_model)
    cfg_hash = cfg["config_hash"]
    short_hash = cfg_hash[:12]

    questions = load_questions(args.split, args.abstention_file)
    total = len(questions)
    print(f"=== FinVault AI Answer-Level Eval | split={args.split} (n={total}) | model={generator_model} | prompt={args.prompt_version} | top_k={args.top_k} | cfg_hash={short_hash} ===")

    model_slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", generator_model)
    judge_slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", judge_model)
    gen_cache_path = CACHE_DIR / f"{args.split}_{model_slug}_{args.prompt_version}_k{args.top_k}_{short_hash}.jsonl"
    judge_cache_path = CACHE_DIR / f"judge_{judge_slug}_{cfg['judge_rubric_sha256'][:12]}.jsonl"
    gen_cache = load_cache(gen_cache_path, "cache_key")
    judge_cache = load_cache(judge_cache_path, "cache_key")

    print(f"Cache loaded: {len(gen_cache)}/{total} generated answers in {gen_cache_path.name}; {len(judge_cache)} cached judge verdicts.")

    pacer = LLMPacer()
    conn = psycopg2.connect(settings.database_url)

    records: List[Dict[str, Any]] = []
    api_models_seen = set()
    judge_models_seen = set()

    for idx, q in enumerate(questions, 1):
        fb_id = q["financebench_id"]
        q_text = q["question"]
        gen_cache_key = sha256_text(f"{generator_model}|{cfg_hash}|{fb_id}")

        # 1. Resumable generation + retrieval (cache key includes LLM_MODEL and config_hash)
        if gen_cache_key in gen_cache:
            cached = gen_cache[gen_cache_key]
        else:
            if conn.closed:
                conn = psycopg2.connect(settings.database_url)
            ret = retrieve_chunks_with_meta(q_text, top_k=args.top_k, conn=conn)
            chunks = ret["chunks"]
            prompt = build_rag_prompt(q_text, chunks, prompt_version=args.prompt_version)

            llm_res = pacer.call(prompt=prompt, model=generator_model)
            cached = {
                "cache_key": gen_cache_key,
                "financebench_id": fb_id,
                "requested_model": generator_model,
                "config_hash": cfg_hash,
                "question": q_text,
                "company": q.get("company"),
                "doc_name": q.get("doc_name"),
                "inferred_company": ret["company"],
                "inferred_year": ret["year"],
                "used_fallback_no_year": ret["used_fallback_no_year"],
                "retrieved_chunks": chunks,
                "predicted_answer": (llm_res.get("output") or "").strip(),
                "api_model": llm_res["model"],
                "tokens_used": llm_res["tokens_used"],
                "prompt_tokens": llm_res.get("prompt_tokens", 0),
                "completion_tokens": llm_res.get("completion_tokens", 0),
                "latency_ms": llm_res["latency_ms"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            with open(gen_cache_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(cached, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
            gen_cache[gen_cache_key] = cached
            print(f"[{idx}/{total}] {fb_id} | model={cached['api_model']} | tok={cached['tokens_used']} | chunks={len(chunks)}")

        api_models_seen.add(cached["api_model"])
        chunks = cached["retrieved_chunks"]
        pred_answer = cached["predicted_answer"]

        # 2. Scoring
        if args.split == "abstention":
            abstained = check_abstention(pred_answer)
            verdict = "abstained" if abstained else "false_answer"
            rec = {
                **cached,
                "category": q.get("category"),
                "reason": q.get("reason"),
                "abstained": abstained,
                "verdict": verdict,
                "eval_method": "abstention_check",
                "judge_reason": "Abstained cleanly" if abstained else "Failed to abstain on unanswerable query",
                "judge_model": None,
            }
            records.append(rec)
            continue

        target_doc = q.get("doc_name", "")
        gold_evidence = q.get("evidence", [])
        gold_pages = {int(ev["evidence_page_num"]) for ev in gold_evidence if "evidence_page_num" in ev}
        page_hit = any(is_page_hit(c.get("doc_name", ""), c.get("page"), target_doc, gold_pages) for c in chunks)
        token_hit = any(is_token_recall_hit(c.get("text", ""), c.get("doc_name", ""), target_doc, gold_evidence, threshold=0.8) for c in chunks)

        abstained = check_abstention(pred_answer)
        gold_answer = q.get("answer", "")
        justification = q.get("justification") or ""

        if abstained:
            verdict = "abstained"
            eval_method = "abstention"
            judge_reason = "Model explicitly abstained."
            j_model_used = None
        else:
            num_res = try_numeric_match(q_text, gold_answer, pred_answer)
            if num_res is True:
                verdict = "correct"
                eval_method = "numeric_tolerance"
                judge_reason = "Numeric value matches gold within tolerance."
                j_model_used = None
            elif num_res is False:
                verdict = "wrong"
                eval_method = "numeric_tolerance"
                judge_reason = f"Numeric value does not match gold ({gold_answer})."
                j_model_used = None
            else:
                j_entry = judge_answer(
                    pacer=pacer,
                    judge_cache=judge_cache,
                    judge_cache_path=judge_cache_path,
                    fb_id=fb_id,
                    question=q_text,
                    gold_answer=gold_answer,
                    justification=justification,
                    pred_answer=pred_answer,
                    judge_model=judge_model,
                )
                verdict = j_entry["verdict"]
                eval_method = "llm_judge"
                judge_reason = j_entry["reason"]
                j_model_used = j_entry["judge_model"]
                judge_models_seen.add(j_model_used)

        records.append({
            **cached,
            "gold_answer": gold_answer,
            "justification": justification,
            "gold_pages": sorted(gold_pages),
            "retrieval_page_hit": page_hit,
            "retrieval_token_hit": token_hit,
            "abstained": abstained,
            "verdict": verdict,
            "eval_method": eval_method,
            "judge_reason": judge_reason,
            "judge_model": j_model_used,
        })

    conn.close()

    metrics = compute_metrics_summary(records, is_abstention_set=(args.split == "abstention"))
    review_paths = {}
    if args.generate_reviews and args.split == "test":
        review_paths = generate_review_files(records, tag=f"{args.split}_{short_hash[:8]}", seed=42)

    out_path = Path(args.output) if args.output else (RESULTS_DIR / f"answer_eval_{args.split}_{args.prompt_version}_k{args.top_k}.json")
    payload = {
        "metadata": {
            "split": args.split,
            "split_seed": 42,
            "git_commit": get_git_commit(),
            "config_hash": cfg_hash,
            "frozen_config": cfg,
            "generator_models_returned_by_api": sorted(api_models_seen),
            "judge_models_returned_by_api": sorted(judge_models_seen),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "review_files": review_paths,
        },
        "metrics": metrics,
        "records": [
            {k: v for k, v in r.items() if k != "retrieved_chunks"}
            | {
                "citations": [
                    {
                        "n": ci + 1,
                        "company": ch.get("company"),
                        "doc_name": ch.get("doc_name"),
                        "year": ch.get("year"),
                        "page": ch.get("page"),
                        "similarity_score": ch.get("similarity_score"),
                    }
                    for ci, ch in enumerate(r["retrieved_chunks"])
                ]
            }
            for r in records
        ],
    }

    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nSaved evaluation report to {out_path}")
    print(json.dumps({"metadata": {k: v for k, v in payload["metadata"].items() if k != "frozen_config"}, "metrics": metrics}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="FinVault AI Answer-Level Evaluation")
    parser.add_argument("--split", choices=["dev", "test", "abstention"], required=True)
    parser.add_argument("--prompt-version", default="v0")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--model", default=None)
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--abstention-file", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--generate-reviews", action="store_true")
    args = parser.parse_args()
    run_eval(args)


if __name__ == "__main__":
    main()
