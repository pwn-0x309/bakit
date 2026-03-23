# Phase 3: BA Agent Roles

**Priority:** High
**Status:** completed
**Dependencies:** Phase 1

---

## Description

Define 6 specialized BA agent roles for subagent delegation. These agents are spawned via Claude Code's Task tool to handle specific BA activities in parallel or sequentially.

---

## Design Principles

1. **Clear specialization** — Each agent has a distinct, non-overlapping focus area
2. **Tool-appropriate** — Agents get only the tools they need (e.g., researcher gets Read/Bash/WebSearch, not Write)
3. **Output-focused** — Each agent produces specific deliverables saved to reports directory
4. **Lean context** — Agent definitions are concise (~200-400 words) for token efficiency

---

## Deliverables

### 3.1 requirements-engineer.md
**File:** `agents/requirements-engineer.md`

**Role:** Specialist in requirements elicitation, documentation, and validation
**Tools:** Read, Write, Edit, Glob, Grep, Bash
**Responsibilities:**
- Analyze business context and extract requirements
- Create BRD, FRD, SRS documents using templates
- Write user stories with acceptance criteria
- Build traceability matrices
- Validate requirements against SMART criteria
- Prioritize using MoSCoW or WSJF

### 3.2 stakeholder-analyst.md
**File:** `agents/stakeholder-analyst.md`

**Role:** Specialist in stakeholder identification, analysis, and engagement planning
**Tools:** Read, Write, Glob, Grep
**Responsibilities:**
- Identify and classify stakeholders
- Create Power/Interest matrices
- Build RACI matrices
- Develop communication plans
- Design engagement strategies
- Map stakeholder relationships and influence

### 3.3 process-mapper.md
**File:** `agents/process-mapper.md`

**Role:** Expert in process modeling, optimization, and visualization
**Tools:** Read, Write, Edit, Glob, Grep
**Responsibilities:**
- Create BPMN process models using Mermaid
- Map current-state (AS-IS) processes
- Design future-state (TO-BE) processes
- Identify bottlenecks and optimization opportunities
- Build value stream maps
- Document swimlane diagrams

### 3.4 ba-researcher.md
**File:** `agents/ba-researcher.md`

**Role:** Domain and market research specialist for BA engagements
**Tools:** Read, Bash, Glob, Grep, WebSearch, WebFetch
**Responsibilities:**
- Research industry standards and regulations
- Analyze competitor solutions
- Investigate technology options for solutions
- Gather market data and trends
- Synthesize findings into structured reports
- Identify best practices for the domain

### 3.5 compliance-auditor.md
**File:** `agents/compliance-auditor.md`

**Role:** Regulatory compliance and governance specialist
**Tools:** Read, Write, Glob, Grep, WebSearch
**Responsibilities:**
- Audit requirements against regulatory frameworks (GDPR, HIPAA, SOX, PCI-DSS)
- Create compliance checklists
- Perform privacy impact assessments
- Map requirements to regulatory obligations
- Identify compliance gaps
- Recommend remediation actions

### 3.6 ba-documentation-manager.md
**File:** `agents/ba-documentation-manager.md`

**Role:** BA documentation quality and lifecycle management
**Tools:** Read, Write, Edit, Glob, Grep
**Responsibilities:**
- Review and improve BA documents for quality and completeness
- Ensure template compliance
- Maintain document version history
- Update docs/ directory with latest artifacts
- Create document summaries and indexes
- Validate cross-references between documents

---

## Implementation Steps

1. Create `agents/` directory
2. Write each agent .md file with:
   - YAML frontmatter (name, description, tools, memory, color)
   - Role description
   - Responsibilities list
   - Output format expectations
3. Ensure agent roles don't overlap (clear specialization boundaries)

---

## Success Criteria

- [x] All 6 agent files created in `agents/`
- [x] Each agent has YAML frontmatter with name, description, tools
- [x] Agent roles have clear, non-overlapping specializations
- [x] Each agent specifies expected output format and delivery path
