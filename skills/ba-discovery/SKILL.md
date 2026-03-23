---
name: ba-discovery
description: Orchestrates end-to-end BA discovery from stakeholder mapping through recommendations, grounded in BABOK planning and elicitation practices.
---

# BA Discovery

Use this skill when you need to run a full discovery engagement and produce a clear decision-ready summary.

## Inputs
- Business objective or problem statement
- Known stakeholders, constraints, and timeline
- Any existing notes, docs, or process artifacts

## Workflow

### Phase 1 — Document Intake

Prompt the user for input documents before any analysis begins.

**Step 1.1 — Ask for document location**

Use `AskUserQuestion` to ask the user where their source documents live:

```
Question: "Where are the source documents for this discovery engagement?"
Options:
  - "Specify a folder path" — user provides directory containing requirements, notes, or process docs
  - "Paste or describe inline" — user will paste text or describe the business context directly
  - "No existing documents" — start from scratch with interview questions
```

If the user provides a folder path:
- Use `Glob` to list files in the provided directory (support `.md`, `.txt`, `.pdf`, `.png`, `.jpg`, `.docx`)
- Present the file list to the user for confirmation

**Step 1.2 — Read and digest documents**

When a folder path is provided with documents:
- Spawn `ba-researcher` sub-agent(s) to read and summarize each document
  - For PDF/markdown/text: use `Read` tool directly
  - For images: delegate to `ai-multimodal` skill for extraction
  - For `.docx`: delegate to `ai-multimodal` skill or ask user to export
- Each sub-agent produces a brief summary: key topics, stakeholders mentioned, requirements extracted, open questions found

If the user pastes text or describes inline:
- Parse the text directly and extract the same structure

If no documents exist:
- Skip to Phase 2 with an empty context file

**Step 1.3 — Save discovery context file**

Consolidate all findings into a single reusable context file using [discovery-context-template.md](../../templates/discovery-context-template.md).

Save location: `plans/{date}-{slug}/context/DISCOVERY-CONTEXT.md`

This file is the **single source of truth** for all downstream agents. No subsequent agent should re-read the raw source documents — they read `DISCOVERY-CONTEXT.md` instead.

The context folder (`plans/{date}-{slug}/context/`) may also hold per-document summaries if individual files are large:
```
plans/{date}-{slug}/
├── context/
│   ├── DISCOVERY-CONTEXT.md    ← main digest (always created)
│   ├── summary-{doc-name}.md   ← per-document summary (optional, for large files)
│   └── ...
├── plan.md
└── reports/
```

**Token efficiency rule**: Keep `DISCOVERY-CONTEXT.md` under 300 lines. Use tables over prose. Facts over commentary. If a source document summary exceeds 80 lines, save it as a separate `summary-{doc-name}.md` and reference it from the main context file.

### Phase 2 — Clarifying Questions

Use `AskUserQuestion` to ask 3-8 targeted questions based on `DISCOVERY-CONTEXT.md` (or from scratch if no documents). Focus on:

1. **Business objective**: What is the core problem or opportunity? What does success look like?
2. **Scope**: What is in scope and out of scope for this engagement?
3. **Stakeholders**: Who are the key decision makers, users, and subject matter experts?
4. **Desired deliverables**: What does the user need AI to produce? (e.g., stakeholder map, requirements doc, process diagram, gap analysis, wireframes)
5. **Constraints**: Timeline, budget, regulatory, or technical constraints?
6. **Current state**: Are there existing systems, processes, or pain points already documented?
7. **Methodology preference**: Agile user stories, formal BRD/SRS, or hybrid?
8. **Priority**: What is most urgent or highest risk?

Adapt questions based on what `DISCOVERY-CONTEXT.md` already answers — skip questions that are clearly covered.

Incorporate answers back into `DISCOVERY-CONTEXT.md` (update the relevant sections).

### Phase 3 — Discovery Analysis

With `DISCOVERY-CONTEXT.md` + clarifying answers in hand:

1. **Identify stakeholders**, decision makers, and subject matter experts.
2. **Capture the current state** with a process view and pain points.
3. **Group opportunities**, risks, assumptions, and open questions.
4. **Define follow-up elicitation** needed for requirements or feasibility.
5. **Recommend deliverables and skill chain** — which BA artifacts to produce next and in what order.
6. **Produce a discovery summary** with recommendations and next steps.

### Phase 4 — Save Outputs

Save the discovery report to `plans/reports/discovery-{slug}-{date}.md`.

If a work plan is warranted, save it to `plans/{date}-{slug}/plan.md`.

## Deliverables
- `DISCOVERY-CONTEXT.md` — reusable context file for all downstream agents
- Per-document summaries (optional, for large source files)
- Stakeholder map
- Current-state summary
- Pain point and opportunity list
- Discovery report with recommended next actions and skill chain

## Agent Delegation

| Condition | Agent | Purpose |
| --- | --- | --- |
| Source documents need reading | `ba-researcher` | Read, summarize, extract key findings |
| Images or Word files present | `ai-multimodal` skill | Extract text and details from visual/binary sources |
| Stakeholders need mapping | `stakeholder-analyst` | Classification, RACI, engagement plan |
| Processes need modeling | `process-mapper` | AS-IS flow and pain point diagram |
| Final packaging needed | `ba-documentation-manager` | Quality check and deliverable formatting |

## Templates
- Use [discovery-context-template.md](../../templates/discovery-context-template.md) — **primary output of Phase 1**
- Use [stakeholder-register-template.md](../../templates/stakeholder-register-template.md)
- Use [process-map-template.md](../../templates/process-map-template.md)
- Use [communication-plan-template.md](../../templates/communication-plan-template.md)

## Related Skills
- `ba-stakeholder`
- `ba-process-mapping`
- `ba-requirements`
- `ba-feasibility`
- `ba-kickoff`

## Quality Check
- `DISCOVERY-CONTEXT.md` exists and is under 300 lines
- Context file reflects source material accurately (when provided)
- Business problem is explicit
- Stakeholders are named and classified
- Recommended deliverables match the engagement scope and complexity
- Recommendations are actionable and traceable to evidence
- Open questions are listed explicitly
- No downstream agent needs to re-read raw source documents
