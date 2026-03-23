# BA-kit Methodology Guide

## Overview

BA-kit uses a hybrid business analysis approach. The toolkit can shift toward Agile or Traditional delivery, but the default posture is to use the lightest process that still preserves traceability, stakeholder alignment, and decision quality.

## BABOK Alignment

| BABOK Knowledge Area | BA-kit Support |
| --- | --- |
| Business Analysis Planning and Monitoring | `ba-discovery`, `ba-stakeholder`, `ba-workshop` |
| Elicitation and Collaboration | `ba-discovery`, `ba-requirements`, `ba-workshop`, `ba-communication` |
| Requirements Life Cycle Management | `ba-requirements`, `ba-acceptance-criteria`, `ba-change-management` |
| Strategy Analysis | `ba-swot`, `ba-gap-analysis`, `ba-feasibility`, `ba-cost-benefit` |
| Requirements Analysis and Design Definition | `ba-requirements`, `ba-user-stories`, `ba-process-mapping`, `ba-data-modeling` |
| Solution Evaluation | `ba-gap-analysis`, `ba-feasibility`, `ba-change-management`, `ba-compliance` |

## Agile BA Mode

Use Agile mode when:
- delivery is iterative
- stakeholder feedback cycles are frequent
- documentation needs to stay lightweight

Preferred artifact set:
- discovery summary
- story map
- user stories
- acceptance criteria
- lightweight process flows

Recommended skill chain:
`ba-discovery` -> `ba-user-stories` -> `ba-acceptance-criteria` -> `ba-communication`

## Traditional BA Mode

Use Traditional mode when:
- approvals are formal
- the project has vendors, procurement, or contract dependencies
- governance requires baseline documents

Preferred artifact set:
- BRD
- FRD
- SRS
- RACI
- stakeholder register
- formal review log

Recommended skill chain:
`ba-discovery` -> `ba-stakeholder` -> `ba-requirements` -> `ba-compliance`

## Hybrid BA Mode

Hybrid mode fits most teams:
- use structured discovery and formal scoping where ambiguity is high
- switch to Agile stories and acceptance criteria for delivery execution
- keep a traceability bridge between formal goals and backlog items

Typical pattern:
1. discovery and scope framing
2. stakeholder alignment
3. high-level BRD or initiative brief
4. user story decomposition
5. validation and compliance review

## Common Scenarios

### Process Transformation

Start with `ba-process-mapping` to establish the AS-IS baseline, then use `ba-gap-analysis` and `ba-change-management` to define the TO-BE shift and adoption path.

### Greenfield Product Discovery

Start with `ba-discovery`, then move into `ba-feasibility`, `ba-user-stories`, and `ba-acceptance-criteria`.

### Audit or Regulatory Remediation

Use `ba-compliance` early. Pair it with `ba-requirements` so obligations flow into explicit requirements and testable criteria.

## Modeling Standards

- use Mermaid for diagrams
- prefer one diagram per decision question
- keep labels business-readable
- distinguish current-state from future-state explicitly

## Quality Rules

- SMART for requirements
- INVEST for user stories
- one owner for each approval gate
- every recommendation links to a business outcome, risk reduction, or cost effect
