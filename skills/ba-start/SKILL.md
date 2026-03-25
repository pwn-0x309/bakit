---
name: ba-start
description: Single entry point for BA-kit. Accepts raw requirements (file or text), normalizes into an intake form, clarifies gaps, produces FRD, user stories, SRS, wireframes, and packages deliverables.
---

# BA Start

Use this skill to run an end-to-end business analysis engagement from raw input to packaged deliverables. This is the **only** skill in BA-kit — it orchestrates the full lifecycle.

## Inputs

- A file path to a requirements source (PDF, markdown, text, image, or Word), **or** pasted text directly
- Optional: known project name, requester, timeline constraints

## Workflow

### Step 1 — Accept Input

Ask the user to provide one of:
- A file path (PDF, MD, TXT, image, DOCX)
- Pasted text containing requirements or business context

**File reading approach:**
- **PDF**: Use `Read` tool (native PDF support)
- **Markdown / text**: Use `Read` tool directly
- **Images** (screenshots, whiteboard photos): Use `Read` tool (multimodal vision)
- **Word (.docx)**: Use `ai-multimodal` skill or ask the user to export as PDF/MD first

### Step 2 — Parse and Normalize

Read the source material and extract content into the [intake-form-template.md](../../templates/intake-form-template.md) structure:
- Project name, date, requester
- Business context (problem, goals, stakeholders mentioned)
- Raw requirements (extracted verbatim)
- Screens / UI mentioned
- Processes / workflows mentioned
- Constraints, assumptions, compliance needs
- Open questions identified during parsing

Save the completed intake form to `plans/reports/intake-{slug}-{date}.md`.

### Step 3 — Gap Analysis

Review the normalized intake against a BA completeness checklist:
- Are stakeholders identified with roles and influence?
- Is there a clear problem statement and measurable goal?
- Are scope boundaries defined (in-scope vs. out-of-scope)?
- Are success criteria or KPIs stated?
- Are compliance or regulatory obligations mentioned?
- Are UI screens described enough to wireframe?
- Are processes described enough to map?

Flag each gap explicitly.

### Step 4 — Ask Clarifying Questions

Present the identified gaps to the user as 3-8 targeted questions using `AskUserQuestion`. Focus on:
- Output language
- Missing stakeholders or decision makers
- Ambiguous scope boundaries
- Unstated success criteria
- Regulatory or compliance context
- Priority and sequencing preferences

Incorporate answers back into the intake form.

### Step 5 — Generate Work Plan

Based on the normalized intake, produce a scoped work plan covering:

**Deliverable selection:**

| Condition | Deliverable | Template |
| --- | --- | --- |
| Detailed functional spec needed | FRD | `frd-template.md` |
| Agile team needs stories | User stories | `user-story-template.md` |
| System spec with screens, use cases, or test cases | SRS | `srs-template.md` |
| UI screens mentioned | Wireframes | `designs/{slug}/` via Pencil MCP, grouped by flow/module with frame-level screen mapping |

**SRS default routing** — SRS is included by default alongside FRD when the intake contains **any** of:
- UI screens or screen descriptions
- System-level interactions (APIs, integrations, data flows)
- Mobile or web application scope
- Test case or acceptance testing expectations

**Agent delegation:**

| Agent | When |
| --- | --- |
| `requirements-engineer` | FRD, user stories, SRS production (parallel subagents for SRS) |
| `ui-ux-designer` | Pencil wireframe generation from SRS screens |
| `ba-documentation-manager` | Final packaging and quality review |
| `ba-researcher` | Domain research when external context is needed |

**Execution order:**
Intake → FRD → User Stories → SRS (parallel groups) → Wireframes → Quality Review

**UI design system default:** Unless the user explicitly asks for another system, all wireframes and UI-oriented handoff artifacts should use the Shadcn UI design system as the default component and layout baseline.

Save the work plan to `plans/{date}-{slug}/plan.md`.

### Step 6 — Produce FRD

Delegate to `requirements-engineer` agent. Produce the FRD using [frd-template.md](../../templates/frd-template.md):
- Functional overview
- User personas
- Feature list with MoSCoW priorities
- Workflows (Mermaid)
- Data requirements
- Business rules
- Integration points
- Acceptance criteria

Save to `plans/reports/frd-{date}-{slug}.md`.

**Export FRD to HTML** (for rendered Mermaid workflows):
```
python scripts/md-to-html.py plans/reports/frd-{date}-{slug}.md
```
Output: `plans/reports/frd-{date}-{slug}.html`

### Step 7 — Produce User Stories

