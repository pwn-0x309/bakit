# Pencil Artifacts

Use this directory for Pencil wireframe artifacts that support SRS screen specifications.

## Convention

- Store `.pen` files under `designs/`
- Prefer one subdirectory per initiative or product area
- Prefer one artifact per flow, module, or coherent screen pack
- Allow one `.pen` file to contain multiple frames
- Prefix each screen frame with its SRS screen ID, for example `SCR-01 - Login`
- Give modal, drawer, dialog, or overlay screens their own primary `SCR-xx` IDs when they influence flow or have distinct interaction rules
- Prefix supporting state frames with the parent screen ID plus a stable suffix, for example `SCR-01-EMPTY - Login Empty State` or `SCR-01-TOAST-SUCCESS - Login Success Toast`

Example paths:
- `designs/customer-portal/auth-flow.pen`
- `designs/customer-portal/dashboard-core.pen`
- `designs/customer-portal/exports/auth-flow/SCR-01-login.png`

## Usage

- Link each SRS screen section to the relevant `.pen` artifact and exact frame
- Keep screen IDs aligned between the SRS and Pencil frame names
- Keep supporting state frame IDs aligned between the SRS screen inventory and Pencil frame names
- Use the `.pen` file as the low-fidelity wireframe source of truth

## Notes

- Pencil is used here for wireframes only, not design-to-code generation
- If a single `.pen` file covers multiple screens, list the covered screen IDs in the SRS and identify the target frame per screen
- Supporting frames may be inventory-only in the SRS, but they should still be present in the `.pen` artifact when needed for states such as empty data, errors, confirmations, or feedback messages
