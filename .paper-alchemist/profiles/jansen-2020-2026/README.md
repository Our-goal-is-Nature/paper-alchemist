# Jansen corpus writing profile

Reusable profile: `jansen-2020-2026`. The semantic module files and four integration files are complete. This directory is versioned so a fresh Cyrus worktree can polish without PDFs or extraction caches.

## Coverage and limits

- 10 downloaded English papers; 7 database-marked OA and 3 publicly posted author copies. These are not a claim of exhaustive author coverage.
- Non-review scope includes conceptual research and reflection articles; the 2020 data-driven-personas PDF is labeled Research Article despite a database review tag.
- Two further candidate papers were not downloaded: one failed public link and one lacking a public PDF URL. See `download-audit.json`.
- Automatic module routing: abstract 5, introduction 5, related-work 1, problem-definition 0, methodology 4, experiment-setup 0, results-analysis 9 (4 visual-routed), conclusion 3. These are routing counts, not clean independent prose-example counts.
- Mixed-column PDF extraction includes section spillover, bibliography pollution and a method packet containing author contributions. Semantic guidance excludes these artifacts; seed length/citation statistics are not writing targets.
- No Chinese evidence. Chinese modules explicitly document a low-confidence fallback. English zero-source modules do not invent conventions.
- PDFs and private full-text packets remain server-local and are intentionally not committed. Source hashes and metadata are retained for audit.

## Use

Read the relevant `en/modules/` or `zh/modules/` file, the target `integrated.md`, and both `bilingual/` files. Validate before writing. Preserve all supplied facts, numbers, citation keys and claim strength; the profile supplies writing organization, never research facts. Do not imitate the author.

```sh
paper-alchemist validate-profile --profile jansen-2020-2026 --workspace .
```
