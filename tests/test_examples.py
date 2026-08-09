import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / "examples"


def test_requested_generation_examples_exist_in_both_formats():
    expected = {
        "abstract-en.tex",
        "abstract-zh.md",
        "experiment-setup-en.tex",
        "experiment-setup-zh.md",
        "results-analysis-en.md",
        "results-analysis-zh.tex",
    }
    assert expected == {
        path.name
        for path in EXAMPLES.iterdir()
        if path.suffix in {".md", ".tex"} and path.name != "README.md"
    }
    assert all((EXAMPLES / name).read_text(encoding="utf-8").strip() for name in expected)


def test_examples_use_only_allowed_citation_keys_and_supplied_results():
    context = yaml.safe_load((EXAMPLES / "paper-context.yaml").read_text(encoding="utf-8"))
    allowed = set(context["citations"])
    prose = "\n".join(
        path.read_text(encoding="utf-8")
        for path in EXAMPLES.iterdir()
        if path.suffix in {".md", ".tex"}
    )
    latex_keys = set(re.findall(r"\\cite\{([^}]+)\}", prose))
    markdown_keys = set(re.findall(r"\[([A-Za-z][A-Za-z0-9:_-]+)\]", prose))
    assert latex_keys | markdown_keys <= allowed
    assert "2.4%" in prose
    assert "statistically significant" not in prose.casefold()
