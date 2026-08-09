"""Generation-brief construction for an Agent, without making an LLM call."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .constants import MODULES, OUTPUT_FORMATS
from .context import citation_keys, load_context, missing_context_fields
from .profiles import profile_slug, state_root


def build_generation_brief(
    profile: str,
    module: str,
    language: str,
    output_format: str,
    workspace: Path,
    context_path: Path | None = None,
    section_name: str | None = None,
) -> dict[str, Any]:
    if module not in {*MODULES, "section"}:
        raise ValueError(f"Unknown module: {module}")
    if language not in {"en", "zh"}:
        raise ValueError("Generation language must be en or zh")
    if output_format not in OUTPUT_FORMATS:
        raise ValueError("Output format must be latex or markdown")
    if module == "section" and not section_name:
        raise ValueError("Custom section generation requires --section-name")

    slug = profile_slug(profile)
    profile_dir = state_root(workspace) / "profiles" / slug
    if not profile_dir.exists():
        raise FileNotFoundError(f"Profile does not exist: {profile_dir}")
    secondary = "zh" if language == "en" else "en"
    target_module = module if module != "section" else "methodology"
    target_path = profile_dir / language / "modules" / f"{target_module}.md"
    secondary_path = profile_dir / secondary / "modules" / f"{target_module}.md"
    required_profiles = {
        f"{language}/{target_module}": target_path,
        f"{secondary}/{target_module}": secondary_path,
    }
    incomplete = [
        label for label, path in required_profiles.items() if _synthesis_status(path) != "complete"
    ]
    if incomplete:
        raise ValueError(
            "Generation requires completed semantic module profiles. Incomplete: "
            + ", ".join(incomplete)
        )
    integration_paths = (
        profile_dir / language / "integrated.md",
        profile_dir / "bilingual" / "cross-lingual.md",
        profile_dir / "bilingual" / "conflicts.md",
    )
    missing_integration = [str(path) for path in integration_paths if not path.is_file()]
    if missing_integration:
        raise ValueError(
            "Generation requires an integrated profile. Run `paper-alchemist integrate` "
            "after semantic synthesis. Missing: " + ", ".join(missing_integration)
        )
    target_count = _source_count(target_path)
    secondary_count = _source_count(secondary_path)
    degraded = target_count == 0 or secondary_count == 0
    context = load_context(context_path)
    missing = missing_context_fields(context, module)
    return {
        "schema_version": 1,
        "task": "draft-academic-section",
        "profile": slug,
        "module": module,
        "section_name": section_name,
        "target_language": language,
        "output_format": output_format,
        "bilingual_blend": {
            "target_language": language,
            "target_weight": 0.7,
            "secondary_language": secondary,
            "secondary_weight": 0.3,
            "status": "degraded-single-language" if degraded else "complete",
        },
        "profile_files": {
            "target_module": str(target_path),
            "secondary_module": str(secondary_path),
            "target_integrated": str(profile_dir / language / "integrated.md"),
            "cross_lingual": str(profile_dir / "bilingual" / "cross-lingual.md"),
            "conflicts": str(profile_dir / "bilingual" / "conflicts.md"),
        },
        "source_counts": {language: target_count, secondary: secondary_count},
        "context": context,
        "missing_context_fields": missing,
        "allowed_citation_keys": citation_keys(context),
        "instructions": [
            "Ask interactively for every missing_context_fields item before drafting.",
            "Use target-language wording and grammar; transfer only rhetorical functions from the secondary language.",
            "Do not invent claims, contributions, numerical results, significance, limitations, or citations.",
            "Use only allowed_citation_keys.",
            "Return in chat unless the user explicitly supplied an output path.",
        ],
    }


def render_brief(brief: dict[str, Any], as_json: bool = False) -> str:
    if as_json:
        import json

        return json.dumps(brief, ensure_ascii=False, indent=2) + "\n"
    return yaml.safe_dump(brief, sort_keys=False, allow_unicode=True)


def _source_count(path: Path) -> int:
    if not path.exists():
        return 0
    content = path.read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return 0
    parts = content.split("---", 2)
    if len(parts) < 3:
        return 0
    metadata = yaml.safe_load(parts[1]) or {}
    try:
        return int(metadata.get("source_count", 0))
    except (TypeError, ValueError):
        return 0


def _synthesis_status(path: Path) -> str | None:
    if not path.is_file():
        return None
    content = path.read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    metadata = yaml.safe_load(parts[1]) or {}
    if not isinstance(metadata, dict):
        return None
    value = metadata.get("synthesis_status")
    return str(value) if value is not None else None
