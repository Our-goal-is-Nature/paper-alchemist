"""Shared constants for corpus processing and command adapters."""

from __future__ import annotations

SUPPORTED_EXTENSIONS = {".pdf", ".tex", ".docx", ".md", ".txt"}
LANGUAGES = {"auto", "en", "zh"}
OUTPUT_FORMATS = {"latex", "markdown"}

MODULES = (
    "abstract",
    "introduction",
    "related-work",
    "problem-definition",
    "methodology",
    "experiment-setup",
    "results-analysis",
    "conclusion",
)

OPERATIONS = ("distill", "integrate", *MODULES, "section")

MODULE_TITLES = {
    "abstract": ("Abstract", "摘要"),
    "introduction": ("Introduction", "引言"),
    "related-work": ("Related Work", "相关工作"),
    "problem-definition": ("Problem Definition", "问题定义"),
    "methodology": ("Methodology", "方法"),
    "experiment-setup": ("Experiment Setup", "实验设置"),
    "results-analysis": ("Results Analysis", "结果分析"),
    "conclusion": ("Conclusion", "结论"),
}

PROFILE_HEADINGS = (
    "Rhetorical moves",
    "Organization",
    "Language and stance",
    "Evidence and citations",
    "Cross-lingual transferable patterns",
    "Do",
    "Avoid",
    "Generation checklist",
)

DEFAULT_EXCLUDE_PARTS = {
    ".git",
    ".paper-alchemist",
    "__pycache__",
    "figures",
    "figure",
    "images",
    "image",
}

DEFAULT_EXCLUDE_NAMES = {
    "readme.md",
    "readme.txt",
    "license.txt",
    "changelog.md",
    "cmakelists.txt",
}
