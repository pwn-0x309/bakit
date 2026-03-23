# Claude-Kit (CK) Architecture Analysis

## Executive Summary

Claude-Kit is a sophisticated AI agent orchestration framework built on top of Claude Code's hook system and Claude's skills system. It provides:

1. **Configuration-driven behavior** via `.ck.json` and `CLAUDE.md`
2. **Hook-based context injection** that executes at 8 lifecycle points
3. **Modular skills system** with standardized SKILL.md format
4. **Multi-agent delegation** via Task tool and agent role definitions
5. **Plan-driven development** with structured phase files and reporting

The architecture emphasizes **token efficiency**, **dependency clarity**, **agent specialization**, and **workflow automation** through hooks and configuration, not custom code.

---

## 1. Architecture Pattern Overview

### 1.1 Three-Layer Model

```
┌─────────────────────────────────────────┐
│  CLAUDE.md (Project Instructions)       │ ← User-facing rules, workflows
│  + Local .ck.json (Project Config)      │
├─────────────────────────────────────────┤
│  Hook System ($HOME/.claude/hooks/)     │ ← Session init, context injection,
│  + Config Utils (lib/*)                 │   privacy/scout blocking, reminders
├─────────────────────────────────────────┤
│  Skills ($HOME/.claude/skills/)         │ ← Reusable task patterns (research,
│  + Agent Roles (agents/*.md)            │   cook, debug, code-review, etc.)
└─────────────────────────────────────────┘
```

### 1.2 Configuration Sources (Priority Order)

1. **Local project `.ck.json`** (overrides global)
2. **Global `~/.claude/.ck.json`** (default values)
3. **Hardcoded defaults** in `lib/ck-config-utils.cjs` (fallback)

Deep merge algorithm treats empty objects `{}` as "inherit parent" (not reset), enabling partial overrides.

### 1.3 Environment Variable Injection

**SessionStart hook** populates environment variables (via `CK_*` prefix) that persist throughout the session:

- `CK_PROJECT_ROOT`, `CK_REPORTS_PATH`, `CK_PLANS_PATH`, `CK_DOCS_PATH`
- `CK_PROJECT_TYPE`, `CK_PACKAGE_MANAGER`, `CK_FRAMEWORK` (auto-detected)
- `CK_NAME_PATTERN` (computed from plan naming config)
- `CK_AGENT_TEAM` (if running in team mode)
- Language/locale config: `CK_THINKING_LANGUAGE`, `CK_RESPONSE_LANGUAGE`

Subagent hooks read these env vars to derive paths and context.

---

## 2. Hook System Architecture

### 2.1 Hook Lifecycle

Claude Code fires hooks at **8 distinct lifecycle points**:

| Hook | Trigger | Purpose | Exit Code |
|------|---------|---------|-----------|
| **SessionStart** | Session startup/resume/clear/compact | Detect project, init env vars, inject context | 0 (non-blocking) |
| **SubagentStart** | Task tool spawns subagent | Inject minimal context to subagent | 0 (non-blocking) |
| **SubagentStop** | Subagent completes (Plan agent only) | Remind user to `/cook` after planning | 0 (non-blocking) |
| **UserPromptSubmit** | User sends message | Inject dev rules reminder, usage tracking | 0 (non-blocking) |
| **PreToolUse** | Before tool execution (Read/Write/Bash/etc.) | Block sensitive files, large files, validate names | 0 (non-blocking) |
| **PostToolUse** | After file edit/write | Simplify reminder, usage context | 0 (non-blocking) |
| **TaskCompleted** | Task marked complete | Custom task completion handling | 0 (non-blocking) |
| **TeammateIdle** | Teammate goes idle | Team coordination | 0 (non-blocking) |

**All hooks exit with code 0** (fail-open design): failures do not block Claude's execution.

### 2.2 Hook File Organization