Generate Agile user stories from the FRD feature list using [user-story-template.md](../../templates/user-story-template.md):
- Epic and feature breakdown
- User stories with acceptance criteria (Given/When/Then)
- INVEST validation
- Story-to-screen alignment when UI exists

**User stories with their acceptance criteria become primary input for SRS, wireframes, and downstream artifacts.** Every SRS functional requirement, use case, and screen description should trace back to one or more user stories.

Save to `plans/reports/user-stories-{date}-{slug}.md`.

### Step 8 — Produce SRS Core, Use Cases, and Screen Contract Lite

SRS is the largest artifact. Produce it in dependency order so wireframes are generated before final screen descriptions are expanded.

**Prerequisite:** Intake form, FRD output, and **user stories with AC** must be provided as context to all subagents. User stories drive the scope — every FR, UC, and SCR should map to user stories.

**Sub-agent context management:**
- Each sub-agent has a 200K token context window. To avoid overflow:
  - Pass only **relevant sections** of upstream artifacts, not full documents
  - Group A receives: intake summary (not raw source), FRD features + business rules, user stories
  - Group B receives: Group A FR table + user stories
  - Group C receives: Group B use cases + user stories
  - Group D receives: Group A FR table + FRD technical sections only
  - Group E receives: Group B use cases + Group C screen contract + generated wireframe mapping
  - Group F receives: FR IDs + UC IDs + SCR IDs (reference lists, not full content)
- When a group produces more than **15 use cases or 10 screens**, split into sub-groups to prevent context overflow.

#### Group A — Core (runs first, blocks all others)

**Agent:** `requirements-engineer`
**Sections:** Purpose and Scope, Overall Description, Functional Requirements table
**Input:** Intake form, FRD, user stories
**Output:** `plans/reports/srs-{date}-{slug}-group-a.md`

#### Groups B, D — run after Group A

**Group B — Behavioral**
**Agent:** `requirements-engineer`
**Sections:** Use Case Specifications (summary + detailed use cases with alternate flows)
**Input:** Group A output, user stories
**Output:** `plans/reports/srs-{date}-{slug}-group-b.md`
**Consistency:** Each UC must link to user stories (US-xxx) and screens (SCR-xx). UC actor actions must use the same terminology as user story descriptions and FRD features.

**Group C — Screen Contract Lite**
**Agent:** `requirements-engineer`
**Sections:** Screen Contract Lite + Screen Inventory
**Input:** Group A output, user stories, **Group B output (use cases)**
**Output:** `plans/reports/srs-{date}-{slug}-group-c.md`
**Consistency:** Each primary screen must link to its use cases and user stories. This section is concise but must still define the screen IDs, entry/exit, key actions, and required states needed to drive wireframes. Modal, dialog, drawer, and overlay screens with their own interaction logic must be treated as primary screens, not supporting states.

**Group D — Technical**
**Agent:** `requirements-engineer`
**Sections:** Non-Functional Requirements, Data Flow Diagrams, ERD, API Specs, Constraints
**Input:** Group A output, FRD
**Output:** `plans/reports/srs-{date}-{slug}-group-d.md`

### Step 9 — Generate Wireframes from Use Cases + Screen Contract Lite

When SRS contains Screen Contract Lite entries, generate Pencil wireframes before expanding the final screen descriptions.

**Step 9.1 — Extract screen contract**

Parse the Use Case Specifications, Screen Contract Lite, and Screen Inventory to build a generation plan.
Group related screens into one or more Pencil artifacts by flow, module, or journey. Treat modal/dialog/drawer overlays with flow impact as primary screens. For each primary screen, derive any required supporting frames from the documented states, validation rules, table/list behavior, and feedback surfaces.

**Step 9.2 — Ask user for wireframe preferences**

```
"The screen contract defines {N} primary screens. How should I generate wireframes?"
- "Generate all wireframes automatically"
- "Let me pick which screens"
- "Skip wireframes"
```

**Step 9.3 — Delegate to ui-ux-designer agent**

For each approved screen group:
1. Read the linked Use Cases and Screen Contract Lite entries
2. Verify wireframe intent will match: same actions, same flow steps, same required states
3. Get design guidelines: `get_guidelines(topic="web-app")` or `"mobile-app"`
4. Use Shadcn UI as the default design system baseline for the wireframes unless the user explicitly overrides it
5. Create or update one `.pen` artifact per approved screen group via Pencil MCP tools
6. Create one frame per primary screen, including modal/drawer/dialog overlays that affect flow, and one frame per required supporting state/view inside that artifact
7. Validate with `get_screenshot` — check frame labels, actions, and implied states against the Use Cases and Screen Contract Lite
8. Save artifact to `designs/{slug}/{artifact-name}.pen`

