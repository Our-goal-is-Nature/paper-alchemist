import json
from pathlib import Path

from paper_alchemist.briefs import build_generation_brief
from paper_alchemist.profiles import build_profile, profile_slug, validate_profile


FIXTURES = Path(__file__).parent / "fixtures"


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
    assert (profile_dir / "bilingual" / "cross-lingual.md").is_file()

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
    assert any(item.startswith("semantic synthesis pending:") for item in validation["warnings"])


def test_update_reuses_unchanged_extraction(tmp_path):
    build_profile(FIXTURES / "corpus", "demo", tmp_path, min_characters=200)
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
    brief = build_generation_brief("demo", "results-analysis", "zh", "markdown", tmp_path)
    assert brief["missing_context_fields"] == ["research.results"]
    assert brief["allowed_citation_keys"] == []
