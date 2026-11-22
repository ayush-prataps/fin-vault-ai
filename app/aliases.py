"""
Company and year alias extractors backed by config/aliases.json.
"""
import json
import re
from pathlib import Path
from typing import Optional, List, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config" / "aliases.json"

_COMPANIES: List[Tuple[str, List[re.Pattern]]] = []
_YEAR_PATTERNS: List[re.Pattern] = []


def _load_config():
    global _COMPANIES, _YEAR_PATTERNS
    if _COMPANIES and _YEAR_PATTERNS:
        return
    if not CONFIG_PATH.exists():
        return
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    _COMPANIES = []
    for comp, pats in data.get("companies", {}).items():
        compiled = [re.compile(p, re.IGNORECASE) for p in pats]
        _COMPANIES.append((comp, compiled))

    _YEAR_PATTERNS = [re.compile(p, re.IGNORECASE) for p in data.get("year_patterns", [])]


def infer_company(text: str) -> Optional[str]:
    """Infer company name from question text using configured regex patterns."""
    _load_config()
    for comp, patterns in _COMPANIES:
        for pat in patterns:
            if pat.search(text):
                return comp
    return None


def infer_year(text: str) -> Optional[int]:
    """Infer target fiscal year from question text."""
    _load_config()
    candidates = []
    # 4-digit FY e.g. FY2022
    fy_4 = re.findall(r"\bFY\s*(20\d\d)\b", text, re.IGNORECASE)
    candidates.extend(int(y) for y in fy_4)

    # 2-digit FY e.g. FY22 -> 2022
    fy_2 = re.findall(r"\bFY\s*(\d{2})\b", text, re.IGNORECASE)
    candidates.extend(2000 + int(y) for y in fy_2)

    # Bare 4-digit years e.g. 2022
    bare_4 = re.findall(r"\b(20\d\d)\b", text)
    candidates.extend(int(y) for y in bare_4)

    return max(candidates) if candidates else None
