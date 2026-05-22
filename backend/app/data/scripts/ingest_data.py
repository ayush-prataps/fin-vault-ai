#!/usr/bin/env python3
"""
Data Ingestion Script
Initializes PostgreSQL schema and ingests pipeline output data
Run this after bulk_download.py to populate the AI system with data
"""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[3]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.schema import init_schema
from app.data.adapter import (
    ingest_bulk_download_data,
    ensure_narrative_store_ready
)
from app.data.scripts.ingest_narratives import load_real_narratives, ingest_narrative
from app.utils.helpers import get_logger

logger = get_logger(__name__)


def main():
    """Main ingestion workflow"""
    print("\n" + "="*80)
    print("📊 FINVAULT AI - DATA INGESTION")
    print("="*80)
    
    # Step 1: Initialize PostgreSQL schema
    print("\n[1/3] Initializing PostgreSQL schema...")
    if init_schema():
        print("✅ PostgreSQL schema initialized")
    else:
        print("❌ Failed to initialize PostgreSQL schema")
        print("   Make sure DATABASE_URL is set and database is accessible")
        return
    
    # Step 2: Ingest bulk download CSV data
    print("\n[2/3] Ingesting financial metrics from bulk_download/...")
    summary = ingest_bulk_download_data()
    
    if not summary.get('success'):
        print("⚠️  No data ingested")
    else:
        total_inserted = sum(
            co['records_inserted'] 
            for co in summary.get('companies', {}).values()
        )
        print(f"✅ Ingested {total_inserted} financial metric records")
        
        for ticker, stats in summary.get('companies', {}).items():
            status = "✓" if stats['success'] else "✗"
            print(f"   {status} {ticker}: {stats['records_inserted']} records")
    
    # Step 3: Prepare pgvector storage
    print("\n[3/3] Ingesting SEC filing narratives...")
    if ensure_narrative_store_ready():
        print("✅ pgvector narrative storage ready")
    else:
        print("❌ Could not initialize pgvector narrative storage")
        return

    narratives = load_real_narratives()
    if not narratives:
        print("⚠️  No SEC filing narratives found; the system will still answer numeric queries")
    else:
        total_chunks = 0
        for narrative in narratives:
            total_chunks += ingest_narrative(
                ticker=narrative['ticker'],
                company=narrative['company'],
                year=narrative['year'],
                text=narrative['text'],
                section_title=narrative['section_title'],
                source_file=narrative['source_file'],
            )

        print(f"✅ Ingested {total_chunks} narrative chunks from SEC filings")
    
    print("\n" + "="*80)
    print("📈 INGESTION COMPLETE")
    print("="*80)
    print("\nNext steps:")
    print("  1. Test with: python3 -m backend.app.api.test_query")
    print("  2. Or start the server: uvicorn backend.app.main:app --reload")
    print("  3. POST to /query endpoint with your financial queries")
    print("")


if __name__ == "__main__":
    main()
