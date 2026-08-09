import tomllib
from pathlib import Path
from zipfile import ZipFile

import yaml

from paper_alchemist.packaging import package_skill
from paper_alchemist.skill_validation import validate_skill_bundle

ROOT = Path(__file__).parents[1]


def test_project_uses_mit_and_public_author_name():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["license"] == "MIT"
    assert project["project"]["authors"] == [{"name": "misakimei0331"}]
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert license_text.startswith("MIT License")
    assert "Copyright (c) 2026 misakimei0331" in license_text


def test_skill_frontmatter_remains_portable_and_minimal():
    content = (ROOT / "skills" / "paper-alchemist" / "SKILL.md").read_text(encoding="utf-8")
    metadata = yaml.safe_load(content.split("---", 2)[1])
    assert set(metadata) == {"name", "description"}
    assert metadata["name"] == "paper-alchemist"
    openai_metadata = yaml.safe_load(
        (ROOT / "skills" / "paper-alchemist" / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    assert "$paper-alchemist" in openai_metadata["interface"]["default_prompt"]
    validation = validate_skill_bundle(ROOT / "skills" / "paper-alchemist")
    assert validation["valid"], validation["errors"]


def test_private_research_paths_are_ignored_by_default():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for entry in (
        "/.paper-alchemist/",
        "/paper-context.yaml",
        "/papers/",
        "/corpus/",
        "*.pdf",
        "/.env",
    ):
        assert entry in ignore


def test_skill_archive_contains_only_the_portable_bundle(tmp_path):
    archive = package_skill(tmp_path)
    with ZipFile(archive) as bundle:
        names = set(bundle.namelist())
    assert "paper-alchemist/SKILL.md" in names
    assert "paper-alchemist/references/workflow.md" in names
    assert all("__pycache__" not in name for name in names)
