import time
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.retrieval import retrieve_chunks, build_rag_prompt
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
    question: str
    tickers: Optional[List[str]] = None
    year: Optional[int] = None


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    model: str
    latency_ms: int
    tokens: int


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
async def query_pipeline(payload: QueryRequest) -> QueryResponse:
    if not payload.question or not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

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

    # Call LLM
    try:
        llm_result = call_llm(prompt)
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
    )