```
~/.claude/hooks/
├── session-init.cjs                    ← SessionStart (project detection + env setup)
├── subagent-init.cjs                   ← SubagentStart (context injection)
├── dev-rules-reminder.cjs              ← UserPromptSubmit (rules + plan context)
├── privacy-block.cjs                   ← PreToolUse (sensitive file protection)
├── scout-block.cjs                     ← PreToolUse (large file warnings)
├── post-edit-simplify-reminder.cjs     ← PostToolUse (code simplification nudge)
├── descriptive-name.cjs                ← PreToolUse (filename validation)
├── cook-after-plan-reminder.cjs        ← SubagentStop (post-plan guidance)
├── task-completed-handler.cjs          ← TaskCompleted (task completion hooks)
├── teammate-idle-handler.cjs           ← TeammateIdle (team coordination)
├── gsd-*.js                            ← GSD-specific workflow hooks
├── lib/                                ← Shared utilities
│   ├── ck-config-utils.cjs             ← Config loading, env vars, path resolution
│   ├── project-detector.cjs            ← Auto-detect tech stack
│   ├── context-builder.cjs             ← Build context strings for hooks
│   ├── privacy-checker.cjs             ← Sensitive file detection
│   ├── scout-checker.cjs               ← Large file detection
│   └── ...
└── .logs/                              ← Hook execution logs (hook-log.jsonl)
```

### 2.3 Key Hook: SessionStart

**Flow:**

1. **Project Detection** → Infer project type, package manager, framework
2. **Plan Resolution** → Check session state, branch name, or fallback to none
3. **Reports Path** → Resolve from plan or config
4. **Env Vars** → Write to `CLAUDE_ENV_FILE` for all subsequent hooks
5. **Output Context** → Print to console (shown to user)

**Critical Mechanism:**

```javascript
// From session-init.cjs
const resolved = resolvePlanPath(sessionId, config);
const reportsPath = getReportsPath(resolved.path, resolved.resolvedBy, config);

// Persist env vars
writeEnv(envFile, 'CK_ACTIVE_PLAN', resolved.path);
writeEnv(envFile, 'CK_REPORTS_PATH', reportsPath);
```

Plan resolution order:
1. Session state (if user explicitly activated a plan)
2. Branch matching (if git branch matches pattern, e.g., `feat/add-auth`)
3. None (no plan context)

### 2.4 Key Hook: SubagentStart

**Purpose:** Minimize context (~200 tokens) while enabling subagent to know:
- Where to save reports/plans
- What plan is active (if any)
- Naming templates
- Language preferences
- Trust verification (if configured)

**Output Format:**

```markdown
## Subagent: researcher
ID: a7b04eb0355c97a19 | CWD: /path/to/project

## Context
- Plan: /path/to/plan
- Reports: /path/to/plans/reports/
- Paths: /path/to/plans/ | /path/to/docs/

## Rules
- Reports → {reportsPath}
- YAGNI / KISS / DRY
- Concise, list unresolved Qs at end
```

Emitted as JSON with `hookSpecificOutput.additionalContext` structure.

### 2.5 Privacy & Scout Blocking (PreToolUse)

**Privacy Block:**
- Detects sensitive files: `.env`, `.env.*`, `secrets*`, credentials, API keys
- Blocks Read/Bash/Edit on sensitive files without user approval
- Emits JSON marker: `@@PRIVACY_PROMPT_START@@...@@PRIVACY_PROMPT_END@@`
- LLM uses `AskUserQuestion` tool to get user approval
- If approved, LLM retries with `APPROVED:` prefix (special handling in tool)

**Scout Block:**
- Detects large files (> 100KB by default) before Read
- Warns but doesn't block (scout files are ok, just reminder)
- Suggests `repomix` for compact analysis

Both hooks extract logic to `lib/privacy-checker.cjs` and `lib/scout-checker.cjs` for reuse in plugins.

---

## 3. Skills System Architecture

### 3.1 Skill Structure

Minimum skill:

```
my-skill/
└── SKILL.md
    ├── YAML frontmatter (name, description, license, args)
    └── Markdown instructions (Claude follows these like a prompt)
```

Full skill:

```
my-skill/
├── SKILL.md                    ← Frontmatter + instructions
├── references/                 ← Markdown guides (loaded on-demand)
│   ├── technique-1.md
│   ├── technique-2.md
│   └── ...
├── scripts/                    ← Shell/Python utilities
├── examples/                   ← Sample outputs
└── THIRD_PARTY_NOTICES.md     ← Dependency licenses
```