**Step 9.4 — Export wireframes to PNG**

Export each relevant primary frame node to PNG for embedding in the final SRS HTML:
```
mcp__pencil__export_nodes(filePath="designs/{slug}/{artifact-name}.pen", nodeIds=[frameNodeId], outputDir="designs/{slug}/exports/{artifact-name}/", format="png")
```
Rename or map the exported files so each primary SRS screen points to a stable image path such as `designs/{slug}/exports/{artifact-name}/SCR-01-login.png`.

### Step 10 — Produce Final Screen Descriptions

After wireframes are generated, expand the full Screen Descriptions from:
- Use Case Specifications
- Screen Contract Lite
- Wireframe artifact/frame mapping
- Supporting frame inventory

**Group E — Final Screen Descriptions**
**Agent:** `requirements-engineer`
**Sections:** Screen Descriptions (full screen detail sections for primary screens)
**Input:** Group B output, Group C output, wireframe mapping, exported images
**Output:** `plans/reports/srs-{date}-{slug}-group-e.md`
**Consistency:** Final Screen Descriptions must match the wireframes and remain traceable to Use Cases and user stories. Field names, action labels, state behavior, and modal flow must align across all three.

**Screen field table format:**

| Field Name | Field Type | Description |
| --- | --- | --- |
| [Field] | [Type] | Display: [...] / Behaviour: [...] / Validation: [...] |

The Description column contains up to three rule categories as needed:
- **Display Rules**: visibility, defaults, read-only conditions, formatting
- **Behaviour Rules**: on-change actions, auto-fill, cascading, navigation triggers
- **Validation Rules**: required, format, range, cross-field, error messages

**Group F — Validation**
**Agent:** `requirements-engineer`
**Sections:** Test Cases, Glossary, Traceability cross-references
**Input:** Group A through Group E outputs
**Output:** `plans/reports/srs-{date}-{slug}-group-f.md`

### Step 11 — Assembly and Quality Review

After all groups complete:
1. Merge groups into a single SRS following `srs-template.md` section order
2. **Cross-artifact consistency check:**
   - Every UC step maps to a screen field or action (and vice versa)
   - Screen Contract Lite entries have matching wireframes and final screen descriptions
   - UC actor actions use the same wording as screen User Actions
   - UC system responses match screen field Behaviour Rules
   - UC alternate flows are reflected in screen Error/States
   - Field names are identical between UC steps, screen field tables, and wireframe labels
   - User story AC conditions are covered by UC postconditions and screen Validation Rules
3. Cross-link pass: resolve UC-TBD placeholders in screens
4. Resolve ID conflicts across namespaces (FR, UC, SCR, NFR, TC)
5. Verify every SCR and UC traces back to user stories
6. Save to `plans/reports/srs-{date}-{slug}.md`
7. Delete group fragments only after merged SRS is verified

**Execution pattern:**
```
Group A
    ├── Group B ─┐
    └── Group D ─┘
          │
    Group C (Screen Contract Lite)
          │
    Wireframes
          │
    Group E (Final Screen Descriptions)
          │
    Group F (Validation)
          │
    Assembly + Quality Review
```

**Failure handling:** If a group subagent fails, retry once. If still failing, the orchestrator produces that group inline.
### Step 12 — Package Deliverables

Delegate to `ba-documentation-manager` agent:
- Verify all deliverables follow their templates
- Check cross-references between FRD, user stories, and SRS
- Verify user story traceability: every SRS FR, UC, and SCR maps to at least one user story
- **Cross-artifact consistency audit:**
  - UC actor actions match screen User Actions (same wording)
  - Screen Contract Lite entries match both the wireframes and the final Screen Descriptions
  - UC system responses match screen Behaviour Rules
  - Field names are identical across UC steps, screen field tables, and wireframes
  - User story AC conditions are covered by UC postconditions and screen Validation Rules
  - FRD features are fully covered by user stories and SRS requirements
- Validate naming conventions and file structure
- Flag broken links or missing sections
- Produce a delivery summary

**Step 12.1 — Generate unified SRS HTML with embedded wireframes**

Convert the merged SRS markdown to HTML with wireframe images embedded inline:
```
python scripts/md-to-html.py plans/reports/srs-{date}-{slug}.md
```

This script:
- Embeds explicitly referenced wireframe PNGs as base64 images
- Generates a styled HTML document with table of contents
- Supports page breaks for PDF printing (browser Print → Save as PDF)

Output: `plans/reports/srs-{date}-{slug}.html`

