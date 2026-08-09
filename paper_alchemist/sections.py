"""Academic section recognition and deterministic descriptive statistics."""

from __future__ import annotations

import re
from collections import defaultdict
from statistics import mean

from .constants import MODULES

_HEADING_PREFIX = re.compile(r"^\s*(?:#{1,6}\s+|(?:\d+(?:\.\d+)*)[.)]?\s+)?(.{2,120}?)\s*$")
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?。！？])\s*")
_CITATION_RE = re.compile(
    r"(?:\\cite\w*\{[^}]+\}|\[[0-9,;\-\s]+\]|\([A-Z][A-Za-z-]+(?:\s+et al\.)?,?\s+\d{4}\))"
)

_ALIASES: dict[str, tuple[str, ...]] = {
    "abstract": ("abstract", "summary", "摘要", "摘 要"),
    "introduction": ("introduction", "background", "引言", "绪论", "研究背景"),
    "related-work": (
        "related work",
        "literature review",
        "related studies",
        "文献综述",
        "相关工作",
        "国内外研究",
    ),
    "problem-definition": (
        "problem definition",
        "problem statement",
        "problem description",
        "mathematical formulation",
        "model formulation",
        "问题定义",
        "问题描述",
        "数学模型",
        "模型构建",
    ),
    "methodology": (
        "method",
        "methods",
        "methodology",
        "proposed approach",
        "algorithm",
        "solution method",
        "方法",
        "研究方法",
        "算法设计",
        "求解方法",
    ),
    "experiment-setup": (
        "experimental setup",
        "experiment setup",
        "computational setup",
        "experimental design",
        "implementation details",
        "benchmark instances and experimental setup",
        "benchmark instances and experimental configurations",
        "experimental configurations",
        "instances, reference algorithms and parameter setting",
        "instances and parameters",
        "parameter setting",
        "parameter tuning",
        "实验设置",
        "实验设计",
        "数据与参数",
        "算例与参数",
    ),
    "results-analysis": (
        "results",
        "results and discussion",
        "computational results",
        "computational tests",
        "computational experiments",
        "experimental results",
        "comparative study",
        "analysis",
        "ablation study",
        "结果分析",
        "实验结果",
        "计算结果",
        "对比分析",
        "消融实验",
    ),
    "conclusion": (
        "conclusion",
        "conclusions",
        "concluding remarks",
        "discussion and conclusion",
        "结论",
        "总结",
        "结语",
    ),
}

_STOP_HEADINGS = (
    "references",
    "bibliography",
    "appendix",
    "acknowledgement",
    "acknowledgment",
    "参考文献",
    "附录",
    "致谢",
)


def normalize_heading(raw: str) -> str:
    heading = re.sub(r"\s+", " ", raw.strip().strip(".:："))
    heading = re.sub(r"^\d+(?:\.\d+)*[.)]?\s*", "", heading)
    return heading.casefold()


def classify_heading(raw: str) -> str | None:
    normalized = normalize_heading(raw)
    if normalized in {"article info abstract", "article information abstract"}:
        return "abstract"
    if any(normalized == stop or normalized.startswith(stop + " ") for stop in _STOP_HEADINGS):
        return "__stop__"
    for module, aliases in _ALIASES.items():
        for alias in aliases:
            key = alias.casefold()
            if (
                normalized == key
                or normalized.startswith(key + ":")
                or normalized.startswith(key + " ")
            ):
                return module
    if re.search(r"\b(?:instance|benchmark|parameter)s?\b", normalized) and re.search(
        r"\b(?:setup|setting|configuration|design|implementation|tuning)s?\b", normalized
    ):
        return "experiment-setup"
    if re.search(
        r"\b(?:result|experiment|comparison|analysis|performance|sensitivity|ablation|evaluation|test)s?\b",
        normalized,
    ):
        return "results-analysis"
    if re.search(
        r"\b(?:algorithm|heuristic|matheuristic|method|procedure|framework|search|formulation)s?\b",
        normalized,
    ):
        return "methodology"
    return None


def looks_like_heading(line: str) -> str | None:
    stripped = line.strip()
    if not stripped:
        return None
    candidate = re.split(r"\s{4,}", stripped, maxsplit=1)[0].strip()
    if len(candidate) > 120:
        return None
    markdown = candidate.startswith("#")
    numbered = bool(re.match(r"^\d+(?:\.\d+)*[.)]?\s+", candidate))
    plain = candidate.lstrip("# ")
    known = classify_heading(plain)
    has_cjk = bool(re.search(r"[\u3400-\u9fff]", plain))
    letters = re.sub(r"[^A-Za-z]", "", plain)
    visibly_styled = bool(has_cjk or (letters and (letters.isupper() or plain.istitle())))
    if known and (markdown or numbered or visibly_styled):
        return known
    match = _HEADING_PREFIX.match(candidate)
    if match and (markdown or numbered):
        return classify_heading(match.group(1))
    return None


