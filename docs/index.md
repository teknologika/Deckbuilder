# Deckbuilder

Turn Markdown or JSON into `.pptx` decks with templates, images, and language settings — all from an MCP Server, CLI or Python API.

---

## Install

```bash
uv add deckbuilder
```

---

## Basic usage

```bash
# Create template folder
deckbuilder init

# Build from Markdown
deckbuilder create slides.md

# Build from JSON
deckbuilder create slides.json
```

---

## Features

- **Markdown / JSON input** — YAML frontmatter supported.
- **Template system** — `.pptx` + JSON layout definitions.
- **CLI subcommands** — `create`, `template`, `image`, `pattern`, `config`, `remap`, and more.
- **Image handling** — generate, crop, and embed.
- **Language & font control** — per-deck proofing language and font.
- **MCP server mode** — run under Claude Desktop.

---

## Environment variables

| Variable                 | Purpose                     |
| ------------------------ | --------------------------- |
| `DECK_TEMPLATE_FOLDER`   | Path to template folder     |
| `DECK_TEMPLATE_NAME`     | Template file name (no ext) |
| `DECK_OUTPUT_FOLDER`     | Output directory            |
| `DECK_PROOFING_LANGUAGE` | Proofing language code      |
| `DECK_DEFAULT_FONT`      | Default font family         |

---

## Docs

- [Quick start](tutorials/first-deck.md)
- [Branded templates](tutorials/branded-template.md)
- [Fonts & proofing language](howtos/fonts-language.md)
- [Run as MCP server](howtos/mcp.md)
- [CLI reference](cli.md)
- [Python API](reference/deckbuilder.md)
