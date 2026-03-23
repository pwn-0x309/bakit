# Phase 5: Document Templates

**Priority:** Medium
**Status:** completed
**Dependencies:** Phase 2 (skills reference templates)

---

## Description

Create 12+ comprehensive BA document templates. Templates are pre-structured markdown files that Claude fills in when using BA skills. They ensure consistency, completeness, and professional quality across all BA deliverables.

---

## Design Principles

1. **Ready-to-fill** — Each template has clear sections with placeholder guidance
2. **Complete but concise** — Cover all standard sections without bloat
3. **Mermaid-ready** — Include Mermaid diagram placeholders where visual outputs are expected
4. **Cross-referenced** — Templates reference related templates and skills
5. **Methodology-neutral** — Work for Agile, Waterfall, or Hybrid approaches

---

## Deliverables

### 5.1 brd-template.md (Business Requirements Document)
**File:** `templates/brd-template.md`

Sections: Executive Summary, Business Problem, Proposed Solution, Business Goals & KPIs, Scope (In/Out), Stakeholders, High-Level Timeline, Budget, Risks, Approval

### 5.2 frd-template.md (Functional Requirements Document)
**File:** `templates/frd-template.md`

Sections: Functional Overview, User Personas, Feature List (MoSCoW), Workflows (Mermaid swimlanes), Data Requirements, Business Rules, Performance Requirements, Integration Points, Acceptance Criteria

### 5.3 srs-template.md (Software Requirements Specification)
**File:** `templates/srs-template.md`

Based on IEEE 830 / ISO/IEC 29148:
Sections: Purpose & Scope, Overall Description, Functional Requirements (numbered), Non-Functional Requirements, Data Flow Diagrams (Mermaid), ERD (Mermaid), API Specs, Constraints, Test Cases, Glossary

### 5.4 user-story-template.md
**File:** `templates/user-story-template.md`

Format: Epic → Feature → Story structure with:
- Story: "As a [role], I want [feature] so that [benefit]"
- Acceptance Criteria (Given/When/Then)
- INVEST validation checklist
- Story points estimation guide
- Definition of Ready / Definition of Done

### 5.5 raci-template.md
**File:** `templates/raci-template.md`

RACI matrix with:
- Stakeholder rows, task columns
- R/A/C/I assignments
- Validation rules (exactly one A per task)
- Example for common BA activities

### 5.6 gap-analysis-template.md
**File:** `templates/gap-analysis-template.md`

Sections: Current State, Target State, Gap Identification Table (gap, impact, effort, priority), Root Cause Analysis, Solution Recommendations, Implementation Roadmap

### 5.7 feasibility-template.md
**File:** `templates/feasibility-template.md`

Sections: Technical Feasibility, Operational Feasibility, Economic Feasibility (ROI), Schedule Feasibility, Risk Feasibility, Go/No-Go Recommendation, Contingency Plan

### 5.8 swot-template.md
**File:** `templates/swot-template.md`

SWOT matrix with:
- Strengths, Weaknesses (internal)
- Opportunities, Threats (external)
- Strategy formulation (SO/WO/ST/WT)
- Action items per quadrant

### 5.9 communication-plan-template.md
**File:** `templates/communication-plan-template.md`

Sections: Stakeholder List, Communication Matrix (who/what/when/how), Message Templates, Cadence Schedule, Escalation Path, Feedback Channels

### 5.10 process-map-template.md
**File:** `templates/process-map-template.md`

Mermaid-based template with:
- BPMN process flow (start → activities → gateways → end)
- Swimlane example
- Process metadata (owner, frequency, SLA)
- Current vs. Future state comparison structure
- Bottleneck annotation format

### 5.11 stakeholder-register-template.md
**File:** `templates/stakeholder-register-template.md`

Sections: Stakeholder ID, Name, Role, Organization, Interest, Influence Level, Power/Interest Classification, Communication Preference, Engagement Strategy, Notes

### 5.12 change-impact-template.md
**File:** `templates/change-impact-template.md`

Sections: Change Description, Impacted Systems/Processes/People, Impact Assessment (High/Med/Low), Readiness Assessment, Training Needs, Adoption Strategy, Risk Mitigation, Success Metrics, Rollback Plan

---

## Implementation Steps

1. Create `templates/` directory
2. Write each template with:
   - Clear section headers with guidance comments
   - Placeholder text explaining what to fill in
   - Mermaid diagram stubs where applicable
   - Cross-references to related templates
3. Validate templates are consistent in style and structure
4. Ensure skills in Phase 2 correctly reference these templates

---

## Success Criteria

- [x] All 12 templates created in `templates/`
- [x] Each template has clear section structure with guidance
- [x] Mermaid diagram placeholders included where relevant
- [x] Templates cross-reference related templates
- [x] Skills from Phase 2 reference correct template paths
