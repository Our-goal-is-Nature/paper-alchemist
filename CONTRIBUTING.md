# Contributing

Thank you for improving Paper Alchemist.

## Before opening a change

1. Search existing issues and pull requests.
2. Keep one change focused on one problem.
3. Do not commit papers, extracted text, generated profiles, private contexts, credentials, or real research outputs.
4. Add or update original fixtures for behavior changes.
5. Preserve the separation between deterministic Python work and Agent semantic judgment.

## Development

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
ruff check .
pytest
python -m build
paper-alchemist package-skill --output dist
```

Changes to `skills/paper-alchemist/` must keep `SKILL.md` concise, use only `name` and `description` in its frontmatter, and preserve progressive disclosure through `references/`, `scripts/`, and `assets/`.

## Pull requests

Explain the user-facing problem, the chosen behavior, privacy implications, and validation performed. If an Agent adapter changes, identify the platform documentation or runtime version used to verify it.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
