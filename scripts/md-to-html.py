#!/usr/bin/env python3
"""Convert BA markdown documents to HTML with rendered Mermaid diagrams and embedded images.

Usage:
    python scripts/md-to-html.py plans/reports/frd-260325-project.md
    python scripts/md-to-html.py plans/reports/srs-260325-project.md

Works with any BA-kit document: FRD (Mermaid workflows), SRS (wireframe images + diagrams),
user stories, or any markdown file.

Supports:
    - Mermaid diagrams (rendered client-side via mermaid.js CDN)
    - Inline wireframe images from explicit PNG references in the markdown
    - In-browser editing without touching raw HTML code
    - Page breaks for PDF printing (browser Print → Save as PDF)
    - Table of contents generation
"""

import argparse
import base64
import re
import sys
from pathlib import Path

# Minimal markdown-to-html without external deps.
# Handles: headings, tables, bold, italic, code blocks, lists, blockquotes, links, images.


def embed_image(img_path: str, base_dir: Path) -> str:
    """Convert image path to base64 data URI."""
    full_path = base_dir / img_path
    if not full_path.exists():
        return f'<span class="missing-image">[Missing image: {img_path}]</span>'
    suffix = full_path.suffix.lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "webp": "image/webp"}.get(suffix.lstrip("."), "image/png")
    data = base64.b64encode(full_path.read_bytes()).decode()
    return f'<img src="data:{mime};base64,{data}" alt="{full_path.stem}" class="wireframe">'


def md_to_html(md: str, base_dir: Path) -> str:
    """Convert markdown to HTML with embedded images."""
    lines = md.split("\n")
    html_parts = []
    toc = []
    in_code = False
    in_table = False
    in_list = False
    code_lang = ""
    table_rows = []

    def flush_table():
        nonlocal table_rows, in_table
        if not table_rows:
            return ""
        out = '<table>\n<thead>\n<tr>'
        headers = [c.strip() for c in table_rows[0].strip("|").split("|")]
        for h in headers:
            out += f"<th>{inline(h)}</th>"
        out += "</tr>\n</thead>\n<tbody>\n"
        # Skip separator row (index 1)
        for row in table_rows[2:]:
            out += "<tr>"
            cells = [c.strip() for c in row.strip("|").split("|")]
            for c in cells:
                out += f"<td>{inline(c)}</td>"
            out += "</tr>\n"
        out += "</tbody>\n</table>\n"
        table_rows = []
        in_table = False
        return out

    def flush_list():
        nonlocal in_list
        in_list = False
        return "</ul>\n"

    def inline(text: str) -> str:
        """Process inline markdown: bold, italic, code, links, images."""
        # Images: ![alt](path)
        text = re.sub(
            r"!\[([^\]]*)\]\(([^)]+)\)",
            lambda m: embed_image(m.group(2), base_dir),
            text,
        )
        # Links
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
        # Bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        # Italic
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        # Inline code
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        return text

    for line in lines:
        # Code blocks
        if line.startswith("```"):
            if in_code:
                html_parts.append("</code></pre>\n")
                in_code = False
            else:
                code_lang = line[3:].strip()
                cls = f' class="language-{code_lang}"' if code_lang else ""
                if code_lang == "mermaid":
                    html_parts.append(f'<pre class="mermaid">')
                else:
                    html_parts.append(f"<pre><code{cls}>")
                in_code = True
            continue
        if in_code:
            if code_lang == "mermaid":
                html_parts.append(line + "\n")
            else:
                from html import escape
                html_parts.append(escape(line) + "\n")
            continue

        # Table detection
        if "|" in line and line.strip().startswith("|"):
            if not in_table:
                if in_list:
                    html_parts.append(flush_list())
                in_table = True
                table_rows = []
            table_rows.append(line)
            continue
        elif in_table:
            html_parts.append(flush_table())

        # List items
        if re.match(r"^[-*]\s", line.strip()):
            if not in_list:
                in_list = True
                html_parts.append("<ul>\n")
            item = re.sub(r"^[-*]\s", "", line.strip())
            html_parts.append(f"<li>{inline(item)}</li>\n")
            continue
        elif in_list and line.strip():
            html_parts.append(flush_list())

        # Empty line
        if not line.strip():
            if in_list:
                html_parts.append(flush_list())
            html_parts.append("\n")
            continue

        # Headings
        m = re.match(r"^(#{1,6})\s+(.+)", line)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            toc.append((level, text, slug))
            # Page break before h1 and h2 (except first)
            if level <= 2 and len(toc) > 1:
                html_parts.append('<div class="page-break"></div>\n')
            html_parts.append(f'<h{level} id="{slug}">{inline(text)}</h{level}>\n')
            continue

        # Blockquote
        if line.startswith(">"):
            text = line.lstrip("> ")
            html_parts.append(f"<blockquote>{inline(text)}</blockquote>\n")
            continue

        # Horizontal rule
        if re.match(r"^[-*_]{3,}$", line.strip()):
            html_parts.append("<hr>\n")
            continue

        # Paragraph
        html_parts.append(f"<p>{inline(line)}</p>\n")

    # Flush remaining
    if in_table:
        html_parts.append(flush_table())
    if in_list:
        html_parts.append(flush_list())

    # Build TOC
    toc_html = '<nav class="toc"><h2>Table of Contents</h2>\n<ul>\n'
    for level, text, slug in toc:
        indent = "  " * (level - 1)
        toc_html += f'{indent}<li class="toc-{level}"><a href="#{slug}">{text}</a></li>\n'
    toc_html += "</ul>\n</nav>\n"

    body = "".join(html_parts)
    return toc_html + body


