# Design Artifacts

Use this directory for project runtime `DESIGN.md` rules and Stitch UI exports that support SRS screen specifications.

## Stitch MCP Default

Wireframes and UI layouts are generated using **Stitch MCP**. Local `.pen` offline layout files are deprecated.

- Generate UI variants via Stitch MCP `generate_screen_from_text` or `generate_variants`.
- Maintain the state locally in `designs/{slug}/stitch-state.json`.
- Export physical PNGs referencing the generated Screen IDs to `designs/{slug}/exports/{artifact-name}/{screen-id}.png`.

## Rules

- Link each SRS screen section to the relevant Stitch Project ID and Screen ID.
- Keep supporting state screen IDs aligned between the SRS screen inventory and Stitch variants (e.g. Empty State, Error State).
- If a single Stitch Project covers multiple screens, list the covered screen IDs in the SRS and identify the target Screen ID per use-case.
- Supporting frames may be inventory-only in the SRS, but they should still be present in the Stitch Project Cloud when needed for states such as empty data, errors, confirmations, or feedback messages.
