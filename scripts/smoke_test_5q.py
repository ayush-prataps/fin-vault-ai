#!/usr/bin/env python3
"""5-question live smoke test over dev split for OpenAI-compatible LLM pipeline."""
import json
import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.core.retrieval import retrieve_chunks, build_rag_prompt
from app.core.llm import call_llm
from app.config import settings

DATA_PATH = BASE_DIR / "data" / "financebench_filtered.jsonl"
SPLIT_PATH = BASE_DIR / "eval" / "results" / "split_75_75.json"

with open(SPLIT_PATH, "r", encoding="utf-8") as f:
    dev_ids = json.load(f)["dev_ids"]

dev_id_set = set(dev_ids[:5])
questions = []
with open(DATA_PATH, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        d = json.loads(line)
        if d["financebench_id"] in dev_id_set:
            questions.append(d)

print(f"=== Running 5-Question Smoke Test (Dev Split) ===")
print(f"Endpoint: {settings.llm_base_url} | Model: {settings.llm_model}\n")

results = []
for idx, q in enumerate(questions, 1):
    q_id = q["financebench_id"]
    q_text = q["question"]
    company = q.get("company")
    
    start_t = time.time()
    chunks = retrieve_chunks(
        query=q_text,
        company=company,
        year=None,
        top_k=10,
    )
    prompt = build_rag_prompt(q_text, chunks)
    llm_resp = call_llm(prompt, use_cache=False, allow_fallback=False)
    elapsed_ms = int((time.time() - start_t) * 1000)

    res_item = {
        "index": idx,
        "id": q_id,
        "company": company,
        "question": q_text,
        "model_returned": llm_resp["model"],
        "requested_model": llm_resp["requested_model"],
        "latency_ms": llm_resp["latency_ms"],
        "pipeline_latency_ms": elapsed_ms,
        "prompt_tokens": llm_resp["prompt_tokens"],
        "completion_tokens": llm_resp["completion_tokens"],
        "total_tokens": llm_resp["tokens_used"],
        "answer": llm_resp["output"],
        "chunks_retrieved": len(chunks),
    }
    results.append(res_item)

    print(f"[{idx}/5] {q_id} ({company})")
    print(f"  Question: {q_text}")
    print(f"  Model (API): {res_item['model_returned']}")
    print(f"  Latency: LLM={res_item['latency_ms']}ms | Total={elapsed_ms}ms")
    print(f"  Tokens: {res_item['total_tokens']} (prompt={res_item['prompt_tokens']}, comp={res_item['completion_tokens']})")
    print(f"  Answer:\n    {res_item['answer']}\n")

total_tokens = sum(r["total_tokens"] for r in results)
avg_llm_latency = sum(r["latency_ms"] for r in results) / len(results)
print("=== SMOKE TEST SUMMARY ===")
print(f"Total questions: {len(results)}")
print(f"Total tokens used: {total_tokens}")
print(f"Average LLM latency: {avg_llm_latency:.1f}ms")
print(f"Models returned by API: {set(r['model_returned'] for r in results)}")
