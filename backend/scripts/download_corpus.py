#!/usr/bin/env python3
"""
Download real SEC filing PDFs and the matching FinanceBench question subset.
Stores raw PDFs in backend/data/raw/ (gitignored).
"""
import os
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"

DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Selected companies and their referenced filing documents
SELECTED_DOCS = {
    "3M": ["3M_2018_10K", "3M_2022_10K", "3M_2023Q2_10Q"],
    "AMD": ["AMD_2015_10K", "AMD_2022_10K"],
    "Boeing": ["BOEING_2018_10K", "BOEING_2022_10K"],
    "American Express": ["AMERICANEXPRESS_2022_10K"],
}

ALL_DOC_NAMES = {doc for docs in SELECTED_DOCS.values() for doc in docs}

FINANCEBENCH_URL = (
    "https://raw.githubusercontent.com/patronus-ai/financebench/main/data/"
    "financebench_open_source.jsonl"
)
PDF_BASE_URL = (
    "https://raw.githubusercontent.com/patronus-ai/financebench/main/pdfs/"
)


def download_questions() -> list[dict]:
    """Download full 150 FinanceBench dataset and keep only selected docs."""
    print("Downloading FinanceBench questions...")
    req = urllib.request.Request(FINANCEBENCH_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        all_lines = [json.loads(line) for line in resp.read().decode("utf-8").strip().split("\n")]

    filtered = [q for q in all_lines if q.get("doc_name") in ALL_DOC_NAMES]

    output_path = DATA_DIR / "financebench_filtered.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for q in filtered:
            f.write(json.dumps(q) + "\n")

    print(f"Saved {len(filtered)} questions matching selected corpus to {output_path}")
    return filtered


def download_pdfs():
    """Download the referenced PDFs into backend/data/raw/."""
    print(f"\nDownloading {len(ALL_DOC_NAMES)} raw PDFs to {RAW_DIR}...")
    for doc in sorted(ALL_DOC_NAMES):
        target_path = RAW_DIR / f"{doc}.pdf"
        if target_path.exists() and target_path.stat().st_size > 1000:
            print(f"  * {doc}.pdf already exists ({target_path.stat().st_size} bytes)")
            continue

        url = f"{PDF_BASE_URL}{doc}.pdf"
        print(f"  * Downloading {doc}.pdf from {url}...")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
        with open(target_path, "wb") as f:
            f.write(content)
        print(f"    Done ({len(content)} bytes)")


if __name__ == "__main__":
    download_questions()
    download_pdfs()
