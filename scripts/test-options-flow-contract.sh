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

def normalize(text):
    return " ".join(text.split())

def require_all(text, snippets, message):
    normalized = normalize(text)
    missing = [snippet for snippet in snippets if normalize(snippet) not in normalized]
    if missing:
        fail(f"{message}: missing {missing}")

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
if "plan.md" in behavior:
    fail("contract-behavior should reference paths.plan, not hardcoded plan.md")

require_all(
    behavior,
    [
        "Use one status vocabulary for optioning and Project Home lifecycle guidance:",
        "`recommended`: should run next, not started",
        "`in-progress`: active work or decision cycle is open",
        "`completed`: required work or decision is accepted",
        "`skipped`: intentionally bypassed with rationale",
        "`not-needed`: safely unnecessary for this project",
        "When `paths.options_root` exists as an active decision cycle, treat `paths.plan` as the execution decision ledger.",
        "Intake may seed only `recommended` or `not-needed`.",
        "`backbone` must stop when the ledger status is `recommended` or `in-progress`.",
        "`backbone` may proceed only when the ledger records either `selected option` (`completed`) or `skipped`.",
        "If intake judged optioning unnecessary, the ledger may remain `not-needed` and point to `backbone` as the next command.",
    ],
    "contract-behavior options gate guidance regressed",
)

require_all(
    intake_step,
    [
        "go direct to `backbone`",
        "recommend `options`",
        "strongly recommend `options`",
        "Use the canonical optioning lifecycle statuses `recommended | in-progress | completed | skipped | not-needed`.",
        "Keep `recommend` versus `strongly recommend` in the recommendation summary only; do not create extra status values.",
        "options status: `not-needed` or `recommended`",
        "expected next command: `backbone` when status is `not-needed`, otherwise `options`",
    ],
    "intake recommendation gate contract regressed",
)

if "Todo / Doing / Done" in project_home or "Not needed / Todo / Doing / Done" in project_home:
    fail("Project Home still uses legacy Todo/Doing/Done lifecycle labels")

require_all(
    project_home,
    [
        "Trạng thái lifecycle chuẩn trong dashboard này:",
        "`recommended` = nên làm tiếp nhưng chưa bắt đầu",
        "`in-progress` = đang thực hiện",
        "`completed` = đã xong/đã chốt",
        "`skipped` = chủ động bỏ qua có lý do",
        "`not-needed` = không cần cho dự án này",
        "| Phương án giải pháp | [recommended | in-progress | completed | skipped | not-needed] |",
        "Decision ledger cho optioning status, khuyến nghị bước tiếp theo, và artifact cần sinh",
    ],
    "Project Home options lifecycle guidance regressed",
)
PY
