---
name: paper-alchemist
description: Distill corpus-level academic writing patterns from folders of English and Chinese PDF, LaTeX, DOCX, Markdown, or text papers; integrate module-specific bilingual profiles; and draft grounded abstracts, introductions, related work, problem definitions, methodologies, experiment setups, results analyses, conclusions, custom sections, or complete multi-section papers. Use when an Agent must analyze how a paper corpus writes, build or update a reusable style profile, or generate paper content from verified research facts without imitating one author or inventing evidence.
---

# Paper Alchemist

Use a deterministic local CLI for extraction and validation. Perform semantic distillation and drafting as the active Agent. Never call an LLM API from the bundled scripts.

## Lead with the user's outcome

- Accept natural-language requests for installation, corpus profiling, integration, validation, and drafting. Infer command arguments from paths and outcomes the user provides; ask only for choices that materially change the result.
- When the user requests an end-to-end task, carry it through extraction, semantic distillation, integration, validation, and drafting as far as the available evidence allows. Do not make the user relay intermediate CLI commands.
- When the user requests several sections or a complete paper, build and apply the matching module brief to each section separately, then assemble the requested deliverable with consistent terminology, contributions, numbers, and citations. Do not replace module-specific generation with one undifferentiated prompt.
- For a distillation request, extraction and seed creation are only intermediate results. Say that distillation is complete only after semantic synthesis and integration finish and `validate-profile` returns `generation_ready: true`.
- Translate internal status into user outcomes. Lead with “the profile is ready for writing” or “the profile still needs work,” then explain included or excluded papers, limitations, and any action the user must take. Show raw fields or commands only when the user asks, when they are useful for reproducibility or troubleshooting, or when the user must run something the Agent cannot execute.
- Infer the current Agent adapter when it is evident from the runtime. Do not ask the user to choose from adapter identifiers merely to reproduce the CLI interface.

## Choose the operation

- For `distill`, read [references/workflow.md](references/workflow.md) and execute the complete corpus workflow.
- For `integrate`, validate completed module profiles, then run the integration workflow in [references/workflow.md](references/workflow.md).
- For `abstract`, `introduction`, `related-work`, `problem-definition`, `methodology`, `experiment-setup`, `results-analysis`, `conclusion`, or `section`, read [references/generation.md](references/generation.md).
- For multiple sections or a complete draft, read [references/generation.md](references/generation.md) and follow its multi-section orchestration rules.
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

When the user explicitly asks for installation, you may clone the repository, create an isolated Python application environment, install the Python package, and install the matching Agent adapter. Ensure the `paper-alchemist` command remains discoverable in future sessions; do not rely on a shell-local virtual-environment activation. Follow the runtime's permission model, do not overwrite an existing installation without explicit confirmation, and ask before installing or upgrading Python or optional system tools such as `pdftotext`, `pdftoppm`, Tesseract, or OCR language data. If installation was not requested, explain the missing prerequisite and provide or offer the smallest applicable setup step instead of changing the environment.

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
- If the user has no context file, do not make them author YAML manually. Read user-supplied drafts, notes, tables, and bibliography files when available; otherwise conduct a short guided interview. Collect only module-required facts, ask in small groups, distinguish missing or ambiguous claims, and present a fact checklist for confirmation before writing a user-requested context path.
- Ask only for module-required missing facts before drafting. Never turn an unknown answer into a guessed value.
- Never invent contributions, methods, datasets, baselines, parameter values, numerical results, statistical significance, limitations, or citations.
- Use only citation keys listed in the context file or supplied explicitly by the user.
- Return content in chat by default. Write a file only when the user explicitly provides an output path.

## Validate completion

- Run `paper-alchemist validate-profile --profile <name>` after distillation or integration.
- Treat `pending` and `stale` module profiles as incomplete. Never bypass the integration or generation gate.
- If `generation_ready` is false, use `incomplete_profiles` and `errors` internally to continue any work that can be completed safely. Tell the user only what remains, why the Agent cannot continue, or what user action is required; never describe the profile as ready for generation.
- Confirm every used profile path and source count from the generation brief.
- At completion, clearly say that the named profile is ready for writing and summarize source coverage, exclusions, warnings, and degraded evidence in plain language. Include raw validation values only for troubleshooting or on request. For drafted content, also report target language, secondary language, bilingual status, and output format.
