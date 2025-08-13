# Batch build

Generate a deck for each Markdown file in a folder:

```bash
for f in content/*.md; do
  deckbuilder create "$f"
done
```
