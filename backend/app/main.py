from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.auth import router as auth_router
from app.config import settings
from app.core.db import get_db_connection
from app.utils.helpers import setup_logging, get_logger
from app.core.schema import init_schema
from app.core.auth_schema import init_auth_schema
from app.agents.graph import build_graph
from app.data.adapter import ingest_bulk_download_data
from app.data.scripts.ingest_narratives import load_real_narratives, ingest_narrative

logger = get_logger(__name__)


def _get_data_coverage() -> dict:
    """Return current row counts for the primary financial tables."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM financial_metrics")
                financial_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM narrative_documents")
                narrative_count = cur.fetchone()[0]

        return {
            "financial_metrics": int(financial_count or 0),
            "narrative_documents": int(narrative_count or 0),
        }
    except Exception as exc:
        logger.warning(f"Failed to inspect data coverage: {exc}")
        return {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.log_level)
    logger.info(f"Starting {settings.app_name} in {settings.env} mode")

    # Initialize database schema
    try:
        if init_schema():
            logger.info("Database schema verified")
        else:
            logger.warning("Failed to initialize database schema (continuing anyway)")
    except Exception as exc:
        logger.warning(f"Database initialization issue: {exc} (continuing anyway)")

    # Initialize auth schema
    try:
        if init_auth_schema():
            logger.info("Authentication schema verified")
        else:
            logger.warning("Failed to initialize auth schema (continuing anyway)")
    except Exception as exc:
        logger.warning(f"Auth schema initialization issue: {exc} (continuing anyway)")

    # Check whether the system has real data loaded.
    coverage = _get_data_coverage()
    if coverage:
        logger.info(
            "Data coverage: %s financial rows, %s narrative rows",
            coverage.get("financial_metrics", 0),
            coverage.get("narrative_documents", 0),
        )

        if coverage.get("financial_metrics", 0) == 0 or coverage.get("narrative_documents", 0) == 0:
            logger.warning(
                "Financial data is incomplete. Run `python3 -m backend.app.data.scripts.ingest_data` before asking queries."
            )

        if os.getenv("AUTO_INGEST_ON_STARTUP", "0") == "1" and (
            coverage.get("financial_metrics", 0) == 0 or coverage.get("narrative_documents", 0) == 0
        ):
            logger.info("AUTO_INGEST_ON_STARTUP=1, bootstrapping local SEC data into PostgreSQL")
            try:
                ingest_bulk_download_data()
                narratives = load_real_narratives()
                for narrative in narratives:
                    ingest_narrative(
                        ticker=narrative["ticker"],
                        company=narrative["company"],
                        year=narrative["year"],
                        text=narrative["text"],
                        section_title=narrative["section_title"],
                        source_file=narrative["source_file"],
                    )
                logger.info("Startup SEC bootstrap completed")
            except Exception as exc:
                logger.warning(f"Startup SEC bootstrap failed: {exc}")

    # Build agent graph
    try:
        build_graph()
        logger.info("Agent graph built successfully")
    except Exception as exc:
        logger.error(f"Failed to build agent graph: {exc}")

    yield

    logger.info(f"Shutting down {settings.app_name}")


app = FastAPI(title=settings.app_name, lifespan=lifespan)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://localhost:3000",
        "https://fin-vault-ai.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(auth_router)