The final HTML should present:
- Use Case Specifications
- Wireframe images for primary screens
- Final Screen Descriptions
- Remaining SRS sections needed for traceability and review

**Step 12.2 — Final output structure**

```
plans/
  reports/
    intake-{slug}-{date}.md
    frd-{date}-{slug}.md              # Source markdown
    frd-{date}-{slug}.html            # With rendered Mermaid diagrams
    user-stories-{date}-{slug}.md
    srs-{date}-{slug}.md              # Source markdown
    srs-{date}-{slug}.html            # With embedded wireframes + diagrams
  {date}-{slug}/
    plan.md
designs/
  {slug}/
    auth-flow.pen                     # Editable wireframe source with multiple frames
    checkout.pen                      # Another artifact if scope is large
    exports/
      auth-flow/
        SCR-01-login.png              # Exported frame image for embedding
        SCR-02-otp.png
      checkout/
        SCR-05-review-order.png
```

The `.html` files are the **primary deliverables** for stakeholders. The `.md` files remain as editable sources for future revisions.

## Deliverables

- Normalized intake form
- Gap analysis summary
- Scoped BA work plan
- FRD (functional requirements document) — HTML with rendered Mermaid diagrams
- User stories with acceptance criteria
- SRS working fragments: core, use cases, screen contract lite, technical, final screen descriptions, validation
- Unified SRS (software requirements specification) with use cases, wireframe-backed screen descriptions, NFRs, and test cases
- SRS as HTML with embedded wireframe images and rendered diagrams (primary stakeholder deliverable)
- Pencil wireframes for SRS screens, including supporting state frames in `.pen` and selected frame-level `.png` exports
- Quality review summary

## Templates

- [intake-form-template.md](../../templates/intake-form-template.md)
- [frd-template.md](../../templates/frd-template.md)
- [user-story-template.md](../../templates/user-story-template.md)
- [srs-template.md](../../templates/srs-template.md)

## Agent Delegation

| Agent | Role |
| --- | --- |
| `requirements-engineer` | FRD, user stories, SRS groups A-F |
| `ui-ux-designer` | Pencil wireframe generation |
| `ba-documentation-manager` | Quality review and packaging |
| `ba-researcher` | Domain research when needed |

## Quality Check

- Intake form has no blank required sections
- Every gap is resolved or listed as an open question
- FRD covers all features with priorities and acceptance criteria
- User stories follow INVEST and have Given/When/Then acceptance criteria
- SRS flow follows: FRD → User Stories → Use Case Specification → Screen Contract Lite → Wireframes → Final Screen Descriptions → Unified HTML
- SRS covers functional requirements, use cases, screen contract lite, final screens, NFRs, and test cases
- Every FR, UC, and SCR links to at least one user story
- Screen Contract Lite exists for every primary screen before wireframes are generated
- Screen field tables use the Display/Behaviour/Validation description format
- **Cross-artifact consistency:** UC steps, screen fields/actions, and wireframe labels use identical terminology
- **Use Case → Wireframe → Screen Description chain:** wireframes are generated from the use cases and screen contract, then final screen descriptions are completed from the wireframes
- **UC-Screen alignment:** every UC actor action has a matching screen User Action; every UC system response has a matching screen Behaviour Rule
- **Wireframe fidelity:** wireframes match their SRS screen descriptions field-by-field
- **Design system consistency:** wireframes use Shadcn UI as the default component baseline unless the user explicitly requests another system
- SRS screens have linked `.pen` artifacts and frame references (unless user skipped)
- Screen IDs are aligned between SRS and Pencil frame names
- Modal/drawer/dialog overlays with flow impact are modeled as primary screens with full screen details
- Supporting state frames implied by the screen behavior exist in `.pen` and are listed in the SRS screen inventory, even when they are not expanded into full screen sections
- Cross-references between FRD, user stories, and SRS are consistent

## Token Efficiency

- **Pass minimal context to sub-agents.** Each agent receives only the sections it needs — never the full set of upstream documents.
- **Cache reusable artifacts.** Style guide and design guidelines are fetched once per project and passed to all wireframe agents as context.
- **Read templates once.** The orchestrator reads template files and passes the relevant template section to each sub-agent — agents do not re-read templates.
- **Chunk large groups.** When a group would produce more than 15 use cases or 10 screens, split into sub-groups to prevent context overflow.
- **Assembly reads only outputs.** The merge agent reads final group outputs, not intermediate context or full upstream docs.
- **Wireframe agents get screen slices.** Each wireframe agent receives only its assigned 3-5 screen descriptions, not the full SRS.
