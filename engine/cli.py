"""Paper Alchemist command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from . import __version__
from .briefs import build_generation_brief, render_brief
from .constants import LANGUAGES, MODULES, OUTPUT_FORMATS
from .installer import AGENTS, install
from .packaging import package_skill
from .profiles import build_profile, integrate_profile, validate_profile
from .skill_validation import validate_skill_bundle


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        prog="paper-alchemist",
        description="Prepare bilingual academic style profiles for Agent-driven writing.",
    )
    root.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = root.add_subparsers(dest="command", required=True)

    distill = sub.add_parser("distill", help="Extract and partition an academic paper corpus")
    distill.add_argument("source", type=Path)
    distill.add_argument("--profile", required=True)
    distill.add_argument("--language", choices=sorted(LANGUAGES), default="auto")
    distill.add_argument("--workspace", type=Path, default=Path.cwd())
    distill.add_argument("--update", action="store_true")
    distill.add_argument("--min-characters", type=int, default=800)
    distill.add_argument(
        "--ocr",
        choices=("auto", "never", "always"),
        default="auto",
        help="OCR policy for PDFs: auto for low-text files, never, or always",
    )

    integrate = sub.add_parser("integrate", help="Build language and cross-lingual integrations")
    integrate.add_argument("--profile", required=True)
    integrate.add_argument("--workspace", type=Path, default=Path.cwd())

    validate = sub.add_parser(
        "validate-profile", help="Validate a profile's structure and confidence"
    )
    validate.add_argument("--profile", required=True)
    validate.add_argument("--workspace", type=Path, default=Path.cwd())

    brief = sub.add_parser("brief", help="Prepare a grounded bilingual generation brief")
    brief.add_argument("module", choices=[*MODULES, "section"])
    brief.add_argument("--profile", required=True)
    brief.add_argument("--language", choices=["en", "zh"], required=True)
    brief.add_argument("--format", choices=sorted(OUTPUT_FORMATS), default="latex")
    brief.add_argument("--context", type=Path)
    brief.add_argument("--section-name")
    brief.add_argument("--workspace", type=Path, default=Path.cwd())
    brief.add_argument("--json", action="store_true")
    brief.add_argument("--out", type=Path)

    installer = sub.add_parser("install", help="Install the skill and a native Agent adapter")
    installer.add_argument("--agent", choices=sorted(AGENTS), required=True)
    installer.add_argument("--scope", choices=["user", "project"], default="user")
    installer.add_argument("--project-root", type=Path, default=Path.cwd())
    installer.add_argument("--home", type=Path)
    installer.add_argument("--force", action="store_true")
    installer.add_argument("--dry-run", action="store_true")

    package = sub.add_parser("package-skill", help="Build the paper-alchemist.skill archive")
    package.add_argument("--output", type=Path, default=Path("dist"))

    skill_validation = sub.add_parser(
        "validate-skill", help="Validate the portable Agent Skill bundle"
    )
    skill_validation.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("paper-alchemist"),
    )
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result: Any
        if args.command == "distill":
            result = build_profile(
                args.source,
                args.profile,
                args.workspace,
                language=args.language,
                update=args.update,
                min_characters=args.min_characters,
                ocr_mode=args.ocr,
            )
            _print_json(result)
        elif args.command == "integrate":
            _print_json(integrate_profile(args.profile, args.workspace))
        elif args.command == "validate-profile":
            result = validate_profile(args.profile, args.workspace)
            _print_json(result)
            return 0 if result["valid"] else 2
        elif args.command == "brief":
            result = build_generation_brief(
                args.profile,
                args.module,
                args.language,
                args.format,
                args.workspace,
                args.context,
                args.section_name,
            )
            rendered = render_brief(result, as_json=args.json)
            if args.out:
                args.out.parent.mkdir(parents=True, exist_ok=True)
                args.out.write_text(rendered, encoding="utf-8")
                _print_json(
                    {
                        "brief": str(args.out),
                        "missing_context_fields": result["missing_context_fields"],
                    }
                )
            else:
                print(rendered, end="")
        elif args.command == "install":
            result = install(
                args.agent,
                args.scope,
                args.project_root,
                home=args.home,
                force=args.force,
                dry_run=args.dry_run,
            )
            _print_json(asdict(result))
        elif args.command == "package-skill":
            target = package_skill(args.output)
            _print_json({"package": str(target)})
        elif args.command == "validate-skill":
            result = validate_skill_bundle(args.path)
            _print_json(result)
            return 0 if result["valid"] else 2
        else:  # pragma: no cover
            raise AssertionError(f"Unhandled command: {args.command}")
        return 0
    except (FileNotFoundError, FileExistsError, ValueError, TimeoutError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
