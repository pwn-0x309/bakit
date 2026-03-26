#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/ba-kit-md-to-html.XXXXXX")"
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$TMP_DIR/designs/test-flow"

python3 - "$TMP_DIR/designs/test-flow/SCR-01-login.png" <<'PY'
import base64
import pathlib
import sys

png = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8"
    "/w8AAgMBgI6D+wAAAABJRU5ErkJggg=="
)
pathlib.Path(sys.argv[1]).write_bytes(base64.b64decode(png))
PY

cat >"$TMP_DIR/sample.md" <<'EOF'
# Sample BA Output

## Risks & Constraints <Review>

1. Capture credentials
  - Show username field
  - Show password field with reference `designs/test-flow/SCR-01-login.png`
2. Validate sign-in
  1. Reject empty values
  2. Show an inline error

- Delivery packaging
  1. Generate stakeholder HTML
  2. Preserve Mermaid blocks

> Stakeholder copy should render without editing controls.

| Artifact | Status |
| --- | --- |
| FRD | Ready |
| SRS | Ready |

```mermaid
flowchart TD
  A[User submits] --> B{Valid?}
  B -- Yes --> C[Continue]
  B -- No --> D[Show error]
```

```bash
echo "package"
```
EOF

python3 "$ROOT_DIR/scripts/md-to-html.py" --base-dir "$TMP_DIR" --no-editor "$TMP_DIR/sample.md"

OUTPUT_HTML="$TMP_DIR/sample.html"
test -f "$OUTPUT_HTML"

python3 - "$OUTPUT_HTML" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys


class Probe(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.ids = set()
        self.has_table = False
        self.has_blockquote = False
        self.has_mermaid = False
        self.has_bash = False
        self.has_nav = False
        self.has_image = False
        self.has_nested_ol_ul = False
        self.has_nested_ul_ol = False
        self.raw_html = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.stack.append((tag, attrs))
        element_ids = attrs.get("id")
        if element_ids:
            self.ids.add(element_ids)
        if tag == "table":
            self.has_table = True
        elif tag == "blockquote":
            self.has_blockquote = True
        elif tag == "nav" and attrs.get("class") == "toc":
            self.has_nav = True
        elif tag == "img" and attrs.get("src", "").startswith("data:image/png;base64,"):
            self.has_image = True
        elif tag == "pre" and attrs.get("class") == "mermaid":
            self.has_mermaid = True
        elif tag == "code" and attrs.get("class") == "language-bash":
            self.has_bash = True

        parent_tags = [name for name, _ in self.stack[:-1]]
        if tag == "ul" and parent_tags[-2:] == ["ol", "li"]:
            self.has_nested_ol_ul = True
        if tag == "ol" and parent_tags[-2:] == ["ul", "li"]:
            self.has_nested_ul_ol = True

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


html = Path(sys.argv[1]).read_text(encoding="utf-8")
probe = Probe()
probe.feed(html)

assert "editor-toolbar" not in probe.ids, "Unexpected editor toolbar found in read-only output"
assert probe.has_nav, "Missing table of contents"
assert probe.has_table, "Missing table"
assert probe.has_blockquote, "Missing blockquote"
assert probe.has_mermaid, "Missing Mermaid block"
assert probe.has_bash, "Missing bash code block"
assert probe.has_image, "Missing embedded image"
assert probe.has_nested_ol_ul, "Missing ordered list with nested unordered list"
assert probe.has_nested_ul_ol, "Missing unordered list with nested ordered list"
assert html.count('<pre class="mermaid">') == 1, "Unexpected Mermaid block count"
assert html.count('</code></pre>') == 1, "Unexpected fenced code closing count"
assert 'Risks &amp; Constraints &lt;Review&gt;' in html, "TOC/body heading escaping regression"
PY

grep -q '<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>' "$OUTPUT_HTML"

echo "Smoke test passed: $OUTPUT_HTML"
