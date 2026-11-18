import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "FinVault AI")
    env: str = os.getenv("ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "")
    database_url: str = os.getenv("DATABASE_URL", "")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")


settings = Settings()