### 3.2 SKILL.md Frontmatter

**Required fields:**

```yaml
---
name: ck:skill-name          # Unique, lowercase, hyphens
description: "What & when"   # 1-2 sentences, include use cases
---
```

**Optional fields:**

```yaml
version: 1.0.0
license: MIT
argument-hint: "[topic]"      # Usage example
languages: ["ts", "py"]       # Supported languages
```

### 3.3 Skill Patterns in CK

**Research Skill** (`ck:research`)
- Methodology: Scope → Gather → Analyze → Report
- Uses Gemini or WebSearch (configurable in `.ck.json`)
- Outputs markdown report to reports directory
- Max 5 searches per invocation

**Cook Skill** (`ck:cook`)
- End-to-end implementation workflow
- Detects intent: "fast", "auto", "parallel", "no-test"
- Orchestrates: Research → Scout → Plan → Code → Test → Review → Finalize
- Uses subagents at each phase
- Supports `--interactive`, `--fast`, `--auto`, `--parallel` flags

**Debug Skill** (`ck:debug`)
- Systematic debugging framework
- Techniques: systematic-debugging, root-cause-tracing, defense-in-depth, verification
- Multi-layer validation (entry → business logic → environment → debug)
- Verification mandate: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"

**Code Review Skill** (`ck:code-review`)
- Pre-review edge case scouting via `/scout`
- Assessment: structure, logic, types, performance, security
- Task-managed review pipeline for multi-file features (3+ files)
- Forces verification before completion claims

### 3.4 Skill Activation & Loading

Skills are loaded by Claude **on-demand**:

1. User writes `/ck:skill-name` or mentions skill in prompt
2. Claude Code searches `~/.claude/skills/` for SKILL.md
3. Reads frontmatter + instructions
4. Follows instructions like a prompt modifier

**Skills catalog** (~70 skills available):

- **Research & Planning:** research, brainstorm, planning
- **Development:** cook, debug, code-review, backend-development, mobile-development
- **Design:** ui-ux-pro-max, design-systems, copywriting
- **Databases:** databases, devops
- **Other:** gkg (knowledge graph), team, business-analyst

Installed locally via `install.sh` (downloads dependencies: npm packages, Python, system tools).

---

## 4. Agent Roles & Delegation System

### 4.1 Agent Role Definition

Agents are `.md` files in `~/.claude/agents/`:

```yaml
---
name: agent-type-name
description: "What this agent does"
tools: [Read, Bash, Glob, Grep, Write, Edit, Task*]
memory: project|global|none
color: green
---

<role>
Detailed instructions for this agent role
</role>

<project_context>
How to load project-specific instructions
</project_context>
```

**Tools:** Agents are given subset of tools (e.g., `code-reviewer` gets Glob/Grep/Read/Bash, not Write)

**Memory:** Agents can load persistent memory from `~/.claude/agent-memory/{agent-type}/`

**Color:** UI hint for terminal rendering

### 4.2 Primary Agent Roles in CK

| Agent | Role | Spawned By | Key Responsibilities |
|-------|------|-----------|----------------------|
| **researcher** | Multi-source technical analysis | cook, planner | Gemini/WebSearch, cross-reference, synthesis |
| **planner** | Task breakdown & dependency graphs | cook | Phase files, PLAN.md, task list, verification |
| **code-reviewer** | Quality assessment & verification | cook, user | Scout edge cases, assess Critical/High/Med/Low |
| **tester** | Test execution & coverage validation | cook | Run tests, validate 100% pass, no mocks |
| **debugger** | Root cause analysis | cook, user | 4-phase systematic debugging, evidence-based fixes |
| **docs-manager** | Documentation updates | cook finalize | Update docs/, roadmap, changelog |
| **git-manager** | Git commits & push | cook finalize | Commit, push, PR creation |
| **project-manager** | Plan sync-back & status | cook finalize | Update plan.md, mark tasks complete |
| **ui-ux-designer** | UI/UX implementation | cook (if frontend) | Design, Figma, component specs |

### 4.3 Subagent Spawning via Task Tool

**Pattern:**

