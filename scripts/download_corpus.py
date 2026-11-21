#!/usr/bin/env python3
"""
Download real SEC filing PDFs and the FinanceBench dataset.
Stores raw PDFs in data/raw/ (gitignored).
Uses ThreadPoolExecutor for fast parallel downloads.
"""
import concurrent.futures
import json
import time
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"

DATA_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

FINANCEBENCH_URL = (
    "https://raw.githubusercontent.com/patronus-ai/financebench/main/data/"
    "financebench_open_source.jsonl"
)
PDF_BASE_URL = (
    "https://raw.githubusercontent.com/patronus-ai/financebench/main/pdfs/"
)


def download_questions() -> list[dict]:
    """Download full 150 FinanceBench dataset and save to data/financebench_filtered.jsonl."""
    print("Downloading FinanceBench questions...")
    req = Request(FINANCEBENCH_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=30) as resp:
        all_lines = [
            json.loads(line)
            for line in resp.read().decode("utf-8").strip().split("\n")
            if line.strip()
        ]

    output_path = DATA_DIR / "financebench_filtered.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for q in all_lines:
            f.write(json.dumps(q) + "\n")

    print(f"Saved {len(all_lines)} questions to {output_path}")
    return all_lines


def _download_single_pdf(doc: str) -> tuple[str, bool, str]:
    """Download a single PDF with retries."""
    target_path = RAW_DIR / f"{doc}.pdf"
    if target_path.exists() and target_path.stat().st_size > 5000:
        return doc, True, f"exists ({target_path.stat().st_size:,} bytes)"

    url = f"{PDF_BASE_URL}{doc}.pdf"
    for attempt in range(3):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=45) as resp:
                content = resp.read()
            if len(content) < 1000:
                raise ValueError(f"Downloaded file too small: {len(content)} bytes")
            with open(target_path, "wb") as f:
                f.write(content)
            return doc, True, f"downloaded ({len(content):,} bytes)"
        except Exception as exc:
            if attempt == 2:
                return doc, False, str(exc)
            time.sleep(1)

    return doc, False, "unknown error"


def download_pdfs(doc_names: set[str], max_workers: int = 8):
    """Download referenced PDFs in parallel into data/raw/."""
    print(f"\nDownloading {len(doc_names)} raw PDFs to {RAW_DIR} using {max_workers} threads...")
    completed = 0
    total = len(doc_names)
    failed = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_doc = {executor.submit(_download_single_pdf, doc): doc for doc in sorted(doc_names)}
        for future in concurrent.futures.as_completed(future_to_doc):
            completed += 1
            doc, success, msg = future.result()
            status = "OK" if success else "FAILED"
            print(f"[{completed}/{total}] {doc}.pdf: {status} ({msg})")
            if not success:
                failed.append((doc, msg))

    print(f"\nDownload summary: {total - len(failed)}/{total} succeeded.")
    if failed:
        print(f"Failed downloads ({len(failed)}):")
        for doc, msg in failed:
            print(f"  - {doc}: {msg}")


if __name__ == "__main__":
    questions = download_questions()
    all_doc_names = {q["doc_name"] for q in questions if "doc_name" in q}
    print(f"Found {len(all_doc_names)} unique documents referenced across {len(questions)} questions.")
    download_pdfs(all_doc_names, max_workers=8)
