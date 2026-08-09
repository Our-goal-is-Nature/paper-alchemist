# Public repository and local research boundary

This project is open source; the papers and research projects processed with it usually are not. Keep code reviewable while treating research data as private by default.

## Publish these

| Path | Why it is public |
|---|---|
| `paper_alchemist/` | Deterministic engine source |
| `skills/paper-alchemist/` | Portable Agent Skill and its required resources |
| `adapters/` | Cross-Agent compatibility manifest |
| `tests/fixtures/` | Small, original, synthetic bilingual papers and contexts |
| `examples/` | Original outputs grounded in synthetic context |
| `docs/` | Architecture, privacy, and contribution guidance |
| `.github/` | CI and community templates |
| `README*`, `LICENSE`, `CHANGELOG.md` | Public project documentation and terms |

## Keep these local

| Path or content | Reason |
|---|---|
| `.paper-alchemist/cache/` | Contains extracted source text and private packets |
| `.paper-alchemist/profiles/` | May reveal corpus names, domain patterns, and local paths |
| `paper-context.yaml` | Contains unpublished claims, results, citations, and environment details |
| `papers/`, `corpus/`, `*.pdf` | Copyrighted or licensed source material |
| `.env*` | May contain credentials or machine-specific settings |
| `test-artifacts/`, `scratch/`, `*.local.md` | Disposable or private development notes |
| real-paper output samples | May leak unpublished facts or recognizable source wording |

These paths are covered by `.gitignore`, but ignore rules are not a security boundary. Before every commit, inspect `git status` and the staged diff. Never force-add private research files.

## Safe public fixtures

Fixtures and examples must be original, minimal, and clearly synthetic. They may demonstrate a citation key or numerical result only when that value also appears in the committed synthetic context file. Do not anonymize a real paper and call it synthetic; write a new fixture from scratch.

## Profile sharing

Generated profiles are local by default. Share one only when all source licenses and research policies permit it, absolute paths and identifying filenames have been removed, and the profile has been checked for long or distinctive source phrases.
