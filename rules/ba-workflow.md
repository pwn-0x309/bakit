# BA Workflow

Consolidated workflow rules for BA-kit covering lifecycle, delegation, documentation, and methodology.

Related rules:
- [BA Quality Standards](./ba-quality-standards.md)

## Lifecycle

BA-kit is optimized for a solo IT BA. The workflow should reduce duplicated writing and emit only the artifacts justified by the engagement.

1. Accept input (file or text)
2. Parse and normalize into intake form
3. Gap analysis and clarification
4. Scope lock and engagement-mode selection (`lite`, `hybrid`, or `formal`; default `hybrid`)
5. Build the persisted requirements backbone
6. Emit downstream artifacts from the backbone only when their gates are met
7. Produce behavioral specifications only for complex or risky flows
8. Produce technical specification slices only when integrations, NFR risk, or handoff needs justify them
9. Generate wireframes only for critical or explicitly requested screens
10. Run quality review and package only the artifacts actually emitted for the engagement

## Agent Delegation

| Agent | Scope |
| --- | --- |
| `requirements-engineer` | Intake refinement, requirements backbone, FRD, user stories, selective SRS content |
| `ui-ux-designer` | Pencil wireframes from SRS screens |
| `ba-documentation-manager` | Validation pack, quality review, packaging, cross-references |
| `ba-researcher` | Domain research, standards, market context |

## Delegation Rules

- Route parallel work only when scopes do not overlap.
- Do not have two agents edit the same artifact at the same time.
- Prefer one primary owner per artifact.
- Merge outputs through the documentation manager or orchestrator.
- Escalate unresolved ambiguity before finalizing downstream work.
- Default to inline solo execution unless delegation materially reduces cycle time or improves quality.

## Delegation Hardening

- Build delegated work as narrow handoff packets, not full-document dumps.
- Each delegated packet should contain only the objective, target artifact, allowed write scope, exact upstream excerpts, trace IDs, and expected output sections.
- For non-trivial delegated work, include a dedicated tracker path under `plans/{date}-{slug}/delegation/` so progress is visible outside the live chat session.
- Do not pass the full playbook, full rule set, and full template into every sub-agent call once the orchestrator has already resolved the workflow.
- If the delegated packet still requires large merged artifacts to be understandable, repartition the work before spawning.
- When a delegated scope grows too large to keep terminology and traceability consistent, split it into smaller groups and rerun only the affected slice.
- If a worker lacks context or receives an overloaded scope, it must stop and return the exact missing inputs or a repartition request instead of guessing.
- A repartition response should identify the overloaded section, the reason it is too large, the smallest viable split, and the exact upstream inputs needed for the rerun.
- The orchestrator should create one tracker file per delegated slice, mark it `queued` before spawn, and require the worker to update it to `running` immediately on start.
- Workers should heartbeat after each major milestone and at least every 5 minutes during long-running work.
- If a delegated slice shows no heartbeat for more than 10 minutes and the target artifact has not advanced, treat it as likely stalled and recover intentionally instead of waiting blindly.

## Documentation Rules

- Use templates from `templates/` whenever a matching template exists.
- Keep document titles, headings, and filenames aligned.
- Use descriptive kebab-case filenames.
- Final artifacts go in `plans/reports/`. Work plans go in `plans/{date}-{slug}/`.
- Delegation trackers for active sub-agent slices belong in `plans/{date}-{slug}/delegation/`.
- Preserve traceability links between source, analysis, and final outputs.
- Broken links and stale references must be corrected before handoff.
- For UI-backed SRS work, persist a `wireframe-input-{date}-{slug}.md` artifact before Step 9 and a `wireframe-map-{date}-{slug}.md` artifact after successful wireframe generation.
- Persist the backbone as `plans/reports/backbone-{date}-{slug}.md`. This is the default authoring source for downstream artifact emission.
- Do not infer current-playbook state from legacy report filenames such as `002-intake-form.md`; legacy suites must be migrated or rerun explicitly before they enter the current exact-pattern lifecycle.

## Naming Convention

- `{date}` uses `YYMMDD-HHmm` format matching `.ck.json` convention.
- Use the same `{date}` token for the report artifacts and the corresponding `plans/{date}-{slug}/plan.md` directory so a dated artifact set resolves unambiguously.
- Intake: `plans/reports/intake-{slug}-{date}.md`
- Backbone: `plans/reports/backbone-{date}-{slug}.md`
- FRD: `plans/reports/frd-{date}-{slug}.md`
- SRS: `plans/reports/srs-{date}-{slug}.md`
- User stories: `plans/reports/user-stories-{date}-{slug}.md`
- Wireframes: `designs/{slug}/{artifact-name}.pen` plus frame-level screen mapping in the SRS
- Supporting wireframe frames: use the parent screen ID prefix plus a stable suffix such as `SCR-01-EMPTY`, `SCR-01-ERROR`, or `SCR-01-TOAST-SUCCESS`
- Modal/drawer/dialog overlays that affect flow should get their own primary `SCR-xx` IDs, not supporting-state suffix IDs

## Methodology

- Default to hybrid BA: formal analysis where risk is high, lightweight artifacts where speed matters.
- Optimize for one analyst holding the primary context. Prefer one persisted source of truth plus derived artifacts over parallel authoring of overlapping documents.
- Reference BABOK 3.0 knowledge areas where useful, but keep outputs practical.
- Match artifact depth to business criticality, regulatory exposure, and audience.
- Start with discovery before solutioning.
- Validate requirements against business goals before finalizing.

## Critical Gates

- Approve scope before deep analysis.
- Build and review the backbone before emitting FRD, stories, SRS, or wireframes.
- Approve requirements before downstream production.
- Once a mutating rerun step is explicitly approved, keep that step locked for the current run; do not reopen generic discovery or ask the user to restate the task unless command, slug, date, or overwrite approval became genuinely ambiguous.
- `lite` mode should stop at intake + backbone + stories unless the user explicitly asks for more.
- `hybrid` mode is the default for solo IT BA work: backbone + targeted FRD + stories + selective SRS + critical-screen wireframes when needed.
- `formal` mode should emit the full artifact set only when governance, vendor handoff, or regulatory needs require it.
- **Cross-artifact consistency check before packaging:** UC steps, screen fields/actions, and wireframe labels must use identical terminology and describe the same behavior.
- Wireframe linkage must be screen-to-frame, not screen-to-file only. A single `.pen` file may cover multiple screens.
- Supporting frames that are not expanded into full screen sections must still be captured in the SRS screen inventory and present in the `.pen` artifact.
- Modal and overlay screens that affect flow must be treated like first-class screens in traceability, not collapsed into supporting-state inventory entries.
- Verify quality before handoff.
- **SRS preflight gate:** once slug/date and prerequisites are resolved, start from the exact backbone and user-stories artifacts, and pull the FRD only when it exists or is explicitly required.
- **FRD/stories preflight gate:** once slug/date and prerequisites are resolved, start from the exact backbone artifact instead of rereading the entire `plans/reports/` suite.
- **Context-loss recovery gate:** if exploration causes context pressure, recover from resolved command + slug/date + exact artifacts on disk; do not ask the user to restate the task unless the target really became ambiguous.
