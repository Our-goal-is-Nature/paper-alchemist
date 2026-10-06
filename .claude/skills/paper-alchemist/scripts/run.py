#!/usr/bin/env python3
"""Thin entrypoint used by Agents when the console script is unavailable."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    try:
        from paper_alchemist.cli import main as cli_main
    except ImportError:
        command = shutil.which("paper-alchemist")
        if command:
            return subprocess.call([command, *sys.argv[1:]])
        repo_root = next(
            (parent for parent in Path(__file__).resolve().parents
             if (parent / "engine" / "cli.py").is_file()),
            None,
        )
        if repo_root is not None:
            sys.path.insert(0, str(repo_root))
            from engine.cli import main as cli_main
        else:
            print(
                "Paper Alchemist Python package is missing. Clone the repository and run "
                "`python -m pip install -e .` before using this skill.",
                file=sys.stderr,
            )
            return 2
    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
