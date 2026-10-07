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
python3 - "$@" <<'PY'
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata

parser = argparse.ArgumentParser(description="Install published profiles without overwriting local state.")
parser.add_argument("profile", nargs="?", default=None, help="Selected profile (default: IPM)")
parser.add_argument("--profile", "-p", dest="flag_profile", default=None, help="Selected profile (default: IPM)")
args = parser.parse_args()
workspace = Path.cwd()


# Match the CLI's NFKC/casefold slug convention without requiring its Python
# package in the system interpreter (the installed CLI may use its own venv).
def profile_slug(value):
    normalized = unicodedata.normalize("NFKC", value).casefold().replace("_", "-")
    slug = re.sub(r"[^\w-]+", "-", normalized, flags=re.UNICODE).replace("_", "-")
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise SystemExit("Profile name must contain at least one letter or digit")
    return slug[:100].rstrip("-")


raw_profile = args.flag_profile or args.profile or "IPM"
selected = profile_slug(raw_profile)
published = workspace / "profiles"
bundles = sorted(
    path for path in published.iterdir()
    if path.is_dir() and (path / "source-manifest.json").is_file()
) if published.is_dir() else []


def validate(root, profile):
    profile_dir = Path(root) / ".paper-alchemist" / "profiles" / profile
    for required in ("source-manifest.json", "quality.json"):
        target_file = profile_dir / required
        if not target_file.is_file():
            raise SystemExit(f"Profile {profile} is missing {required}")
        try:
            json.loads(target_file.read_text(encoding="utf-8"))
        except Exception as exc:
            raise SystemExit(f"Profile {profile} has invalid {required}: {exc}")
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


for bundle in bundles:
    profile = profile_slug(bundle.name)
    if profile != bundle.name:
        raise SystemExit(f"Published directory must use its CLI slug: {bundle}")
    target = workspace / ".paper-alchemist" / "profiles" / profile
    if target.exists() or target.is_symlink():
        validate(workspace, profile)
        print(f"Preserved existing valid {profile} profile (including newer local versions).")
        continue
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".profile-install-", dir=target.parent) as scratch:
        root = Path(scratch)
        staged = root / ".paper-alchemist" / "profiles" / profile
        shutil.copytree(bundle, staged)
        validate(root, profile)
        if target.exists() or target.is_symlink():
            raise SystemExit("Profile appeared during setup; refusing to overwrite it. Rerun setup.")
        staged.rename(target)
    validate(workspace, profile)
    print(f"Installed reusable {profile} profile from tracked bundle.")

# A selected private profile need not have a published bundle, but must pass
# the same gate; never silently substitute the default for the user's choice.
validate(workspace, selected)
display_name = "IPM" if selected == "ipm" and raw_profile.upper() == "IPM" else raw_profile
print(f"Selected profile ready: {display_name} (slug: {selected}).")
PY
echo "paper-alchemist ready for ${LINEAR_ISSUE_IDENTIFIER:-unknown}"
