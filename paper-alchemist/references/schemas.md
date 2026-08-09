# Data Schemas

## Contents

- Source manifest
- Module profile
- Paper context
- Generation brief
- Confidence

## Source manifest

Each document records its hash, format, detected language, inclusion decision, extraction backend, warnings, and recognized modules. PDF-specific audit fields are:

- `content_mode`: `prose` or `figure-or-table-heavy`;
- `ocr_used`: whether OCR text replaced the text-layer result;
- root-level `ocr_mode`: `auto`, `never`, or `always` for the run.

`figure-or-table-heavy` is descriptive, not an exclusion reason. A visual supplement with enough recovered text but no conventional headings is routed only to `results-analysis`; it is not treated as a complete paper narrative.

## Module profile

Keep this YAML frontmatter:

```yaml
profile: profile-slug
language: en
module: abstract
source_count: 8
visual_source_count: 0
confidence: high
synthesis_status: complete
```

`visual_source_count` reports how many sources in this module are figure/table-heavy. It is normally nonzero only for `results-analysis`; treat those sources as evidence about visual presentation, not as factual evidence for generated claims.

Status values:

- `pending`: deterministic seed exists, but Agent semantic synthesis has not been completed;
- `stale`: the underlying module evidence changed after the last synthesis;
- `complete`: semantic findings match the current module evidence.

Only `complete` profiles may be integrated or used for generation.

Keep these H2 headings exactly:

1. `Rhetorical moves`
2. `Organization`
3. `Language and stance`
4. `Evidence and citations`
5. `Cross-lingual transferable patterns`
6. `Do`
7. `Avoid`
8. `Generation checklist`

## Paper context

Use `assets/paper-context.example.yaml` as the template. The stable top-level fields are:

```yaml
project: {}
research: {}
citations: {}
```

`research` may contain `problem`, `gap`, `contributions`, `method`, `experiments`, `results`, and `limitations`. Preserve numerical values and units exactly. Store citations by citation key; their descriptions provide grounding but do not authorize invented claims.

## Generation brief

The CLI emits:

- target module and secondary module paths;
- target integrated, cross-lingual, and conflict paths;
- target/secondary source counts and 70/30 weights;
- validated context data and missing required fields;
- allowed citation keys;
- `complete` or `degraded-single-language` status.

Treat the brief as a routing artifact, not generated prose.

## Confidence

- `high`: at least eight qualifying sources for the language/module.
- `medium`: three to seven sources.
- `low`: zero to two sources.

Low confidence permits generation but requires a visible caveat. It never permits inventing patterns or facts.