```typescript
// In cook skill or orchestrator
await Task.create({
  name: "Phase 1: Research",
  agent: "researcher",
  prompt: `Research X. Report to {CK_REPORTS_PATH}...`,
  context: {
    workContext: "/path/to/project",
    reportsPath: "/path/to/project/plans/reports/",
    plansPath: "/path/to/project/plans/"
  }
});
```

When subagent spawns:

1. **SubagentStart hook fires** → Injects plan context (~200 tokens)
2. **Subagent receives context** → Knows where to save reports
3. **Subagent executes** → Reads project context, produces output
4. **Output saved** to reports directory

**Token Efficiency:**

Subagent context is ~200 tokens (lean). Main session keeps full context, subagents get minimal injected context via hooks.

---

## 5. Planning & Report System

### 5.1 Plan Structure

Plans live in `./plans/{date}-{issue}-{slug}/`:

```
plans/
└── 260319-1130-phase5-6-parallel-plan/
    ├── plan.md                         ← Overview, phase list, status
    ├── phase-01-setup-environment.md   ← Detailed phase 1
    ├── phase-02-implement-database.md  ← Detailed phase 2
    ├── phase-03-...
    └── reports/                        ← Subagent reports
        ├── researcher-260319-0900-topic-1.md
        ├── researcher-260319-0905-topic-2.md
        ├── code-reviewer-260319-0930-review.md
        └── ...
```

### 5.2 Plan File Format

**plan.md** (overview):
- Phase list with status (pending/in-progress/complete)
- Links to detailed phase files
- Key dependencies between phases
- Progress % per phase

**phase-XX-name.md** (detailed):
- Context links (reports, docs)
- Priority, status, description
- Key insights from research
- Requirements (functional + non-functional)
- Architecture & component interactions
- Related code files (create/modify/delete)
- Implementation steps (numbered, specific)
- Todo list (checkboxes for tracking)
- Success criteria & definition of done
- Risk assessment & mitigation
- Security considerations
- Next steps & dependencies

### 5.3 Report Naming Pattern

```
{agent-type}-{date}-{time}-{slug}.md

Examples:
- researcher-260319-0900-api-design.md
- code-reviewer-260319-0930-backend-review.md
- planner-260319-1100-phase-tasks.md
```

**Pattern Resolution:**

Computed once in SessionStart, stored in `CK_NAME_PATTERN` env var.

Configuration in `.ck.json`:
```json
{
  "plan": {
    "namingFormat": "{date}-{issue}-{slug}",
    "dateFormat": "YYMMDD-HHmm",
    "issuePrefix": "GH-"
  }
}
```

Example: If branch is `feat/GH-88-auth`, pattern becomes `260319-1100-GH-88-{slug}`

### 5.4 Report Delivery

Subagents write reports to:

```
${CK_REPORTS_PATH}/${agent-type}-${CK_NAME_PATTERN}.md
```

Example:
```
/Users/damtuana/Projects/BA-kit/plans/reports/researcher-260319-0900-architecture-analysis.md
```

Main agent or user reads report from this path after subagent completes.

---

## 6. Configuration Files

### 6.1 CLAUDE.md (Project Instructions)

**Location:** `./CLAUDE.md` (project root)

**Purpose:** User-facing instructions for all agents working on this project

**Sections:**

```markdown
# CLAUDE.md

## Role & Responsibilities
- Project goals and philosophy

## Workflows
- Links to rule files in `$HOME/.claude/rules/`
- Links to primary-workflow.md, development-rules.md, etc.
- Project-specific overrides

## Hook Response Protocol
- Privacy block flow (AskUserQuestion integration)

## Python Scripts (Skills)
- Where to find Python venv
- How to run scripts

## Consider Modularization
- When to split files (200+ lines)
- Naming conventions (kebab-case)

## Documentation Management
- Where docs live (`./docs`)
- Roadmap, changelog, architecture formats

## IMPORTANT: Workflows
- Points to primary-workflow.md as MANDATORY
```

### 6.2 .ck.json (CK Configuration)

**Location:** `./ck.json` (project) or `~/.claude/.ck.json` (global)

**Top-level keys:**

