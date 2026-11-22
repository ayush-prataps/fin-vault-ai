"""
pgvector search over chunks table.
"""
from typing import Optional, Any
import psycopg2

from app.config import settings
from app.utils.helpers import get_logger

logger = get_logger(__name__)


def _vector_literal(values: list[float]) -> str:
    """Format a Python vector as a pgvector literal."""
    return "[" + ",".join(f"{float(v):.8f}" for v in values) + "]"


def search_chunks(
    query_embedding: list[float],
    company: Optional[str] = None,
    year: Optional[int] = None,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Search chunks using pgvector cosine distance.
    Returns full chunk text and metadata. Never truncates.
    """
    embedding_literal = _vector_literal(query_embedding)
    try:
        with psycopg2.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                query = [
                    "SELECT",
                    "    id,",
                    "    company,",
                    "    doc_name,",
                    "    year,",
                    "    page,",
                    "    chunk_index,",
                    "    text,",
                    "    1 - (embedding <=> %s::vector) AS similarity_score",
                    "FROM chunks_v2",
                    "WHERE embedding IS NOT NULL",
                ]
                params: list[Any] = [embedding_literal]

                if company:
                    query.append("AND UPPER(company) = UPPER(%s)")
                    params.append(company)
                if year:
                    query.append("AND year = %s")
                    params.append(year)

                query.append("ORDER BY embedding <=> %s::vector")
                params.append(embedding_literal)
                query.append("LIMIT %s")
                params.append(top_k)

                cur.execute("\n".join(query), params)
                rows = cur.fetchall()

        results = []
        for row in rows:
            chunk_id, comp, doc_name, yr, page, chunk_idx, text, score = row
            results.append({
                "id": chunk_id,
                "company": comp,
                "doc_name": doc_name,
                "year": yr,
                "page": page,
                "chunk_index": chunk_idx,
                "text": text,
                "similarity_score": float(score or 0.0),
            })
        return results

    except Exception as exc:
        logger.error("Vector search failed: %s", exc)
        return []


def get_corpus_metadata() -> dict[str, list[int]]:
    """Return distinct companies and their available years from chunks table."""
    try:
        with psycopg2.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT DISTINCT company, year FROM chunks_v2 ORDER BY company, year;"
                )
                rows = cur.fetchall()

        corpus: dict[str, list[int]] = {}
        for company, year in rows:
            corpus.setdefault(company, []).append(year)
        return corpus
    except Exception as exc:
        logger.error("Failed to fetch corpus metadata: %s", exc)
        return {}
