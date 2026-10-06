---
profile: jansen-2020-2026
language: en
module: methodology
source_count: 4
visual_source_count: 0
confidence: medium
synthesis_status: complete
---

# methodology

## Corpus evidence

- `2021-10-1016-j-eswa-2021-115611.pdf` (prose)
- `2022-10-1371-journal-pone-0268212.pdf` (prose)
- `2023-10-1007-s10796-023-10395-5.pdf` (prose)
- `2025-10-1145-3750069-3750390.pdf` (prose)


## Extraction caveat

Automatic section counts are routing diagnostics, not verified prose counts. Mixed columns and section spillover were manually reviewed; do not impose the seed statistics as style quotas.

## Rhetorical moves

Describe data provenance and aggregation, introduce the analysis pipeline, define representations and measures, justify comparison baselines, and explain the evaluation procedure.

## Organization

Use process-oriented subsections. The longitudinal study proceeds through collection, persona generation, topical-interest calculation and temporal overlap metrics; the hyperparameter study fixes data and algorithm while varying persona-set size.

## Language and stance

Use explicit actor/action descriptions for operations, definitions for symbols and units, and qualified justification for a constructed baseline. A methodological convenience is not automatically ground truth.

## Evidence and citations

Cite established algorithms rather than re-derive all prior work. Define matrix dimensions and metric denominators. Explain why a statistical procedure is chosen, as in the non-normality justification for the Wilcoxon test.

## Cross-lingual transferable patterns

Transfer reproducibility and definition order, not specific algorithms or parameters. Chinese module evidence is absent.

## Do

Keep collection, transformation, model, comparison and test decisions recoverable. Separate qualitative thematic coding from quantitative statistical testing.

## Avoid

Ignore the PLOS author-contribution fragment as method evidence. Do not use contaminated packet counts as paragraph or sentence targets; do not silently strengthen an approximate baseline.

## Generation checklist

Are units, sampling, baseline rationale, controlled variables and evaluation stated in the source draft? Flag omissions instead of inventing them.