def segment_sections(text: str) -> dict[str, str]:
    """Split extracted paper text into canonical academic modules."""
    buckets: dict[str, list[str]] = defaultdict(list)
    current: str | None = None
    lines = text.splitlines()
    introduction_line: int | None = None
    for index, line in enumerate(lines):
        heading = looks_like_heading(line)
        if heading == "__stop__":
            if current is not None:
                current = None
                break
            continue
        if heading:
            current = heading
            if heading == "introduction" and introduction_line is None:
                introduction_line = index
            continue
        if current:
            buckets[current].append(line.rstrip())
    result = {
        module: "\n".join(lines).strip()
        for module, lines in buckets.items()
        if module in MODULES and len("".join(lines).strip()) >= 120
    }
    if "abstract" not in result and introduction_line is not None:
        inferred = _infer_preamble_abstract(lines[:introduction_line])
        if len(inferred) >= 300:
            result["abstract"] = inferred
    return result


def _infer_preamble_abstract(lines: list[str]) -> str:
    """Recover an unlabeled abstract from the front matter of journal PDFs."""
    metadata = re.compile(
        r"journal homepage|available online|article history|article info|keywords?|received|accepted|copyright|doi:|e-mail|corresponding author",
        re.I,
    )
    candidates: list[str] = []
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue
        parts = [part.strip() for part in re.split(r"\s{4,}", stripped) if part.strip()]
        if parts and metadata.search(parts[0]) and len(parts) > 1:
            stripped = " ".join(parts[1:])
        elif metadata.search(stripped):
            continue
        if len(stripped) < 45:
            continue
        if len(re.findall(r"[A-Za-z\u3400-\u9fff]", stripped)) < 35:
            continue
        candidates.append(stripped)
    return "\n".join(candidates[-30:])[:8000].strip()


def academic_heading_count(text: str) -> int:
    found = set()
    for line in text.splitlines():
        module = looks_like_heading(line)
        if module and module != "__stop__":
            found.add(module)
    return len(found)


def prose_density(text: str) -> float:
    """Estimate how much extracted text resembles prose rather than labels or tables."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    total_characters = sum(len(line) for line in lines)
    if not total_characters:
        return 0.0
    prose_characters = 0
    for line in lines:
        word_count = len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", line))
        cjk_count = len(re.findall(r"[\u3400-\u9fff]", line))
        language_characters = len(re.findall(r"[A-Za-z\u3400-\u9fff]", line))
        language_ratio = language_characters / max(len(line), 1)
        if language_ratio >= 0.5 and (word_count >= 8 or cjk_count >= 24):
            prose_characters += len(line)
    return round(prose_characters / total_characters, 4)


def text_statistics(text: str, language: str) -> dict[str, float | int]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) >= 20]
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text) if len(s.strip()) >= 5]
    if language == "zh":
        sentence_lengths = [len(re.findall(r"[\u3400-\u9fffA-Za-z0-9]", s)) for s in sentences]
    else:
        sentence_lengths = [len(re.findall(r"\b[\w'-]+\b", s)) for s in sentences]
    citation_count = len(_CITATION_RE.findall(text))
    hedges = len(
        re.findall(
            r"\b(?:may|might|could|suggests?|indicates?|approximately|typically)\b|可能|表明|大约|通常",
            text,
            re.I,
        )
    )
    first_person = len(re.findall(r"\b(?:we|our)\b|本文|我们", text, re.I))
    figure_mentions = len(re.findall(r"\bfig(?:ure)?\.?\s*\d+[a-z]?|图\s*\d+[a-z]?", text, re.I))
    table_mentions = len(re.findall(r"\btable\s*\d+[a-z]?|表\s*\d+[a-z]?", text, re.I))
    return {
        "characters": len(text),
        "paragraphs": len(paragraphs),
        "sentences": len(sentences),
        "average_sentence_length": round(mean(sentence_lengths), 2) if sentence_lengths else 0.0,
        "citations": citation_count,
        "hedges": hedges,
        "first_person_markers": first_person,
        "figure_mentions": figure_mentions,
        "table_mentions": table_mentions,
    }
