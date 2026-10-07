---
profile: npj
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

## Reviewed corpus boundary

- Five Judy Gichoya coauthored npj Digital Medicine publications, 2021–2026; not author imitation or journal-wide rules. Two empirical studies, one narrative review, two conceptual/commentary.
- Methods/setup have two sources and low confidence; results-analysis contains two empirical studies plus one narrative synthesis. Proposed agent architecture/evaluation is not conducted experimentation.
- Zero Chinese sources. Use English-supported functions only with degraded-single-language disclosure.
- MinerU VLM still produces malformed numbers, duplicated prose, Box/column interleaving and table continuation artifacts. Canonical inputs remove tables, images, metadata and polluted commentary spans; numerical and visual accuracy unverified.
- See README and manifest for source identity/hash; private locator paths are not included files. Preserve user manuscript facts and citation keys.
