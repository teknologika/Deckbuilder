#!/usr/bin/env bash
set -euo pipefail

# Deckbuilder docs installer
# Usage:
#   ./install-docs.sh            # create files, skip existing
#   ./install-docs.sh --force    # overwrite existing files

FORCE=0
if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

write_file() {
  local path="$1"
  local content="$2"
  if [[ -e "$path" && $FORCE -ne 1 ]]; then
    echo "⏩ Skipping existing $path (use --force to overwrite)"
    return 0
  fi
  mkdir -p "$(dirname "$path")"
  printf "%s" "$content" > "$path"
  echo "✅ Wrote $path"
}

append_file() {
  local path="$1"
  local content="$2"
  mkdir -p "$(dirname "$path")"
  touch "$path"
  printf "\n%s" "$content" >> "$path"
  echo "➕ Appended to $path"
}

# ---------------- content blobs ----------------

read -r -d '' MKDOCS_YML <<'YML'
site_name: Deckbuilder
site_description: Generate professional PowerPoint decks from Markdown/JSON
repo_url: https://github.com/teknologika/Deckbuilder
theme:
  name: material
  features:
    - navigation.sections
    - navigation.tracking
    - navigation.indexes
    - content.code.copy
    - search.suggest
plugins:
  - search
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
            filters: ["!^_"]
markdown_extensions:
  - admonition
  - attr_list
  - fenced_code
  - md_in_html
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.details
  - pymdownx.emoji
  - pymdownx.tabbed
  - pymdownx.tasklist
nav:
  - Home: index.md
  - Tutorials:
      - First deck in 5 minutes: tutorials/first-deck.md
      - Branded templates: tutorials/branded-template.md
  - How-tos:
      - Fonts & proofing language: howtos/fonts-language.md
      - Batch generate decks: howtos/batch.md
      - Run as MCP server: howtos/mcp.md
  - CLI: cli.md
  - API Reference:
      - deckbuilder: reference/deckbuilder.md
      - placekitten: reference/placekitten.md
YML

read -r -d '' INDEX_MD <<'MD'
# Deckbuilder
Generate professional PowerPoint decks from Markdown or JSON — content first, layout second.

## Quick start
```bash
uv add deckbuilder
deckbuilder init
deckbuilder create presentation.md
```

## Why Deckbuilder?
- One-shot deck generation (Markdown + YAML frontmatter, or JSON)
- Smart templates, image handling, and language/font mapping
- CLI + Python API + MCP server

### Links
- [Tutorial: First deck in 5 minutes](tutorials/first-deck.md)
- [CLI reference](../cli.md)
- [Python API](reference/deckbuilder.md)
- [Run as MCP server](howtos/mcp.md)
MD

read -r -d '' TUT_FIRST_MD <<'MD'
# First deck in 5 minutes
```bash
uv add deckbuilder
deckbuilder init
```
Create `presentation.md`:
```markdown
---
layout: Title Slide
---
# **Deckbuilder** Presentation
## Content-first intelligence
```
Build it:
```bash
deckbuilder create presentation.md
open ./Deckbuilder_Presentation.pptx
```
MD

read -r -d '' TUT_BRANDED_MD <<'MD'
# Branded templates
1) Create/choose a template folder (contains `default.pptx` and `default.json`).
2) Set via CLI flags or env vars.
```bash
export DECK_TEMPLATE_FOLDER=/path/to/templates
export DECK_TEMPLATE_NAME=default
deckbuilder --template-folder "$DECK_TEMPLATE_FOLDER" create presentation.md
```
See also: fonts & proofing language.
MD

read -r -d '' HOWTO_FONTLANG_MD <<'MD'
# Fonts & proofing language
You can set these via env vars or CLI (CLI > env > default).
```bash
export DECK_PROOFING_LANGUAGE="en-AU"
export DECK_DEFAULT_FONT="Arial"
```
```bash
deckbuilder create presentation.md --language "English (Australia)" --font "Arial"
deckbuilder config languages
```
MD

