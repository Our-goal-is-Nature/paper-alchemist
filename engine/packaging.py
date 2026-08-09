"""Create a portable .skill archive from the canonical skill directory."""

from __future__ import annotations

import zipfile
from pathlib import Path

from .installer import find_skill_source


def package_skill(output_dir: Path) -> Path:
    source = find_skill_source()
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / "paper-alchemist.skill"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, Path("paper-alchemist") / path.relative_to(source))
    return target
