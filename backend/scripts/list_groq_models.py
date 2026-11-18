#!/usr/bin/env python3
"""List available Groq models, highlighting non-Llama chat models."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load env from backend/.env
backend_dir = Path(__file__).resolve().parents[1]
load_dotenv(backend_dir / ".env")

from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("GROQ_API_KEY not found in backend/.env", file=sys.stderr)
    sys.exit(1)

client = Groq(api_key=api_key)
models_resp = client.models.list()

print("\n--- ALL AVAILABLE GROQ MODELS ---")
non_llama = []
for m in sorted(models_resp.data, key=lambda x: x.id):
    is_llama = "llama" in m.id.lower()
    tag = " [LLAMA]" if is_llama else " [NON-LLAMA]"
    print(f"  {m.id:<40} {tag} (owned by: {m.owned_by})")
    if not is_llama:
        non_llama.append(m.id)

print("\n--- NON-LLAMA CANDIDATES ---")
for m_id in non_llama:
    print(f"  * {m_id}")
