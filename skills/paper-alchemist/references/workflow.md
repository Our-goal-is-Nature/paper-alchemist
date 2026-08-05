# Corpus Distillation Workflow

## Contents

- Prepare the corpus
- Review private packets
- Complete module profiles
- Integrate bilingual profiles
- Update an existing profile
- Privacy and failure handling

## Prepare the corpus

Run from the research project where `.paper-alchemist/` should live:

```bash
paper-alchemist distill <paper-folder> --profile <name> --language auto
```

Use `--language en` or `--language zh` only when the user explicitly wants to override detection. Use `--update` only for an existing profile the user asked to refresh.

Read the JSON result and inspect `.paper-alchemist/profiles/<name>/source-manifest.json`. Report excluded files and their reasons. Do not claim that scanned or low-text PDFs were distilled.

The command creates:

- private extracted text and batch packets under `.paper-alchemist/cache/<name>/`;
- deterministic seed profiles under `.paper-alchemist/profiles/<name>/<lang>/modules/`;
- source and quality manifests under `.paper-alchemist/profiles/<name>/`.

## Review private packets

Process one language and module at a time. Read packet files under:

`.paper-alchemist/cache/<name>/packets/<lang>/<module>/batch-*.md`

For each packet, record only aggregate observations:

- rhetorical moves and their typical order;
- paragraph roles and transitions;
- stance, voice, tense, hedging, and claim strength;
- citation and quantitative-evidence placement;
- module-specific comparison or analysis patterns;
- reusable checks and failure modes.

Do not create phrase banks from the papers. Do not quote long passages. Treat filenames as evidence labels, not as author personas.

## Complete module profiles

Edit `.paper-alchemist/profiles/<name>/<lang>/modules/<module>.md` using the quantitative `.seed.md` file as evidence. Preserve YAML fields and every required H2 heading listed in [schemas.md](schemas.md).

Replace all `Pending Agent synthesis` markers with corpus-level findings. Set:

`synthesis_status: complete`

Keep claims proportional to `source_count` and `confidence`. For fewer than three sources, label findings tentative. When sources disagree, describe the variation instead of forcing a false rule.

Complete all eight modules for both languages. A zero-source module must remain low-confidence and explicitly state that no corpus evidence is available.

## Integrate bilingual profiles

After module profiles are complete, run:

```bash
paper-alchemist integrate --profile <name>
paper-alchemist validate-profile --profile <name>
```

Review and refine the generated files:

- `en/integrated.md`
- `zh/integrated.md`
- `bilingual/cross-lingual.md`
- `bilingual/conflicts.md`

Align only high-level functions across languages. Keep target-language surface conventions dominant. Preserve conflict notes when English and Chinese corpora favor different paragraph lengths, voice, directness, or citation placement.

## Update an existing profile

Run `distill ... --update`. Unchanged documents reuse cached extraction. Changed and new documents are reprocessed. Read `semantic_refresh_required` in the command result and re-synthesize those module profiles before integration.

Never overwrite a completed semantic profile with a quantitative seed without reviewing it.

## Privacy and failure handling

- Keep `.paper-alchemist/cache/` out of version control.
- Do not copy source papers into the profile or skill.
- Stop and report password-protected, corrupt, scanned, or unsupported files.
- If extraction yields fewer than two recognizable paper modules, exclude the file as insufficient structure.
- If one corpus language is missing, finish the available language and mark bilingual integration as degraded.
