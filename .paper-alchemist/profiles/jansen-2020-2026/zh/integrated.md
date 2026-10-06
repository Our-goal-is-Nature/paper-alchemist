---
profile: jansen-2020-2026
language: zh
target_weight: 0.7
secondary_language: en
secondary_weight: 0.3
---
# Integrated ZH writing profile

Use module-specific profiles before this integrated fallback. Borrow rhetorical functions from the secondary language, but realize all wording in the target language's academic conventions.

## Module routing

- `abstract`: `zh/modules/abstract.md` (0 sources); secondary `en/modules/abstract.md`.
- `introduction`: `zh/modules/introduction.md` (0 sources); secondary `en/modules/introduction.md`.
- `related-work`: `zh/modules/related-work.md` (0 sources); secondary `en/modules/related-work.md`.
- `problem-definition`: `zh/modules/problem-definition.md` (0 sources); secondary `en/modules/problem-definition.md`.
- `methodology`: `zh/modules/methodology.md` (0 sources); secondary `en/modules/methodology.md`.
- `experiment-setup`: `zh/modules/experiment-setup.md` (0 sources); secondary `en/modules/experiment-setup.md`.
- `results-analysis`: `zh/modules/results-analysis.md` (0 sources); secondary `en/modules/results-analysis.md`.
- `conclusion`: `zh/modules/conclusion.md` (0 sources); secondary `en/modules/conclusion.md`.

## Shared constraints

- Preserve factual grounding from `paper-context.yaml`.
- Use only supplied citation keys.
- Transfer discourse functions, never source-language surface syntax.
- Report a degraded bilingual status when either language lacks evidence.

## Reviewed evidence limits

The corpus is English-only. Chinese guidance is a zero-source fallback, not learned Chinese style. Problem-definition and experiment-setup have no recognized module evidence. Related-work has one source. Automatic routing overcounts usable prose where columns and sections overlap; use module caveats, not seed statistics as writing quotas. Apply aggregate discourse functions, never imitate an author or import study facts into another manuscript.
