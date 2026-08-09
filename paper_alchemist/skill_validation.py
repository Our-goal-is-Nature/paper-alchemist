"""Portable validation for the bundled Agent Skill."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


def validate_skill_bundle(skill_dir: Path) -> dict[str, Any]:
    skill_dir = skill_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return {"valid": False, "errors": ["missing SKILL.md"], "warnings": []}

    content = skill_file.read_text(encoding="utf-8")
    metadata = _frontmatter(content, errors)
    name = metadata.get("name") if metadata else None
    if metadata and set(metadata) != {"name", "description"}:
        errors.append("SKILL.md frontmatter must contain only name and description")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]{1,63}", name):
        errors.append("skill name must use 1-63 lowercase letters, digits, or hyphens")
    elif skill_dir.name != name:
        errors.append(f"skill directory must be named {name}")
    description = metadata.get("description") if metadata else None
    if not isinstance(description, str) or not description.strip():
        errors.append("skill description must be a non-empty string")

    for relative in (
        "agents/openai.yaml",
        "assets/paper-context.example.yaml",
        "references/generation.md",
        "references/platforms.md",
        "references/schemas.md",
        "references/workflow.md",
        "scripts/run.py",
    ):
        if not (skill_dir / relative).is_file():
            errors.append(f"missing {relative}")

    openai_path = skill_dir / "agents" / "openai.yaml"
    if openai_path.is_file():
        openai = yaml.safe_load(openai_path.read_text(encoding="utf-8")) or {}
        prompt = openai.get("interface", {}).get("default_prompt", "")
        if name and f"${name}" not in prompt:
            errors.append(f"agents/openai.yaml default_prompt must mention ${name}")

    if len(content.splitlines()) > 500:
        warnings.append("SKILL.md exceeds the recommended 500-line limit")
    return {"valid": not errors, "errors": errors, "warnings": warnings}


def _frontmatter(content: str, errors: list[str]) -> dict[str, Any]:
    if not content.startswith("---\n"):
        errors.append("SKILL.md is missing YAML frontmatter")
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("SKILL.md frontmatter is not closed")
        return {}
    try:
        metadata = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        errors.append(f"invalid SKILL.md YAML: {exc}")
        return {}
    if not isinstance(metadata, dict):
        errors.append("SKILL.md frontmatter must be a mapping")
        return {}
    return metadata
