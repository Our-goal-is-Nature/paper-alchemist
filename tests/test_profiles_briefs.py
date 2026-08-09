import json
import shutil
from pathlib import Path

import pytest

import paper_alchemist.profiles as profiles_module
from paper_alchemist.briefs import build_generation_brief
from paper_alchemist.constants import MODULES
from paper_alchemist.extractors import Extraction
from paper_alchemist.profiles import (
    build_profile,
    integrate_profile,
    profile_slug,
    validate_profile,
)

FIXTURES = Path(__file__).parent / "fixtures"


def complete_semantic_profiles(profile_dir: Path) -> None:
    for language in ("en", "zh"):
        for module in MODULES:
            path = profile_dir / language / "modules" / f"{module}.md"
            content = path.read_text(encoding="utf-8")
            content = content.replace("synthesis_status: pending", "synthesis_status: complete")
            content = content.replace("synthesis_status: stale", "synthesis_status: complete")
            content = content.replace(
                "- Pending Agent synthesis.", "- Fixture-level synthesis completed for testing."
            )
            path.write_text(content, encoding="utf-8")


def test_profile_slug_supports_chinese_names():
    assert profile_slug("团队定向-英文画像") == "团队定向-英文画像"


def test_bilingual_profile_and_generation_brief(tmp_path):
    result = build_profile(
        FIXTURES / "corpus",
        "Bilingual Demo",
        tmp_path,
        min_characters=200,
    )
    assert result["documents_included"] == 2
    assert result["module_samples"]["en"]["abstract"] == 1
    assert result["module_samples"]["zh"]["abstract"] == 1

    profile_dir = tmp_path / ".paper-alchemist" / "profiles" / "bilingual-demo"
    quality = json.loads((profile_dir / "quality.json").read_text(encoding="utf-8"))
    assert quality["bilingual_status"] == "complete"
    assert quality["source_coverage"]["included_ratio"] == 1.0
    assert quality["module_confidence"]["en"]["abstract"] == "low"
    assert quality["anomalies"] == []
    observations = list(
        (
            tmp_path
            / ".paper-alchemist"
            / "cache"
            / "bilingual-demo"
            / "observations"
            / "en"
            / "abstract"
        ).glob("*.md")
    )
    assert len(observations) == 1
    assert "observation_status: pending" in observations[0].read_text(encoding="utf-8")
    assert not (profile_dir / "bilingual" / "cross-lingual.md").exists()

    validation = validate_profile("Bilingual Demo", tmp_path)
    assert validation["valid"], validation["errors"]
    assert validation["semantic_complete"] is False
    assert validation["integration_complete"] is False
    with pytest.raises(ValueError, match="Semantic synthesis is incomplete"):
        integrate_profile("Bilingual Demo", tmp_path)

    complete_semantic_profiles(profile_dir)
    with pytest.raises(ValueError, match="integrated profile"):
        build_generation_brief(
            "Bilingual Demo",
            "abstract",
            "en",
            "latex",
            tmp_path,
            FIXTURES / "paper-context.yaml",
        )
    integrate_profile("Bilingual Demo", tmp_path)

    brief = build_generation_brief(
        "Bilingual Demo",
        "abstract",
        "en",
        "latex",
        tmp_path,
        FIXTURES / "paper-context.yaml",
    )
    assert brief["bilingual_blend"]["status"] == "complete"
    assert brief["bilingual_blend"]["target_weight"] == 0.7
    assert brief["source_counts"] == {"en": 1, "zh": 1}
    assert brief["missing_context_fields"] == []
    assert brief["allowed_citation_keys"] == ["baseline2026"]

    validation = validate_profile("Bilingual Demo", tmp_path)
    assert validation["valid"], validation["errors"]
    assert validation["semantic_complete"] is True
    assert validation["integration_complete"] is True


def test_update_reuses_unchanged_extraction(tmp_path):
    build_profile(FIXTURES / "corpus", "demo", tmp_path, min_characters=200)
    profile_dir = tmp_path / ".paper-alchemist" / "profiles" / "demo"
    complete_semantic_profiles(profile_dir)
    integrate_profile("demo", tmp_path)
    result = build_profile(
        FIXTURES / "corpus",
        "demo",
        tmp_path,
        update=True,
        min_characters=200,
    )
    manifest_path = tmp_path / ".paper-alchemist" / "profiles" / "demo" / "source-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert result["documents_included"] == 2
    assert {item["cache_status"] for item in manifest["documents"]} == {"reused"}
    assert result["semantic_refresh_required"] == []
    assert (profile_dir / "bilingual" / "cross-lingual.md").is_file()


