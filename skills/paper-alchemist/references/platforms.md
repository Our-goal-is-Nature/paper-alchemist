# Platform Invocation and Installation

Install from a cloned repository after `python -m pip install -e .`:

```bash
paper-alchemist install --agent <agent> --scope <user|project>
```

Supported agent identifiers and invocation:

| Agent | Core invocation | Native module wrapper |
|---|---|---|
| Codex | `$paper-alchemist abstract ...` | Use the skill mention; deprecated custom prompts are not installed |
| Claude Code | `/abstract ...` | `.claude/commands/*.md` |
| OpenCode | `/abstract ...` | `.opencode/commands/*.md` |
| Hermes | `/abstract ...` | lightweight wrapper skills |
| Pi Agent | `/abstract ...` | prompt templates; `/skill:paper-alchemist` remains available |
| Kimi Code | `/skill:abstract ...` | lightweight wrapper skills; `/skill:paper-alchemist` remains available |

Kimi Code's documented portable invocation is `/skill:<name>`. A runtime may expose an unprefixed shorthand when it is unambiguous, but do not rely on that shorthand for portability.

Use `--dry-run` to list destinations without writing. Existing targets are protected unless `--force` is explicitly supplied.

For project-scoped Hermes installation, the installer adds the project `.agents/skills` directory to `~/.hermes/config.yaml` under `skills.external_dirs`.
