"""Research context loading and module-specific grounding checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


MODULE_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "abstract": ("research.problem", "research.gap", "research.contributions", "research.method", "research.results"),
    "introduction": ("research.problem", "research.gap", "research.contributions"),
    "related-work": ("research.gap", "citations"),
    "problem-definition": ("research.problem",),
    "methodology": ("research.method",),
    "experiment-setup": ("research.experiments",),
    "results-analysis": ("research.results",),
    "conclusion": ("research.contributions", "research.results"),
    "section": (),
}


def load_context(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Context file does not exist: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("paper-context.yaml must contain a YAML mapping")
    return data


def get_nested(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def missing_context_fields(data: dict[str, Any], module: str) -> list[str]:
    missing = []
    for field in MODULE_REQUIREMENTS.get(module, ()):
        value = get_nested(data, field)
        if value is None or value == "" or value == [] or value == {}:
            missing.append(field)
    return missing


def citation_keys(data: dict[str, Any]) -> list[str]:
    citations = data.get("citations", {})
    if isinstance(citations, dict):
        return sorted(str(key) for key in citations)
    if isinstance(citations, list):
        keys = []
        for item in citations:
            if isinstance(item, dict) and item.get("key"):
                keys.append(str(item["key"]))
        return sorted(keys)
    return []
