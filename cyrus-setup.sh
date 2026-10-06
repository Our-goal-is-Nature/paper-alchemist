#!/usr/bin/env bash
# 每个议题工作区开工时运行。确认 skill 和命令都在，不下载论文。
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"

test -f .claude/skills/paper-alchemist/SKILL.md
test -x .claude/skills/paper-alchemist/scripts/run.py
command -v paper-alchemist
paper-alchemist --version
paper-alchemist validate-skill .claude/skills/paper-alchemist
echo "paper-alchemist ready for ${LINEAR_ISSUE_IDENTIFIER:-unknown}"
