# BA-kit Artifact Contract

Use this reference when a BA command needs to resolve an existing project set or recommend the next command.

## Exact Artifact Patterns

- `plans/reports/final/intake-{slug}-{date}.md`
- `plans/reports/final/backbone-{date}-{slug}.md`
- `plans/reports/final/frd-{date}-{slug}.md`
- `plans/reports/final/user-stories-{date}-{slug}.md`
- `plans/reports/final/srs-{date}-{slug}.md`
- `plans/reports/final/frd-{date}-{slug}.html`
- `plans/reports/final/srs-{date}-{slug}.html`
- `plans/reports/drafts/wireframe-input-{date}-{slug}.md`
- `plans/reports/drafts/wireframe-map-{date}-{slug}.md`
- `plans/reports/drafts/wireframe-state-{date}-{slug}.md`
- `plans/{date}-{slug}/plan.md`

## Resolution Rules

1. Resolve `--slug <slug>` first when the user supplied it.
2. Otherwise detect candidate slugs from exact artifact patterns only.
3. If more than one slug exists, stop and ask the user to choose.
4. After the slug is known, resolve the dated set from exact artifact patterns only.
5. If more than one dated set exists, stop and ask the user to choose.
6. Never silently choose the newest file by mtime.
7. Treat legacy suites such as `plans/reports/002-intake-form.md` as out-of-contract until they are migrated or rerun explicitly.

## Source-of-Truth Order

When impact or next-step logic needs a source of truth:

1. `backbone` when it exists
2. otherwise `intake`

Downstream artifacts are derived from the source of truth and should not be treated as the baseline for requirement changes.

## Default Next-Step Order

Use this order when the next action is not explicitly known:

1. `intake`
2. `backbone`
3. `frd` only when the gate requires it or the user explicitly asks for it
4. `stories`
5. `srs` when the gate requires it or the current scope is UI-heavy, integration-heavy, or test-heavy
6. `wireframes` only when the SRS set requires UI-backed screen design
7. `package`
8. `status` for inspection only
