---
profile: routing-literature
language: zh
module: problem-definition
source_count: 0
visual_source_count: 0
confidence: low
synthesis_status: complete
---
# Problem Definition / 问题定义

> Current semantic synthesis uses completed source observations and per-section learning/check ledgers. Seed metrics are extraction/routing descriptions, not clean prose targets.

## Corpus evidence

- No qualifying samples.

## Quantitative baseline

- paragraphs: 0
- sentences: 0
- average sentence length: 0
- citations: 0
- hedges: 0
- first person markers: 0
- figure mentions: 0
- table mentions: 0


## Rhetorical moves

- 无中文语料（source_count: 0）。本模块不能总结中文修辞顺序；英文所见逻辑只可标为单语功能参考。

## Organization

- 无中文篇章组织证据，不能由英文 PDF 句长/段落数推导中文模板。章节是否存在、顺序和格式以用户稿件及期刊要求为准。

## Language and stance

- 无中文语态、缓和语、人称或术语习惯样本；保留 low confidence。语言能力不等于本语料的中文经验。

## Evidence and citations

- 无中文引文标点、引用位置、定量或图表叙述规范证据。事实与 citation keys 只能来自已确认研究 context。

## Cross-lingual transferable patterns

- 仅迁移英文有来源的高层功能：问题/设计/单位→证据→解释→边界。披露 degraded-single-language，不能制造中文 30% 证据。

## Do

- 明确零来源和低置信度；按实际研究类型、用户目标和出版规范实现中文表层。

## Avoid

- 不制造中文习惯、风格冲突、数字、引用、实验或独立复现；不模仿同一作者。

## Generation checklist

- 检查中文零证据声明、low confidence、事实/引用出处、研究类型匹配、样本重叠和 claim 强度。缺失事实就询问，不以风格语料补足。

## Provenance, confidence and generation boundary

- Expanded input: 47 canonical sources; 46 included (44 empirical/evaluated-system and 2 conceptual/reflection), one unstructured CACM source excluded from module synthesis but retained for learning. Original 10 sources and 70 completed observations unchanged.
- Source counts are publication coverage, not independent replications. Historical Excite/AltaVista/Dogpile logs, retailer campaigns, conference/journal versions and APG development reports overlap. High automatic confidence reflects counts, not diversity or independent evidence strength.
- Predominantly search behavior, sponsored advertising, HCI, persona analytics and digital measurement; not routing optimization/science. Older technologies and sample prevalence are historical, not current defaults.
- Zero Chinese evidence; any functional transfer is degraded-single-language, not an invented Chinese corpus contribution. Use user/journal rules for target-language surface conventions.
- No imported corpus facts, claims, numbers, participant quotes or citation keys for new manuscripts; use confirmed research context. Tables, formulas, font substitutions and residual source metadata require original-PDF checks.
