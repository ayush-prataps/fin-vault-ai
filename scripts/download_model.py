#!/usr/bin/env python3
"""
Pre-download the BAAI/bge-small-en-v1.5 ONNX model into fixed cache directory.
Run at build/deployment time before starting the server.
"""
from pathlib import Path
from fastembed import TextEmbedding

BASE_DIR = Path(__file__).resolve().parents[1]
CACHE_DIR = BASE_DIR / ".fastembed_cache"


def download_model() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading BAAI/bge-small-en-v1.5 into {CACHE_DIR}...")
    model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5", cache_dir=str(CACHE_DIR))
    list(model.embed(["test"]))
    print("Model downloaded and verified successfully.")


if __name__ == "__main__":
    download_model()