```json
{
  "plan": { /* naming, dating, resolution strategy */ },
  "paths": { "docs": "docs", "plans": "plans" },
  "locale": { "thinkingLanguage": null, "responseLanguage": null },
  "trust": { "enabled": false, "passphrase": "..." },
  "project": { "type": "auto", "packageManager": "auto", "framework": "auto" },
  "skills": { "research": { "useGemini": true } },
  "hooks": { /* enable/disable hooks */ },
  "assertions": [ /* user-specified rules */ ],
  "codingLevel": 5,
  "gemini": { "model": "gemini-3-flash-preview" }
}
```

### 6.3 Settings.json (Claude Code Config)

**Location:** `~/.claude/settings.json`

**Purpose:** Hook registration with Claude Code

```json
{
  "hooks": {
    "SessionStart": [{ "type": "command", "command": "node ...", "matcher": "..." }],
    "SubagentStart": [{ ... }],
    "PreToolUse": [{ ... }],
    "PostToolUse": [{ ... }],
    ...
  },
  "model": "opus",
  "mcpServers": { /* MCP integrations */ }
}
```

Each hook specifies:
- `matcher` (regex on context, e.g., "startup|resume|clear")
- `type` ("command" = run shell script)
- `command` (node script to execute)
- `timeout` (ms, optional)

---

## 7. Workflow Integration

### 7.1 Primary Workflow (Orchestration)

From `primary-workflow.md`:

```
[Code Implementation]
  ↓
[Planning] (delegate to planner)
  ↓
[Research] (multiple researchers in parallel)
  ↓
[Code Implementation] (follow plan, delegate to devs)
  ↓
[Testing] (delegate to tester)
  ↓
[Code Review] (delegate to code-reviewer)
  ↓
[Integration] (ensure backward compatibility)
  ↓
[Documentation] (delegate to docs-manager)
```

**Critical Gates:**

- Plan approval (user) before implementation
- 100% test pass (tester) before review
- Code review completion (code-reviewer) before merge
- Documentation update (docs-manager) before finalize

### 7.2 Cook Skill Workflow Modes

**Interactive mode (default):**
- Research → Review → Plan → Review → Code → Test → Review → Finalize
- Stops at each review gate for user approval

**Fast mode (`--fast`):**
- Skips research, goes Scout → Plan → Code → Test → Review → Finalize

**Auto mode (`--auto`):**
- Runs all phases continuously, auto-approves if quality score ≥ 9.5

**Parallel mode (`--parallel`):**
- Multiple agents on independent phases (needs coordination)

### 7.3 Finalize Phase (Mandatory)

Always runs at end of cook:

1. **project-manager subagent** → Sync all phase files, update plan.md status
2. **docs-manager subagent** → Update docs/ if changes warrant
3. **TaskUpdate** → Mark Claude Tasks as complete
4. **git-manager subagent** → Ask user if they want commit, then commit + push

---

## 8. Team Mode (Optional)

### 8.1 Agent Teams

When `CK_AGENT_TEAM` env var is set, agents are teammates:

```
~/.claude/teams/{team-name}/
├── config.json               ← Team config (members, roles)
├── task-list.json            ← Shared task list
└── ...
```

### 8.2 Team Coordination Rules

- **File ownership:** Each teammate owns distinct files (no overlaps)
- **Git safety:** Use git worktrees to avoid conflicts
- **Communication:** SendMessage tool for peer DMs
- **Task claiming:** Lowest-ID unblocked task first
- **Status:** Mark tasks complete via TaskUpdate, then message lead

### 8.3 Team-Specific Hooks

- **SubagentStart** includes `team-context-inject.cjs` → Injects team config
- **TeammateIdle** hook → Alerts if team member unresponsive
- **TaskCompleted** hook → Team-wide task coordination

---

## 9. Memory System

### 9.1 Persistent Agent Memory

**Location:** `~/.claude/agent-memory/{agent-type}/`

**Purpose:** Agents learn from past interactions (persistent across sessions)

**Files:**

- `MEMORY.md` (primary, max 200 lines, always loaded)
- `topic-1.md`, `topic-2.md` (overflow, linked from MEMORY.md)

**Rules:**

