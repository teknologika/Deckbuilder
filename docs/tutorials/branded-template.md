# Branded templates

1. Create a template folder with `default.pptx` and `default.json`.
2. Point Deckbuilder at it via CLI or env vars:

```bash
export DECK_TEMPLATE_FOLDER=/path/to/templates
export DECK_TEMPLATE_NAME=default
deckbuilder --template-folder "$DECK_TEMPLATE_FOLDER" create slides.md
```

Tips:
- Keep brand fonts installed locally to avoid PowerPoint substitutions.
- Store your template folder under version control.
