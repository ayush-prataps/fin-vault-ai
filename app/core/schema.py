"""
PostgreSQL schema initialization for FinVault AI.
Single table: chunks with pgvector embeddings.
"""
import psycopg2
from app.config import settings
from app.utils.helpers import get_logger

logger = get_logger(__name__)

SCHEMA_DDL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    company VARCHAR(100) NOT NULL,
    doc_name VARCHAR(255) NOT NULL,
    year INTEGER NOT NULL,
    page INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(384)
);

CREATE INDEX IF NOT EXISTS idx_chunks_company ON chunks (company);
CREATE INDEX IF NOT EXISTS idx_chunks_year ON chunks (year);
"""


def init_schema() -> bool:
    """Initialize PostgreSQL schema with pgvector and chunks table."""
    if not settings.database_url:
        logger.warning("DATABASE_URL not set; skipping schema init")
        return False

    try:
        with psycopg2.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_DDL)
                conn.commit()
        logger.info("Database schema initialized successfully")
        return True
    except Exception as exc:
        logger.error("Failed to initialize schema: %s", exc)
        return False
