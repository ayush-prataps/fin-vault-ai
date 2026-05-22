from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import time

from app.agents.graph import build_graph
from app.utils.helpers import get_logger
from app.core.retrieval import perform_hybrid_retrieval
from app.core.embeddings import embed_text
from app.core.db import get_db_connection

logger = get_logger(__name__)
router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    mode: Optional[str] = None  # 'quick' or 'deep', overrides default
    tickers: Optional[list[str]] = None  # Filter to specific companies
    retrieval_mode: Optional[str] = None  # Force retrieval type: 'numeric', 'narrative', 'hybrid'


class SourceReference(BaseModel):
    doc_type: str
    ticker: str
    year: int
    section: Optional[str] = None
    similarity_score: Optional[float] = None


class QueryResponse(BaseModel):
    query: str
    analysis: str
    retrieval_mode: str
    model_used: str
    numeric_data_count: int
    narrative_chunks_count: int
    sources: List[SourceReference] = []
    latency_ms: int
    tokens_used: Optional[int] = None
    contradictions_detected: Optional[str] = None


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.get("/status")
def status() -> dict:
    """Return ingestion status: row counts and last ingest times."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM financial_metrics")
                fin_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM narrative_documents")
                nar_count = cur.fetchone()[0]
                cur.execute("SELECT MAX(ingested_at) FROM financial_metrics")
                last_fin = cur.fetchone()[0]
                cur.execute("SELECT MAX(ingested_at) FROM narrative_documents")
                last_nar = cur.fetchone()[0]

        return {
            "financial_metrics_count": int(fin_count or 0),
            "narrative_documents_count": int(nar_count or 0),
            "last_financial_ingest": str(last_fin) if last_fin else None,
            "last_narrative_ingest": str(last_nar) if last_nar else None,
        }
    except Exception as exc:
        logger.warning(f"Status endpoint failed: {exc}")
        return {"error": "Unable to query database"}


@router.get("/")
def root() -> dict:
    return {"service": "FinVault AI", "status": "ok"}


@router.post("/query", response_model=QueryResponse)
async def query_financial_data(payload: QueryRequest) -> QueryResponse:
    """
    Execute financial query with hybrid retrieval + LLM reasoning.
    
    Phase 2 Hybrid Retrieval Workflow:
    1. Classify query intent (numeric, narrative, or hybrid)
    2. Retrieve numeric metrics from PostgreSQL if applicable
    3. Retrieve narrative chunks from pgvector-backed PostgreSQL if applicable
    4. Assemble citation-rich context for LLM
    5. Detect contradictions between metrics and narrative
    6. Generate analysis with grounded citations
    
    DEFENSIVE: Graceful degradation if components fail.
    - Missing numeric data? Continue with narrative only
    - Missing narrative data? Continue with numeric only
    - LLM timeout? Return available data with error message
    - Contradiction detection fails? Proceed without it (non-blocking)
    """
    try:
        start_time = time.time()
        
        # DEFENSIVE: Validate query
        if not payload.query or len(payload.query.strip()) < 5:
            raise HTTPException(status_code=400, detail="Query must be at least 5 characters")
        
        logger.info(f"Processing query: {payload.query[:100]}...")

        # DEFENSIVE: Run the LangGraph workflow with a graceful fallback path
        try:
            graph = build_graph()
            result = graph.invoke({
                "query": payload.query,
                "mode": payload.mode or "quick",
                "tickers": payload.tickers,
                "retrieval_mode": payload.retrieval_mode,
            })

            # Defensive fallback: if client requested a specific retrieval_mode
            # but the graph result did not include narratives, re-run retrieval
            # directly with force_mode to ensure the response is grounded.
            if payload.retrieval_mode in ("narrative", "hybrid"):
                retrieval_summary = result.get("retrieval_context", {}).get("retrieval_summary", {})
                if retrieval_summary.get("query_mode") != payload.retrieval_mode:
                    try:
                        context = perform_hybrid_retrieval(
                            query=payload.query,
                            embeddings_model_fn=embed_text,
                            tickers=payload.tickers,
                            force_mode=payload.retrieval_mode,
                        )
                        # Patch result to include the forced retrieval context
                        result["retrieval_context"] = context
                    except Exception:
                        # Non-fatal: leave original result
                        pass

            analysis = result.get("raw_analysis", "Unable to generate analysis")
            context = result.get("retrieval_context", {})
        except Exception as graph_exc:
            logger.error(f"Graph invocation failed: {graph_exc}")
            analysis = "Unable to generate analysis"
            context = {}

        numeric_data = context.get('numeric_data', []) or []
        narrative_chunks = context.get('narrative_chunks', []) or []
        retrieval_summary = context.get('retrieval_summary', {})

        if not numeric_data and not narrative_chunks:
            logger.warning("No retrieval data available")

        # DEFENSIVE: Build sources list with validation
        sources = []
        for chunk in narrative_chunks:
            try:
                if isinstance(chunk, dict):
                    sources.append(SourceReference(
                        doc_type=chunk.get('doc_type', 'unknown'),
                        ticker=chunk.get('ticker', 'unknown'),
                        year=chunk.get('year', 0),
                        section=chunk.get('section_title'),
                        similarity_score=chunk.get('score', 0.0)
                    ))
            except Exception as source_exc:
                logger.warning(f"Failed to build source reference: {source_exc}")
                continue

        contradictions = None
        if retrieval_summary.get('query_mode') in ['hybrid', 'narrative'] and numeric_data and narrative_chunks:
            contradictions = None

        model_used = f"langgraph:{payload.mode or 'quick'}"
        tokens_used = None
        
        # DEFENSIVE: Calculate metrics with fallbacks
        try:
            latency_ms = int((time.time() - start_time) * 1000)
        except Exception:
            latency_ms = 0
        
        # DEFENSIVE: Ensure all response fields are valid types
        response = QueryResponse(
            query=payload.query[:500] if payload.query else "Unknown",
            analysis=analysis[:5000] if analysis else "No analysis",
            retrieval_mode=retrieval_summary.get('query_mode', 'unknown'),
            model_used=model_used,
            numeric_data_count=max(0, retrieval_summary.get('numeric_retrieved', 0)),
            narrative_chunks_count=max(0, retrieval_summary.get('narrative_retrieved', 0)),
            sources=sources or [],
            latency_ms=latency_ms,
            tokens_used=tokens_used if isinstance(tokens_used, int) else None,
            contradictions_detected=contradictions[:500] if contradictions else None
        )
        
        logger.info(f"Query completed in {latency_ms}ms: {len(numeric_data)} metrics, {len(narrative_chunks)} narratives")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, etc.)
        raise
    except Exception as exc:
        # DEFENSIVE: Catch all other errors, don't leak internals (Area #10)
        logger.error(f"Query processing failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Query processing failed. Please try again later."
        )
