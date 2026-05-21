"""
FinVault AI - Data Pipeline Integration Module
Bridges raw financial data from SEC sources to the AI agent
"""
from .adapter import (
    ingest_bulk_download_data,
    load_annual_csv_to_metrics,
    chunk_text,
    embed_and_store_narrative,
    ensure_narrative_store_ready,
    ensure_vector_store_ready,
)

__all__ = [
    'ingest_bulk_download_data',
    'load_annual_csv_to_metrics',
    'chunk_text',
    'embed_and_store_narrative',
    'ensure_narrative_store_ready',
    'ensure_vector_store_ready'
]