CSS = """
:root {
    --primary: #1a1a2e;
    --accent: #0f3460;
    --accent-soft: #d9edf7;
    --bg: #ffffff;
    --text: #1a1a1a;
    --border: #e0e0e0;
    --code-bg: #f5f5f5;
    --toolbar-bg: rgba(255, 255, 255, 0.96);
    --danger: #b42318;
    --success: #0f7b6c;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6; color: var(--text); background: #f5f7fb;
    margin: 0; padding: 0;
}
.editor-shell {
    max-width: 1180px;
    margin: 0 auto;
    padding: 24px 20px 48px;
}
.editor-toolbar {
    position: sticky;
    top: 12px;
    z-index: 1000;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    padding: 14px 16px;
    margin-bottom: 20px;
    background: var(--toolbar-bg);
    border: 1px solid rgba(15, 52, 96, 0.14);
    border-radius: 14px;
    box-shadow: 0 10px 30px rgba(15, 52, 96, 0.08);
    backdrop-filter: blur(12px);
}
.editor-toolbar__group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
}
.editor-toolbar__status {
    margin-left: auto;
    font-size: 0.92rem;
    color: #42526b;
}
.editor-button {
    appearance: none;
    border: 1px solid rgba(15, 52, 96, 0.16);
    background: #fff;
    color: var(--accent);
    padding: 9px 12px;
    border-radius: 10px;
    font-size: 0.92rem;
    font-weight: 600;
    cursor: pointer;
}
.editor-button:hover {
    background: #f0f6ff;
}
.editor-button.is-primary {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
}
.editor-button.is-danger {
    color: var(--danger);
    border-color: rgba(180, 35, 24, 0.18);
}
.editor-help {
    width: 100%;
    font-size: 0.88rem;
    color: #52627a;
}
.document-surface {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px;
    background: var(--bg);
    border: 1px solid rgba(15, 52, 96, 0.08);
    border-radius: 18px;
    box-shadow: 0 16px 40px rgba(15, 52, 96, 0.08);
}
h1 { font-size: 2em; color: var(--primary); margin: 1.5em 0 0.5em; border-bottom: 2px solid var(--accent); padding-bottom: 0.3em; }
h2 { font-size: 1.5em; color: var(--accent); margin: 1.2em 0 0.4em; }
h3 { font-size: 1.2em; margin: 1em 0 0.3em; }
h4,h5,h6 { margin: 0.8em 0 0.2em; }
p { margin: 0.5em 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.9em; }
th, td { border: 1px solid var(--border); padding: 8px 12px; text-align: left; }
th { background: var(--accent); color: white; font-weight: 600; }
tr:nth-child(even) { background: #f9f9f9; }
pre { background: var(--code-bg); padding: 16px; border-radius: 6px; overflow-x: auto; margin: 1em 0; }
code { font-family: 'SF Mono', Consolas, monospace; font-size: 0.9em; }
blockquote { border-left: 4px solid var(--accent); padding: 0.5em 1em; margin: 1em 0; background: #f0f4ff; font-style: italic; }
ul { margin: 0.5em 0 0.5em 1.5em; }
li { margin: 0.2em 0; }
img.wireframe { max-width: 100%; border: 1px solid var(--border); border-radius: 8px; margin: 1em 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.missing-image { color: #d32f2f; font-style: italic; padding: 1em; background: #fff3f3; border: 1px dashed #d32f2f; border-radius: 4px; }
.toc { background: #f8f9fa; border: 1px solid var(--border); border-radius: 8px; padding: 1.5em; margin-bottom: 2em; }
.toc h2 { margin-top: 0; font-size: 1.2em; }
.toc ul { list-style: none; margin: 0; padding: 0; }
.toc li { margin: 0.3em 0; }
.toc .toc-1 { font-weight: 600; }
.toc .toc-2 { padding-left: 1.5em; }
.toc .toc-3 { padding-left: 3em; font-size: 0.9em; }
.toc a { color: var(--accent); text-decoration: none; }
.toc a:hover { text-decoration: underline; }
.page-break { page-break-before: always; }
.editable-block {
    position: relative;
    transition: outline-color 0.15s ease, box-shadow 0.15s ease;
}
.editing-active .editable-block:hover {
    outline: 2px dashed rgba(15, 52, 96, 0.24);
    outline-offset: 6px;
}
.editable-selected {
    outline: 2px solid var(--accent);
    outline-offset: 6px;
    box-shadow: 0 0 0 6px rgba(15, 52, 96, 0.08);
}
.editing-active [contenteditable="true"] {
    cursor: text;
}
.editing-active [contenteditable="true"]:focus {
    outline: 2px solid rgba(15, 52, 96, 0.24);
    border-radius: 6px;
    background: rgba(217, 237, 247, 0.22);
}
.editing-active img.wireframe {
    cursor: pointer;
}
.editor-hidden {
    display: none !important;
}
@media print {
    body { background: #fff; }
    .editor-shell { max-width: none; padding: 0; }
    .document-surface { max-width: none; padding: 0; border: none; border-radius: 0; box-shadow: none; }
    .editor-toolbar { display: none !important; }
    .toc { page-break-after: always; }
    .page-break { page-break-before: always; }
    table { page-break-inside: avoid; }
    img.wireframe { page-break-inside: avoid; max-height: 80vh; }
}
"""


