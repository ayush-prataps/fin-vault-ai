import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
# Load backend/.env first, then root .env if present
load_dotenv(BASE_DIR / ".env")
load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "FinVault AI")
    env: str = os.getenv("ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "")
    llm_fallback_enabled: bool = os.getenv("LLM_FALLBACK_ENABLED", "true").lower() in ("true", "1", "yes")
    llm_fallback_base_url: str = os.getenv("LLM_FALLBACK_BASE_URL", "")
    llm_fallback_api_key: str = os.getenv("LLM_FALLBACK_API_KEY", "")
    llm_fallback_model: str = os.getenv("LLM_FALLBACK_MODEL", "")
    llm_timeout_seconds: float = float(os.getenv("LLM_TIMEOUT_SECONDS", "60.0"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))
    global_daily_cap: int = int(os.getenv("GLOBAL_DAILY_CAP", "500"))
    judge_base_url: str = os.getenv("JUDGE_BASE_URL", os.getenv("LLM_BASE_URL", ""))
    judge_api_key: str = os.getenv("JUDGE_API_KEY", os.getenv("LLM_API_KEY", ""))
    judge_model: str = os.getenv("JUDGE_MODEL", "")
    database_url: str = os.getenv("DATABASE_URL", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")


settings = Settings()
