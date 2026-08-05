"""Install the portable skill and native command adapters."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import sys
import yaml

from .constants import OPERATIONS

AGENTS = {"codex", "claude", "opencode", "hermes", "pi", "kimi"}


@dataclass(slots=True)
class InstallResult:
    agent: str
    scope: str
    installed: list[str]
    notes: list[str]
    dry_run: bool


def find_skill_source() -> Path:
    override = os.environ.get("PAPER_ALCHEMIST_SKILL_SOURCE")
    if override:
        candidates = [Path(override).expanduser().resolve()]
    else:
        candidates = [
            Path(__file__).resolve().parents[1] / "skills" / "paper-alchemist",
            Path(sys.prefix) / "share" / "paper-alchemist" / "skills" / "paper-alchemist",
        ]
    for candidate in candidates:
        if (candidate / "SKILL.md").is_file():
            return candidate
    raise FileNotFoundError(
        "Cannot find the paper-alchemist skill bundle. Reinstall the package, run from a "
        "cloned repository, or set PAPER_ALCHEMIST_SKILL_SOURCE."
    )


def install(
    agent: str,
    scope: str,
    project_root: Path,
    home: Path | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> InstallResult:
    if agent not in AGENTS:
        raise ValueError(f"Unsupported agent: {agent}")
    if scope not in {"user", "project"}:
        raise ValueError("scope must be user or project")
    home = (home or Path.home()).expanduser().resolve()
    project_root = project_root.expanduser().resolve()
    source = find_skill_source()
    installed: list[str] = []
    notes: list[str] = []

    skill_target, command_target, adapter_kind = _targets(agent, scope, project_root, home)
    _copy_directory(source, skill_target, force=force, dry_run=dry_run)
    installed.append(str(skill_target))

    if adapter_kind in {"claude", "opencode", "pi"} and command_target:
        for operation in OPERATIONS:
            suffix = ".md"
            target = command_target / f"{operation}{suffix}"
            content = _prompt_wrapper(adapter_kind, operation)
            _write_file(target, content, force=force, dry_run=dry_run)
            installed.append(str(target))
    elif adapter_kind in {"hermes", "kimi"} and command_target:
        for operation in OPERATIONS:
            target = command_target / operation / "SKILL.md"
            content = _skill_wrapper(adapter_kind, operation)
            _write_file(target, content, force=force, dry_run=dry_run)
            installed.append(str(target.parent))

    if agent == "hermes" and scope == "project":
        config = home / ".hermes" / "config.yaml"
        _configure_hermes_external_dir(config, skill_target.parent, dry_run=dry_run)
        installed.append(str(config))
        notes.append("Added the project .agents/skills directory to Hermes external_dirs.")
    if agent == "codex":
        notes.append("Invoke with $paper-alchemist followed by the operation and arguments.")
    else:
        notes.append("Native slash wrappers were installed for distill, integrate, and section drafting.")
    return InstallResult(agent, scope, installed, notes, dry_run)


def _targets(
    agent: str, scope: str, project: Path, home: Path
) -> tuple[Path, Path | None, str | None]:
    if scope == "project":
        if agent == "codex":
            return project / ".agents" / "skills" / "paper-alchemist", None, None
        if agent == "claude":
            return (
                project / ".claude" / "skills" / "paper-alchemist",
                project / ".claude" / "commands",
                "claude",
            )
        if agent == "opencode":
            return (
                project / ".agents" / "skills" / "paper-alchemist",
                project / ".opencode" / "commands",
                "opencode",
            )
        if agent == "hermes":
            return (
                project / ".agents" / "skills" / "paper-alchemist",
                project / ".agents" / "skills",
                "hermes",
            )
        if agent == "pi":
            return (
                project / ".pi" / "skills" / "paper-alchemist",
                project / ".pi" / "prompts",
                "pi",
            )
        return (
            project / ".kimi-code" / "skills" / "paper-alchemist",
            project / ".kimi-code" / "skills",
            "kimi",
        )
    if agent == "codex":
        return home / ".agents" / "skills" / "paper-alchemist", None, None
    if agent == "claude":
        return (
            home / ".claude" / "skills" / "paper-alchemist",
            home / ".claude" / "commands",
            "claude",
        )
    if agent == "opencode":
        return (
            home / ".agents" / "skills" / "paper-alchemist",
            home / ".config" / "opencode" / "commands",
            "opencode",
        )
    if agent == "hermes":
        return home / ".hermes" / "skills" / "paper-alchemist", home / ".hermes" / "skills", "hermes"
    if agent == "pi":
        return (
            home / ".pi" / "agent" / "skills" / "paper-alchemist",
            home / ".pi" / "agent" / "prompts",
            "pi",
        )
    return home / ".kimi-code" / "skills" / "paper-alchemist", home / ".kimi-code" / "skills", "kimi"


def _prompt_wrapper(agent: str, operation: str) -> str:
    argument_token = "$ARGUMENTS"
    frontmatter = ""
    if agent in {"claude", "opencode"}:
        frontmatter = f"---\ndescription: Run Paper Alchemist {operation}\n---\n\n"
    return (
        frontmatter
        + f"Use the installed `paper-alchemist` Agent Skill. Execute its `{operation}` operation.\n\n"
        + f"User arguments: {argument_token}\n\n"
        + "Follow the core skill's bilingual blending, factual-grounding, privacy, validation, and output rules. "
        + "If required research facts are missing, ask only for those facts before drafting.\n"
    )


def _skill_wrapper(agent: str, operation: str) -> str:
    description = f"Run Paper Alchemist {operation}. Use when the user invokes /{operation} or requests this paper-writing operation."
    kimi_fields = ""
    kimi_arguments = ""
    if agent == "kimi":
        kimi_fields = (
            "type: prompt\n"
            f"whenToUse: Execute the Paper Alchemist {operation} operation\n"
        )
        kimi_arguments = "\nUser arguments: $ARGUMENTS\n"
    return (
        "---\n"
        f"name: {operation}\n"
        f"description: {description}\n"
        f"{kimi_fields}"
        "---\n\n"
        f"# Paper Alchemist: {operation}\n\n"
        "Load the sibling `paper-alchemist` skill and follow it completely. "
        f"Execute the `{operation}` operation with all text supplied after this command as arguments.\n\n"
        "Preserve the core skill's 70/30 target-language bilingual blend and never invent research facts or citations.\n"
        f"{kimi_arguments}"
    )


def _copy_directory(source: Path, target: Path, force: bool, dry_run: bool) -> None:
    if target.exists() and not force:
        raise FileExistsError(f"Install target already exists: {target}. Pass --force to replace it.")
    if dry_run:
        return
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)


def _write_file(path: Path, content: str, force: bool, dry_run: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Adapter already exists: {path}. Pass --force to replace it.")
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _configure_hermes_external_dir(config: Path, skills_dir: Path, dry_run: bool) -> None:
    if dry_run:
        return
    data = {}
    if config.exists():
        loaded = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
        if not isinstance(loaded, dict):
            raise ValueError(f"Hermes config must be a YAML mapping: {config}")
        data = loaded
    skills = data.setdefault("skills", {})
    if not isinstance(skills, dict):
        raise ValueError(f"Hermes config skills entry must be a mapping: {config}")
    external = skills.setdefault("external_dirs", [])
    if not isinstance(external, list):
        raise ValueError(f"Hermes external_dirs must be a list: {config}")
    value = str(skills_dir)
    if value not in external:
        external.append(value)
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
