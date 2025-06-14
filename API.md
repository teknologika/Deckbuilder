# API Reference

This document provides detailed information about the MCP tools available in the Deck Builder server for programmatic PowerPoint presentation creation.

## MCP Tools Overview

The Deck Builder MCP server exposes 5 main tools through the Model Context Protocol for presentation creation and management.

## Tool Endpoints

### create_presentation

**Description:** Initialize a new PowerPoint presentation from a template.

**Parameters:**
- `templateName` (string, required): Name of the PowerPoint template to use
- `title` (string, optional): Title for the presentation (default: "Presentation Title")
- `subTitle` (string, optional): Subtitle for the presentation (default: "")
- `author` (string, optional): Author name for the presentation (default: "")

**Example Request:**
```json
{
  "tool": "create_presentation",
  "arguments": {
    "templateName": "corporate_template",
    "title": "Q4 Financial Report",
    "subTitle": "2024 Performance Overview",
    "author": "Finance Team"
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Successfully created the presentation and added a title slide Q4 Financial Report"
    }
  ]
}
```

**Error Response:**
```json
{
  "content": [
    {
      "type": "text", 
      "text": "Error creating presentation: Template 'nonexistent_template.pptx' not found"
    }
  ]
}
```

---

### write_presentation

**Description:** Save the current presentation to disk with automatic versioning.

**Parameters:**
- `fileName` (string, optional): Name for the saved file (default: "Sample_Presentation")

**Example Request:**
```json
{
  "tool": "write_presentation",
  "arguments": {
    "fileName": "Q4_Financial_Report"
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Successfully created presentation: Q4_Financial_Report.latest.pptx"
    }
  ]
}
```

**File Versioning:** If a file with the same name exists, the existing file is renamed with version numbers (e.g., `file.latest.pptx.v01.pptx`, `file.latest.pptx.v02.pptx`).

---

### add_title_slide

**Description:** Add a title slide to the current presentation using JSON data.

**Parameters:**
- `json_data` (string, required): JSON string containing slide data

**JSON Structure:**
```json
{
  "type": "title",
  "title": "Main Title Text",
  "subtitle": "Subtitle Text (optional)"
}
```

**Example Request:**
```json
{
  "tool": "add_title_slide",
  "arguments": {
    "json_data": "{\"type\": \"title\", \"title\": \"Welcome to Our Presentation\", \"subtitle\": \"An Overview of Our Services\"}"
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Successfully added slide(s) from JSON data"
    }
  ]
}
```

---

### add_content_slide

**Description:** Add a content slide with bullet points to the current presentation.

**Parameters:**
- `json_data` (string, required): JSON string containing slide data

**JSON Structure:**
```json
{
  "type": "content",
  "title": "Slide Title",
  "content": [
    "First bullet point",
    "Second bullet point", 
    "Third bullet point"
  ]
}
```

**Alternative JSON Structure (single content):**
```json
{
  "type": "content",
  "title": "Slide Title",
  "content": "Single paragraph of content"
}
```

**Example Request:**
```json
{
  "tool": "add_content_slide",
  "arguments": {
    "json_data": "{\"type\": \"content\", \"title\": \"Key Benefits\", \"content\": [\"Increased efficiency\", \"Cost reduction\", \"Better user experience\", \"Scalable solution\"]}"
  }
}
```

---

### add_table_slide

**Description:** Add a table slide with advanced styling options to the current presentation.

**Parameters:**
- `json_data` (string, required): JSON string containing table slide data with styling options

**JSON Structure:**
```json
{
  "type": "table",
  "title": "Table Title",
  "table": {
    "header_style": "dark_blue_white_text",
    "row_style": "alternating_light_gray",
    "border_style": "thin_gray",
    "custom_colors": {
      "header_bg": "#2E5984",
      "header_text": "#FFFFFF",
      "alt_row": "#F0F8FF",
      "border_color": "#CCCCCC"
    },
    "data": [
      ["Header 1", "Header 2", "Header 3"],
      ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
      ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]
    ]
  }
}
```

**Style Options:**

**Header Styles:**
- `dark_blue_white_text`: Dark blue background, white text
- `light_blue_dark_text`: Light blue background, dark text  
- `dark_gray_white_text`: Dark gray background, white text
- `light_gray_dark_text`: Light gray background, dark text
- `white_dark_text`: White background, dark text
- `accent_color_white_text`: Theme accent color background, white text

