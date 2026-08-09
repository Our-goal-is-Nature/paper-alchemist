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

    supplied_values = {
        item["value"] for item in context["research"]["results"] if item.get("value")
    }
    generated_percentages = set(re.findall(r"\d+(?:\.\d+)?\\?%", prose))
    assert {value.replace("%", "") for value in supplied_values} >= {
        value.replace("\\", "").replace("%", "") for value in generated_percentages
    }


def test_examples_do_not_reuse_long_fixture_phrases():
    fixture_words = set()
    for source in (ROOT / "tests" / "fixtures" / "corpus").glob("*.md"):
        words = re.findall(r"[a-z]+", source.read_text(encoding="utf-8").casefold())
        fixture_words.update(tuple(words[index : index + 12]) for index in range(len(words) - 11))

    for example in EXAMPLES.iterdir():
        if example.suffix not in {".md", ".tex"}:
            continue
        words = re.findall(r"[a-z]+", example.read_text(encoding="utf-8").casefold())
        example_ngrams = {tuple(words[index : index + 12]) for index in range(len(words) - 11)}
        assert not (fixture_words & example_ngrams), example.name
