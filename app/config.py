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
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "") or os.getenv("LLM_API_KEY", "")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")
    groq_base_url: str = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
    llm_fallback_enabled: bool = os.getenv("LLM_FALLBACK_ENABLED", "true").lower() in ("true", "1", "yes")
    llm_timeout_seconds: float = float(os.getenv("LLM_TIMEOUT_SECONDS", "60.0"))
    llm_max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))
    global_daily_cap: int = int(os.getenv("GLOBAL_DAILY_CAP", "500"))
    database_url: str = os.getenv("DATABASE_URL", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")


settings = Settings()
