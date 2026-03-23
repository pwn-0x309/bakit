# BA Primary Workflow

This is the orchestration rule set for BA-kit. It replaces the dev-centric primary workflow with a BA lifecycle centered on discovery, analysis, validation, and handoff.

Related rules:
- [BA Quality Standards](./ba-quality-standards.md)
- [BA Documentation Rules](./ba-documentation-rules.md)
- [BA Methodology Rules](./ba-methodology-rules.md)

## Lifecycle
1. Discovery and scoping
2. Research and analysis
3. Requirements engineering
4. Process modeling
5. Validation and review
6. Documentation and handoff

## Delegation Map
- `stakeholder-analyst` for stakeholder identification, power/interest mapping, and RACI creation.
- `ba-researcher` for external evidence, standards, market context, and option comparisons.
- `requirements-engineer` for BRD, FRD, SRS, user stories, and traceability.
- `process-mapper` for AS-IS and TO-BE modeling, swimlanes, and optimization.
- `compliance-auditor` for regulatory checks, control mapping, and privacy review.
- `ba-documentation-manager` for final packaging, indexing, and publishing.

## Standard Flow
1. Clarify business goals, scope, constraints, and success criteria.
2. Identify stakeholders and current-state context.
3. Research domain constraints and solution options.
4. Capture requirements with acceptance criteria and priorities.
5. Map processes and identify improvement opportunities.
6. Validate quality, compliance, and traceability.
7. Package the final outputs for approval and handoff.

## Critical Gates
- Approve scope before deep analysis.
- Approve requirements before process redesign.
- Approve compliance findings before handoff.

## Execution Rules
- Prefer one primary owner per artifact.
- Route parallel work only when scopes do not overlap.
- Preserve source meaning; do not invent business intent.
- Escalate unresolved ambiguity before finalizing downstream work.
