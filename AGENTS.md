# Cyrus paper polishing

For polishing, read `.claude/skills/paper-alchemist/SKILL.md` and use default profile `routing-literature` in `.paper-alchemist/profiles/routing-literature/`. The reusable bundle is tracked in `profiles/routing-literature/`; `cyrus-setup.sh` installs it into the ignored workspace state without overwriting an existing profile. If the workspace profile is missing, run `bash cyrus-setup.sh` and stop if setup fails. Do not re-distill or require original PDFs merely to polish a draft.

- Read the profile README, relevant language/module file, target integrated file and bilingual transfer/conflict notes.
- Run `paper-alchemist validate-profile --profile routing-literature --workspace .`; require `generation_ready: true`.
- Preserve manuscript facts, numbers, citation keys and claim strength. Writing examples never authorize importing research facts or imitating an author.
- For generation follow the skill context/brief workflow. For polishing do not require the user to author YAML just to edit wording.
- Disclose English-only evidence and low-confidence/zero-source modules. Source counts are automatic section routing counts with known extraction limitations, not independent replications or certified clean prose counts.
- The bundle covers 47 sources, 46 included, principally Web search/IR, advertising, HCI and persona analytics. Its name does not establish routing-optimization expertise. It guides writing, not factual peer-review judgments; flag unverified scientific claims instead of treating corpus patterns as evidence.

Linear: include `[repo=paper-alchemist]` and `[agent=claude]` for the installed Claude adapter. Default Cursor does not imply automatic loading of Claude skills; an Agent honoring AGENTS.md can explicitly read this portable skill.

Completed reusable profiles and sanitized provenance are tracked on main under `profiles/`. PDFs, extracted full text, observations and `.paper-alchemist/` remain ignored and are unnecessary for reuse. Existing local profiles, including `jansen-2020-2026`, are private state; do not delete or overwrite them. Do not overwrite installations or install Python/PDF/OCR tools without permission.