- Update when you discover stable patterns confirmed across interactions
- Remove if corrected by user
- Never save session-specific context
- Organize semantically by topic, not chronologically

Example MEMORY.md:

```markdown
# Researcher Agent Memory

## Food Safety Standards & Traceability Domain

### Key Regulatory Frameworks
- US FDA FSMA: 4-hour traceback, EPCIS 1.2 + GS1 mandated
- EU EC 178/2002: 48-hour typical, Digital Product Passport by 2026
- ...

### Unresolved Questions
1. Will CFDA accept EPCIS data?
2. Cost of GS1 Digital Link resolver?
```

### 9.2 Project Context Memory

If agent specifies `memory: project`, it loads:

```
.claude/agent-memory/{agent-type}/ (personal learning)
+
./memory/ (project-specific learnings)
```

---

## 10. Development Rules & Assertions

### 10.1 Rules Files

In `$HOME/.claude/rules/`:

- **primary-workflow.md** → Plan → Research → Code → Test → Review → Docs
- **development-rules.md** → YAGNI/KISS/DRY, file size mgmt, code quality
- **documentation-management.md** → Docs in `./docs/`, roadmap/changelog structure
- **orchestration-protocol.md** → How to spawn subagents (work context, reports path)
- **team-coordination-rules.md** → File ownership, git safety, communication

### 10.2 Assertions

User-specified rules in `.ck.json`:

```json
{
  "assertions": [
    "Always use Bun, never npm",
    "Never commit secrets (check .gitignore before committing)",
    "All features must have tests"
  ]
}
```

Injected by SessionStart hook to Claude's system context.

---

## 11. Key Architectural Patterns

### 11.1 Fail-Open Hooks

All hooks exit with code 0 (success), even on errors:

```javascript
try {
  // hook logic
  process.exit(0);
} catch (e) {
  // minimal logging
  process.exit(0); // fail-open
}
```

**Why:** Prevents hook failures from blocking Claude's execution. Errors are logged to `~/.claude/hooks/.logs/hook-log.jsonl`.

### 11.2 Deep Merge Configuration

Local config overrides global, preserving inheritance:

```javascript
// Local .ck.json with partial hooks
{ "hooks": { "scout-block": false } }

// Merges with global, doesn't reset other hooks
// Result: scout-block disabled, privacy-block still enabled
```

### 11.3 Path Resolution (Issue #327)

Supports subdirectory workflows (monorepos):

```
CWD: /path/to/monorepo/packages/app
Git root: /path/to/monorepo

SessionStart resolves:
- CK_PROJECT_ROOT = /path/to/monorepo/packages/app (CWD)
- CK_GIT_ROOT = /path/to/monorepo (git root)
- Plans saved in CWD, not git root
```

### 11.4 Plan Resolution Ordering

```
1. Session state (explicit user activation) → "active" plan
2. Branch name matching (.ck.json pattern) → "suggested" plan (hint only)
3. None → no plan context
```

Session state file path: `/tmp/ck-session-{sessionId}.json`

### 11.5 Token Efficiency Strategy

**SessionStart:** ~400 tokens (full context injection)
**SubagentStart:** ~200 tokens (minimal, uses env vars from SessionStart)
**UserPromptSubmit:** ~300 tokens (dev rules reminder)

**Total per session:** ~2000-3000 tokens (< 2% of typical session budget)

### 11.6 Tool Naming Validation

`descriptive-name.cjs` (PreToolUse Write hook):

Validates file names follow conventions:

```
✓ kebab-case.js
✓ VERY-LONG-DESCRIPTIVE-FILE-NAME.ts
✗ MixedCase.js
✗ generic_name.ts
```

Nudges developer toward self-documenting code.

---

## 12. Integration Points with Claude Code Features

### 12.1 Claude Code Tasks

CK integrates with Claude Code's native Task system:

- **TaskCreate** → Create task in shared list
- **TaskList** → Fetch all tasks
- **TaskGet** → Get single task details
- **TaskUpdate** → Mark complete, update status

**Task Coordination:** `CK_TASK_LIST_ID` env var = plan directory name (shared across sessions)

### 12.2 AskUserQuestion Tool

Privacy block hook uses this for approval gates:

