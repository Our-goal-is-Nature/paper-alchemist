# Changelog

All notable changes are documented here.

## [Unreleased]

## [0.3.0] - 2026-09-10

### Changed

- Rebuilt both READMEs around user tasks, moving CI, repository layout, build commands, and raw internal status details out of the onboarding flow.
- Documented and enabled module-by-module drafting, multi-section drafting, and complete paper-draft assembly through the Agent.
- Corrected MIT copyright attribution to `Wang-Ruibin` while retaining `misakimei0331` as the public developer display name in package metadata.
- Replaced the command-heavy quick start with user-facing installation, distillation, readiness, guided research-context, and generation conversations in both README languages.
- Updated the core Skill to translate outcome-oriented requests into the complete workflow and to perform explicitly requested, guarded installation steps.
- Added `generation_ready` and `incomplete_profiles` to profile validation so users and Agents have one unambiguous distillation-completion signal.

## [0.2.3] - 2026-08-09

### Changed

- Renamed the Python source directory from `paper_alchemist/` to `engine/` so it is visually distinct from the `paper-alchemist/` Skill directory.
- Preserved the installed Python import package and CLI name as `paper_alchemist` through an explicit setuptools package mapping.

## [0.2.2] - 2026-08-09

### Changed

- Flattened the source Skill path from `skills/paper-alchemist/` to the root-level `paper-alchemist/` directory.
- Updated source discovery, packaging metadata, validation defaults, documentation, and local tests for the new path.

## [0.2.1] - 2026-08-09

### Changed

- Reduced the public repository and release archives to the installable engine, portable Skill, Agent adapters, essential project metadata, and minimal CI.
- Kept test suites, fixtures, and grounded examples local-only.
- Replaced public pytest execution with build, Skill, CLI, and six-Agent installer smoke checks.

### Removed

- Removed public tests, examples, stage-specific audit documents, and GitHub community templates from the repository and source distribution.

## [0.2.0] - 2026-08-09

### Changed

- Rewrote the public documentation in English and Simplified Chinese.
- Switched the project license from Apache-2.0 to MIT under `misakimei0331`.
- Added an explicit public/local research-data policy and tighter ignore rules.
- Made semantic synthesis completion mandatory before profile integration or drafting.
- Added module fingerprints so corpus updates invalidate only affected semantic profiles.

### Added

- Architecture, contribution, security, and community documentation.
- Validation for pending, stale, integrated, and generation-ready profile states.
- Support for text-bearing figure/table-heavy PDFs instead of excluding them by prose density.
- Optional `auto`, `never`, and `always` PDF OCR modes backed by `pdftoppm` and Tesseract.
- Figure/table reference statistics in module seeds, observations, and quality reports.

## [0.1.0] - 2026-08-05

- Initial public release with modular bilingual distillation, grounded generation briefs, six Agent adapters, tests, and release packaging.

[Unreleased]: https://github.com/Wang-Ruibin/paper-alchemist/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/Wang-Ruibin/paper-alchemist/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/Wang-Ruibin/paper-alchemist/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/Wang-Ruibin/paper-alchemist/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/Wang-Ruibin/paper-alchemist/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/Wang-Ruibin/paper-alchemist/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Wang-Ruibin/paper-alchemist/releases/tag/v0.1.0
