#!/usr/bin/env python3
"""List available models from the configured OpenAI-compatible LLM endpoint."""
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from app.core.llm import list_available_models
from app.config import settings

print(f"\n--- AVAILABLE LLM MODELS ({settings.llm_base_url}) ---")
models = list_available_models()
for m in sorted(models, key=lambda x: str(x.get("id", ""))):
    m_id = m.get("id", "")
    owned_by = m.get("owned_by", "unknown")
    print(f"  {m_id:<40} (owned by: {owned_by})")
