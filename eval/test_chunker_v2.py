#!/usr/bin/env python3
"""
Prototype & Test for Chunker v2
"""
import re
import sys
from collections import Counter
from pathlib import Path
from typing import List, Dict, Any, Tuple
import pypdf

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.core.embeddings import get_tokenizer

def is_table_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    # Check for financial numbers, dollar signs, percentages, dashes
    has_numbers = bool(re.search(r"(\$?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?|\(\$?\d+(?:,\d{3})*(?:\.\d+)?\)|—|-{2,}|^\s*-\s*$)", stripped))
    # Multiple spaces indicating column separation
    has_column_spacing = bool(re.search(r"\S\s{2,}\S", stripped))
    return has_numbers and has_column_spacing

def count_tokens(tokenizer: Any, text: str) -> int:
    return len(tokenizer.encode(text, add_special_tokens=False))

def chunk_page_v2(
    page_text: str,
    tokenizer: Any,
    max_chunk_tokens: int = 500,
    max_table_tokens: int = 800,
    overlap_lines: int = 1,
) -> List[Dict[str, Any]]:
    """
    Chunk page text by slicing the original page_text string without token decoding.
    Keeps table blocks together up to max_table_tokens.
    Repeats table header rows if table exceeds max_table_tokens.
    Ensures >= 99.5% non-whitespace character coverage.
    """
    if not page_text or not page_text.strip():
        return []

    # First, make sure tokenizer truncation is disabled for counting!
    if hasattr(tokenizer, "_tok") and hasattr(tokenizer._tok, "no_truncation"):
        tokenizer._tok.no_truncation()

    # If entire page fits in max_chunk_tokens, return whole page
    page_tokens = count_tokens(tokenizer, page_text)
    if page_tokens <= max_chunk_tokens:
        return [{
            "text": page_text.strip(),
            "start_char": 0,
            "end_char": len(page_text),
            "tokens": page_tokens,
            "is_table": False
        }]

    # Split page_text into lines with character spans
    lines: List[Tuple[str, int, int]] = []
    # Find lines using regex to get accurate start/end offsets in original text
    for match in re.finditer(r"[^\n]+(?:\n|$)", page_text):
        line_str = match.group()
        start = match.start()
        end = match.end()
        lines.append((line_str, start, end))

    if not lines:
        return []

    # Group lines into semantic units (paragraphs and table blocks)
    # Each unit: {"type": "table"|"text", "lines": [(line_str, start, end)], "start": int, "end": int}
    units: List[Dict[str, Any]] = []
    current_type = None
    current_lines = []

    for line_str, start, end in lines:
        stripped = line_str.strip()
        if not stripped:
            if current_lines:
                current_lines.append((line_str, start, end))
            continue

        tbl = is_table_line(line_str)
        l_type = "table" if tbl else "text"

        if current_type is None:
            current_type = l_type
            current_lines = [(line_str, start, end)]
        elif l_type == current_type:
            current_lines.append((line_str, start, end))
        else:
            # Type switch
            units.append({
                "type": current_type,
                "lines": current_lines,
                "start": current_lines[0][1],
                "end": current_lines[-1][2],
            })
            current_type = l_type
            current_lines = [(line_str, start, end)]

    if current_lines:
        units.append({
            "type": current_type,
            "lines": current_lines,
            "start": current_lines[0][1],
            "end": current_lines[-1][2],
        })

    # Now assemble units into chunks
    chunks: List[Dict[str, Any]] = []
    current_chunk_lines: List[Tuple[str, int, int]] = []
    current_tokens = 0

    for unit in units:
        unit_text = page_text[unit["start"]:unit["end"]]
        unit_toks = count_tokens(tokenizer, unit_text)

        if unit["type"] == "table":
            # Table handling
            # If current chunk has text, flush it before starting table
            if current_chunk_lines:
                c_start = current_chunk_lines[0][1]
                c_end = current_chunk_lines[-1][2]
                c_text = page_text[c_start:c_end].strip()
                if c_text:
                    chunks.append({
                        "text": c_text,
                        "start_char": c_start,
                        "end_char": c_end,
                        "tokens": count_tokens(tokenizer, c_text),
                        "is_table": False
                    })
                current_chunk_lines = []
                current_tokens = 0

            # Does the whole table fit within max_table_tokens?
            if unit_toks <= max_table_tokens:
                c_text = unit_text.strip()
                chunks.append({
                    "text": c_text,
                    "start_char": unit["start"],
                    "end_char": unit["end"],
                    "tokens": unit_toks,
                    "is_table": True
                })
            else:
                # Table exceeds max_table_tokens: split at row boundaries and repeat header
                # Identify header row(s): top 1-2 non-empty lines
                table_lines = [l for l in unit["lines"] if l[0].strip()]
                header_lines = table_lines[:2] if len(table_lines) >= 2 else table_lines[:1]
                header_text = "".join(l[0] for l in header_lines)
                header_toks = count_tokens(tokenizer, header_text)

                sub_table_lines: List[Tuple[str, int, int]] = []
                sub_toks = 0
                is_first_slice = True

                data_lines = unit["lines"] if is_first_slice else unit["lines"][len(header_lines):]
                for l_str, l_start, l_end in unit["lines"]:
                    l_toks = count_tokens(tokenizer, l_str)
                    if sub_toks + l_toks > max_table_tokens and sub_table_lines:
                        # Flush sub-table
                        st_start = sub_table_lines[0][1]
                        st_end = sub_table_lines[-1][2]
                        st_raw = page_text[st_start:st_end].strip()
                        if not is_first_slice:
                            # Prepend header text to repeated slice
                            combined_text = header_text + "\n" + st_raw
                        else:
                            combined_text = st_raw
                        chunks.append({
                            "text": combined_text,
                            "start_char": st_start,
                            "end_char": st_end,
                            "tokens": count_tokens(tokenizer, combined_text),
                            "is_table": True
                        })
                        is_first_slice = False
                        sub_table_lines = [(l_str, l_start, l_end)]
                        sub_toks = header_toks + l_toks
                    else:
                        sub_table_lines.append((l_str, l_start, l_end))
                        sub_toks += l_toks

                if sub_table_lines:
                    st_start = sub_table_lines[0][1]
                    st_end = sub_table_lines[-1][2]
                    st_raw = page_text[st_start:st_end].strip()
                    if not is_first_slice:
                        combined_text = header_text + "\n" + st_raw
                    else:
                        combined_text = st_raw
                    chunks.append({
                        "text": combined_text,
                        "start_char": st_start,
                        "end_char": st_end,
                        "tokens": count_tokens(tokenizer, combined_text),
                        "is_table": True
                    })
        else:
            # Paragraph / text unit
            # If adding unit exceeds max_chunk_tokens, flush or split
            if current_tokens + unit_toks <= max_chunk_tokens:
                current_chunk_lines.extend(unit["lines"])
                current_tokens += unit_toks
            else:
                if current_chunk_lines:
                    c_start = current_chunk_lines[0][1]
                    c_end = current_chunk_lines[-1][2]
                    c_text = page_text[c_start:c_end].strip()
                    if c_text:
                        chunks.append({
                            "text": c_text,
                            "start_char": c_start,
                            "end_char": c_end,
                            "tokens": count_tokens(tokenizer, c_text),
                            "is_table": False
                        })
                    current_chunk_lines = []
                    current_tokens = 0

                # If single unit is larger than max_chunk_tokens, slice it by lines
                if unit_toks > max_chunk_tokens:
                    sub_lines: List[Tuple[str, int, int]] = []
                    sub_toks = 0
                    for l_str, l_start, l_end in unit["lines"]:
                        l_toks = count_tokens(tokenizer, l_str)
                        if sub_toks + l_toks > max_chunk_tokens and sub_lines:
                            sl_start = sub_lines[0][1]
                            sl_end = sub_lines[-1][2]
                            sl_text = page_text[sl_start:sl_end].strip()
                            if sl_text:
                                chunks.append({
                                    "text": sl_text,
                                    "start_char": sl_start,
                                    "end_char": sl_end,
                                    "tokens": count_tokens(tokenizer, sl_text),
                                    "is_table": False
                                })
                            # Overlap by taking last line if overlap_lines > 0
                            overlap = sub_lines[-overlap_lines:] if overlap_lines > 0 and len(sub_lines) >= overlap_lines else []
                            sub_lines = list(overlap) + [(l_str, l_start, l_end)]
                            sub_toks = sum(count_tokens(tokenizer, x[0]) for x in sub_lines)
                        else:
                            sub_lines.append((l_str, l_start, l_end))
                            sub_toks += l_toks

                    if sub_lines:
                        sl_start = sub_lines[0][1]
                        sl_end = sub_lines[-1][2]
                        sl_text = page_text[sl_start:sl_end].strip()
                        if sl_text:
                            chunks.append({
                                "text": sl_text,
                                "start_char": sl_start,
                                "end_char": sl_end,
                                "tokens": count_tokens(tokenizer, sl_text),
                                "is_table": False
                            })
                else:
                    current_chunk_lines = list(unit["lines"])
                    current_tokens = unit_toks

    if current_chunk_lines:
        c_start = current_chunk_lines[0][1]
        c_end = current_chunk_lines[-1][2]
        c_text = page_text[c_start:c_end].strip()
        if c_text:
            chunks.append({
                "text": c_text,
                "start_char": c_start,
                "end_char": c_end,
                "tokens": count_tokens(tokenizer, c_text),
                "is_table": False
            })

    return chunks

