# Paper Alchemist

Paper Alchemist is a model-agnostic [Agent Skills](https://agentskills.io/) package for distilling corpus-level academic writing patterns and drafting evidence-grounded paper sections. It keeps English and Chinese profiles separate during analysis, then blends both during generation with the target language dominant (approximately 70/30).

It does **not** call an LLM API. Local Python code handles extraction, sectioning, statistics, manifests, and validation; the active Agent performs semantic synthesis and writing.

## Features

- Recursively processes PDF, LaTeX, DOCX, Markdown, and text papers.
- Recognizes abstract, introduction, related work, problem definition, methodology, experiment setup, results analysis, and conclusion modules.
- Produces separate English and Chinese profiles plus cross-lingual integration and conflict reports.
- Uses `paper-context.yaml` as the factual boundary and asks interactively for missing module-specific facts.
- Generates LaTeX or Markdown without inventing results, significance, contributions, or citations.
- Installs native adapters for Codex, Claude Code, OpenCode, Hermes, Pi Agent, and Kimi Code.
- Keeps extracted paper text in a gitignored local cache.

## Install

Python 3.11 or newer is required. `pdftotext` is recommended; `pypdf` is used as the fallback.

```bash
git clone https://github.com/Wang-Ruibin/paper-alchemist.git
cd paper-alchemist
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

Install the skill for one Agent:

```bash
paper-alchemist install --agent codex --scope user
paper-alchemist install --agent claude --scope project
paper-alchemist install --agent opencode --scope project
paper-alchemist install --agent hermes --scope user
paper-alchemist install --agent pi --scope user
paper-alchemist install --agent kimi --scope user
```

Use `--dry-run` to inspect destinations and `--force` only when intentionally replacing an existing installation.

## Distill a corpus

From the research project where the local profile should live:

```bash
paper-alchemist distill /path/to/papers --profile routing-literature --language auto
```

The command prepares private packets in `.paper-alchemist/cache/` and seed profiles in `.paper-alchemist/profiles/`. Invoke the installed `paper-alchemist` skill and ask the Agent to finish `distill`; the skill directs it to review packets, complete semantic module profiles, integrate the languages, and validate the result.

Refresh an existing profile without re-extracting unchanged papers:

```bash
paper-alchemist distill /path/to/papers --profile routing-literature --language auto --update
```

## Draft a section

Copy the context template and fill only verified facts:

```bash
cp skills/paper-alchemist/assets/paper-context.example.yaml paper-context.yaml
```

Examples by platform:

| Agent | Example |
|---|---|
| Codex | `$paper-alchemist abstract profile=routing-literature lang=en format=latex context=paper-context.yaml` |
| Claude Code | `/abstract profile=routing-literature lang=en format=latex context=paper-context.yaml` |
| OpenCode | `/abstract profile=routing-literature lang=en format=latex context=paper-context.yaml` |
| Hermes | `/abstract profile=routing-literature lang=en format=latex context=paper-context.yaml` |
| Pi Agent | `/abstract profile=routing-literature lang=en format=latex context=paper-context.yaml` |
| Kimi Code | `/skill:abstract profile=routing-literature lang=en format=latex context=paper-context.yaml` |

The target language controls grammar, terminology, voice, and citation punctuation. The secondary language contributes transferable rhetorical structure. If one language is absent, generation continues with an explicit degraded-confidence notice.

See [`examples/`](examples/) for original English and Chinese abstract, experiment-setup, and results-analysis outputs in both LaTeX and Markdown. Every example is bounded by its accompanying context file.

## CLI reference

```text
paper-alchemist distill SOURCE --profile NAME [--language auto|en|zh] [--update]
paper-alchemist integrate --profile NAME
paper-alchemist validate-profile --profile NAME
paper-alchemist brief MODULE --profile NAME --language en|zh --format latex|markdown [--context FILE]
paper-alchemist install --agent AGENT --scope user|project [--dry-run]
paper-alchemist package-skill --output dist
```

The CLI prepares a generation brief; the active Agent writes the section. Omitting a context file is supported, but the Agent must obtain required facts interactively before drafting.

## 中文说明

Paper Alchemist 将中文和英文论文分别蒸馏为模块化画像，再在生成阶段同时借鉴两种语言。目标写作语言约占 70%：它决定自然措辞、语法、术语和引用格式；另一语言约占 30%：只迁移问题铺垫、研究缺口、贡献排序、实验论证链等高层写法。

论文语料只回答“如何写”，`paper-context.yaml` 和用户明确提供的信息才回答“研究事实是什么”。Skill 禁止自行编造贡献、方法、实验数字、统计显著性和引用。

## Privacy and copyright

- Source papers are never copied into the skill or public repository.
- Extracted text remains under `.paper-alchemist/cache/`, which is ignored by Git.
- Profiles record aggregate patterns and source counts, not long quotations or author imitation.
- Scanned, corrupt, password-protected, low-text, and structurally unrecognized files are reported rather than silently treated as evidence.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
paper-alchemist package-skill --output dist
```

Licensed under Apache-2.0.