EDITOR_JS = r"""
const EditorApp = (() => {
  const BLOCK_SELECTOR = 'p, h1, h2, h3, h4, h5, h6, blockquote, ul, ol, table, pre, img.wireframe, hr';
  const TEXT_SELECTOR = 'p, h1, h2, h3, h4, h5, h6, blockquote, li, td, th';
  let selectedBlock = null;
  let editMode = false;

  const qs = (selector) => document.querySelector(selector);
  const qsa = (selector) => Array.from(document.querySelectorAll(selector));

  function getSurface() {
    return qs('#document-surface');
  }

  function getStatus() {
    return qs('#editor-status');
  }

  function ensureEditableBlocks() {
    qsa('#document-surface .editable-block').forEach((node) => node.classList.remove('editable-block'));
    qsa('#document-surface ' + BLOCK_SELECTOR).forEach((node) => {
      if (node.closest('#editor-toolbar')) return;
      node.classList.add('editable-block');
    });
  }

  function applyEditMode() {
    document.body.classList.toggle('editing-active', editMode);
    qsa('#document-surface ' + TEXT_SELECTOR).forEach((node) => {
      node.setAttribute('contenteditable', editMode ? 'true' : 'false');
      node.setAttribute('spellcheck', editMode ? 'true' : 'false');
    });
    const toggle = qs('[data-action="toggle-edit"]');
    if (toggle) {
      toggle.textContent = editMode ? 'Disable Editing' : 'Enable Editing';
      toggle.classList.toggle('is-primary', editMode);
    }
    getStatus().textContent = editMode
      ? 'Editing enabled. Click a block to select it, then edit text or use the toolbar.'
      : 'Editing disabled. Enable it to modify text, replace images, or add/remove blocks.';
  }

  function selectBlock(node) {
    if (selectedBlock) selectedBlock.classList.remove('editable-selected');
    selectedBlock = node;
    if (selectedBlock) selectedBlock.classList.add('editable-selected');
    updateSelectionStatus();
  }

  function updateSelectionStatus() {
    if (!selectedBlock) return;
    const label = selectedBlock.tagName.toLowerCase();
    getStatus().textContent = editMode
      ? `Editing enabled. Selected ${label} block.`
      : `Selected ${label} block. Enable editing to modify it.`;
  }

  function closestBlock(target) {
    if (!(target instanceof Element)) return null;
    return target.closest(BLOCK_SELECTOR);
  }

  function addParagraph() {
    const p = document.createElement('p');
    p.textContent = 'New paragraph';
    insertAfterSelection(p);
  }

  function addHeading() {
    const h = document.createElement('h2');
    h.textContent = 'New section';
    insertAfterSelection(h);
  }

  function addImageFromFile(file, replace = false) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const img = replace && selectedBlock?.tagName === 'IMG'
        ? selectedBlock
        : document.createElement('img');
      img.src = reader.result;
      img.alt = file.name.replace(/\.[^.]+$/, '');
      img.className = 'wireframe editable-block';
      if (!replace || selectedBlock?.tagName !== 'IMG') {
        insertAfterSelection(img);
      }
      ensureEditableBlocks();
      selectBlock(img);
    };
    reader.readAsDataURL(file);
  }

  function requestImage(replace = false) {
    const input = qs('#editor-image-input');
    input.dataset.replace = replace ? 'true' : 'false';
    input.click();
  }

  function insertAfterSelection(node) {
    const surface = getSurface();
    if (!surface) return;
    if (selectedBlock && selectedBlock.parentNode) {
      selectedBlock.parentNode.insertBefore(node, selectedBlock.nextSibling);
    } else {
      surface.appendChild(node);
    }
    ensureEditableBlocks();
    applyEditMode();
    selectBlock(node);
    if (node.matches?.(TEXT_SELECTOR)) node.focus();
  }

  function deleteSelected() {
    if (!selectedBlock) return;
    const next = selectedBlock.nextElementSibling || selectedBlock.previousElementSibling;
    selectedBlock.remove();
    ensureEditableBlocks();
    selectBlock(next ? closestBlock(next) || next : null);
    if (!selectedBlock) getStatus().textContent = 'Block removed.';
  }

  function duplicateSelected() {
    if (!selectedBlock) return;
    const clone = selectedBlock.cloneNode(true);
    selectedBlock.parentNode.insertBefore(clone, selectedBlock.nextSibling);
    ensureEditableBlocks();
    applyEditMode();
    selectBlock(clone);
  }

  function rebuildToc() {
    const toc = qs('.toc');
    const surface = getSurface();
    if (!toc || !surface) return;
    const headings = qsa('#document-surface h1, #document-surface h2, #document-surface h3');
    const list = toc.querySelector('ul');
    if (!list) return;
    list.innerHTML = '';
    headings.forEach((heading) => {
      const level = Number(heading.tagName.slice(1));
      const rawText = heading.textContent.trim() || heading.tagName;
      const slug = rawText.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || `section-${level}`;
      heading.id = slug;
      const li = document.createElement('li');
      li.className = `toc-${level}`;
      const a = document.createElement('a');
      a.href = `#${slug}`;
      a.textContent = rawText;
      li.appendChild(a);
      list.appendChild(li);
    });
  }

  function prepareCleanClone() {
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll('.editable-selected').forEach((node) => node.classList.remove('editable-selected'));
    clone.querySelectorAll('.editable-block').forEach((node) => node.classList.remove('editable-block'));
    clone.querySelectorAll('[contenteditable]').forEach((node) => node.removeAttribute('contenteditable'));
    clone.querySelectorAll('[spellcheck]').forEach((node) => node.removeAttribute('spellcheck'));
    clone.querySelectorAll('body').forEach((body) => body.classList.remove('editing-active'));
    return clone;
  }

  function downloadEditedHtml() {
    rebuildToc();
    const html = '<!DOCTYPE html>\n' + prepareCleanClone().outerHTML;
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${document.title || 'ba-output'}-edited.html`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function bindEvents() {
    document.addEventListener('click', (event) => {
      const actionTarget = event.target.closest('[data-action]');
      if (actionTarget) {
        const action = actionTarget.dataset.action;
        if (action === 'toggle-edit') {
          editMode = !editMode;
          applyEditMode();
        } else if (action === 'add-paragraph') {
          addParagraph();
        } else if (action === 'add-heading') {
          addHeading();
        } else if (action === 'add-image') {
          requestImage(false);
        } else if (action === 'replace-image') {
          requestImage(true);
        } else if (action === 'delete-block') {
          deleteSelected();
        } else if (action === 'duplicate-block') {
          duplicateSelected();
        } else if (action === 'rebuild-toc') {
          rebuildToc();
          getStatus().textContent = 'Table of contents refreshed.';
        } else if (action === 'download-html') {
          downloadEditedHtml();
        }
        event.preventDefault();
        return;
      }

      const block = closestBlock(event.target);
      if (block && block.closest('#document-surface')) {
        selectBlock(block);
      }
    });

    qs('#editor-image-input')?.addEventListener('change', (event) => {
      const input = event.target;
      const [file] = input.files || [];
      addImageFromFile(file, input.dataset.replace === 'true');
      input.value = '';
    });
  }

  function init() {
    ensureEditableBlocks();
    bindEvents();
    editMode = true;
    applyEditMode();
    rebuildToc();
  }

  return { init };
})();

window.addEventListener('DOMContentLoaded', EditorApp.init);
"""


