#!/usr/bin/env python3
"""List available Groq models, highlighting non-Llama chat models."""
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from app.core.llm import list_available_groq_models

models = list_available_groq_models()

print("\n--- ALL AVAILABLE GROQ MODELS ---")
non_llama = []
for m in sorted(models, key=lambda x: x.id):
    is_llama = "llama" in m.id.lower()
    tag = " [LLAMA]" if is_llama else " [NON-LLAMA]"
    print(f"  {m.id:<40} {tag} (owned by: {m.owned_by})")
    if not is_llama:
        non_llama.append(m.id)

print("\n--- NON-LLAMA CANDIDATES ---")
for m_id in non_llama:
    print(f"  * {m_id}")
