from pathlib import Path

from paper_alchemist.language import detect_language
from paper_alchemist.sections import looks_like_heading, segment_sections, text_statistics

FIXTURES = Path(__file__).parent / "fixtures" / "corpus"


def test_language_detection_separates_english_and_chinese():
    assert detect_language((FIXTURES / "english-paper.md").read_text(encoding="utf-8")) == "en"
    assert detect_language((FIXTURES / "chinese-paper.md").read_text(encoding="utf-8")) == "zh"


def test_section_detection_finds_all_standard_modules():
    for name in ("english-paper.md", "chinese-paper.md"):
        sections = segment_sections((FIXTURES / name).read_text(encoding="utf-8"))
        assert set(sections) == {
            "abstract",
            "introduction",
            "related-work",
            "problem-definition",
            "methodology",
            "experiment-setup",
            "results-analysis",
            "conclusion",
        }


def test_statistics_are_language_aware():
    en = text_statistics("We report a result. It may improve reliability.", "en")
    zh = text_statistics("本文报告实验结果。该方法可能提高稳定性。", "zh")
    assert en["sentences"] == 2
    assert zh["sentences"] == 2
    assert en["hedges"] == 1
    assert zh["hedges"] == 1


def test_two_column_and_descriptive_headings_are_recognized():
    assert (
        looks_like_heading("1. Introduction                    text in the other column")
        == "introduction"
    )
    assert looks_like_heading("3. A biased random-key genetic algorithm") == "methodology"
    assert (
        looks_like_heading("5.1. Benchmark instances and experimental configurations")
        == "experiment-setup"
    )
    assert looks_like_heading("algorithm") is None


def test_references_and_appendices_are_not_included_in_sections():
    text = (
        "# Introduction\n"
        "This introduction has enough grounded prose to be recognized as a paper module. "
        + ("Evidence. " * 20)
        + "\n# References\n"
        "[1] A reference that must not become introduction evidence.\n"
        "# Appendix\n"
        "Supplementary text that must not become introduction evidence.\n"
    )
    sections = segment_sections(text)
    assert "References" not in sections["introduction"]
    assert "Supplementary" not in sections["introduction"]
