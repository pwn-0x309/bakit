# Phase 4: BA Workflow Rules

**Priority:** High
**Status:** completed
**Dependencies:** Phase 1

---

## Description

Create 5 BA-specific workflow rule files that replace claude-kit's dev-centric rules. These rules govern how Claude behaves during BA engagements — methodology, quality standards, orchestration, documentation, and general guidelines.

---

## Deliverables

### 4.1 ba-primary-workflow.md
**File:** `rules/ba-primary-workflow.md`

The master workflow — replaces `primary-workflow.md` from claude-kit.

**BA Lifecycle Workflow:**

```
1. Discovery & Scoping
   - Stakeholder identification (delegate to stakeholder-analyst)
   - Current-state assessment
   - Scope definition & constraints

2. Research & Analysis
   - Domain research (delegate to ba-researcher in parallel)
   - Gap analysis
   - Feasibility assessment
   - Competitor/market analysis

3. Requirements Engineering
   - Elicitation (interviews, workshops, observation)
   - Documentation (BRD → FRD → SRS as needed)
   - User story creation (if Agile)
   - Prioritization (MoSCoW/WSJF)
   - Delegate to requirements-engineer

4. Process Modeling
   - AS-IS process mapping
   - TO-BE process design
   - Optimization recommendations
   - Delegate to process-mapper

5. Validation & Review
   - Requirements review (SMART validation)
   - Stakeholder sign-off
   - Compliance audit (delegate to compliance-auditor)
   - Traceability check

6. Documentation & Handoff
   - Final document packaging
   - Delegate to ba-documentation-manager
   - Handoff checklist
   - Lessons learned
```

**Critical Gates:**
- Scope approval before detailed analysis
- Requirements approval before process modeling
- Compliance review before handoff

### 4.2 ba-quality-standards.md
**File:** `rules/ba-quality-standards.md`

Quality rules for all BA deliverables:
- **SMART requirements:** Specific, Measurable, Achievable, Relevant, Time-bound
- **INVEST user stories:** Independent, Negotiable, Valuable, Estimable, Small, Testable
- **Requirement completeness:** Every requirement needs acceptance criteria
- **Traceability:** Link business goals → requirements → test cases
- **No ambiguity:** One interpretation per requirement
- **Prioritization mandate:** All requirements must be prioritized
- **Review checklist:** Standard checklist for each document type

### 4.3 ba-orchestration-protocol.md
**File:** `rules/ba-orchestration-protocol.md`

Agent delegation rules adapted for BA context:
- Work context, reports path, plans path (same as claude-kit)
- Sequential chaining: Discovery → Analysis → Modeling → Validation → Documentation
- Parallel execution: Multiple researchers on different domains simultaneously
- Agent selection guide: which agent for which task
- Report naming convention: `{agent-type}-{date}-{time}-{slug}.md`

### 4.4 ba-documentation-rules.md
**File:** `rules/ba-documentation-rules.md`

Document management standards:
- Template compliance: All documents must use templates from `./templates/`
- Version control: major.minor versioning for all BA docs
- Document hierarchy: BRD (executive) → FRD (functional) → SRS (technical)
- Naming convention: kebab-case, descriptive names
- Docs directory structure: `./docs/` for finalized deliverables
- Review & approval process

### 4.5 ba-methodology-rules.md
**File:** `rules/ba-methodology-rules.md`

Methodology guidelines:
- BABOK 3.0 knowledge areas as reference framework
- Agile BA: lightweight documentation, user stories, sprint-based
- Traditional BA: formal BRD/FRD/SRS, waterfall approach
- Hybrid: adapt based on project needs (default)
- Elicitation best practices
- Stakeholder engagement principles
- Compliance awareness (always consider regulatory context)

---

## Implementation Steps

1. Create `rules/` directory
2. Write ba-primary-workflow.md (master workflow)
3. Write ba-quality-standards.md (quality gates & criteria)
4. Write ba-orchestration-protocol.md (agent delegation)
5. Write ba-documentation-rules.md (document standards)
6. Write ba-methodology-rules.md (BA methodology guidelines)
7. Verify cross-references between rules are consistent

---

## Success Criteria

- [x] All 5 rule files created in `rules/`
- [x] ba-primary-workflow.md covers full BA lifecycle
- [x] Quality standards define clear, measurable criteria
- [x] Orchestration protocol has correct agent delegation examples
- [x] Documentation rules reference templates directory
- [x] Methodology rules cover both Agile and traditional approaches
