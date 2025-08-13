# Fonts & proofing language

CLI flags override environment variables, which override defaults.

Common env vars:
```bash
export DECK_PROOFING_LANGUAGE="en-AU"
export DECK_DEFAULT_FONT="Arial"
```

Examples:
```bash
deckbuilder create slides.md --language "English (Australia)" --font "Arial"
deckbuilder config languages
```
