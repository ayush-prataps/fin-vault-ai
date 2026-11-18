from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.utils.helpers import setup_logging, get_logger
from app.core.schema import init_schema

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.log_level)
    logger.info("Starting %s in %s mode", settings.app_name, settings.env)

    try:
        if init_schema():
            logger.info("Database schema verified")
        else:
            logger.warning("Failed to initialize database schema")
    except Exception as exc:
        logger.warning("Database initialization issue: %s", exc)

    yield

    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://localhost:3000",
        "https://fin-vault-ai.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
