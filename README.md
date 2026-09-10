<div align="center">

# Paper Alchemist

### Distill how great papers write. Draft with evidence, not invention.

A model-agnostic Agent Skill for modular, bilingual academic-writing distillation and grounded paper drafting.

[![CI](https://github.com/Wang-Ruibin/paper-alchemist/actions/workflows/ci.yml/badge.svg)](https://github.com/Wang-Ruibin/paper-alchemist/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Wang-Ruibin/paper-alchemist)](https://github.com/Wang-Ruibin/paper-alchemist/releases)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**English** · [简体中文](README.zh-CN.md)

</div>

## Why Paper Alchemist?

Academic corpora can teach an Agent **how to write**: how an abstract moves from problem to evidence, how an introduction places its gap, or how a results section separates observation from interpretation. They must never be treated as evidence for **what is true** about your research.

Paper Alchemist keeps those responsibilities separate:

- local Python extracts, sections, hashes, measures, and validates papers;
- the active Agent distills corpus-level writing patterns and drafts prose;
- `paper-context.yaml` and explicit user answers are the only factual sources;
- no bundled script calls an LLM API;
- no single author is imitated and no long source passage is retained in a profile.

## Highlights

- **Modular distillation** — separate profiles for abstract, introduction, related work, problem definition, methodology, experiment setup, results analysis, and conclusion.
- **Bilingual by design** — preserve English and Chinese evidence separately, then blend both during generation; the target writing language leads at roughly 70/30.
- **Grounded generation** — block drafting until semantic profiles are complete, report missing research facts, and allow only declared citation keys.
- **Incremental and resumable** — reuse hash-matched extraction caches and invalidate only profiles affected by corpus changes.
- **Figure/table-aware PDFs** — retain text-bearing visual papers, count figure/table callouts, and optionally OCR low-text or scanned pages.
- **Cross-Agent** — one open Agent Skill with adapters for Codex, Claude Code, OpenCode, Hermes, Pi Agent, and Kimi Code.
- **Private by default** — source papers, extracted text, research context, and generated profiles remain outside version control.

## 60-second start: install → distill → generate

The entire workflow happens through a terminal-and-file-capable Agent. **A paper profile answers “how papers like these write,” not “what is true about your research.”** New content must take its research facts from `paper-context.yaml` or your explicit answers.

### 1. First use: ask the Agent to install it

Send this to Codex, Claude Code, OpenCode, Hermes, Pi Agent, or Kimi Code:

```text
Install Paper Alchemist from https://github.com/Wang-Ruibin/paper-alchemist and
configure it at user scope for the Agent you are currently running as. Check for
Python 3.11+, choose this platform's adapter, create an isolated Python environment
that remains callable from future sessions, and verify both the CLI and Skill.
Do not overwrite an existing installation. Ask before installing or upgrading Python,
PDF tools, or OCR components. Tell me whether I must start a new session when done.
```

Replace “user scope” with “project scope” to enable it only in the current research project. If the Agent says Skill discovery requires a reload, start a new session.

### 2. Start distilling: provide a paper folder and profile name

Put the reference papers in a folder such as `./papers/`, then tell the Agent from your research project:

```text
Use Paper Alchemist to distill ./papers into a profile named routing-literature.
Before processing, check the research project's .gitignore and keep the papers,
paper-context.yaml, and .paper-alchemist/ out of version control. Detect English,
Chinese, and OCR needs automatically. Complete paper extraction,
per-paper observations, module-level semantic synthesis, bilingual integration, and
final validation. Do not stop after producing extraction results or seed files; keep
working until validate-profile returns generation_ready: true, or report a blocker
that requires me. Finally report the profile directory, included and excluded papers,
warnings, incomplete modules, and generation_ready.
```

The reusable profile is stored at `.paper-alchemist/profiles/routing-literature/` in the current research project. Source papers, research context, extracted text, and profiles may contain private material and should be excluded by that project's `.gitignore`.

### 3. Know when distillation is complete: require `generation_ready`

The Agent's final report must contain:

```text
generation_ready: true
```

This means the profile is structurally valid, every English and Chinese module has completed semantic synthesis, and all bilingual integration artifacts exist. **`valid: true` alone does not mean distillation is complete**; it may only mean the files are structurally valid.

If `generation_ready: false`, inspect the reported `incomplete_profiles` and `errors`, then say:

```text
Complete every module listed in incomplete_profiles, resolve errors, integrate again,
and revalidate until generation_ready: true. Do not call pending, stale, or seed-only
profiles complete.
```

Warnings may indicate a small corpus or missing evidence in one language. They do not always block generation, but the Agent must explain the limitations.

### 4. Generate new content from the profile

Prepare `paper-context.yaml` with your research problem, method, experiments, results, and allowed citation keys. If you do not have one, first say: “Use Paper Alchemist's `paper-context.example.yaml` to guide me through creating my research context.”

Once the profile is ready, describe the content you want:

```text
First confirm that routing-literature has generation_ready: true. Then use that profile
and ./paper-context.yaml to draft a new English LaTeX abstract. Research facts and
citations may come only from paper-context.yaml or my explicit answers. If required
facts are missing, ask only for what the abstract needs. When done, report which
language profiles were used and any degraded status, then return the draft in chat.
```

Replace “abstract” with introduction, related work, problem definition, methodology, experiment setup, results analysis, conclusion, or a custom section. You may also provide an exact output path. The underlying [command table](#commands) is only for automation and troubleshooting.

## How it works

```mermaid
flowchart LR
    A[PDF / LaTeX / DOCX / Markdown / TXT] --> B[Text layer / optional OCR]
    B --> C[Sectioning and visual-callout statistics]
    C --> D[Private bilingual packets]
    D --> E[Agent semantic synthesis by module]
    E --> F[English and Chinese profiles]
    F --> G[Cross-lingual integration]
    H[Verified paper-context.yaml] --> I[Grounded section drafting]
    G --> I
```

1. `distill` discovers papers, extracts text layers or optional OCR, removes references and appendices, detects language, segments modules, and creates private evidence packets.
2. The active Agent reviews packets and replaces quantitative seeds with aggregate semantic findings.
3. `integrate` refuses incomplete or stale module profiles, then builds English, Chinese, cross-lingual, and conflict profiles.
4. A section command builds a generation brief, checks required facts and citations, and drafts in the requested language and format.

## Commands

| Command | Purpose |
|---|---|
| `distill SOURCE --profile NAME --language auto\|en\|zh --ocr auto\|never\|always` | Extract and partition a corpus, with optional PDF OCR |
| `integrate --profile NAME` | Integrate completed semantic profiles |
| `validate-profile --profile NAME` | Report structure, semantic and integration status, and the `generation_ready` completion signal |
| `brief MODULE --profile NAME --language en\|zh` | Build a grounded bilingual drafting brief |
| `install --agent AGENT --scope user\|project` | Install the core Skill and native wrappers |
| `package-skill --output dist` | Build `paper-alchemist.skill` |
| `validate-skill [PATH]` | Validate the portable Agent Skill bundle |

Section operations:

`abstract` · `introduction` · `related-work` · `problem-definition` · `methodology` · `experiment-setup` · `results-analysis` · `conclusion` · `section`

## Agent support

| Agent | Installed entry point |
|---|---|
| Codex | `$paper-alchemist abstract ...` |
| Claude Code | `/abstract ...` |
| OpenCode | `/abstract ...` |
| Hermes | `/abstract ...` |
| Pi Agent | `/abstract ...` |
| Kimi Code | `/skill:abstract ...` |

See [platform details](paper-alchemist/references/platforms.md) for user/project paths and native behavior.

## Evidence and language contract

Generation applies this priority:

1. target-language module profile;
2. secondary-language module profile;
3. target-language integrated profile;
4. cross-lingual structure profile;
5. factual and academic-writing constraints.

The secondary language contributes rhetorical function and information organization—not translated surface syntax. If either language has no valid evidence, generation continues with an explicit low-confidence, single-language fallback.

Paper Alchemist never invents contributions, methods, datasets, baselines, parameters, results, significance, limitations, or citations. LaTeX uses `\cite{key}`; Markdown uses only the citation convention and keys declared in the context.

For figure/table-heavy PDFs, the corpus may teach how authors introduce, compare, and interpret visual evidence. Numeric values remain research facts: the Agent may use them in generated prose only when they are also present in `paper-context.yaml` or explicitly confirmed by the user. OCR recovers text; it does not infer chart geometry or unlabelled values.

## Repository layout

```text
engine/                      deterministic Python engine source
paper-alchemist/             portable Agent Skill
adapters/                    cross-Agent installation manifest
.github/workflows/           minimal build and compatibility checks
```

The public repository contains only the installable project. Tests, synthetic fixtures, grounded examples, source papers, extracted text, generated profiles, research contexts, and temporary artifacts stay local and are ignored by Git.

## Validation

GitHub Actions checks Python 3.11–3.13 builds, portable Skill structure, packaging, CLI startup, and dry-run installation for all six supported Agents. The full behavioral test suite and research-corpus validation remain local to prevent fixtures, generated profiles, or copyrighted inputs from entering the public project.

## Development

```bash
python -m pip install -e '.[dev]'
ruff check engine
paper-alchemist validate-skill
python -m build
paper-alchemist package-skill --output dist
```

## License

MIT © 2026 [misakimei0331](https://github.com/misakimei0331). See [LICENSE](LICENSE).

If Paper Alchemist helps your research writing, a Star would make this little alchemist smile. ✨
