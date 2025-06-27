# Deckbuilder API Reference

## Overview

The Deckbuilder server provides a streamlined MCP (Model Context Protocol) interface for programmatic PowerPoint presentation creation. The server exposes comprehensive tools that handle complete presentation workflows with automatic saving.

## MCP Tools

### `create_presentation`
Creates a complete PowerPoint presentation from JSON data with automatic saving.

**Parameters:**
- `json_data` (string): JSON string containing complete presentation data with all slides
- `fileName` (string): Output filename (default: "Sample_Presentation")
- `templateName` (string): Template to use (default: "default")

**Returns:** Success message with filename and save confirmation

**JSON Schema:**
```json
{
  "presentation": {
    "slides": [
      {
        "type": "title",
        "title": "**Main Title** with *formatting*",
        "subtitle": "Subtitle with ___underline___"
      },
      {
        "type": "content",
        "title": "Content Slide",
        "content": [
          "**Bold** bullet point",
          "*Italic* text with ___underline___",
          "***Bold italic*** combination"
        ]
      },
      {
        "type": "table",
        "title": "Table Example",
        "table": {
          "header_style": "dark_blue_white_text",
          "row_style": "alternating_light_gray",
          "data": [
            ["**Header 1**", "*Header 2*", "___Header 3___"],
            ["Data 1", "Data 2", "Data 3"]
          ]
        }
      }
    ]
  }
}
```

**Supported Slide Types:**
- `title`: Title slide with title and subtitle
- `content`: Content slide with rich text, bullets, headings
- `table`: Table slide with full styling support
- All PowerPoint layout types supported via template mapping

**Inline Formatting Support:**
- `**bold**` - Bold text
- `*italic*` - Italic text
- `___underline___` - Underlined text
- `***bold italic***` - Combined bold and italic
- `***___all three___***` - Bold, italic, and underlined

### `create_presentation_from_markdown`
Creates complete presentations from markdown with frontmatter and automatic saving.

**Parameters:**
- `markdown_content` (string): Markdown with YAML frontmatter slide definitions
- `fileName` (string): Output filename (default: "Sample_Presentation")
- `templateName` (string): Template to use (default: "default")

**Returns:** Success message with slide count and save confirmation

**Markdown Format:**
```markdown
---
layout: title
---
# **Main Title** with *Formatting*
## Subtitle with ___underline___

---
layout: content
---
# Content Slide Title

## Section Heading
This section demonstrates rich content with formatting.

- **Bold** bullet point
- *Italic* text with ___underline___
- ***Bold italic*** combination

Additional paragraph with **mixed** *formatting*.

---
layout: table
style: dark_blue_white_text
row_style: alternating_light_gray
---
# Table Slide Title

| **Header 1** | *Header 2* | ___Header 3___ |
| Data 1 | Data 2 | Data 3 |
| More data | More data | More data |
```

**Supported Layouts:**
- `title`: Title slide with title and subtitle
- `content`: Content slide with rich text support (headings, paragraphs, bullets)
- `table`: Table slide with styling options
- All template-specific layout names

**Table Styling Options:**
- `style`: Header style (dark_blue_white_text, light_blue_dark_text, etc.)
- `row_style`: Row style (alternating_light_gray, solid_white, etc.)
- `border_style`: Border style (thin_gray, thick_gray, no_borders, etc.)
- `custom_colors`: Custom color overrides (header_bg, header_text, alt_row, border_color)

## Template System

### JSON Mapping Structure

Templates use paired files:
- `templateName.pptx`: PowerPoint template
- `templateName.json`: Layout mapping configuration

**Mapping Schema:**
```json
{
  "template_info": {
    "name": "Template Name",
    "version": "1.0"
  },
  "layouts": {
    "Layout Name": {
      "index": 0,
      "placeholders": {
        "0": "field_name"
      }
    }
  },
  "aliases": {
    "user_name": "Layout Name"
  }
}
```

### Template Analysis

Use the CLI tools to generate JSON mappings from existing PowerPoint templates:

```bash
python src/deckbuilder/cli_tools.py analyze default --verbose
```

This creates `templateName.g.json` files with extracted structure ready for customization.

## Environment Configuration

**Required Environment Variables:**
- `DECK_TEMPLATE_FOLDER`: Directory containing template files
- `DECK_OUTPUT_FOLDER`: Directory for generated presentations

**Optional Variables:**
- `DECK_TEMPLATE_NAME`: Default template name
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: "8050")

## Error Handling

**Common Error Types:**
- **Template Not Found**: Falls back to basic layout support
- **Invalid JSON**: Returns JSON parsing error with details
- **Missing Placeholders**: Gracefully skips unavailable placeholders
- **File I/O Errors**: Returns specific error messages for debugging

**Error Response Format:**
```
"Error [operation]: [specific error message]"
```

**Example Error Responses:**
```
"Error creating presentation: Template file not found: custom.pptx"
"Error parsing JSON: Expecting ',' delimiter: line 4 column 5"
"Error adding slide from JSON: Layout index 15 not found in template"
```
