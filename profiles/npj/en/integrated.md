---
profile: npj
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
- `related-work`: `en/modules/related-work.md` (5 sources); secondary `zh/modules/related-work.md`.
- `problem-definition`: `en/modules/problem-definition.md` (5 sources); secondary `zh/modules/problem-definition.md`.
- `methodology`: `en/modules/methodology.md` (2 sources); secondary `zh/modules/methodology.md`.
- `experiment-setup`: `en/modules/experiment-setup.md` (2 sources); secondary `zh/modules/experiment-setup.md`.
- `results-analysis`: `en/modules/results-analysis.md` (3 sources); secondary `zh/modules/results-analysis.md`.
- `conclusion`: `en/modules/conclusion.md` (5 sources); secondary `zh/modules/conclusion.md`.

## Shared constraints

- Preserve factual grounding from `paper-context.yaml`.
- Use only supplied citation keys.
- Transfer discourse functions, never source-language surface syntax.
- Report a degraded bilingual status when either language lacks evidence.

## Reviewed corpus boundary

- Five Judy Gichoya coauthored npj Digital Medicine publications, 2021–2026; not author imitation or journal-wide rules. Two empirical studies, one narrative review, two conceptual/commentary.
- Methods/setup have two sources and low confidence; results-analysis contains two empirical studies plus one narrative synthesis. Proposed agent architecture/evaluation is not conducted experimentation.
- Zero Chinese sources. Use English-supported functions only with degraded-single-language disclosure.
- MinerU VLM still produces malformed numbers, duplicated prose, Box/column interleaving and table continuation artifacts. Canonical inputs remove tables, images, metadata and polluted commentary spans; numerical and visual accuracy unverified.
- See README and manifest for source identity/hash; private locator paths are not included files. Preserve user manuscript facts and citation keys.
