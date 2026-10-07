#!/usr/bin/env bash
# 每个议题工作区开工时运行；只复用画像，不安装工具或下载论文。
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

test -f .claude/skills/paper-alchemist/SKILL.md
test -x .claude/skills/paper-alchemist/scripts/run.py
command -v paper-alchemist
paper-alchemist --version
paper-alchemist validate-skill .claude/skills/paper-alchemist
python3 .claude/skills/paper-alchemist/scripts/run.py --version
python3 - <<'PY'
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

workspace = Path.cwd()
profile = "routing-literature"
bundle = workspace / "profiles" / profile
target = workspace / ".paper-alchemist" / "profiles" / profile


def validate(root):
    result = subprocess.run(
        ["paper-alchemist", "validate-profile", "--profile", profile,
         "--workspace", str(root)], capture_output=True, text=True,
    )
    try:
        report = json.loads(result.stdout)
    except ValueError:
        raise SystemExit(f"Profile validation failed: {result.stderr or result.stdout}")
    print(json.dumps(report, indent=2))
    if result.returncode or not report.get("generation_ready"):
        raise SystemExit("Profile is invalid or incomplete; refusing to overwrite existing data.")


if target.exists() or target.is_symlink():
    validate(workspace)
    print("Preserved existing valid routing-literature profile (including newer local versions).")
else:
    if not bundle.is_dir():
        raise SystemExit(f"Missing reusable profile bundle: {bundle}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".routing-install-", dir=target.parent) as scratch:
        root = Path(scratch)
        staged = root / ".paper-alchemist" / "profiles" / profile
        shutil.copytree(bundle, staged)
        validate(root)
        if target.exists() or target.is_symlink():
            raise SystemExit("Profile appeared during setup; refusing to overwrite it. Rerun setup.")
        staged.rename(target)
    validate(workspace)
    print("Installed reusable routing-literature profile from tracked bundle.")
PY
echo "paper-alchemist ready for ${LINEAR_ISSUE_IDENTIFIER:-unknown}"
