# BA Orchestration Protocol

This rule defines how BA-kit coordinates agents and workstreams.

Related rules:
- [BA Primary Workflow](./ba-primary-workflow.md)
- [BA Methodology Rules](./ba-methodology-rules.md)

## Agent Selection
- Use `stakeholder-analyst` for who is involved and how they are engaged.
- Use `ba-researcher` for external facts, standards, and comparisons.
- Use `requirements-engineer` for requested behavior and acceptance criteria.
- Use `process-mapper` for flow and operating model questions.
- Use `compliance-auditor` for obligations and control checks.
- Use `ba-documentation-manager` for cleanup, publishing, and indexing.

## Sequencing
1. Discovery work can run first to establish the frame.
2. Research and stakeholder work can run in parallel when independent.
3. Requirements and process modeling should follow once scope is stable.
4. Compliance and documentation review should happen before handoff.

## Parallelism Rules
- Run parallel tasks only when they answer different questions.
- Do not have two agents edit the same artifact at the same time.
- Merge outputs through the documentation manager or a single lead agent.

## Report Naming
- Use clear kebab-case names.
- Include date and role where it helps traceability.
- Store working reports under `plans/reports/` when the project uses report capture.

## Escalation
- Escalate missing scope, conflicting ownership, or unresolved approval paths immediately.
- If a task crosses role boundaries, split it rather than overloading one agent.
