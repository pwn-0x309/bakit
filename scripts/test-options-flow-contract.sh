#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 - "${ROOT_DIR}/core/contract.yaml" "${ROOT_DIR}/templates/manifest.json" <<'PY'
import json
import sys
from pathlib import Path

contract = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
manifest = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))

assert "options" in contract["commands"], "Missing commands.options"
assert contract["commands"]["options"]["requires"] == ["intake"], "options must require intake"
assert "options" in contract["next_step_order"], "options missing from next_step_order"
assert contract["next_step_order"].index("intake") < contract["next_step_order"].index("options") < contract["next_step_order"].index("backbone"), "options must sit between intake and backbone"

paths = contract["paths"]
for key in ("options_root", "options_index", "option_item", "options_comparison"):
    assert key in paths, f"Missing contract path: {key}"

for template_name in (
    "options-index-template.md",
    "solution-option-template.md",
    "options-comparison-template.md",
):
    assert template_name in manifest, f"Missing template manifest entry: {template_name}"
PY
