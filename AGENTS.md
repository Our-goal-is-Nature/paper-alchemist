# Cyrus paper polishing

For polishing, read `.claude/skills/paper-alchemist/SKILL.md` and use default profile `jansen-2020-2026` in `.paper-alchemist/profiles/jansen-2020-2026/`. Do not re-distill or require original PDFs merely to polish a draft.

- Read the profile README, relevant language/module file, target integrated file and bilingual transfer/conflict notes.
- Run `paper-alchemist validate-profile --profile jansen-2020-2026 --workspace .`; require `generation_ready: true`.
- Preserve manuscript facts, numbers, citation keys and claim strength. Writing examples never authorize importing research facts or imitating an author.
- For generation follow the skill context/brief workflow. For polishing do not require the user to author YAML just to edit wording.
- Disclose English-only evidence and low-confidence/zero-source modules. Source counts are automatic routing counts with known section spillover, not clean prose counts.

Linear: include `[repo=paper-alchemist]` and `[agent=claude]` for the installed Claude adapter. Default Cursor does not imply automatic loading of Claude skills; an Agent honoring AGENTS.md can explicitly read this portable skill.

Completed profiles and provenance are tracked on main. PDFs and extracted full-text caches remain ignored and are unnecessary for reuse. Do not overwrite installations or install Python/PDF/OCR tools without permission.