def verify_coverage(page_text: str, chunks: List[Dict[str, Any]]) -> float:
    raw_non_ws = re.sub(r"\s+", "", page_text)
    if not raw_non_ws:
        return 1.0
    # Collect non-ws characters from chunks
    chunk_non_ws = re.sub(r"\s+", "", "".join(c["text"] for c in chunks))
    # Check what set or sequence is covered
    # Because slicing includes lines, check if all chars in raw_non_ws are present
    # Multiset / Counter comparison:
    c_raw = Counter(raw_non_ws)
    c_chk = Counter(chunk_non_ws)
    covered = sum(min(c_raw[ch], c_chk[ch]) for ch in c_raw)
    return covered / len(raw_non_ws)

if __name__ == "__main__":
    tokenizer = get_tokenizer()
    for doc, pg in [("ADOBE_2015_10K", 58), ("3M_2018_10K", 59), ("AES_2022_10K", 131)]:
        pdf_path = BASE_DIR / "data" / "raw" / f"{doc}.pdf"
        reader = pypdf.PdfReader(str(pdf_path))
        text = reader.pages[pg].extract_text() or ""
        chks = chunk_page_v2(text, tokenizer)
        cov = verify_coverage(text, chks)
        print(f"\nDoc: {doc} Page: {pg}")
        print(f"Raw len: {len(text)}, Chunks: {len(chks)}, Coverage: {cov*100:.2f}%")
        for i, c in enumerate(chks):
            print(f"  Chunk {i}: tokens={c['tokens']}, tbl={c['is_table']}, len={len(c['text'])}")
