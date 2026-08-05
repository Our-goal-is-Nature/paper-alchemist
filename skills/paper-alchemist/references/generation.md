# Grounded Bilingual Section Generation

## Contents

- Build the generation brief
- Fill missing research facts
- Blend bilingual profiles
- Draft the module
- Validate the output

## Build the generation brief

Run:

```bash
paper-alchemist brief <module> \
  --profile <name> \
  --language <en|zh> \
  --format <latex|markdown> \
  --context <paper-context.yaml>
```

For a custom section, use module `section` and add `--section-name <name>`.

Read every path in `profile_files`. Use the target module first, the secondary-language module second, the target integrated profile third, and the cross-lingual profile fourth. Consult `conflicts.md` before choosing surface wording.

## Fill missing research facts

Inspect `missing_context_fields` in the brief. If it is non-empty, ask the user only for those facts. Accept answers interactively and treat them as an in-session extension of the context file. Do not draft until the required facts are available.

Never infer a research result from a style corpus. The corpus answers “how to write”; the context answers “what is true.”

## Blend bilingual profiles

- Use approximately 70% target-language and 30% secondary-language influence.
- Borrow problem framing, gap placement, contribution ordering, experiment logic, comparison structure, and conclusion closure from either language.
- Do not translate distinctive source sentences.
- Realize all syntax, terminology, tense, voice, punctuation, and citation placement naturally in the target language.
- If either source count is zero, use the available profile and label the result `degraded-single-language`.

## Draft the module

Apply the selected module contract:

- `abstract`: problem, gap, method, main evidence, contribution; do not add citations unless the context and venue practice require them.
- `introduction`: importance, precise gap, research response, contributions, and optional paper organization.
- `related-work`: organize cited work by approach or limitation; connect the comparison to the verified gap.
- `problem-definition`: define entities, assumptions, decisions, constraints, and objective without adding unstated assumptions.
- `methodology`: explain design rationale before procedural detail; connect components to the verified problem.
- `experiment-setup`: state datasets or instances, baselines, metrics, parameters, hardware, seeds, and stopping rules only when supplied.
- `results-analysis`: report result, comparison, magnitude, uncertainty or test, explanation, and implication; distinguish observation from interpretation.
- `conclusion`: answer the research problem, summarize verified evidence, state supplied limitations, and avoid unsupported future work.
- `section`: follow the user-provided section purpose while applying the same evidence boundaries.

Use `\cite{key}` for LaTeX and the supplied citation convention for Markdown. Never use a key absent from `allowed_citation_keys`.

## Validate the output

Before returning:

1. Match every factual sentence to the context or an explicit user answer.
2. Match every citation to `allowed_citation_keys`.
3. Remove source-like phrasing and single-author imitation.
4. Confirm target-language fluency and module structure.
5. State which profile languages were used and whether blending degraded.
6. Return in chat unless the user explicitly supplied `out`; write only to that exact path.
