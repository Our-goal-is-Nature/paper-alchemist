#!/usr/bin/env bash
# 每个议题工作区开工时运行。确认 skill 和命令都在，不下载论文。
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"

test -f .claude/skills/paper-alchemist/SKILL.md
test -x .claude/skills/paper-alchemist/scripts/run.py
command -v paper-alchemist
paper-alchemist --version
paper-alchemist validate-skill .claude/skills/paper-alchemist
python3 .claude/skills/paper-alchemist/scripts/run.py --version
paper-alchemist validate-profile --profile jansen-2020-2026 --workspace . | python3 -c 'import json,sys; result=json.load(sys.stdin); print(json.dumps(result, indent=2)); sys.exit(0 if result.get("generation_ready") else 1)'
echo "paper-alchemist ready for ${LINEAR_ISSUE_IDENTIFIER:-unknown}"
