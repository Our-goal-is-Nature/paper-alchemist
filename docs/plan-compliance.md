# Original plan compliance

This audit maps the implementation to the approved Paper Alchemist plan. Later user decisions take precedence over earlier defaults.

| Requirement | Status | Evidence or note |
|---|---|---|
| Public `paper-alchemist` repository | Complete | Public source layout, CI, packaging, community files, and repository links are present. |
| Apache-2.0 license | Superseded | The later request selected MIT under `misakimei0331`; released Apache-licensed copies remain under their original terms. |
| Open Agent Skills core | Complete | `skills/paper-alchemist/SKILL.md` uses portable minimal frontmatter and is checked by `validate-skill`. |
| Codex, Claude Code, OpenCode, Hermes, Pi Agent, and Kimi Code | Complete | The installer and `adapters/manifest.json` generate platform-native entry points. |
| Python for deterministic processing; Agent for semantic work | Complete | Extraction, sectioning, statistics, state, validation, and packaging are deterministic; no LLM API is called. |
| Separate English and Chinese distillation | Complete | Module evidence, observations, seeds, semantic profiles, and integrations are language-scoped. |
| Both languages influence generation | Complete | Generation briefs route target and secondary module profiles at approximately 70/30 and report fallback status. |
| Modular paper sections | Complete | Eight canonical modules plus custom `section` are supported. |
| Recursive PDF, LaTeX, DOCX, Markdown, and TXT discovery | Complete | Format-specific discovery and extractors are covered by tests. |
| Figure/table-heavy PDFs excluded | Superseded | The later request requires support. Such PDFs are retained when text is sufficient and routed to `results-analysis` when conventional sections are absent; optional OCR handles low-text pages. |
| References and appendices excluded | Complete | Section recognition stops before reference and appendix content. |
| Per-paper, per-module observations | Complete | Private observation records are generated under `.paper-alchemist/cache/<profile>/observations/`. |
| Batch synthesis and resumable updates | Complete | Private packets, SHA-256 caches, module fingerprints, stale-state invalidation, and interrupted-run recovery are implemented. |
| Source coverage, anomalies, and confidence | Complete | `source-manifest.json` and `quality.json` expose inclusion reasons, warnings, coverage, module samples, and confidence. |
| Chinese, English, cross-lingual, and conflict profiles | Complete | Integration produces all four artifacts and refuses pending, stale, missing, or invalid semantic modules. |
| Grounded context and citation keys | Complete | The generation brief reports missing section facts and restricts citations to declared keys. |
| Default chat output; file output only with `out` | Complete | Agent instructions and CLI brief routing preserve this rule. |
| LaTeX and Markdown generation | Complete | Both formats are supported and represented by grounded bilingual examples. |
| Public/local data boundary | Complete | Papers, caches, profiles, local context, real outputs, and secrets are ignored and documented as local-only. |
| Unit and integration tests | Complete | Tests cover bilingual sectioning, profiles, updates, fallback, grounding, overlap, installers, packaging, Skill validation, and PDF/OCR behavior. |
| Real English corpus validation | Complete with caveat | The specified directory has grown from the original 25-PDF plus one-LaTeX corpus to 41 candidates. The latest local run included 29 sources, including seven visual PDFs, without committing papers or generated profiles. One low-text PDF transparently reported missing Tesseract. |
| Real Chinese corpus quality validation | Pending external corpus | Synthetic Chinese behavior is tested; domain-level Chinese style quality still requires a suitable real Chinese corpus, as anticipated by the plan. |
| `paper-alchemist.skill` release artifact | Complete | The archive is reproducibly built and checked to contain only the portable Skill bundle. |

## Figure/table support boundary

Paper Alchemist extracts textual captions, labels, table text, and prose references from the PDF text layer. `--ocr auto` attempts OCR for low-text PDFs; `--ocr always` can recover more image-contained text; `--ocr never` disables OCR. OCR requires `pdftoppm` and Tesseract and records both tool failures and actual use in the manifest.

The distillation corpus may teach rhetorical patterns for presenting visual evidence. It is never a factual source for generated results: chart values, table values, identifiers, comparisons, and interpretations must still be present in `paper-context.yaml` or explicitly supplied by the user.