```typescript
// Hook outputs JSON marker
@@PRIVACY_PROMPT_START@@
{ "type": "PRIVACY_PROMPT", "file": ".env", ... }
@@PRIVACY_PROMPT_END@@

// Claude uses AskUserQuestion tool
await AskUserQuestion({
  questions: [{
    question: "Allow reading .env?",
    options: [
      { label: "Yes, approve" },
      { label: "No, skip" }
    ]
  }]
});
```

### 12.3 MCP Servers

Configured in `settings.json`:

```json
{
  "mcpServers": {
    "plugin_claude-mem_mcp-search": {
      "type": "stdio",
      "command": "node",
      "args": ["... mcp-server.cjs"],
      "env": { "CLAUDE_PLUGIN_ROOT": "..." }
    }
  }
}
```

Enables Claude to search persistent agent memory via MCP.

---

## 13. How BA-Kit Should Model This

### 13.1 Essential Components

Minimum viable clone:

1. **`.ck.json`** → Plan naming, paths, project config
2. **`CLAUDE.md`** → Project instructions
3. **`~/.claude/hooks/` subset** → session-init, subagent-init, privacy-block (modified for BA context)
4. **`~/.claude/agents/` subset** → business-analyst, planner, researcher roles
5. **`~/.claude/skills/` subset** → research, brainstorm, business-analysis skills
6. **Plan directory** → `./plans/{date}-{slug}/` with phase files

### 13.2 Customize for BA

Adapt these areas:

| Component | CK Original | BA-Kit Variant |
|-----------|-------------|----------------|
| **Agents** | code-reviewer, tester, debugger | business-analyst, stakeholder-interviewer, requirements-engineer |
| **Skills** | cook, debug, code-review | business-analysis, user-story-mapping, requirement-validation |
| **Hooks** | Dev rules reminder | BA methodology reminder (personas, use cases, acceptance criteria) |
| **Plans** | phase-01-setup-env | phase-01-stakeholder-interviews, phase-02-requirements-analysis |
| **Reports** | Technical analysis | Requirements documents, user story templates, process maps |
| **Memory** | Code patterns | Domain knowledge, stakeholder profiles, requirement patterns |

### 13.3 Key Adaptations

1. **Agent roles** → BA-specific (requirements engineer, UX researcher, stakeholder manager)
2. **Skills** → BA techniques (user story mapping, requirement prioritization, process mapping)
3. **Plan format** → Discovery → Analysis → Validation → Documentation (not Code → Test → Review)
4. **Reports** → Requirements specs, user stories, wireframes, process diagrams
5. **Dev rules** → BA best practices (stakeholder engagement, requirement traceability, acceptance criteria)
6. **Memory** → Stakeholder profiles, domain models, requirement patterns

### 13.4 Hook Customization

Modify hooks for BA:

```javascript
// Instead of project detection for package managers
// Detect: project phase (discovery/analysis/validation/documentation)
// Detect: key stakeholders (from config)
// Detect: requirement categories (functional/non-functional/business rules)

// Instead of "simplify code" reminder
// Inject "define acceptance criteria" reminder
```

---

## Unresolved Questions

1. **How does GSD (get-shit-done) differ from standard CK?** (`/gsd` commands visible in `.claude` directory)
2. **What's the role of `/Users/damtuana/.claude/projects/` directory?**
3. **How does the coding-level configuration affect LLM behavior?** (Found in `.ck.json`: values -1 to 10)
4. **What do the `get-shit-done/` hooks do differently?** (Saw gsd-*.js files in hooks directory)
5. **What's the purpose of the metadata.json file** (416KB)?

---

## Summary

Claude-Kit is a **configuration-driven orchestration framework** that enables:

- **Hooks** inject context at 8 lifecycle points
- **Skills** package reusable task patterns
- **Agents** specialize in distinct roles (research, code-review, testing, etc.)
- **Plans** structure work into phases with detailed task lists
- **Configuration** enables project customization without modifying code
- **Token efficiency** through lean subagent context + minimal session overhead

For BA-Kit, the key is **adopting this architectural pattern** (not copying code) and customizing agents, skills, plans, and hooks for business analysis instead of software development.
