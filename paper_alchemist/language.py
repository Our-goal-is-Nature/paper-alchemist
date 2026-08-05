"""Small deterministic language detector for English and Chinese corpora."""

from __future__ import annotations

import re

_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
_LATIN_RE = re.compile(r"[A-Za-z]")


def language_scores(text: str) -> dict[str, float | int]:
    """Return character evidence and normalized English/Chinese scores."""
    cjk = len(_CJK_RE.findall(text))
    latin = len(_LATIN_RE.findall(text))
    total = cjk + latin
    if total == 0:
        return {"zh_chars": 0, "en_chars": 0, "zh_score": 0.0, "en_score": 0.0}
    return {
        "zh_chars": cjk,
        "en_chars": latin,
        "zh_score": round(cjk / total, 6),
        "en_score": round(latin / total, 6),
    }


def detect_language(text: str, minimum_evidence: int = 20) -> str:
    """Classify text as ``zh``, ``en`` or ``unknown``.

    Chinese is selected when CJK characters provide at least 20% of the
    English/Chinese character evidence. This intentionally treats technical
    Chinese prose containing many Latin symbols as Chinese.
    """
    scores = language_scores(text)
    evidence = int(scores["zh_chars"]) + int(scores["en_chars"])
    if evidence < minimum_evidence:
        return "unknown"
    if float(scores["zh_score"]) >= 0.20:
        return "zh"
    return "en"
