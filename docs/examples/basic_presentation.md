# Basic Presentation Example

This example demonstrates the basic usage of Deckbuilder for creating PowerPoint presentations from markdown.

## Usage

```bash
deckbuilder create examples/basic_presentation.md --output "My First Presentation"
```

## Presentation Content

---
layout: Title Slide
title: **Welcome to Deckbuilder**
subtitle: Intelligent PowerPoint generation with *content-first* design
---

---
layout: Title and Content
title: Key Features
content: |
  • **Smart Image Fallbacks** - Automatic PlaceKitten generation
  • ***Content-First Intelligence*** - Understand goals before layouts
  • **Rich Formatting** - Bold, italic, underline support
  • ___Professional Templates___ - 50+ business layouts planned
---

---
layout: Two Content
title: Before vs After
left:
  title: Traditional Approach
  content: |
    1. Choose layout first
    2. Force content to fit
    3. Manual image hunting
    4. Time-consuming process
right:
  title: Deckbuilder Approach  
  content: |
    1. **Define your message**
    2. *Smart layout recommendations*
    3. ***Automatic image fallbacks***
    4. ___Instant generation___
---

---
layout: Picture with Caption
title: Smart Image Processing
media:
  image_path: "examples/demo_image.png"  # This will trigger PlaceKitten fallback
  caption: "Professional placeholder generation with **smart cropping** and *grayscale filtering*"
---

---
layout: Four Columns
title: Comprehensive Toolkit
columns:
  - title: CLI Tools
    content: "Standalone **command-line** interface"
  - title: MCP Server
    content: "*Claude Desktop* integration"
  - title: Python Library
    content: "Direct ***programmatic*** access"
  - title: Template System
    content: "___Extensible___ layout library"
---

---
layout: Table
title: Supported Formats
style: dark_blue_white_text
---

| **Input Format** | *File Extension* | ___Use Case___ |
|------------------|------------------|----------------|
| Markdown + YAML  | `.md` | **Human-friendly** authoring |
| JSON Structure  | `.json` | ***Programmatic*** generation |
| Direct Python   | `.py` | ___Embedded___ applications |

---
layout: Section Header
title: Thank You
subtitle: Questions & **Demo**
---