# Architecture

Paper Alchemist deliberately separates deterministic processing from Agent judgment.

```text
paper corpus
    |
    v
local extraction -> canonical sections -> language-specific private packets
                                              |
                                              v
                                    Agent semantic synthesis
                                              |
                     +------------------------+------------------------+
                     v                        v                        v
               English modules         Chinese modules        quality metadata
                     +------------------------+------------------------+
                                              |
                                              v
                                  cross-lingual integration
                                              |
verified paper-context.yaml ------------------+----> grounded drafting brief
```

## Deterministic layer

The `paper_alchemist` Python package owns operations that should be reproducible:

- recursive discovery and format-specific extraction;
- SHA-256 cache identity and interruption recovery;
- language detection and canonical section recognition;
- descriptive statistics, manifests, confidence, and schema validation;
- installation adapters and release packaging.

It does not call a language-model API and does not author semantic style findings.

## Agent layer

The active Agent owns tasks that require interpretation:

- comparing evidence across papers;
- extracting recurring rhetorical and organizational patterns;
- resolving bilingual similarities and conflicts;
- asking for missing research facts;
- drafting and checking the requested section.

Semantic module profiles carry a `synthesis_status`. Quantitative seeds are `pending`; changed evidence marks completed profiles `stale`. Integration and generation accept only `complete` profiles.

## Data boundary

Corpus text is read from `.paper-alchemist/cache/` only while distilling. Public profiles contain aggregate observations and counts rather than source passages. Research facts enter generation exclusively through `paper-context.yaml` and explicit user answers.

See [repository-policy.md](repository-policy.md) for the version-control boundary.
