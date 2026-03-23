---
name: ba-requirements
description: Handles requirements elicitation, analysis, documentation, prioritization, and validation across BRD, FRD, SRS, and user story formats.
---

# BA Requirements

Use this skill to turn business intent into precise, testable requirements.

## Workflow

### Phase 1 — Requirements Elicitation & Documentation
1. Confirm scope, goal, and audience.
2. Elicit requirements using interviews, workshops, or document review.
3. Normalize statements into clear business, functional, and non-functional requirements.
4. Add supporting structure for the chosen artifact: use cases, business rules, screen descriptions, and traceability where needed.
5. Prioritize with MoSCoW or WSJF.
6. Validate each requirement for SMART quality and ambiguity.
7. Package the result in the right document format.

### Phase 2 — Wireframe Generation (automatic for SRS)

When the deliverable is an **SRS** and contains **Screen Descriptions** (SCR-xx entries), automatically generate Pencil wireframes.

**Step 2.1 — Extract screen list**

Parse the completed SRS for all `SCR-xx` entries. Build a generation plan:

| Screen ID | Screen Name | Key Elements | Target File |
|-----------|-------------|-------------|-------------|
| SCR-01 | Login | email, password, social login, forgot password | `designs/{slug}/SCR-01-login.pen` |
| SCR-02 | Dashboard | stats cards, recent activity, nav sidebar | `designs/{slug}/SCR-02-dashboard.pen` |

**Step 2.2 — Ask user for wireframe preferences**

Use `AskUserQuestion`:
```
Question: "The SRS defines {N} screens. How should I generate wireframes?"
Options:
  - "Generate all wireframes automatically" — create .pen files for every screen
  - "Let me pick which screens" — user selects subset
  - "Skip wireframes" — no .pen files, just the SRS
```

**Step 2.3 — Generate wireframes with Pencil MCP**

For each approved screen:
1. Read the Screen Detail section from the SRS (layout summary, regions, fields, actions, states)
2. Get design guidelines: `get_guidelines(topic="web-app")` (or `"mobile-app"` based on context)
3. Get style guide: `get_style_guide_tags` → `get_style_guide(tags=[...])`
4. Create `.pen` file: `open_document("new")` → `batch_design` with layout, fields, buttons, nav per the SRS spec
5. Validate: `get_screenshot` → visually verify layout matches SRS intent
6. Save to `designs/{initiative-slug}/SCR-xx-{screen-name}.pen`

**Step 2.4 — Link wireframes back to SRS**

Update the SRS document to fill in:
- `Pencil Artifact:` paths in each Screen Detail section
- `Wireframe / Mockup Reference` section with file paths and covered screen IDs

**Token efficiency**: Generate screens sequentially (one `.pen` at a time) to keep Pencil context manageable. Reuse the same style guide across all screens.

## Deliverables
- Requirements list with IDs
- Use case specifications for critical interactions
- Screen descriptions for UI-backed scope
- Pencil `.pen` wireframes auto-generated for SRS screens (unless user skips)
- Prioritized backlog or requirement set
- Traceability matrix
- Change log and open questions

## Templates
- Use [brd-template.md](../../templates/brd-template.md)
- Use [frd-template.md](../../templates/frd-template.md)
- Use [srs-template.md](../../templates/srs-template.md)
- Use [user-story-template.md](../../templates/user-story-template.md)
- Use [change-impact-template.md](../../templates/change-impact-template.md)

## Pencil Wireframes
- Use Pencil for low-fidelity screen wireframes referenced by the SRS
- Store `.pen` artifacts under `designs/[initiative-slug]/`
- Keep screen IDs aligned between the SRS and artifact filenames
- Reference the `.pen` path directly in each screen description

## Related Skills
- `ba-acceptance-criteria`
- `ba-user-stories`
- `ba-gap-analysis`
- `ba-compliance`

## Quality Check
- Every requirement has acceptance criteria
- Use cases cover primary and alternate flows for critical scope
- Screen descriptions capture fields, validations, and navigation where applicable
- SRS screens have corresponding `.pen` wireframes in `designs/` (unless user explicitly skipped)
- Each `.pen` filename matches its SRS screen ID (SCR-xx alignment)
- Wireframe screenshots visually match the SRS screen layout intent
- Each requirement has one interpretation
- Priorities are explicit and defensible
