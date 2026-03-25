# BA-kit Skill Catalog

## Purpose

This catalog explains the single BA-kit skill, what it produces, and which agents support it.

## Skill

| Skill | When to Use | Related Templates | Related Agents | Typical Output |
| --- | --- | --- | --- | --- |
| `ba-start` | End-to-end BA engagement from raw input to packaged deliverables | `intake-form-template.md`, `frd-template.md`, `user-story-template.md`, `srs-template.md` | `requirements-engineer`, `ui-ux-designer`, `ba-documentation-manager`, `ba-researcher` | Intake form, FRD, user stories, use cases, Screen Contract Lite, wireframes, final browser-editable SRS HTML, quality review |

## Workflow

`/ba-start` handles the entire lifecycle:

1. Accept raw input (file or text)
2. Parse and normalize into intake form
3. Gap analysis and clarifying questions
4. Work plan generation
5. FRD production
6. User story generation
7. Use case specification production
8. Screen Contract Lite production
9. Wireframe generation from use cases and screen contract
10. Final screen description production
11. Unified browser-editable HTML packaging and quality review

## Invocation

```text
/ba-start
```

## Agent Delegation

| Agent | Role in Workflow |
| --- | --- |
| `requirements-engineer` | FRD, user stories, use cases, Screen Contract Lite, final screen descriptions, validation |
| `ui-ux-designer` | Pencil wireframe generation from use cases and screen contract |
| `ba-documentation-manager` | Quality review, consistency, packaging |
| `ba-researcher` | Domain research when external context is needed |

## HTML Editing

The final HTML deliverable is meant to be edited in the browser. Update copy, swap images, and add or remove blocks directly in the rendered HTML instead of hand-editing source HTML.

## Expected Quality Bar

- Outputs reference business goals
- Every requirement has acceptance criteria
- Use cases cover primary and alternate flows
- Screen descriptions use field tables with Display/Behaviour/Validation rules
- Every SRS requirement, use case, and screen traces to user stories
- Diagrams use Mermaid
- Risks, assumptions, and open questions are visible
