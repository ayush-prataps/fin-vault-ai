import time
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app.core.retrieval import retrieve_chunks, build_rag_prompt
from app.core.vector import get_corpus_metadata
from app.core.rate_limit import check_rate_limit, CONCURRENCY_SEMAPHORE
from app.core.llm import call_llm
from app.utils.helpers import get_logger

logger = get_logger(__name__)
router = APIRouter()


class Citation(BaseModel):
    n: int
    company: str
    doc: str
    year: int
    page: int
    text: str


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    tickers: Optional[List[str]] = None
    year: Optional[int] = None


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    model: str
    latency_ms: int
    tokens: int
    prompt_tokens: int = 0
    completion_tokens: int = 0
    fallback_used: bool = False
    primary_model: Optional[str] = None
    primary_error: Optional[str] = None


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.get("/corpus")
def get_corpus() -> dict[str, list[int]]:
    return get_corpus_metadata()


@router.post("/query", response_model=QueryResponse)
async def query_pipeline(payload: QueryRequest, request: Request) -> QueryResponse:
    await check_rate_limit(request)

    start_time = time.time()
    company = payload.tickers[0] if payload.tickers and len(payload.tickers) > 0 else None

    # Retrieve relevant filing chunks
    try:
        chunks = retrieve_chunks(
            query=payload.question,
            company=company,
            year=payload.year,
            top_k=5,
        )
    except Exception as exc:
        logger.error("Retrieval failed: %s", exc)
        raise HTTPException(status_code=500, detail=f"Retrieval error: {exc}")

    # Build prompt with numbered citations
    prompt = build_rag_prompt(payload.question, chunks)

    # Call LLM with concurrency limiting (fallback allowed for chatbot)
    async with CONCURRENCY_SEMAPHORE:
        try:
            llm_result = call_llm(prompt, allow_fallback=True)
        except Exception as exc:
            logger.error("LLM call failed: %s", exc)
            raise HTTPException(status_code=502, detail=f"LLM call failed: {exc}")

    total_latency_ms = int((time.time() - start_time) * 1000)

    # Format citations
    citations = [
        Citation(
            n=idx,
            company=chunk.get("company", "Unknown"),
            doc=chunk.get("doc_name", "Unknown"),
            year=chunk.get("year", 0),
            page=chunk.get("page", 0),
            text=chunk.get("text", ""),
        )
        for idx, chunk in enumerate(chunks, 1)
    ]

    return QueryResponse(
        answer=llm_result["output"],
        citations=citations,
        model=llm_result["model"],
        latency_ms=total_latency_ms,
        tokens=llm_result["tokens_used"],
        prompt_tokens=llm_result.get("prompt_tokens", 0),
        completion_tokens=llm_result.get("completion_tokens", 0),
        fallback_used=bool(llm_result.get("fallback_used", False)),
        primary_model=llm_result.get("primary_model"),
        primary_error=llm_result.get("primary_error"),
    )