**Row Styles:**
- `alternating_light_gray`: White/light gray alternating rows
- `alternating_light_blue`: White/light blue alternating rows
- `solid_white`: All white rows
- `solid_light_gray`: All light gray rows
- `no_fill`: Transparent/no background

**Border Styles:**
- `thin_gray`: Thin gray borders all around
- `thick_gray`: Thick gray borders
- `header_only`: Border only under header
- `outer_only`: Border only around table perimeter
- `no_borders`: No borders

**Custom Colors (hex codes):**
- `header_bg`: Header background color
- `header_text`: Header text color
- `alt_row`: Alternating row background color
- `border_color`: Border color

**Example Request:**
```json
{
  "tool": "add_table_slide",
  "arguments": {
    "json_data": "{\"type\": \"table\", \"title\": \"Sales Performance\", \"table\": {\"header_style\": \"dark_blue_white_text\", \"row_style\": \"alternating_light_gray\", \"data\": [[\"Rep Name\", \"Q4 Sales\", \"Target\", \"% of Target\"], [\"John Smith\", \"$125,000\", \"$100,000\", \"125%\"], [\"Sarah Jones\", \"$98,500\", \"$95,000\", \"104%\"]]}}"
  }
}
```

## Authentication

This MCP server does not require authentication. Access is controlled through the MCP client configuration (e.g., Claude Desktop configuration file).

## Error Handling

### Common Error Codes and Messages

**JSON Parsing Errors:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Error parsing JSON: Expecting ',' delimiter: line 1 column 45 (char 44)"
    }
  ]
}
```

**Template Errors:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Error creating presentation: Template 'custom_template.pptx' not found"
    }
  ]
}
```

**File System Errors:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Error creating presentation: Permission denied: Unable to write to output directory"
    }
  ]
}
```

**Slide Creation Errors:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Error adding slide: Invalid slide type 'unknown_type' specified"
    }
  ]
}
```

### Error Prevention Best Practices

1. **Validate JSON:** Use a JSON validator before sending requests
2. **Check File Paths:** Ensure template and output directories exist and are writable
3. **Verify Templates:** Confirm template files exist in the specified template directory
4. **Handle Large Data:** Be mindful of table size limits in PowerPoint
5. **Use Valid Colors:** Ensure hex color codes are properly formatted (e.g., #FFFFFF)

### Debugging

Enable debug mode by setting the `DEBUG=1` environment variable when running the MCP server. This provides additional logging information for troubleshooting issues.

```bash
DEBUG=1 python src/main.py
```

## Usage Examples

### Complete Presentation Workflow

```json
// 1. Create presentation
{
  "tool": "create_presentation",
  "arguments": {
    "templateName": "default",
    "title": "Monthly Report",
    "author": "Analytics Team"
  }
}

// 2. Add title slide
{
  "tool": "add_title_slide", 
  "arguments": {
    "json_data": "{\"type\": \"title\", \"title\": \"Monthly Analytics Report\", \"subtitle\": \"December 2024\"}"
  }
}

// 3. Add content slide
{
  "tool": "add_content_slide",
  "arguments": {
    "json_data": "{\"type\": \"content\", \"title\": \"Key Metrics\", \"content\": [\"User engagement up 23%\", \"Revenue increased 18%\", \"Customer retention at 94%\"]}"
  }
}

// 4. Add table slide
{
  "tool": "add_table_slide",
  "arguments": {
    "json_data": "{\"type\": \"table\", \"title\": \"Performance Data\", \"table\": {\"header_style\": \"dark_blue_white_text\", \"data\": [[\"Metric\", \"Current\", \"Previous\", \"Change\"], [\"Users\", \"45,230\", \"42,100\", \"+7.4%\"], [\"Revenue\", \"$892K\", \"$756K\", \"+18.0%\"]]}}"
  }
}

// 5. Save presentation
{
  "tool": "write_presentation",
  "arguments": {
    "fileName": "Monthly_Report_Dec_2024"
  }
}
```

This workflow creates a complete presentation with multiple slide types and saves it to disk with version management.