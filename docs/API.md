# API Reference

## Overview

The deck-builder-mcp server exposes MCP (Model Context Protocol) tools for programmatic PowerPoint presentation creation. All tools are accessed through MCP clients and support both simple and advanced template-based slide generation.

## MCP Tools

### Presentation Management

#### `create_presentation`
Creates a new empty presentation from a specified template.

**Parameters:**
- `templateName` (string): Name of template to use (default: "default")  
- `fileName` (string): Output filename (default: "Sample_Presentation")

**Returns:** Success message with presentation name

**Example:**
```python
create_presentation(templateName="corporate", fileName="Q4_Report")
```

#### `write_presentation`  
Saves the current presentation to disk with timestamp.

**Parameters:**
- `fileName` (string): Base filename (default: "Sample_Presentation")

**Returns:** Success message with generated filename

**Example:**
```python
write_presentation(fileName="Marketing_Deck")
# Creates: Marketing_Deck.2024-06-20_1430.g.pptx
```

### Slide Creation

#### `add_slide`
Adds slides to the presentation using JSON data.

**Parameters:**
- `json_data` (string): JSON string containing slide information

**Supported Slide Types:**
- `title`: Title slide with title and subtitle
- `content`: Content slide with title and bullet points  
- `table`: Table slide with styling options
- Custom layout names from template JSON mappings

**Example:**
```python
slide_data = {
    "type": "title",
    "title": "Project Overview", 
    "subtitle": "Q4 2024 Results"
}
add_slide(json.dumps(slide_data))
```

#### `add_title_slide` / `add_content_slide` / `add_table_slide`
Specialized slide creation tools with specific JSON schemas.

### Advanced Features

#### `create_presentation_from_markdown`
Creates complete presentations from markdown with frontmatter.

**Parameters:**
- `markdown_content` (string): Markdown with YAML frontmatter slide definitions
- `fileName` (string): Output filename  
- `templateName` (string): Template to use

**Example:**
```markdown
---
layout: title
---
# Main Title
## Subtitle

---
layout: content  
---
# Key Points
- Point one
- Point two
```

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

Use `tools.py` to generate JSON mappings from existing PowerPoint templates:

```bash
python tests/test_tools.py
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
