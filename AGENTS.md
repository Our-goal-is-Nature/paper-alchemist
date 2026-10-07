# Cyrus paper polishing

For polishing, read `.claude/skills/paper-alchemist/SKILL.md` and use default profile IPM (canonical CLI slug and metadata: `ipm`) in `.paper-alchemist/profiles/ipm/`. The reusable bundle is tracked in `profiles/ipm/`; `cyrus-setup.sh` installs each manifest-bearing public profile into the ignored workspace state using an isolated copy validated before rename, without overwriting existing local profiles.

## Profile selection and gating

- If the user explicitly selects a profile (e.g. `npj` or a private local profile), honor that explicit choice: run `bash cyrus-setup.sh <selected>` and gate on `paper-alchemist validate-profile --profile <selected_slug> --workspace .`. The selected profile must report `generation_ready: true`. If setup fails or `generation_ready: true` is not met, STOP immediately and report the failure; do NOT silently fall back to IPM or substitute any other profile.
- If no profile is specified, default to IPM: run `bash cyrus-setup.sh IPM` (or `bash cyrus-setup.sh`), gate on `paper-alchemist validate-profile --profile ipm --workspace .`, and require `generation_ready: true`. Stop if setup or validation fails.
- Do not re-distill or require original PDFs merely to polish a draft.

## Polishing rules and corpus boundaries

- Read the selected profile README, relevant language/module file, target integrated file, and bilingual transfer/conflict notes.
- Preserve manuscript facts, numbers, citation keys, and claim strength. Writing examples never authorize importing research facts or imitating an author.
- For generation follow the skill context/brief workflow. For polishing do not require the user to author YAML just to edit wording.
- Disclose English-only evidence and low-confidence/zero-source modules. Source counts are automatic section routing counts with known extraction limitations, not independent replications or certified clean prose counts.
- The IPM bundle covers 47 sources, 46 included (1998–2026), principally Web search/IR, advertising, HCI, persona analytics, and digital measurement (the Jansen corpus). The display name IPM does not denote an IPM-exclusive corpus or certified journal rules, nor does it establish routing-optimization expertise. It was NOT re-parsed with MinerU; existing extraction limitations remain. All Chinese modules have zero direct evidence and low confidence. It guides writing style and rhetoric, not factual peer-review judgments; flag unverified scientific claims instead of treating corpus patterns as evidence.

## System instructions

Linear: include `[repo=paper-alchemist]` and `[agent=claude]` for the installed Claude adapter. Default Cursor does not imply automatic loading of Claude skills; an Agent honoring AGENTS.md can explicitly read this portable skill.

Completed reusable profiles and sanitized provenance are tracked on main under `profiles/`. PDFs, extracted full text, observations, research materials, and `.paper-alchemist/` remain ignored and are unnecessary for reuse. Existing local profiles, including `jansen-2020-2026` and the previous `routing-literature`, are private state; do not delete, alter, or overwrite them. Do not alter any `.paper-alchemist` private data or `npj` files. Do not overwrite installations or install Python/PDF/OCR tools without permission.
