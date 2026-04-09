# Bản đồ wireframe (Wireframe Map)

## Thông tin bộ artifact (Artifact Set Information)

- Slug: [initiative-slug]
- Date: [YYMMDD-HHmm]
- Module: [module-slug]
- Source DESIGN.md: `designs/{slug}/DESIGN.md`
- Source input pack: `plans/{slug}-{date}/03_modules/{module_slug}/wireframe-input.md`
- State marker: `plans/{slug}-{date}/03_modules/{module_slug}/wireframe-state.md`

## Artifact Summary

| Artifact Name | Stitch Project ID | Export Folder | Included Primary Screens | Included Supporting Screens |
| --- | --- | --- | --- | --- |
| [artifact-name] | [ID] | `designs/{slug}/exports/[artifact-name]/` | [SCR-01, SCR-02] | [SCR-01-EMPTY, SCR-01-ERROR] |

## Screen To UI Mapping

| Screen ID | Screen Name | Classification | Stitch Project ID | Stitch Screen ID | Export PNG | Supporting Screens | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCR-01 | [Screen] | Primary screen | [Project ID] | [Screen ID] | `designs/{slug}/exports/[artifact-name]/SCR-01-[screen-name].png` | [SCR-01-EMPTY, SCR-01-ERROR] | [Mapping notes] |

## Supporting Screen Inventory

| Screen ID | Parent Screen | Classification | Stitch Project ID | Stitch Screen ID | Reason |
| --- | --- | --- | --- | --- | --- |
| SCR-01-EMPTY | SCR-01 | Supporting state | [Project ID] | [Screen ID] | [Why this state exists] |

## Coverage Checks

- Every primary screen in the input pack has a Stitch Screen generated
- Every required supporting state inferred during wireframing is mapped to Stitch
- Every exported PNG path matches the actual generated layout
- Frame names preserve screen IDs for SRS linkback
- Wireframe outputs remain aligned with the approved `DESIGN.md`