def test_update_marks_changed_corpus_profiles_stale(tmp_path):
    corpus = tmp_path / "corpus"
    shutil.copytree(FIXTURES / "corpus", corpus)
    build_profile(corpus, "changed-demo", tmp_path, min_characters=200)
    profile_dir = tmp_path / ".paper-alchemist" / "profiles" / "changed-demo"
    complete_semantic_profiles(profile_dir)
    integrate_profile("changed-demo", tmp_path)

    english = corpus / "english-paper.md"
    english.write_text(
        english.read_text(encoding="utf-8").replace(
            "stable runtime behavior",
            "stable and reproducible runtime behavior",
        ),
        encoding="utf-8",
    )
    result = build_profile(
        corpus,
        "changed-demo",
        tmp_path,
        update=True,
        min_characters=200,
    )

    assert "en/abstract" in result["semantic_refresh_required"]
    assert "en/introduction" not in result["semantic_refresh_required"]
    assert not (profile_dir / "bilingual" / "cross-lingual.md").exists()
    abstract = (profile_dir / "en" / "modules" / "abstract.md").read_text(encoding="utf-8")
    assert "synthesis_status: stale" in abstract


def test_update_resumes_from_cache_when_manifest_is_missing(tmp_path):
    build_profile(FIXTURES / "corpus", "resume-demo", tmp_path, min_characters=200)
    profile_dir = tmp_path / ".paper-alchemist" / "profiles" / "resume-demo"
    (profile_dir / "source-manifest.json").unlink()

    build_profile(
        FIXTURES / "corpus",
        "resume-demo",
        tmp_path,
        update=True,
        min_characters=200,
    )
    manifest = json.loads((profile_dir / "source-manifest.json").read_text(encoding="utf-8"))
    assert {item["cache_status"] for item in manifest["documents"]} == {"reused"}


def test_missing_context_is_reported_not_invented(tmp_path):
    build_profile(FIXTURES / "corpus", "demo", tmp_path, min_characters=200)
    profile_dir = tmp_path / ".paper-alchemist" / "profiles" / "demo"
    with pytest.raises(ValueError, match="completed semantic module profiles"):
        build_generation_brief("demo", "results-analysis", "zh", "markdown", tmp_path)
    complete_semantic_profiles(profile_dir)
    integrate_profile("demo", tmp_path)
    brief = build_generation_brief("demo", "results-analysis", "zh", "markdown", tmp_path)
    assert brief["missing_context_fields"] == ["research.results"]
    assert brief["allowed_citation_keys"] == []


def test_figure_or_table_heavy_pdf_is_included_when_it_has_structure(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    paper = corpus / "visual-results.pdf"
    paper.write_bytes(b"synthetic pdf placeholder")
    table_rows = "\n".join(f"Table 1 {index} 0.12 0.34 0.56" for index in range(30))
    figure_rows = "\n".join(f"Figure 2 {index} 1.20 1.30 1.40" for index in range(30))
    extracted = f"{table_rows}\n{figure_rows}"

    def fake_extract(path, ocr_mode="auto"):
        assert path == paper
        assert ocr_mode == "never"
        return Extraction(extracted, "test-pdf", [], ocr_used=False)

    monkeypatch.setattr(profiles_module, "extract_text", fake_extract)
    result = build_profile(
        corpus,
        "visual-demo",
        tmp_path,
        min_characters=200,
        ocr_mode="never",
    )

    manifest = json.loads(
        (
            tmp_path / ".paper-alchemist" / "profiles" / "visual-demo" / "source-manifest.json"
        ).read_text(encoding="utf-8")
    )
    document = manifest["documents"][0]
    assert result["documents_included"] == 1
    assert document["included"] is True
    assert document["content_mode"] == "figure-or-table-heavy"
    assert document["ocr_used"] is False
    assert result["module_samples"]["en"]["results-analysis"] == 1


def test_single_language_profile_degrades_without_blocking_generation(tmp_path):
    corpus = tmp_path / "english-only"
    corpus.mkdir()
    shutil.copy(FIXTURES / "corpus" / "english-paper.md", corpus)
    build_profile(corpus, "english-only", tmp_path, min_characters=200)
    profile_dir = tmp_path / ".paper-alchemist" / "profiles" / "english-only"
    complete_semantic_profiles(profile_dir)
    integrate_profile("english-only", tmp_path)

    brief = build_generation_brief(
        "english-only",
        "abstract",
        "en",
        "latex",
        tmp_path,
        FIXTURES / "paper-context.yaml",
    )
    assert brief["bilingual_blend"]["status"] == "degraded-single-language"
    assert brief["source_counts"] == {"en": 1, "zh": 0}
