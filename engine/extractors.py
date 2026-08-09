"""Document discovery and text extraction backends."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from .constants import DEFAULT_EXCLUDE_NAMES, DEFAULT_EXCLUDE_PARTS, SUPPORTED_EXTENSIONS


@dataclass(slots=True)
class Extraction:
    text: str
    backend: str
    warnings: list[str]
    ocr_used: bool = False


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_papers(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Source directory does not exist: {root}")
    papers = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.casefold() not in SUPPORTED_EXTENSIONS:
            continue
        if path.name.casefold() in DEFAULT_EXCLUDE_NAMES:
            continue
        relative_parts = {part.casefold() for part in path.relative_to(root).parts[:-1]}
        if relative_parts & DEFAULT_EXCLUDE_PARTS:
            continue
        papers.append(path)
    return sorted(papers, key=lambda item: item.as_posix().casefold())


def extract_text(path: Path, ocr_mode: str = "auto") -> Extraction:
    if ocr_mode not in {"auto", "never", "always"}:
        raise ValueError("ocr_mode must be auto, never, or always")
    suffix = path.suffix.casefold()
    if suffix == ".pdf":
        return _extract_pdf(path, ocr_mode)
    if suffix == ".docx":
        return _extract_docx(path)
    if suffix == ".tex":
        return Extraction(_extract_tex(path), "latex", [])
    if suffix in {".md", ".txt"}:
        return Extraction(path.read_text(encoding="utf-8", errors="replace"), "text", [])
    raise ValueError(f"Unsupported paper format: {path.suffix}")


def _extract_pdf(path: Path, ocr_mode: str) -> Extraction:
    warnings: list[str] = []
    text = ""
    backend = "none"
    executable = shutil.which("pdftotext")
    if executable:
        try:
            completed = subprocess.run(
                [executable, "-layout", str(path), "-"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
                check=False,
            )
            if completed.returncode == 0 and completed.stdout.strip():
                text = completed.stdout
                backend = "pdftotext"
            else:
                warnings.append(f"pdftotext failed with exit code {completed.returncode}")
        except subprocess.TimeoutExpired:
            warnings.append("pdftotext timed out after 180 seconds")
    if not text.strip():
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(path))
            text = "\n\n".join((page.extract_text() or "") for page in reader.pages)
            backend = "pypdf"
        except Exception as exc:  # pragma: no cover - backend-specific failures
            warnings.append(f"pypdf failed: {exc}")

    if _should_ocr(text, ocr_mode):
        ocr_text, ocr_warnings = _ocr_pdf(path)
        warnings.extend(ocr_warnings)
        if ocr_text.strip() and len(ocr_text) > len(text):
            return Extraction(ocr_text, f"{backend}+tesseract", warnings, ocr_used=True)
    return Extraction(text, backend, warnings)


def _should_ocr(text: str, ocr_mode: str) -> bool:
    if ocr_mode == "always":
        return True
    if ocr_mode == "never":
        return False
    return len(text.strip()) < 800


def _ocr_pdf(path: Path) -> tuple[str, list[str]]:
    renderer = shutil.which("pdftoppm")
    tesseract = shutil.which("tesseract")
    missing = [
        name for name, value in (("pdftoppm", renderer), ("tesseract", tesseract)) if not value
    ]
    if missing:
        return "", [f"OCR unavailable; missing tool(s): {', '.join(missing)}"]

    warnings: list[str] = []
    with tempfile.TemporaryDirectory(prefix="paper-alchemist-ocr-") as temporary:
        temporary_path = Path(temporary)
        prefix = temporary_path / "page"
        try:
            rendered = subprocess.run(
                [renderer, "-jpeg", "-r", "200", str(path), str(prefix)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=600,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return "", ["pdftoppm OCR rendering timed out after 600 seconds"]
        if rendered.returncode != 0:
            return "", [f"pdftoppm OCR rendering failed with exit code {rendered.returncode}"]
        images = sorted(temporary_path.glob("page-*.jpg"))
        if not images:
            return "", ["pdftoppm produced no OCR page images"]
        language = _tesseract_language(tesseract)
        pages: list[str] = []
        for page_number, image in enumerate(images, start=1):
            try:
                completed = subprocess.run(
                    [tesseract, str(image), "stdout", "-l", language, "--psm", "3"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=300,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                warnings.append(f"tesseract timed out on page {page_number}")
                continue
            if completed.returncode == 0:
                pages.append(completed.stdout)
            else:
                warnings.append(
                    f"tesseract failed on page {page_number} with exit code {completed.returncode}"
                )
        return "\n\n".join(pages), warnings


def _tesseract_language(executable: str) -> str:
    completed = subprocess.run(
        [executable, "--list-langs"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    available = {
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip() and "available languages" not in line.casefold()
    }
    preferred = [language for language in ("eng", "chi_sim") if language in available]
    if preferred:
        return "+".join(preferred)
    return sorted(available)[0] if available else "eng"


def _extract_docx(path: Path) -> Extraction:
    from docx import Document

    document = Document(str(path))
    lines = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if not text:
            lines.append("")
            continue
        style = paragraph.style.name.casefold() if paragraph.style else ""
        if style.startswith("heading"):
            lines.append(f"# {text}")
        else:
            lines.append(text)
    return Extraction("\n".join(lines), "python-docx", [])


def _extract_tex(path: Path) -> str:
    source = path.read_text(encoding="utf-8", errors="replace")
    source = re.sub(r"(?<!\\)%.*", "", source)
    source = re.sub(r"\\begin\{abstract\}", "\n# Abstract\n", source)
    source = re.sub(r"\\end\{abstract\}", "\n", source)
    source = re.sub(
        r"\\(?:section|section\*|subsection|subsubsection)\{([^{}]+)\}",
        lambda match: f"\n# {match.group(1)}\n",
        source,
    )
    source = re.sub(r"\\(?:label|ref|eqref|url|footnote)\{[^{}]*\}", " ", source)
    source = re.sub(r"\\cite\w*\{([^{}]+)\}", lambda match: f"\\cite{{{match.group(1)}}}", source)
    source = re.sub(
        r"\\begin\{(?:figure|table|equation\*?|align\*?)\}.*?\\end\{[^{}]+\}",
        " ",
        source,
        flags=re.S,
    )
    source = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^]]*\])?", " ", source)
    source = source.replace("~", " ").replace("{", "").replace("}", "")
    source = re.sub(r"[ \t]+", " ", source)
    source = re.sub(r"\n{3,}", "\n\n", source)
    return source.strip()
