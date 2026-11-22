"""
Retrieval module for FinVault AI.
Performs vector search over filing chunks and formats numbered citations.
"""
from typing import Optional, Any
from app.core.embeddings import embed_text
from app.core.vector import search_chunks
from app.aliases import infer_company, infer_year
from app.utils.helpers import get_logger

logger = get_logger(__name__)


def retrieve_chunks(
    query: str,
    company: Optional[str] = None,
    year: Optional[int] = None,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Retrieve top-k chunks matching the query embedding with inferred alias fallback."""
    if company is None:
        company = infer_company(query)
    if year is None:
        year = infer_year(query)

    query_embedding = embed_text(query)
    chunks = search_chunks(
        query_embedding=query_embedding,
        company=company,
        year=year,
        top_k=top_k,
    )

    # If filtering by both company and year returned 0 results (e.g. filing year not in corpus
    # but comparative tables exist in adjacent 10-K filings), fall back to company search without year filter
    if not chunks and company is not None and year is not None:
        chunks = search_chunks(
            query_embedding=query_embedding,
            company=company,
            year=None,
            top_k=top_k,
        )

    return chunks


def build_rag_prompt(query: str, chunks: list[dict[str, Any]]) -> str:
    """
    Build prompt with numbered citations [1], [2], etc.
    Instructs the model to answer strictly from context and cite chunk numbers.
    """
    context_lines = []
    for idx, chunk in enumerate(chunks, 1):
        context_lines.append(
            f"[{idx}] Source: {chunk.get('company')} {chunk.get('doc_name')} "
            f"FY{chunk.get('year')} (Page {chunk.get('page')})\n"
            f"{chunk.get('text')}\n"
        )

    context_str = "\n".join(context_lines)

    return f"""You are a financial analyst answering questions strictly based on the provided SEC filing excerpts.

CONTEXT:
{context_str}

USER QUESTION:
{query}

INSTRUCTIONS:
1. Answer the question using ONLY facts directly mentioned in the CONTEXT above.
2. For every factual claim, cite the relevant source using its bracketed number, e.g. [1], [2].
3. If the context does not contain enough information to answer the question, state clearly: "I cannot answer this question based on the provided filing excerpts." Do not speculate or invent numbers.
4. Keep the answer direct, factual, and concise.

ANSWER:"""
