"""Corpus preparation, deterministic seed profiles, and bilingual integration."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from statistics import mean
from typing import Any
import unicodedata

import yaml

from .constants import MODULES, MODULE_TITLES, PROFILE_HEADINGS
from .extractors import discover_papers, extract_text, file_sha256
from .language import detect_language, language_scores
from .sections import academic_heading_count, segment_sections, text_statistics


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def profile_slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold().replace("_", "-")
    slug = re.sub(r"[^\w-]+", "-", normalized, flags=re.UNICODE).replace("_", "-")
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("Profile name must contain at least one letter or digit")
    return slug[:100].rstrip("-")


def state_root(workspace: Path) -> Path:
    return workspace.resolve() / ".paper-alchemist"


def build_profile(
    source: Path,
    profile: str,
    workspace: Path,
    language: str = "auto",
    update: bool = False,
    min_characters: int = 800,
) -> dict[str, Any]:
    slug = profile_slug(profile)
    root = state_root(workspace)
    profile_dir = root / "profiles" / slug
    cache_dir = root / "cache" / slug
    if profile_dir.exists() and not update:
        raise FileExistsError(
            f"Profile already exists: {profile_dir}. Pass --update to refresh it."
        )
    profile_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    previous_manifest = _read_json(profile_dir / "source-manifest.json", default={})
    previous_by_path = {
        item.get("path"): item
        for item in previous_manifest.get("documents", [])
        if isinstance(item, dict)
    }

    documents: list[dict[str, Any]] = []
    module_samples: dict[str, dict[str, list[dict[str, Any]]]] = {
        "en": defaultdict(list),
        "zh": defaultdict(list),
    }
    for path in discover_papers(source.resolve()):
        digest = file_sha256(path)
        relative = path.relative_to(source.resolve()).as_posix()
        doc_id = f"{_safe_stem(path.stem)}-{digest[:10]}"
        document_cache = cache_dir / "documents" / doc_id
        cached_meta = _read_json(document_cache / "meta.json", default={})
        previous = previous_by_path.get(str(path.resolve()))
        cache_matches = bool(
            cached_meta.get("sha256") == digest
            and (document_cache / "full.txt").exists()
        )
        manifest_matches = bool(previous and previous.get("sha256") == digest)
        # A matching private cache is sufficient for --update. This also lets an
        # interrupted first run resume when it stopped before writing the manifest.
        can_reuse = bool(update and cache_matches and (manifest_matches or not previous))
        warnings: list[str] = []
        if can_reuse:
            text = (document_cache / "full.txt").read_text(encoding="utf-8")
            backend = cached_meta.get("backend", "cache")
            warnings.extend(cached_meta.get("warnings", []))
            status = "reused"
        else:
            extraction = extract_text(path)
            text = extraction.text.replace("\x00", "").strip()
            backend = extraction.backend
            warnings.extend(extraction.warnings)
            status = "extracted"

        doc_language = language if language in {"en", "zh"} else detect_language(text)
        sections = segment_sections(text)
        heading_count = academic_heading_count(text)
        included = True
        reason = "included"
        if len(text) < min_characters:
            included, reason = False, "low-text-or-scanned"
        elif doc_language == "unknown":
            included, reason = False, "language-undetermined"
        elif len(sections) < 2:
            included, reason = False, "insufficient-paper-structure"

        entry = {
            "id": doc_id,
            "path": str(path.resolve()),
            "relative_path": relative,
            "sha256": digest,
            "format": path.suffix.casefold().lstrip("."),
            "backend": backend,
            "language": doc_language,
            "language_scores": language_scores(text),
            "characters": len(text),
            "recognized_modules": sorted(sections),
            "academic_heading_count": heading_count,
            "included": included,
            "reason": reason,
            "cache_status": status,
            "warnings": warnings,
        }
        documents.append(entry)

        document_cache.mkdir(parents=True, exist_ok=True)
        (document_cache / "full.txt").write_text(text, encoding="utf-8")
        _write_json(
            document_cache / "meta.json",
            {"sha256": digest, "backend": backend, "warnings": warnings},
        )
        if not included:
            continue
        sections_dir = document_cache / "sections"
        sections_dir.mkdir(parents=True, exist_ok=True)
        for module, section_text in sections.items():
            section_language = (
                language if language in {"en", "zh"} else detect_language(section_text)
            )
            if section_language == "unknown":
                section_language = doc_language
            section_path = sections_dir / f"{module}.txt"
            section_path.write_text(section_text, encoding="utf-8")
            module_samples[section_language][module].append(
                {
                    "document_id": doc_id,
                    "source": relative,
                    "cache_path": str(section_path.resolve()),
                    "text": section_text,
                    "statistics": text_statistics(section_text, section_language),
                }
            )

    manifest = {
        "schema_version": 1,
        "profile": slug,
        "source": str(source.resolve()),
        "created_at": previous_manifest.get("created_at", utc_now()),
        "updated_at": utc_now(),
        "language_mode": language,
        "documents": documents,
    }
    _write_json(profile_dir / "source-manifest.json", manifest)

    semantic_refresh: list[str] = []
    for lang in ("en", "zh"):
        modules_dir = profile_dir / lang / "modules"
        modules_dir.mkdir(parents=True, exist_ok=True)
        for module in MODULES:
            samples = module_samples[lang].get(module, [])
            seed = _render_module_seed(slug, lang, module, samples)
            seed_path = modules_dir / f"{module}.seed.md"
            seed_path.write_text(seed, encoding="utf-8")
            profile_path = modules_dir / f"{module}.md"
            if not profile_path.exists() or "synthesis_status: pending" in profile_path.read_text(
                encoding="utf-8", errors="replace"
            ):
                profile_path.write_text(seed, encoding="utf-8")
            elif update:
                semantic_refresh.append(f"{lang}/{module}")
            _write_packets(cache_dir, lang, module, samples)

    quality = _quality_report(slug, documents, module_samples, semantic_refresh)
    _write_json(profile_dir / "quality.json", quality)
    integrate_profile(slug, workspace)
    return {
        "profile": slug,
        "profile_dir": str(profile_dir),
        "cache_dir": str(cache_dir),
        "documents_found": len(documents),
        "documents_included": sum(1 for item in documents if item["included"]),
        "documents_excluded": sum(1 for item in documents if not item["included"]),
        "module_samples": quality["module_samples"],
        "semantic_refresh_required": semantic_refresh,
    }


def integrate_profile(profile: str, workspace: Path) -> dict[str, Any]:
    slug = profile_slug(profile)
    profile_dir = state_root(workspace) / "profiles" / slug
    if not profile_dir.exists():
        raise FileNotFoundError(f"Profile does not exist: {profile_dir}")
    quality = _read_json(profile_dir / "quality.json", default={})
    for lang in ("en", "zh"):
        integrated = _render_integrated(slug, lang, profile_dir, quality)
        target = profile_dir / lang / "integrated.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(integrated, encoding="utf-8")
    bilingual = profile_dir / "bilingual"
    bilingual.mkdir(parents=True, exist_ok=True)
    cross = _render_cross_lingual(slug, profile_dir, quality)
    conflicts = _render_conflicts(slug, quality)
    (bilingual / "cross-lingual.md").write_text(cross, encoding="utf-8")
    (bilingual / "conflicts.md").write_text(conflicts, encoding="utf-8")
    return {
        "profile": slug,
        "integrated": [
            str(profile_dir / "en" / "integrated.md"),
            str(profile_dir / "zh" / "integrated.md"),
            str(bilingual / "cross-lingual.md"),
            str(bilingual / "conflicts.md"),
        ],
    }


def validate_profile(profile: str, workspace: Path) -> dict[str, Any]:
    slug = profile_slug(profile)
    profile_dir = state_root(workspace) / "profiles" / slug
    errors: list[str] = []
    warnings: list[str] = []
    for required in ("source-manifest.json", "quality.json"):
        if not (profile_dir / required).is_file():
            errors.append(f"missing {required}")
    for lang in ("en", "zh"):
        for module in MODULES:
            path = profile_dir / lang / "modules" / f"{module}.md"
            if not path.is_file():
                errors.append(f"missing {lang}/modules/{module}.md")
                continue
            content = path.read_text(encoding="utf-8")
            try:
                metadata = _frontmatter(content)
            except ValueError as exc:
                errors.append(f"{path}: {exc}")
                continue
            for field in ("profile", "language", "module", "source_count", "confidence"):
                if field not in metadata:
                    errors.append(f"{path}: missing frontmatter field {field}")
            if metadata.get("synthesis_status") != "complete":
                warnings.append(f"semantic synthesis pending: {lang}/{module}")
            for heading in PROFILE_HEADINGS:
                if f"## {heading}" not in content:
                    errors.append(f"{path}: missing section {heading}")
            if metadata.get("source_count", 0) < 3:
                warnings.append(f"low-confidence corpus: {lang}/{module}")
    for relative in (
        "en/integrated.md",
        "zh/integrated.md",
        "bilingual/cross-lingual.md",
        "bilingual/conflicts.md",
    ):
        if not (profile_dir / relative).is_file():
            errors.append(f"missing {relative}")
    return {"profile": slug, "valid": not errors, "errors": errors, "warnings": warnings}


def _render_module_seed(
    profile: str, language: str, module: str, samples: list[dict[str, Any]]
) -> str:
    count = len(samples)
    confidence = "high" if count >= 8 else "medium" if count >= 3 else "low"
    statistics = [sample["statistics"] for sample in samples]
    averages = {
        key: round(mean(float(item[key]) for item in statistics), 2) if statistics else 0
        for key in (
            "paragraphs",
            "sentences",
            "average_sentence_length",
            "citations",
            "hedges",
            "first_person_markers",
        )
    }
    metadata = {
        "profile": profile,
        "language": language,
        "module": module,
        "source_count": count,
        "confidence": confidence,
        "synthesis_status": "pending",
    }
    front = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True).strip()
    source_list = "\n".join(f"- `{item['source']}`" for item in samples) or "- No qualifying samples."
    body = [
        f"---\n{front}\n---",
        f"# {MODULE_TITLES[module][0]} / {MODULE_TITLES[module][1]}",
        "",
        "> Quantitative seed generated locally. The active Agent must review the private packet files, replace pending notes with corpus-level semantic findings, and set `synthesis_status: complete`. Do not copy source sentences.",
        "",
        "## Corpus evidence",
        "",
        source_list,
        "",
        "## Quantitative baseline",
        "",
        *[f"- {key.replace('_', ' ')}: {value}" for key, value in averages.items()],
    ]
    for heading in PROFILE_HEADINGS:
        body.extend(["", f"## {heading}", "", "- Pending Agent synthesis."])
    return "\n".join(body).rstrip() + "\n"


def _write_packets(
    cache_dir: Path, language: str, module: str, samples: list[dict[str, Any]], batch_size: int = 4
) -> None:
    target = cache_dir / "packets" / language / module
    target.mkdir(parents=True, exist_ok=True)
    for old in target.glob("batch-*.md"):
        old.unlink()
    for start in range(0, len(samples), batch_size):
        batch = samples[start : start + batch_size]
        lines = [
            f"# Private distillation packet: {language}/{module}",
            "",
            "Summarize recurring rhetorical and organizational patterns. Never reproduce long phrases.",
        ]
        for sample in batch:
            lines.extend(
                [
                    "",
                    f"## Source {sample['document_id']}",
                    "",
                    f"Path label: `{sample['source']}`",
                    "",
                    sample["text"][:16000],
                ]
            )
        (target / f"batch-{start // batch_size + 1:03d}.md").write_text(
            "\n".join(lines).rstrip() + "\n", encoding="utf-8"
        )


def _quality_report(
    profile: str,
    documents: list[dict[str, Any]],
    module_samples: dict[str, dict[str, list[dict[str, Any]]]],
    semantic_refresh: list[str],
) -> dict[str, Any]:
    sample_counts = {
        lang: {module: len(module_samples[lang].get(module, [])) for module in MODULES}
        for lang in ("en", "zh")
    }
    metrics: dict[str, dict[str, dict[str, float]]] = {"en": {}, "zh": {}}
    for lang in ("en", "zh"):
        for module in MODULES:
            stats = [item["statistics"] for item in module_samples[lang].get(module, [])]
            metrics[lang][module] = {
                key: round(mean(float(value[key]) for value in stats), 2) if stats else 0.0
                for key in ("average_sentence_length", "citations", "hedges", "first_person_markers")
            }
    return {
        "schema_version": 1,
        "profile": profile,
        "updated_at": utc_now(),
        "documents_found": len(documents),
        "documents_included": sum(1 for item in documents if item["included"]),
        "documents_excluded": sum(1 for item in documents if not item["included"]),
        "module_samples": sample_counts,
        "metrics": metrics,
        "semantic_refresh_required": semantic_refresh,
        "bilingual_status": (
            "complete"
            if any(sample_counts["en"].values()) and any(sample_counts["zh"].values())
            else "degraded-single-language"
        ),
    }


def _render_integrated(
    profile: str, language: str, profile_dir: Path, quality: dict[str, Any]
) -> str:
    other = "zh" if language == "en" else "en"
    counts = quality.get("module_samples", {}).get(language, {})
    lines = [
        "---",
        f"profile: {profile}",
        f"language: {language}",
        "target_weight: 0.7",
        f"secondary_language: {other}",
        "secondary_weight: 0.3",
        "---",
        f"# Integrated {language.upper()} writing profile",
        "",
        "Use module-specific profiles before this integrated fallback. Borrow rhetorical functions from the secondary language, but realize all wording in the target language's academic conventions.",
        "",
        "## Module routing",
        "",
    ]
    for module in MODULES:
        lines.append(
            f"- `{module}`: `{language}/modules/{module}.md` ({counts.get(module, 0)} sources); secondary `{other}/modules/{module}.md`."
        )
    lines.extend(
        [
            "",
            "## Shared constraints",
            "",
            "- Preserve factual grounding from `paper-context.yaml`.",
            "- Use only supplied citation keys.",
            "- Transfer discourse functions, never source-language surface syntax.",
            "- Report a degraded bilingual status when either language lacks evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_cross_lingual(profile: str, profile_dir: Path, quality: dict[str, Any]) -> str:
    counts = quality.get("module_samples", {})
    lines = [
        "---",
        f"profile: {profile}",
        "mode: bilingual",
        "target_language_weight: 0.7",
        "secondary_language_weight: 0.3",
        "---",
        "# Cross-lingual academic structure profile",
        "",
        "Align high-level rhetorical functions across English and Chinese. Do not translate or reuse source sentences.",
        "",
        "## Aligned modules",
        "",
        "| Module | English sources | Chinese sources | Transfer rule |",
        "|---|---:|---:|---|",
    ]
    for module in MODULES:
        en = counts.get("en", {}).get(module, 0)
        zh = counts.get("zh", {}).get(module, 0)
        rule = "bidirectional" if en and zh else "single-language fallback"
        lines.append(f"| {module} | {en} | {zh} | {rule} |")
    lines.extend(
        [
            "",
            "## Transfer boundaries",
            "",
            "- Transfer problem framing, gap placement, contribution ordering, evidence chains, and conclusion closure.",
            "- Keep terminology, grammar, voice, citation punctuation, and sentence rhythm under the target-language profile.",
            "- When evidence exists in one language only, mark the generation brief as degraded rather than blocking.",
        ]
    )
    return "\n".join(lines) + "\n"


def _render_conflicts(profile: str, quality: dict[str, Any]) -> str:
    metrics = quality.get("metrics", {})
    lines = [
        "---",
        f"profile: {profile}",
        "resolution: target-language-wins",
        "---",
        "# Bilingual profile conflicts",
        "",
        "When English and Chinese conventions conflict, preserve the rhetorical function but use the target language's wording and grammar.",
        "",
        "| Module | Potential metric differences | Resolution |",
        "|---|---|---|",
    ]
    for module in MODULES:
        en = metrics.get("en", {}).get(module, {})
        zh = metrics.get("zh", {}).get(module, {})
        differences = (
            f"sentence length en={en.get('average_sentence_length', 0)}, "
            f"zh={zh.get('average_sentence_length', 0)}; "
            f"first-person en={en.get('first_person_markers', 0)}, "
            f"zh={zh.get('first_person_markers', 0)}"
        )
        lines.append(f"| {module} | {differences} | Target-language convention |")
    return "\n".join(lines) + "\n"


def _frontmatter(content: str) -> dict[str, Any]:
    if not content.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("unclosed YAML frontmatter")
    data = yaml.safe_load(parts[1]) or {}
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a mapping")
    return data


def _safe_stem(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9-]+", "-", value).strip("-").casefold()
    return safe[:60] or "paper"


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
