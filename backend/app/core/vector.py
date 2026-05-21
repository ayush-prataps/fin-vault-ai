from typing import Optional, Dict, List, Any

from app.core.db import get_db_connection
from app.utils.helpers import get_logger

logger = get_logger(__name__)


def _vector_literal(values: List[float]) -> str:
    """Format a Python vector as a pgvector literal."""
    return "[" + ",".join(f"{float(value):.8f}" for value in values) + "]"


def test_vector_connection() -> bool:
    """Test PostgreSQL + pgvector availability."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return True
    except Exception as exc:
        logger.warning("Vector store connection failed: %s", exc)
        return False


def search_narrative(
    query_embedding: List[float],
    tickers: Optional[List[str]] = None,
    years: Optional[List[int]] = None,
    doc_types: Optional[List[str]] = None,
    top_k: int = 5,
    score_threshold: float = 0.5
) -> List[Dict[str, Any]]:
    """
    Search narrative data stored in PostgreSQL using pgvector cosine distance.
    
    Retrieves narrative chunks (transcript excerpts, 10-K sections, etc) relevant
    to a query embedding, with optional filtering by company, year, or document type.
    Gracefully returns empty list if the database is unavailable or no rows match.
    
    Args:
        query_embedding: Vector embedding of user query (e.g., from embed_text)
        tickers: Filter by stock tickers (e.g., ['AAPL', 'MSFT'])
        years: Filter by fiscal years (e.g., [2025, 2024])
        doc_types: Filter by document type (e.g., ['earnings_transcript', 'risk_factors'])
        top_k: Number of results to return (default 5, capped at 10 for safety)
        score_threshold: Minimum similarity score (0.0-1.0, default 0.5)
        
    Returns:
        List of narrative chunk dicts with keys:
        - point_id: Unique narrative document ID
        - text: Narrative chunk text (max 500 chars)
        - metadata: Dict with company, ticker, year, doc_type, section_title
        - similarity_score: Cosine similarity score (0.0-1.0)
    """
    # DEFENSIVE: Sanitize parameters
    top_k = min(max(top_k, 1), 10)  # Cap between 1 and 10
    score_threshold = max(0.0, min(score_threshold, 1.0))  # Clamp 0-1
    embedding_literal = _vector_literal(query_embedding)
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = [
                    "SELECT",
                    "    id AS point_id,",
                    "    company,",
                    "    ticker,",
                    "    year,",
                    "    doc_type,",
                    "    section_title,",
                    "    COALESCE(summary, '') AS text,",
                    "    COALESCE(summary, '') AS summary,",
                    "    1 - (embedding <=> %s::vector) AS similarity_score",
                    "FROM narrative_documents",
                    "WHERE embedding IS NOT NULL",
                ]

                params: list[Any] = [embedding_literal]

                if tickers:
                    query.append("AND ticker = ANY(%s)")
                    params.append([ticker.upper() for ticker in tickers])
                if years:
                    query.append("AND year = ANY(%s)")
                    params.append(years)
                if doc_types:
                    query.append("AND doc_type = ANY(%s)")
                    params.append(doc_types)

                query.append("AND (embedding <=> %s::vector) <= %s")
                params.extend([embedding_literal, 1 - score_threshold])
                query.append("ORDER BY embedding <=> %s::vector")
                params.append(embedding_literal)
                query.append("LIMIT %s")
                params.append(top_k)

                cur.execute("\n".join(query), params)
                rows = cur.fetchall()

        results = []
        for row in rows:
            point_id, company, ticker, year, doc_type, section_title, text, summary, similarity_score = row
            
            results.append({
                'point_id': point_id,
                'text': (text or summary or '')[:500],
                'metadata': {
                    'company': company or 'Unknown',
                    'ticker': ticker or 'Unknown',
                    'year': year or 0,
                    'doc_type': doc_type or 'unknown',
                    'section_title': section_title or '',
                    'chunk_id': 0,
                },
                'similarity_score': similarity_score or 0.0
            })
        
        logger.debug(f"Found {len(results)} narrative chunks for query")
        return results
        
    except Exception as exc:
        logger.error(f"Narrative search failed: {exc}")
        return []
