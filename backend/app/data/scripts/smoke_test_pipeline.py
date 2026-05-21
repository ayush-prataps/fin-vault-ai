#!/usr/bin/env python3
"""
End-to-end smoke test for the FinVault AI data pipeline.

This runner verifies the pipeline with one command:
1. Initialize PostgreSQL schema
2. Ingest numeric metrics from bulk_download CSVs
3. Ingest narrative samples into pgvector-backed PostgreSQL storage
4. Run a hybrid retrieval query
5. Assemble prompt context and call the LLM

The script exits non-zero if any critical step fails or if the pipeline
fails to retrieve both structured and narrative context.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Add backend to path (go up 4 levels from backend/app/data/scripts/)
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.core.schema import init_schema
from app.core.embeddings import embed_text
from app.core.llm import quick_model_call
from app.core.retrieval import assemble_context, perform_hybrid_retrieval
from app.data.adapter import ingest_bulk_download_data
from app.data.scripts.ingest_narratives import main as ingest_narratives_main
from app.utils.helpers import get_logger

logger = get_logger(__name__)


TEST_QUERY = "Compare Apple and Microsoft financial performance in 2025 with supporting context"
TEST_TICKERS = ["AAPL", "MSFT"]


def _fail(message: str) -> None:
    print(f"❌ {message}")
    raise SystemExit(1)


def main() -> None:
    start_time = time.time()
    print("\n" + "=" * 80)
    print("FINVAULT AI PIPELINE SMOKE TEST")
    print("=" * 80)

    print("\n[1/5] Initializing PostgreSQL schema...")
    if not init_schema():
        _fail("PostgreSQL schema initialization failed")
    print("✅ PostgreSQL schema ready")

    print("\n[2/5] Ingesting numeric metrics from bulk_download CSVs...")
    metrics_summary = ingest_bulk_download_data()
    if not metrics_summary.get("success"):
        _fail(f"Numeric ingestion failed: {metrics_summary.get('error', 'unknown error')}")

    inserted_total = sum(
        company_stats.get("records_inserted", 0)
        for company_stats in metrics_summary.get("companies", {}).values()
    )
    if inserted_total <= 0:
        _fail("Numeric ingestion completed but inserted zero rows")
    print(f"✅ Inserted {inserted_total} structured metric records")

    print("\n[3/5] Ingesting narrative samples into pgvector storage...")
    ingest_narratives_main()
    print("✅ Narrative ingestion completed")

    print("\n[4/5] Running hybrid retrieval...")
    context = perform_hybrid_retrieval(
        query=TEST_QUERY,
        embeddings_model_fn=embed_text,
        tickers=TEST_TICKERS,
        force_mode="hybrid",
        numeric_limit=20,
        narrative_limit=5,
    )

    retrieval_summary = context.get("retrieval_summary", {})
    numeric_count = retrieval_summary.get("numeric_retrieved", 0)
    narrative_count = retrieval_summary.get("narrative_retrieved", 0)
    if numeric_count <= 0:
        _fail("Hybrid retrieval did not return any structured metrics")
    if narrative_count <= 0:
        _fail("Hybrid retrieval did not return any narrative chunks")

    print(
        f"✅ Retrieval returned {numeric_count} numeric records and {narrative_count} narrative chunks"
    )

    print("\n[5/5] Assembling context and calling LLM...")
    assembled = assemble_context(
        query=TEST_QUERY,
        numeric_data=context.get("numeric_data", []),
        narrative_chunks=[
            {
                "text": chunk.get("text", ""),
                "metadata": {
                    "ticker": chunk.get("ticker", ""),
                    "year": chunk.get("year", 0),
                    "doc_type": chunk.get("doc_type", ""),
                    "section_title": chunk.get("section_title", ""),
                },
                "similarity_score": chunk.get("score", 0.0),
            }
            for chunk in context.get("narrative_chunks", [])
        ],
        include_contradiction_check=True,
    )

    if "[Source:" not in assembled:
        _fail("Assembled context is missing source citations")

    llm_result = quick_model_call(assembled + "\n\nProvide your analysis:\n")
    analysis = llm_result.get("output", "")
    if not analysis:
        _fail("LLM returned an empty response")
    if llm_result.get("mock"):
        _fail("LLM step fell back to a mock response; GROQ_API_KEY or live inference is required")

    total_latency_ms = int((time.time() - start_time) * 1000)
    print("✅ LLM returned a response")
    print(f"✅ Smoke test completed in {total_latency_ms}ms")
    print(f"   • Structured records: {numeric_count}")
    print(f"   • Narrative chunks: {narrative_count}")
    print(f"   • Response chars: {len(analysis)}")

    print("\n✅ PIPELINE SMOKE TEST PASSED")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        logger.error(f"Smoke test failed: {exc}", exc_info=True)
        _fail(str(exc))