def convert(md_path: Path) -> Path:
    """Convert any BA markdown to HTML with embedded images and Mermaid support."""
    base_dir = md_path.parent.parent.parent  # plans/reports/srs.md → project root
    md = md_path.read_text(encoding="utf-8")

    # Convert wireframe file references to embedded images
    # Pattern: `designs/.../*.png`
    md = re.sub(
        r"`(designs/[^`]+\.png)`",
        r"![\1](\1)",
        md,
    )

    body = md_to_html(md, base_dir)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{md_path.stem}</title>
<style>{CSS}</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true}});</script>
<script>{EDITOR_JS}</script>
</head>
<body>
<div class="editor-shell">
  <div id="editor-toolbar" class="editor-toolbar">
    <div class="editor-toolbar__group">
      <button class="editor-button is-primary" data-action="toggle-edit" type="button">Disable Editing</button>
      <button class="editor-button" data-action="add-paragraph" type="button">Add Paragraph</button>
      <button class="editor-button" data-action="add-heading" type="button">Add Heading</button>
      <button class="editor-button" data-action="add-image" type="button">Add Image</button>
      <button class="editor-button" data-action="replace-image" type="button">Replace Image</button>
      <button class="editor-button" data-action="duplicate-block" type="button">Duplicate Block</button>
      <button class="editor-button is-danger" data-action="delete-block" type="button">Delete Block</button>
      <button class="editor-button" data-action="rebuild-toc" type="button">Refresh TOC</button>
      <button class="editor-button" data-action="download-html" type="button">Download Edited HTML</button>
    </div>
    <div id="editor-status" class="editor-toolbar__status">Editing enabled. Click a block to select it, then edit text or use the toolbar.</div>
    <div class="editor-help">You can edit text directly, replace wireframe images from local files, add new headings or paragraphs, remove blocks, then download a clean HTML copy without touching source code.</div>
  </div>
  <input id="editor-image-input" class="editor-hidden" type="file" accept="image/png,image/jpeg,image/webp,image/gif,image/svg+xml">
  <main id="document-surface" class="document-surface">
{body}
  </main>
</div>
</body>
</html>"""

    out_path = md_path.with_suffix(".html")
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Convert BA markdown to HTML with Mermaid diagrams and embedded images")
    parser.add_argument("input", help="Path to markdown file (FRD, SRS, or any BA document)")
    args = parser.parse_args()

    md_path = Path(args.input)
    if not md_path.exists():
        print(f"Error: {md_path} not found", file=sys.stderr)
        sys.exit(1)

    out = convert(md_path)
    print(f"Generated: {out}")


if __name__ == "__main__":
    main()
