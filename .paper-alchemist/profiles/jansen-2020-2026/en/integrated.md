---
profile: jansen-2020-2026
language: en
target_weight: 0.7
secondary_language: zh
secondary_weight: 0.3
---
# Integrated EN writing profile

Use module-specific profiles before this integrated fallback. Borrow rhetorical functions from the secondary language, but realize all wording in the target language's academic conventions.

## Module routing

- `abstract`: `en/modules/abstract.md` (5 sources); secondary `zh/modules/abstract.md`.
- `introduction`: `en/modules/introduction.md` (5 sources); secondary `zh/modules/introduction.md`.
- `related-work`: `en/modules/related-work.md` (1 sources); secondary `zh/modules/related-work.md`.
- `problem-definition`: `en/modules/problem-definition.md` (0 sources); secondary `zh/modules/problem-definition.md`.
- `methodology`: `en/modules/methodology.md` (4 sources); secondary `zh/modules/methodology.md`.
- `experiment-setup`: `en/modules/experiment-setup.md` (0 sources); secondary `zh/modules/experiment-setup.md`.
- `results-analysis`: `en/modules/results-analysis.md` (9 sources); secondary `zh/modules/results-analysis.md`.
- `conclusion`: `en/modules/conclusion.md` (3 sources); secondary `zh/modules/conclusion.md`.

## Shared constraints

- Preserve factual grounding from `paper-context.yaml`.
- Use only supplied citation keys.
- Transfer discourse functions, never source-language surface syntax.
- Report a degraded bilingual status when either language lacks evidence.

## Reviewed evidence limits

The corpus is English-only. Chinese guidance is a zero-source fallback, not learned Chinese style. Problem-definition and experiment-setup have no recognized module evidence. Related-work has one source. Automatic routing overcounts usable prose where columns and sections overlap; use module caveats, not seed statistics as writing quotas. Apply aggregate discourse functions, never imitate an author or import study facts into another manuscript.
