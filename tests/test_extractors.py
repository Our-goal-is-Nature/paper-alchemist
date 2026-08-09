from pathlib import Path

from paper_alchemist.extractors import _ocr_pdf, _should_ocr


def test_automatic_ocr_is_limited_to_low_text_pdfs():
    assert _should_ocr("short text", "auto") is True
    assert _should_ocr("x" * 800, "auto") is False
    assert _should_ocr("x" * 800, "always") is True
    assert _should_ocr("", "never") is False


def test_ocr_reports_missing_runtime_without_hiding_the_failure(monkeypatch, tmp_path):
    def fake_which(name):
        return "/usr/bin/pdftoppm" if name == "pdftoppm" else None

    monkeypatch.setattr("paper_alchemist.extractors.shutil.which", fake_which)
    text, warnings = _ocr_pdf(Path(tmp_path / "scan.pdf"))
    assert text == ""
    assert warnings == ["OCR unavailable; missing tool(s): tesseract"]
