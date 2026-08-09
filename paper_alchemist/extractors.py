"""Document discovery and text extraction backends."""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from .constants import DEFAULT_EXCLUDE_NAMES, DEFAULT_EXCLUDE_PARTS, SUPPORTED_EXTENSIONS


@dataclass(slots=True)
class Extraction:
    text: str
    backend: str
    warnings: list[str]


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


def extract_text(path: Path) -> Extraction:
    suffix = path.suffix.casefold()
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix == ".docx":
        return _extract_docx(path)
    if suffix == ".tex":
        return Extraction(_extract_tex(path), "latex", [])
    if suffix in {".md", ".txt"}:
        return Extraction(path.read_text(encoding="utf-8", errors="replace"), "text", [])
    raise ValueError(f"Unsupported paper format: {path.suffix}")


def _extract_pdf(path: Path) -> Extraction:
    warnings: list[str] = []
    executable = shutil.which("pdftotext")
    if executable:
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
            return Extraction(completed.stdout, "pdftotext", warnings)
        warnings.append(f"pdftotext failed with exit code {completed.returncode}")
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        text = "\n\n".join((page.extract_text() or "") for page in reader.pages)
        return Extraction(text, "pypdf", warnings)
    except Exception as exc:  # pragma: no cover - backend-specific failures
        warnings.append(f"pypdf failed: {exc}")
        return Extraction("", "none", warnings)


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
