# BA-kit Improvement Plan

**Date:** 2026-03-26
**Scope:** Fix gaps, harden pipeline, align agents with workflow promises
**Status:** Completed

---

## Current State Summary

BA-kit remains a 12-step single-skill orchestration (`/ba-start`) producing FRD, user stories, SRS, wireframes, and HTML deliverables via 4 agents. The markdown-to-HTML packaging path is now smoke-tested end-to-end, even though no real project artifacts have been generated yet.

### Key Findings

- **Resolved parser gap**: `scripts/md-to-html.py` now supports ordered lists, nested mixed lists, configurable `--base-dir`, and read-only `--no-editor` output
- **Resolved agent mismatch**: `ba-documentation-manager` now covers Step 12 cross-artifact consistency auditing and HTML packaging responsibilities
- **Resolved docs clarification**: `docs/getting-started.md` keeps `./install.sh` for Claude Code, keeps `scripts/install-codex-ba-kit.sh` scoped to Codex bundle installs, and documents `--no-editor` for read-only stakeholder HTML
- **Resolved pipeline validation**: `scripts/test-md-to-html.sh` now smoke-tests HTML generation, embedded images, Mermaid, tables, blockquotes, and nested list structure
- **Empty designs/**: Still expected — no `.pen` files yet because no real project has run

---

## Implementation Outcome

- Phase 1 completed in `scripts/md-to-html.py`
- Phase 2 completed in `agents/ba-documentation-manager.md` and `codex/agents/ba-documentation-manager.md`
- Phase 3 completed in `docs/getting-started.md`, `CONTRIBUTING.md`, and `.github/pull_request_template.md`
- Phase 4 completed in `scripts/test-md-to-html.sh`
- Validation passed: `python3 -m py_compile scripts/md-to-html.py`, `bash scripts/test-md-to-html.sh`, `bash -n install.sh`, `bash -n scripts/install-codex-ba-kit.sh`

## Decisions

1. Keep editable HTML as the default output. Use `--no-editor` for read-only stakeholder distribution.
2. Keep the existing root `install.sh` for Claude Code. Keep `scripts/install-codex-ba-kit.sh` scoped to Codex bundle installation.

## Phases

### Phase 1 — Fix md-to-html.py Parser Gaps

**Goal:** Make the markdown parser production-ready for actual FRD/SRS content.

**Why:** Templates use numbered lists (FRD acceptance criteria, SRS constraints) and nested lists (screen states, alternate flows). Without support, these render as broken paragraphs in HTML output.

| Task | File | Detail |
|---|---|---|
| 1.1 | `scripts/md-to-html.py` | Add ordered list (`1.`, `2.`) support — detect `^\d+\.\s` pattern, render as `<ol><li>` |
| 1.2 | `scripts/md-to-html.py` | Add nested list support — detect indentation (2+ spaces or tab before `- ` or `1.`), nest `<ul>`/`<ol>` inside parent `<li>` |
| 1.3 | `scripts/md-to-html.py` | Make `base_dir` configurable via `--base-dir` CLI flag, default to current `parent.parent.parent` behavior for backward compat |
| 1.4 | `scripts/md-to-html.py` | Add `--no-editor` CLI flag to produce clean read-only HTML (no toolbar, no EditorApp JS) for stakeholder distribution |

**Validation:** Create a test markdown file exercising ordered lists, nested lists, mixed lists, images, Mermaid, and tables. Run conversion, verify HTML renders correctly in browser.

**Status:** Completed

---

### Phase 2 — Align ba-documentation-manager Agent

**Goal:** Agent file matches its actual responsibilities in SKILL.md Step 12.

**Why:** Current agent describes light formatting work. Step 12 requires cross-artifact consistency auditing (UC↔screen, field names, traceability). Agent prompt must match or sub-agents will underperform.

| Task | File | Detail |
|---|---|---|
| 2.1 | `agents/ba-documentation-manager.md` | Add explicit cross-artifact consistency audit responsibilities from Step 12 (UC↔screen matching, field name identity, traceability verification) |
| 2.2 | `agents/ba-documentation-manager.md` | Add `Bash` to tools list — needed to run `md-to-html.py` for HTML packaging |
| 2.3 | `agents/ba-documentation-manager.md` | Keep `haiku` model — audit tasks are pattern-matching, not generative |

**Validation:** Read updated agent file, confirm all Step 12 audit items are covered.

**Status:** Completed
**Note:** The packaged Codex agent copy in `codex/agents/ba-documentation-manager.md` was updated as part of the same alignment work.

---

### Phase 3 — Fix getting-started.md Install Reference

**Goal:** Documentation references match actual files.

| Task | File | Detail |
|---|---|---|
| 3.1 | `docs/getting-started.md` | Verify installer references and keep `./install.sh` as the Claude Code installer while keeping `scripts/install-codex-ba-kit.sh` scoped to Codex bundle installs |
| 3.2 | `docs/getting-started.md` | Document `--no-editor` usage for read-only stakeholder HTML packaging |
| 3.3 | `CONTRIBUTING.md`, `.github/pull_request_template.md` | Add maintainer validation guidance for the Codex installer and `scripts/test-md-to-html.sh` |

**Validation:** Follow the relevant install instructions from scratch and verify no broken references or stale maintainer guidance remain.

**Status:** Completed

---

### Phase 4 — Add Smoke Test for End-to-End Pipeline

**Goal:** Verify the full conversion pipeline works before any real project runs.

**Why:** No HTML output has ever been produced. Better to catch issues in a controlled test than during a real engagement.

| Task | File | Detail |
|---|---|---|
| 4.1 | `scripts/test-md-to-html.sh` | Create a shell script that: (a) generates a sample markdown with all supported elements (headings, tables, ordered/unordered/nested lists, Mermaid, image refs, code blocks, blockquotes), (b) runs `md-to-html.py` on it, (c) checks output exists and is valid HTML |
| 4.2 | — | Run the test, fix any issues found |

**Validation:** Script exits 0, output HTML contains expected elements.

**Status:** Completed
**Note:** The test now validates nested list structure and confirms `--no-editor` removes the editor toolbar.

---

## Dependency Graph

```
Phase 1 (parser fixes)
    │
Phase 4 (smoke test) ─── depends on Phase 1

Phase 2 (agent alignment) ─── independent
Phase 3 (docs fix) ─── independent
```

Phases 1, 2, 3 can run in parallel. Phase 4 runs after Phase 1.

---

## Out of Scope

- Adding `stakeholder-analyst` / `process-mapper` agents (referenced in global protocol but not needed for current BA-kit workflow)
- Creating actual `.pen` wireframes or running a real project through the pipeline
- Changing SRS/FRD templates (they're well-structured already)
- Upgrading `ba-documentation-manager` from `haiku` to a heavier model

## Resolved Questions

1. `--no-editor` stays opt-in to preserve existing editable HTML behavior.
2. No wrapper was needed because the root `install.sh` already exists for Claude Code installs.
