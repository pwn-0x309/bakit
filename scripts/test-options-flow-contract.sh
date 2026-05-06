#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "${ROOT_DIR}" "${ROOT_DIR}/core/contract.yaml" "${ROOT_DIR}/templates/manifest.json" <<'PY'
import json
import sys
from pathlib import Path

root_dir = Path(sys.argv[1])
contract = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
manifest = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
source_skill = (root_dir / "skills/ba-start/SKILL.md").read_text(encoding="utf-8")
options_step = root_dir / "skills/ba-start/steps/options.md"
behavior = (root_dir / "core/contract-behavior.md").read_text(encoding="utf-8")
intake_step = (root_dir / "skills/ba-start/steps/intake.md").read_text(encoding="utf-8")
project_home = (root_dir / "templates/project-home-template.md").read_text(encoding="utf-8")
generator = (root_dir / "scripts/generate-codex-assets.sh").read_text(encoding="utf-8")
codex_skill = (root_dir / "codex/skills/ba-start/SKILL.md").read_text(encoding="utf-8")

def fail(message):
    raise SystemExit(message)

if "options" not in contract["commands"]:
    fail("Missing commands.options")
if contract["commands"]["options"]["requires"] != ["intake"]:
    fail("options must require intake")
if "options" not in contract["next_step_order"]:
    fail("options missing from next_step_order")
if not (
    contract["next_step_order"].index("intake")
    < contract["next_step_order"].index("options")
    < contract["next_step_order"].index("backbone")
):
    fail("options must sit between intake and backbone")

paths = contract["paths"]
for key in ("options_root", "options_index", "option_item", "options_comparison"):
    if key not in paths:
        fail(f"Missing contract path: {key}")

for template_name in (
    "options-index-template.md",
    "solution-option-template.md",
    "options-comparison-template.md",
):
    if template_name not in manifest:
        fail(f"Missing template manifest entry: {template_name}")

if "/ba-start options --slug <slug>" not in source_skill:
    fail("Missing ba-start options invocation in source skill")
if "| `options` | `steps/options.md` |" not in source_skill:
    fail("Missing ba-start options dispatch row in source skill")
if not options_step.exists():
    fail("Missing ba-start options step placeholder")
if "`impact` -> `impact.md`" not in generator or "`options` -> `options.md`" not in generator:
    fail("Codex asset generator missing options step mapping")
if "`impact` -> `impact.md`" not in codex_skill or "`options` -> `options.md`" not in codex_skill:
    fail("Generated Codex ba-start asset missing options step mapping")
if "options" not in behavior:
    fail("contract-behavior must mention options")
if "recommendation gate" not in intake_step.lower() and "options" not in intake_step:
    fail("intake step must mention options recommendation")
if "Phương án giải pháp" not in project_home:
    fail("Project Home must expose options status")
PY
