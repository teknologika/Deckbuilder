# Deckbuilder API Reference

## Overview

The Deckbuilder server provides a streamlined MCP (Model Context Protocol) interface for programmatic PowerPoint presentation creation. The server exposes comprehensive tools that handle complete presentation workflows with automatic saving.

## MCP Tools



**Canonical JSON Schema:**
```json
{
  "slides": [
    {
      "layout": "Title Slide",
      "style": "default_style",
      "placeholders": {
        "title": "This is the Title",
        "subtitle": "This is the subtitle"
      },
      "content": [
        {
          "type": "heading",
          "level": 1,
          "text": "A Formatted **Heading**"
        },
        {
          "type": "paragraph",
          "text": "This is a paragraph with *italic* and ___underline___."
        },
        {
          "type": "bullets",
          "items": [
            { "level": 1, "text": "First bullet" },
            { "level": 2, "text": "Second-level bullet" }
          ]
        },
        {
          "type": "table",
          "style": "dark_blue_white_text",
          "border_style": "thin_gray",
          "header": ["Header 1", "Header 2"],
          "rows": [
            ["Cell 1.1", "Cell 1.2"],
            ["Cell 2.1", "Cell 2.2"]
          ]
        },
        {
          "type": "image",
          "path": "path/to/image.png",
          "caption": "An image caption",
          "alt_text": "Accessibility text"
        }
      ]
    }
  ]
}
```

**Key Design Points of Canonical JSON:**
-   **`slides` array:** The root object contains a single `slides` array.
-   **`layout`:** A mandatory string specifying the slide layout from the template.
-   **`placeholders`:** A key-value map for direct placeholder replacement (e.g., `title`, `subtitle`, `body`). This is for simple content.
-   **`content` array:** A structured list of content blocks for the main content area of a slide. This allows for rich, mixed content.
-   **Explicit `type` in content blocks:** Each object in the `content` array has a `type` (`heading`, `paragraph`, `bullets`, `table`, `image`) to remove ambiguity.
-   **Inline Formatting:** All `text` fields throughout the model are strings that will be processed by the existing `content_formatting.py` module to handle `**bold**`, `*italic*`, etc.

**Supported Content Block Types:**
- `heading`: Headings with specified level.
- `paragraph`: Standard text paragraphs.
- `bullets`: Bulleted lists with support for nesting.
- `table`: Tables with header and row data.
- `image`: Images with path, caption, and alt text.

**Inline Formatting Support (within `text` fields):**
- `**bold**` - Bold text
- `*italic*` - Italic text
- `___underline___` - Underlined text
- `***bold italic***` - Combined bold and italic
- `***___all three___***` - Bold, italic, and underlined


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
