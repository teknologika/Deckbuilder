# Feature Documentation: Multi-Content Layouts in Markdown

This document outlines the proposed Markdown syntax and conversion strategy for populating multi-content slide layouts in Deckbuilder. This feature extends the `markdown_to_canonical_json` converter to intelligently distribute Markdown content into specific, named content areas (placeholders) within a slide, rather than a single generic content block.

## Problem Statement

Previously, Markdown input was primarily designed for single-content area slides. For layouts like "Two Content", "Three Columns", or "Four Columns With Titles", there was no clear mechanism to specify which part of the Markdown body should populate which content placeholder.

## Proposed Solution: Section-Based Content Mapping

We will introduce a convention where specific Markdown headings (e.g., `###`) within the slide's body are used to delineate content sections. These sections will then be mapped to corresponding content placeholders defined in the template's JSON mapping.

### Key Principles:

*   **Heading as Delimiter:** A specific heading level (e.g., `###` for sub-sections) will act as a separator for distinct content areas.
*   **Mapping by Order/Name:** The converter will attempt to map these sections to named placeholders (e.g., `content_left`, `content_col1`) based on their order of appearance in the Markdown and the layout's defined placeholders.
*   **Fallback to Generic Content:** If a section heading does not correspond to a specific named content placeholder, or if the layout only has a generic content area, the content will be added to the main `content` array of the slide.

### Markdown Syntax Examples

#### 1. Two Content Layout

**Template Placeholders (Example from `default.json`):**
`content_left`, `content_right`

**Markdown Input:**
```markdown
---
layout: Two Content
title: My Two Content Slide
---

### Left Content Area
This is the content for the left column.
- Item 1
- Item 2

### Right Content Area
This is the content for the right column.
| Header A | Header B |
|---|---|
| Data 1 | Data 2 |
```

**Conversion Logic:**
*   The content following `### Left Content Area` will be parsed and assigned to the `content_left` placeholder.
*   The content following `### Right Content Area` will be parsed and assigned to the `content_right` placeholder.

**Resulting Canonical JSON (Excerpt):**
```json
{
  "layout": "Two Content",
  "placeholders": {
    "title": "My Two Content Slide",
    "content_left": [
      {"type": "heading", "level": 3, "text": "Left Content Area"},
      {"type": "paragraph", "text": "This is the content for the left column."},
      {"type": "bullets", "items": [{"level": 1, "text": "Item 1"}, {"level": 1, "text": "Item 2"}]}
    ],
    "content_right": [
      {"type": "heading", "level": 3, "text": "Right Content Area"},
      {"type": "paragraph", "text": "This is the content for the right column."},
      {"type": "table", "header": ["Header A", "Header B"], "rows": [["Data 1", "Data 2"]]}
    ]
  },
  "content": [] // Empty, as all content is mapped to specific placeholders
}
```

#### 2. Four Columns With Titles Layout

**Template Placeholders (Example from `default.json`):**
`title_col1`, `content_col1`, `title_col2`, `content_col2`, `title_col3`, `content_col3`, `title_col4`, `content_col4`

**Markdown Input:**
```markdown
---
layout: Four Columns With Titles
title: Our Quarterly Performance
---

### Q1 Highlights
This quarter saw significant growth in our market share.
- Achieved 15% revenue increase
- Expanded into new regions

### Q2 Challenges
Despite growth, we faced some supply chain issues.
| Metric | Q1 | Q2 |
|---|---|---|
| Revenue | $10M | $11.5M |
| Costs | $5M | $6M |

### Q3 Outlook
We anticipate continued expansion and new product launches.
- Focus on innovation
- Strengthen partnerships

### Q4 Goals
Our primary objective is to exceed annual targets.
- 20% year-over-year growth
- Customer satisfaction score of 90%
```

**Conversion Logic:**
*   The converter will identify the `###` headings.
*   The text of the `###` heading will populate the corresponding `title_colX` placeholder.
*   The content following each `###` heading (until the next `###` or end of slide) will be parsed into content blocks and assigned to the corresponding `content_colX` placeholder.

**Resulting Canonical JSON (Excerpt):**
```json
{
  "layout": "Four Columns With Titles",
  "placeholders": {
    "title": "Our Quarterly Performance",
    "title_col1": "Q1 Highlights",
    "content_col1": [
      {"type": "paragraph", "text": "This quarter saw significant growth in our market share."},
      {"type": "bullets", "items": [{"level": 1, "text": "Achieved 15% revenue increase"}, {"level": 1, "text": "Expanded into new regions"}]}
    ],
    "title_col2": "Q2 Challenges",
    "content_col2": [
      {"type": "paragraph", "text": "Despite growth, we faced some supply chain issues."},
      {"type": "table", "header": ["Metric", "Q1", "Q2"], "rows": [["Revenue", "$10M", "$11.5M"], ["Costs", "$5M", "$6M"]]}
    ],
    "title_col3": "Q3 Outlook",
    "content_col3": [
      {"type": "paragraph", "text": "We anticipate continued expansion and new product launches."},
      {"type": "bullets", "items": [{"level": 1, "text": "Focus on innovation"}, {"level": 1, "text": "Strengthen partnerships"}]}
    ],
    "title_col4": "Q4 Goals",
    "content_col4": [
      {"type": "paragraph", "text": "Our primary objective is to exceed annual targets."},
      {"type": "bullets", "items": [{"level": 1, "text": "20% year-over-year growth"}, {"level": 1, "text": "Customer satisfaction score of 90%"}]}
    ]
  },
  "content": []
}
```

## Implementation Considerations

*   The `markdown_to_canonical_json` function will need to be updated to:
    *   Identify the layout from the frontmatter.
    *   Retrieve the expected content placeholders for that layout from the `TemplateManager` (or a similar mechanism).
    *   Iterate through the `body_raw` content, splitting it into sections based on the `###` headings.
    *   Parse each section independently into content blocks.
    *   Map these parsed content blocks to the correct placeholder names in the `slide_obj["placeholders"]` dictionary.
    *   Ensure that if a layout does *not* have specific content placeholders, all body content defaults to the `slide_obj["content"]` array.

This approach provides a flexible and intuitive way for users to define content for complex slide layouts using standard Markdown syntax.
