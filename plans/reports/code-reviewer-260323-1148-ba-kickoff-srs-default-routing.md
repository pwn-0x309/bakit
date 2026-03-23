# Code Review: ba-kickoff SRS Default Routing

**Reviewer:** code-reviewer
**Date:** 2026-03-23
**Commit:** dfd91cc

## Scope

- Files reviewed: `skills/ba-kickoff/SKILL.md`, `skills/ba-requirements/SKILL.md`
- Supporting files checked: `templates/srs-template.md`, `skills/ba-discovery/SKILL.md`, `docs/skill-catalog.md`
- Focus: instruction quality, routing logic clarity, cross-skill consistency
- Change type: markdown skill definition (not code)

## Overall Assessment

The changes are well-structured and achieve their goal: making SRS a default deliverable when the intake signals UI, system interactions, or mobile/web scope. The routing logic is clear, the execution sequence is sound, and the integration with ba-requirements Phase 2 (wireframe generation) is correctly referenced. Five observations below, none critical.

## High Priority

### 1. Skill catalog chain is now stale

`docs/skill-catalog.md` line 32 shows the "Kickoff from Raw Input" chain as:

```
ba-kickoff -> ba-discovery -> ba-stakeholder -> ba-requirements -> ba-process-mapping -> ba-compliance
```

The updated ba-kickoff SKILL.md (line 96) now shows:

```
ba-discovery -> ba-stakeholder -> ba-requirements (FRD + SRS) -> ba-user-stories -> ba-process-mapping -> ba-compliance
```

Two mismatches: (a) the catalog omits `ba-user-stories`, (b) the catalog does not show `(FRD + SRS)`. The skill catalog is the cross-reference document other skills and agents consult. Leaving it out of sync risks downstream agents following the old chain.

**Recommendation:** Update `docs/skill-catalog.md` line 32 to match the new chain.

### 2. Overlap between document-selection table and SRS-default-routing block

The table at line 77 already has a row: "System spec with screens and test cases -> SRS -> ba-requirements -> srs-template.md". The new routing block (lines 87-93) adds a second, broader trigger list for SRS. An agent following the instructions could interpret these as two independent decision points, potentially double-selecting SRS or being confused about which rule takes precedence.

**Recommendation:** Add a clarifying sentence after the routing block, e.g.: "This routing supplements the table above. When SRS is triggered by the conditions below, it is added alongside FRD even if the table row for SRS was not explicitly selected."

## Medium Priority

### 3. Step 7 naming gap for FRD output

Step 7 (line 121) says "Invoke ba-requirements for FRD first" but does not specify the FRD output path. The SRS naming is given (`plans/reports/srs-{date}-{slug}.md`) but the FRD naming is not. An agent executing this step has no path convention for FRD, which could cause inconsistent file placement.

**Recommendation:** Add an FRD naming line: `**FRD naming:** plans/reports/frd-{date}-{slug}.md` (or whatever convention applies).

### 4. SRS routing triggers are broad

The trigger "Mobile or web application scope" would activate SRS for virtually every modern project. This is likely intentional (the commit message says "when UI screens, system interactions, or mobile/web app scope is present"), but it means SRS will rarely be skipped. If this is the desired default, fine. If not, the trigger could be narrowed to "Mobile or web application scope with defined screens or interactions."

**Recommendation:** Confirm intent. If SRS-by-default is the goal for any app project, the current wording is correct. If selectivity is preferred, tighten the mobile/web trigger.

### 5. Quality check items reference ba-requirements Phase 2 but do not define fallback

Line 159: "SRS references correct template and follows ba-requirements Phase 2 for wireframe generation." If the user skips wireframes (ba-requirements Phase 2 Step 2.2 allows "Skip wireframes"), this quality check would technically fail. The ba-requirements quality checks handle this with "(unless user explicitly skipped)" but the ba-kickoff quality check does not include that caveat.

**Recommendation:** Append "(unless user explicitly skipped wireframes)" to line 159 for consistency with ba-requirements quality checks.

## Low Priority

None.

## Positive Observations

- The two-pass invocation model (FRD first, SRS second using FRD as input) is a clean separation that avoids scope bloat in a single pass
- Explicit cross-reference to ba-requirements Phase 2 for wireframe generation avoids duplicating instructions
- The skill chain update correctly inserts `ba-user-stories` which was missing from the original chain
- Quality checks are specific and verifiable

## Recommended Actions

1. **Update `docs/skill-catalog.md`** to reflect the new chain and `(FRD + SRS)` annotation
2. **Add a disambiguation sentence** between the document-selection table and the SRS-routing block
3. **Add FRD naming convention** in Step 7
4. **Add wireframe-skip caveat** to quality check line 159
5. **Confirm intent** on breadth of SRS triggers (especially "Mobile or web application scope")

## Unresolved Questions

- Is the intent for SRS to be default on virtually all app projects (current wording), or only when screens/interactions are explicitly described in the intake?
- Should the skill catalog "Discovery to Formal Requirements" chain (line 36) also be updated to show `(FRD + SRS)` when applicable?
