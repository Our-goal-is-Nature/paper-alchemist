---
name: paper-alchemist
description: Distill corpus-level academic writing patterns from folders of English and Chinese PDF, LaTeX, DOCX, Markdown, or text papers; integrate module-specific bilingual profiles; and draft grounded abstracts, introductions, related work, problem definitions, methodologies, experiment setups, results analyses, conclusions, or custom sections. Use when an Agent must analyze how a paper corpus writes, build or update a reusable style profile, or generate a paper section from verified research facts without imitating one author or inventing evidence.
---

# Paper Alchemist

Use a deterministic local CLI for extraction and validation. Perform semantic distillation and drafting as the active Agent. Never call an LLM API from the bundled scripts.

## Choose the operation

- For `distill`, read [references/workflow.md](references/workflow.md) and execute the complete corpus workflow.
- For `integrate`, validate completed module profiles, then run the integration workflow in [references/workflow.md](references/workflow.md).
- For `abstract`, `introduction`, `related-work`, `problem-definition`, `methodology`, `experiment-setup`, `results-analysis`, `conclusion`, or `section`, read [references/generation.md](references/generation.md).
- For profile and context file fields, read [references/schemas.md](references/schemas.md).
- For installation and platform-native invocation, read [references/platforms.md](references/platforms.md).

## Run the local CLI

Prefer the installed command:

```bash
paper-alchemist --version
```

If the command is unavailable in a cloned repository, run:

```bash
python -m paper_alchemist.cli --version
```

Do not silently install dependencies. Explain that the user must run `python -m pip install -e .` from the repository, then retry.

## Preserve the bilingual contract

Keep English and Chinese evidence separate during extraction and module distillation. During generation, use both languages:

1. Apply the target-language module profile at approximately 70% influence.
2. Apply the secondary-language module profile at approximately 30% influence.
3. Transfer rhetorical functions and organization across languages.
4. Keep grammar, wording, terminology, voice, and citation punctuation under the target-language profile.
5. Continue with a clearly reported degraded status if either language lacks evidence.

## Enforce evidence boundaries

- Use the corpus only to infer aggregate writing patterns. Do not copy long source passages or imitate a single author.
- Use `paper-context.yaml` and explicit user answers as the only sources of research facts.
- Ask only for module-required missing facts before drafting.
- Never invent contributions, methods, datasets, baselines, parameter values, numerical results, statistical significance, limitations, or citations.
- Use only citation keys listed in the context file or supplied explicitly by the user.
- Return content in chat by default. Write a file only when the user explicitly provides an output path.

## Validate completion

- Run `paper-alchemist validate-profile --profile <name>` after distillation or integration.
- Confirm every used profile path and source count from the generation brief.
- Report target language, secondary language, bilingual status, output format, and any missing or degraded evidence with the result.