read -r -d '' HOWTO_BATCH_MD <<'MD'
# Batch-generate decks
Generate a deck per markdown file in a folder:
```bash
for f in content/*.md; do
  deckbuilder create "$f"
done
```
MD

read -r -d '' HOWTO_MCP_MD <<'MD'
# Run as MCP server (Claude Desktop)
Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "deckbuilder": {
      "command": "deckbuilder-server",
      "env": {
        "DECK_TEMPLATE_FOLDER": "/path/to/Templates",
        "DECK_TEMPLATE_NAME": "default",
        "DECK_OUTPUT_FOLDER": "/path/to/Output",
        "DECK_PROOFING_LANGUAGE": "en-AU",
        "DECK_DEFAULT_FONT": "Calibri"
      }
    }
  }
}
```
MD

read -r -d '' REF_DECKBUILDER_MD <<'MD'
# Python API: deckbuilder
::: deckbuilder
MD

read -r -d '' REF_PLACEKITTEN_MD <<'MD'
# Python API: placekitten
::: placekitten
MD

read -r -d '' CLI_MD <<'MD'
# Command-line interface
<!-- If your Click entry is not deckbuilder.cli:cli, update :module: and :command: -->
::: mkdocs-click
    :module: deckbuilder.cli
    :command: cli
    :depth: 2
MD

read -r -d '' WORKFLOW_YML <<'YML'
name: docs
on:
  push: { branches: [main] }
  workflow_dispatch:
permissions:
  contents: write
  pages: write
  id-token: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv venv
      - run: uv pip install mkdocs mkdocs-material mkdocstrings[python] mkdocs-click pymdown-extensions
      - run: mkdocs build --strict
      - uses: actions/upload-pages-artifact@v3
        with: { path: site }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: { name: github-pages }
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
YML

read -r -d '' PRECOMMIT_APPEND <<'YML'

# --- Docs quality gates ---
- repo: https://github.com/pycqa/pydocstyle
  rev: 6.3.0
  hooks:
    - id: pydocstyle
      args: [--convention=google, --add-ignore=D105,D107]

- repo: https://github.com/econchick/interrogate
  rev: 1.7.0
  hooks:
    - id: interrogate
      args: [--fail-under=80, --verbose, --quiet, -i, src]
YML

# ---------------- write files ----------------

write_file "mkdocs.yml" "$MKDOCS_YML"

write_file "docs/index.md" "$INDEX_MD"
write_file "docs/tutorials/first-deck.md" "$TUT_FIRST_MD"
write_file "docs/tutorials/branded-template.md" "$TUT_BRANDED_MD"
write_file "docs/howtos/fonts-language.md" "$HOWTO_FONTLANG_MD"
write_file "docs/howtos/batch.md" "$HOWTO_BATCH_MD"
write_file "docs/howtos/mcp.md" "$HOWTO_MCP_MD"
write_file "docs/reference/deckbuilder.md" "$REF_DECKBUILDER_MD"
write_file "docs/reference/placekitten.md" "$REF_PLACEKITTEN_MD"
write_file "docs/cli.md" "$CLI_MD"

write_file ".github/workflows/docs.yml" "$WORKFLOW_YML"

# Pre-commit: create or append
if [[ -f ".pre-commit-config.yaml" ]]; then
  append_file ".pre-commit-config.yaml" "$PRECOMMIT_APPEND"
else
  write_file ".pre-commit-config.yaml" "$PRECOMMIT_APPEND"
fi

cat <<'TXT'

🎉 Done.
Next steps:
  1) Install dev deps:
     uv add -d mkdocs mkdocs-material mkdocstrings[python] mkdocs-click pymdown-extensions

  2) Preview locally:
     mkdocs serve   # visit http://127.0.0.1:8000

  3) Commit & PR:
     git checkout -b docs/site-mkdocs && git add -A && git commit -m "docs: MkDocs site" && git push -u origin docs/site-mkdocs
     gh pr create --fill --title "Docs overhaul: product-grade site"

⚙️ If your Click entry module isn't 'deckbuilder.cli:cli', edit docs/cli.md accordingly.
TXT
