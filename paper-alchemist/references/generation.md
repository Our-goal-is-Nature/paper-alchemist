# Grounded Bilingual Section Generation

## Contents

- Build or confirm the research context
- Build the generation brief
- Fill missing research facts
- Blend bilingual profiles
- Draft the module
- Validate the output

## Build or confirm the research context

Do not require the user to hand-author YAML. If a usable context file was not supplied, help build one in either of these ways:

1. Read user-named drafts, experiment notes, result tables, and bibliography files. Extract only facts explicitly supported by those materials and keep uncertain or conflicting statements unresolved.
2. If those materials are unavailable or incomplete, interview the user in small groups of easy-to-answer questions.

Determine the requested writing module before collecting facts, then prioritize only its requirements. For example, an abstract needs the problem, gap, method, contributions, and results; a methodology section needs the method; results analysis needs the experiments and results. Optional project metadata may be collected when useful, but do not turn context setup into a requirement to complete every template field.

Before writing a user-requested context path:

- summarize the facts that will be recorded and their supplied source;
- list missing, ambiguous, or contradictory items separately;
- show exact numerical values and units without normalization or reinterpretation;
- list allowed citation keys and what each key may support;
- ask the user to confirm or correct the checklist.

After confirmation, use `assets/paper-context.example.yaml` as the field-shape guide and write only to the exact path the user requested. Keep the file out of version control. When the profile is ready, build the generation brief and use `missing_context_fields` as an internal checklist; ask the user only about remaining facts instead of exposing schema field names unless troubleshooting.

The style corpus never supplies research facts. Do not infer a contribution, result, comparison, significance claim, limitation, or citation authorization from the distilled profile.

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

If the CLI reports an incomplete semantic profile or missing integration artifact, stop. Finish distillation and integration before asking the user for research facts or drafting prose.

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

When profiles include figure/table patterns, transfer only their rhetorical function: how a visual is introduced, what comparison is foregrounded, and how observations are separated from explanations. Use a figure number, table number, caption claim, or numeric value only when it appears in the verified context or the user explicitly supplies it. Never estimate a value from chart pixels.

## Validate the output

Before returning:

1. Match every factual sentence to the context or an explicit user answer.
2. Match every citation to `allowed_citation_keys`.
3. Remove source-like phrasing and single-author imitation.
4. Confirm target-language fluency and module structure.
5. State which profile languages were used and whether blending degraded.
6. Return in chat unless the user explicitly supplied `out`; write only to that exact path.
