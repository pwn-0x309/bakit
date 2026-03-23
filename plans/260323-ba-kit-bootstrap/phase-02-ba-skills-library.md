# Phase 2: BA Skills Library

**Priority:** Critical
**Status:** completed
**Dependencies:** Phase 1

---

## Description

Create all 15 BA-specific skills. Each skill is a self-contained SKILL.md file following claude-kit's skill format (YAML frontmatter + structured markdown instructions). Skills are the primary deliverable of BA-kit — they teach Claude how to perform professional BA tasks.

---

## Skill Design Principles

1. **Actionable, not theoretical** — Each skill provides step-by-step instructions Claude can follow
2. **Template-aware** — Skills reference templates from `./templates/` where applicable
3. **BABOK-aligned** — Reference relevant BABOK 3.0 knowledge areas
4. **Output-focused** — Every skill defines expected deliverables
5. **Mermaid-powered** — Use Mermaid.js for all diagrams within skills
6. **Dual methodology** — Support both Agile and traditional approaches

---

## Deliverables

### 2.1 ba-discovery (End-to-End Discovery Workflow)
**File:** `skills/ba-discovery/SKILL.md`

The flagship skill — orchestrates a complete BA discovery engagement:
- Stakeholder identification & mapping
- Current-state process documentation
- Pain point & opportunity analysis
- Requirements elicitation planning
- Feasibility assessment
- Deliverable: Discovery report with next-step recommendations

**BABOK Areas:** Planning & Monitoring, Elicitation & Collaboration

### 2.2 ba-requirements (Requirements Engineering)
**File:** `skills/ba-requirements/SKILL.md`

Core requirements skill covering:
- Elicitation techniques (interviews, workshops, observation, surveys)
- BRD/FRD/SRS creation using templates
- Requirements prioritization (MoSCoW, WSJF, Kano)
- Traceability matrix creation
- Change request management
- SMART validation for each requirement

**BABOK Areas:** Requirements Analysis, Requirements Life Cycle Management

### 2.3 ba-user-stories (User Story Creation & Mapping)
**File:** `skills/ba-user-stories/SKILL.md`

Agile-focused skill:
- User story format: "As a [role], I want [feature] so that [benefit]"
- Acceptance criteria (Given/When/Then Gherkin format)
- Story mapping (backbone → walking skeleton → iterations)
- INVEST validation (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Epic → Feature → Story decomposition
- Definition of Ready / Definition of Done

### 2.4 ba-process-mapping (Process Modeling)
**File:** `skills/ba-process-mapping/SKILL.md`

Process visualization skill:
- BPMN 2.0 elements (events, activities, gateways, swimlanes) in Mermaid
- Value stream mapping (identify waste, optimize flow)
- Current-state (AS-IS) → Future-state (TO-BE) mapping
- Swimlane diagram creation
- Process optimization recommendations
- Bottleneck identification

### 2.5 ba-stakeholder (Stakeholder Analysis & Management)
**File:** `skills/ba-stakeholder/SKILL.md`

Stakeholder management skill:
- Stakeholder identification & classification
- Power/Interest matrix (Mendelow's)
- RACI matrix creation
- Communication plan development
- Engagement strategy per stakeholder group
- Conflict resolution approaches

### 2.6 ba-gap-analysis (Gap & Impact Analysis)
**File:** `skills/ba-gap-analysis/SKILL.md`

Analysis skill:
- AS-IS → TO-BE gap identification
- Gap prioritization (impact × effort matrix)
- Solution recommendations per gap
- Impact analysis (ripple effects of changes)
- Dependency mapping
- Risk assessment for each gap

### 2.7 ba-feasibility (Feasibility Study)
**File:** `skills/ba-feasibility/SKILL.md`

Feasibility assessment:
- Technical feasibility (can we build it?)
- Operational feasibility (will it work in practice?)
- Economic feasibility (ROI, cost-benefit)
- Schedule feasibility (can we deliver on time?)
- Risk feasibility (are risks acceptable?)
- Go/No-Go recommendation framework

### 2.8 ba-data-modeling (Data Modeling)
**File:** `skills/ba-data-modeling/SKILL.md`

Data architecture skill:
- Entity-Relationship Diagram (ERD) creation in Mermaid
- Data Flow Diagram (DFD) — Level 0, 1, 2
- Data dictionary creation
- Data quality requirements
- Data governance considerations
- API contract basics (OpenAPI reference)

### 2.9 ba-compliance (Compliance & Governance)
**File:** `skills/ba-compliance/SKILL.md`

Regulatory compliance:
- GDPR requirements checklist
- HIPAA considerations
- SOX/financial compliance
- Data classification (public/internal/confidential/restricted)
- Compliance requirements mapping (requirement → regulation → test case)
- Privacy impact assessment (PIA/DPIA)
- Audit trail requirements

### 2.10 ba-workshop (Workshop Facilitation)
**File:** `skills/ba-workshop/SKILL.md`

Facilitation skill:
- Workshop planning (objectives, agenda, participants, logistics)
- Facilitation techniques (brainstorming, affinity mapping, dot voting)
- JAD (Joint Application Design) sessions
- Requirements workshop structure
- Remote workshop best practices
- Output capture & follow-up actions

### 2.11 ba-acceptance-criteria (Acceptance Criteria)
**File:** `skills/ba-acceptance-criteria/SKILL.md`

Quality validation:
- Given/When/Then (Gherkin) format
- Scenario-based AC
- Rule-based AC
- Boundary condition identification
- Negative test cases
- Definition of Done alignment
- AC review checklist

### 2.12 ba-swot (SWOT Analysis)
**File:** `skills/ba-swot/SKILL.md`

Strategic analysis:
- Strengths & Weaknesses (internal)
- Opportunities & Threats (external)
- SWOT matrix creation
- Strategy formulation from SWOT (SO/WO/ST/WT strategies)
- Decision support output

### 2.13 ba-cost-benefit (Cost-Benefit & ROI Analysis)
**File:** `skills/ba-cost-benefit/SKILL.md`

Financial analysis:
- Cost identification (direct, indirect, opportunity)
- Benefit quantification (tangible, intangible)
- ROI calculation
- Payback period
- NPV (Net Present Value) basics
- Break-even analysis
- Recommendation with financial justification

### 2.14 ba-communication (Communication Plans & Reporting)
**File:** `skills/ba-communication/SKILL.md`

Communication skill:
- Stakeholder communication plan creation
- Status report writing
- Executive summary format
- Meeting minutes structure
- Escalation procedures
- Presentation outline for stakeholders

### 2.15 ba-change-management (Change Management)
**File:** `skills/ba-change-management/SKILL.md`

Change management:
- Change impact assessment
- Stakeholder readiness evaluation
- Training needs analysis
- Adoption strategy
- Resistance management
- Success measurement (adoption metrics)
- Rollback planning

---

## Implementation Steps

1. Create all 15 skill directories under `skills/`
2. Write each SKILL.md with:
   - YAML frontmatter (name, description)
   - Structured instructions Claude can follow
   - Step-by-step methodology
   - Expected deliverables/output format
   - Template references where applicable
   - Mermaid diagram examples
3. Validate all skills have consistent format and cross-reference each other appropriately

---

## Success Criteria

- [x] All 15 skill directories created with SKILL.md files
- [x] Each skill has YAML frontmatter with name and description
- [x] Each skill provides step-by-step actionable instructions
- [x] Skills reference templates from `./templates/` where applicable
- [x] Skills include Mermaid diagram examples for visual outputs
- [x] Cross-references between related skills are consistent
