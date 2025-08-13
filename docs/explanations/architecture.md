# Architecture & Workflow

The generation pipeline, end-to-end:

```mermaid
flowchart LR
  A[Markdown / JSON input] --> B[YAML frontmatter parse]
  B --> C[Deckbuilder Engine]
  C --> D[Template Resolver\n(default.pptx + default.json)]
  C --> E[Image Pipeline\n(generate/crop/embed)]
  C --> F[Language & Font Mapper]
  D --> G[PPTX Builder]
  E --> G
  F --> G
  G --> H[.pptx output]
```

**Key points**
- Inputs can be Markdown (with YAML frontmatter) or JSON.
- Template resolver merges content with `default.pptx` + layout JSON.
- Image pipeline can generate/crop assets and embed directly.
- Proofing language and default font are applied per deck.
