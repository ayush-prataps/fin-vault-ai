#!/usr/bin/env python3
"""List available models from configured OpenAI-compatible endpoints (DeepSeek, Groq, or both)."""
import argparse
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from app.core.llm import list_available_models

parser = argparse.ArgumentParser(description="List available LLM models")
parser.add_argument("--provider", choices=["all", "deepseek", "groq"], default="all", help="Provider to query")
args = parser.parse_args()

models = list_available_models(provider=args.provider)

print(f"\n--- AVAILABLE LLM MODELS ({args.provider.upper()}) ---")
for m in sorted(models, key=lambda x: (str(x.get("provider", "")), str(x.get("id", "")))):
    m_id = m.get("id", "")
    owned_by = m.get("owned_by", "unknown")
    prov = m.get("provider", "default")
    print(f"  [{prov:<8}] {m_id:<40} (owned by: {owned_by})")
