# First deck in 5 minutes

```bash
uv add deckbuilder
deckbuilder init
```
Create `slides.md`:
```markdown
---
layout: Title Slide
---
# Deckbuilder Presentation
## Content-first intelligence
```
Build it:
```bash
deckbuilder create slides.md
open ./Deckbuilder_Presentation.pptx
```
