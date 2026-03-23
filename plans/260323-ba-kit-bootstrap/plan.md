# BA-Kit Bootstrap Plan

**Created:** 2026-03-23
**Status:** Completed
**Complexity:** Hard (multi-phase, 6 phases)
**Goal:** Build a Claude Code-powered Business Analysis toolkit modeled on claude-kit architecture

---

## Overview

BA-kit is a specialized toolkit that transforms Claude Code into a professional Business Analyst workstation. It leverages the claude-kit architecture pattern (hooks + skills + agents + rules + plans) but replaces software development workflows with BA-specific methodologies grounded in BABOK 3.0, IIBA standards, and modern Agile BA practices.

**What BA-kit delivers:**
- BA-specific skills (requirements gathering, process mapping, stakeholder analysis, etc.)
- BA agent roles (requirements-engineer, stakeholder-analyst, process-mapper, etc.)
- BA workflow rules (discovery → analysis → validation → documentation)
- Document templates (BRD, FRD, SRS, RACI, gap analysis, etc.)
- BA-adapted hooks (methodology reminders, compliance checks, quality gates)
- Project configuration for BA engagements

---

## Phase Summary

| Phase | Name | Status | Dependencies | Est. Files |
|-------|------|--------|-------------|------------|
| 1 | Project Foundation | completed | none | 8 |
| 2 | BA Skills Library | completed | Phase 1 | 15+ |
| 3 | BA Agent Roles | completed | Phase 1 | 6 |
| 4 | BA Workflow Rules | completed | Phase 1 | 5 |
| 5 | Document Templates | completed | Phase 2 | 12+ |
| 6 | Integration & Testing | completed | Phases 2-5 | 5 |

---

## Phase Details

### Phase 1: Project Foundation
**File:** `phase-01-project-foundation.md`
**Priority:** Critical
**Description:** Set up BA-kit project structure, CLAUDE.md, configuration, and README

### Phase 2: BA Skills Library
**File:** `phase-02-ba-skills-library.md`
**Priority:** Critical
**Description:** Create all BA-specific skills (requirements, process mapping, stakeholder management, etc.)

### Phase 3: BA Agent Roles
**File:** `phase-03-ba-agent-roles.md`
**Priority:** High
**Description:** Define specialized BA agent roles for subagent delegation

### Phase 4: BA Workflow Rules
**File:** `phase-04-ba-workflow-rules.md`
**Priority:** High
**Description:** Create BA-specific workflow rules replacing dev-centric rules

### Phase 5: Document Templates
**File:** `phase-05-document-templates.md`
**Priority:** Medium
**Description:** Build comprehensive BA document template library

### Phase 6: Integration & Testing
**File:** `phase-06-integration-testing.md`
**Priority:** Medium
**Description:** End-to-end integration, README, installation guide, and validation

---

## Architecture

```
BA-kit/
├── CLAUDE.md                          # Project instructions (BA-specific)
├── README.md                          # Installation & usage guide
├── .ck.json                           # BA-kit configuration
├── install.sh                         # Installation script
├── skills/                            # BA-specific skills
│   ├── ba-requirements/SKILL.md       # Requirements engineering
│   ├── ba-process-mapping/SKILL.md    # BPMN, swimlanes, value stream
│   ├── ba-stakeholder/SKILL.md        # Stakeholder analysis & management
│   ├── ba-user-stories/SKILL.md       # User story creation & mapping
│   ├── ba-gap-analysis/SKILL.md       # Gap & impact analysis
│   ├── ba-feasibility/SKILL.md        # Feasibility study
│   ├── ba-data-modeling/SKILL.md      # ERD, DFD, data dictionaries
│   ├── ba-compliance/SKILL.md         # GDPR, audit, governance
│   ├── ba-workshop/SKILL.md           # Workshop facilitation
│   ├── ba-acceptance-criteria/SKILL.md # AC writing & validation
│   ├── ba-swot/SKILL.md              # SWOT analysis
│   ├── ba-cost-benefit/SKILL.md       # Cost-benefit & ROI analysis
│   ├── ba-communication/SKILL.md      # Communication plans & reports
│   ├── ba-change-management/SKILL.md  # Change impact & adoption
│   └── ba-discovery/SKILL.md          # End-to-end discovery workflow
├── agents/                            # BA agent role definitions
│   ├── requirements-engineer.md       # Requirements specialist
│   ├── stakeholder-analyst.md         # Stakeholder engagement
│   ├── process-mapper.md              # Process modeling expert
│   ├── ba-researcher.md               # Domain & market research
│   ├── compliance-auditor.md          # Compliance & governance
│   └── ba-documentation-manager.md    # BA docs management
├── rules/                             # BA workflow rules
│   ├── ba-primary-workflow.md         # Discovery → Analysis → Validation → Docs
│   ├── ba-quality-standards.md        # Requirement quality, SMART criteria
│   ├── ba-orchestration-protocol.md   # Agent delegation for BA
│   ├── ba-documentation-rules.md      # BRD/FRD/SRS standards
│   └── ba-methodology-rules.md        # BABOK, Agile BA guidelines
├── templates/                         # Document templates
│   ├── brd-template.md                # Business Requirements Document
│   ├── frd-template.md                # Functional Requirements Document
│   ├── srs-template.md                # Software Requirements Specification
│   ├── user-story-template.md         # User story with AC
│   ├── raci-template.md               # RACI matrix
│   ├── gap-analysis-template.md       # Gap analysis report
│   ├── feasibility-template.md        # Feasibility study
│   ├── swot-template.md               # SWOT analysis
│   ├── communication-plan-template.md # Communication plan
│   ├── process-map-template.md        # BPMN process map
│   ├── stakeholder-register-template.md # Stakeholder register
│   └── change-impact-template.md      # Change impact assessment
├── docs/                              # BA-kit documentation
│   ├── project-overview-pdr.md
│   ├── ba-methodology-guide.md
│   └── skill-catalog.md
└── plans/                             # Plan storage
    └── reports/                       # Research & analysis reports
```

---

## Key Design Decisions

1. **Standalone project, not a fork** — BA-kit is its own project, designed to be installed alongside claude-kit or independently
2. **Skills-first approach** — Skills are the primary deliverable; agents and rules enhance them
3. **Template-rich** — BA work is heavily template-driven; comprehensive template library is essential
4. **BABOK-grounded** — All skills reference BABOK 3.0 knowledge areas where applicable
5. **Agile + Traditional** — Support both Agile BA (user stories, sprints) and traditional (BRD/FRD/SRS waterfall)
6. **Mermaid for diagrams** — Use Mermaid.js for all process maps, ERDs, DFDs (renderable in markdown)
7. **Compliance-aware** — GDPR, SOX, HIPAA considerations baked into relevant skills

## Completion Note

Bootstrap implementation is complete. Core project files, 15 skills, 6 agent roles, 5 workflow rules, 12 templates, docs, and installation wiring are in place.

---

## Success Criteria

- [x] All 15 BA skills created with actionable, structured SKILL.md files
- [x] All 6 agent roles defined with clear specialization boundaries
- [x] All 5 workflow rules covering BA lifecycle
- [x] All 12+ document templates ready to use
- [x] CLAUDE.md properly references all skills, rules, and workflows
- [x] README.md with clear installation and usage instructions
- [x] End-to-end test: user can run `/ba-discovery` and get a complete discovery workflow
