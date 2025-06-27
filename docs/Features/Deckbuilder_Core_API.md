# Deckbuilder Core API Reference

**For users who need precise control over presentation generation.**

This document covers the essential functions you'll use for creating presentations programmatically. All examples assume you're working with the singleton client.

## Getting Started

```python
from deckbuilder import get_deckbuilder_client

# Get the singleton client (recommended approach)
deck = get_deckbuilder_client()

# Alternative: direct instantiation
# from deckbuilder import Deckbuilder
# deck = Deckbuilder()
```

## Core Functions

### `create_presentation(templateName, fileName)`

Initializes a new presentation with the specified template.

```python
def create_presentation(templateName: str = "default", fileName: str = "Sample_Presentation") -> str
```

**Parameters:**
- `templateName` (str): Template name without .pptx extension. Default: "default"
- `fileName` (str): Base filename for output. Default: "Sample_Presentation"

**Returns:** Status message confirming creation

**What it does:**
- Loads PowerPoint template from templates folder
- Loads corresponding JSON mapping file for layout configuration
- Clears any existing slides
- Prepares presentation for content addition

**Example:**
```python
deck = get_deckbuilder_client()
result = deck.create_presentation("corporate", "Q4_Report")
print(result)  # "Creating presentation: Q4_Report"
```

### `add_slide_from_json(json_data)`

Adds slides to the presentation from JSON data.

```python
def add_slide_from_json(json_data) -> str
```

**Parameters:**
- `json_data` (dict or str): JSON data containing slides array

**Returns:** Status message with slide count

**JSON Structure:**
```python
{
    "presentation": {
        "slides": [
            {
                "type": "Title Slide",           # Layout type
                "title": "Slide Title",          # Content for title placeholder
                "subtitle": "Slide Subtitle"     # Content for subtitle placeholder
            },
            {
                "type": "Title and Content",
                "title": "Content Slide",
                "content": [                     # Array of content items
                    "First bullet point",
                    "Second bullet point"
                ]
            }
        ]
    }
}
```

**Example:**
```python
slides = {
    "presentation": {
        "slides": [
            {
                "type": "Title Slide",
                "title": "**2024 Performance Review**",
                "subtitle": "Annual results and strategic outlook"
            },
            {
                "type": "Title and Content",
                "title": "Key Achievements",
                "content": [
                    "**Revenue Growth**: 25% year-over-year",
                    "*Market Expansion*: 3 new regions",
                    "***Team Growth***: 40% increase in headcount"
                ]
            }
        ]
    }
}

result = deck.add_slide_from_json(slides)
print(result)  # "Successfully added 2 slides to presentation"
```

### `write_presentation(fileName)`

Saves the completed presentation to disk.

```python
def write_presentation(fileName: str = "Sample_Presentation") -> str
```

**Parameters:**
- `fileName` (str): Base filename (timestamp automatically added)

**Returns:** Confirmation message with full filename

**Output Format:** `{fileName}.{YYYY-MM-DD_HHMM}.g.pptx`

**Example:**
```python
result = deck.write_presentation("QuarterlyReport")
print(result)  # "Presentation saved as: QuarterlyReport.2025-01-26_1445.g.pptx"
```

### `create_presentation_from_json(json_data, fileName, templateName)`

Complete workflow: create presentation, add slides, and save in one call.

```python
def create_presentation_from_json(json_data, fileName: str = "Sample_Presentation", templateName: str = "default") -> str
```

**Parameters:**
- `json_data` (dict): Complete presentation data
- `fileName` (str): Output filename base
- `templateName` (str): Template to use

**Returns:** Success message with filename

**Example:**
```python
presentation = {
    "presentation": {
        "slides": [
            {"type": "Title Slide", "title": "**Executive Summary**", "subtitle": "Q4 2024"},
            {"type": "Title and Content", "title": "Revenue", "content": ["Total: **$5.2M**", "Growth: ***15%***"]}
        ]
    }
}

result = deck.create_presentation_from_json(presentation, "Executive_Summary", "corporate")
print(result)  # "Successfully created presentation: Executive_Summary.2025-01-26_1445.g.pptx"
```

## Markdown Functions

### `parse_markdown_with_frontmatter(markdown_content)`

Parses markdown with YAML frontmatter into slide data.

```python
def parse_markdown_with_frontmatter(markdown_content: str) -> list
```

**Parameters:**
- `markdown_content` (str): Markdown with YAML frontmatter sections

**Returns:** List of slide dictionaries

**Markdown Format:**
```markdown
---
layout: Title Slide
---
# Slide Title
## Slide Subtitle

---
layout: Title and Content
---
# Content Title
Content goes here
```

**Example:**
```python
markdown = """
---
layout: Title Slide
---
# **Project Update**
## Weekly status report

---
layout: Title and Content
---
# Progress This Week
- **Backend API**: 90% complete
- *Frontend UI*: 75% complete
- ***Testing***: 60% complete
"""

slides = deck.parse_markdown_with_frontmatter(markdown)
print(f"Parsed {len(slides)} slides")  # "Parsed 2 slides"

# Add to existing presentation
for slide in slides:
    deck._add_slide(slide)
```

### `create_presentation_from_markdown(markdown_content, fileName, templateName)`

Complete workflow: parse markdown, create presentation, and save.

```python
def create_presentation_from_markdown(markdown_content: str, fileName: str = "Sample_Presentation", templateName: str = "default") -> str
```

**Parameters:**
- `markdown_content` (str): Markdown with frontmatter
- `fileName` (str): Output filename base
- `templateName` (str): Template to use

**Returns:** Success message with slide count and filename

**Example:**
```python
markdown_content = """
---
layout: Title Slide
---
# **Sales Report**
## Monthly performance analysis

---
layout: table
style: dark_blue_white_text
---
# Regional Performance

| **Region** | *Sales* | ___Target___ |
| North | $1.2M | $1.0M |
| South | $980K | $1.1M |
| East | $1.5M | $1.3M |
| West | $750K | $900K |
"""

result = deck.create_presentation_from_markdown(markdown_content, "SalesReport")
print(result)  # "Successfully created presentation with 2 slides from markdown..."
```

## Slide Types Reference

### Title Slide
```python
{
    "type": "Title Slide",
    "title": "Main presentation title",
    "subtitle": "Supporting subtitle or date"
}
```

### Title and Content
```python
{
    "type": "Title and Content",
    "title": "Slide title",
    "content": [
        "Bullet point one",
        "Bullet point two",
        "Regular paragraph text"
    ]
}
```

### Table Slide
```python
{
    "type": "table",
    "title": "Table title",
    "table": {
        "header_style": "dark_blue_white_text",     # Header colors
        "row_style": "alternating_light_gray",      # Row colors
        "border_style": "thin_gray",                # Border style
        "data": [
            ["Header 1", "Header 2", "Header 3"],   # First row = headers
            ["Data 1", "Data 2", "Data 3"],         # Subsequent rows = data
            ["Data 4", "Data 5", "Data 6"]
        ]
    }
}
```

**Table Style Options:**

*Header Styles:*
- `"dark_blue_white_text"` - Dark blue background, white text
- `"light_blue_dark_text"` - Light blue background, dark text

*Row Styles:*
- `"alternating_light_gray"` - White and light gray alternating
- `"solid_white"` - All white rows

*Border Styles:*
- `"thin_gray"` - Thin gray borders
- `"thick_gray"` - Thick gray borders
- `"no_borders"` - No borders

### Section Header
```python
{
    "type": "Section Header",
    "title": "Section title",
    "subtitle": "Section description"
}
```

## Text Formatting

All text fields support inline formatting:

```python
"**bold text**"           # Bold
"*italic text*"           # Italic
"___underlined text___"   # Underlined
"***bold italic***"       # Bold + Italic
"***___all three___***"   # Bold + Italic + Underlined
```

## Error Handling

The API includes comprehensive error handling:

```python
try:
    result = deck.create_presentation_from_json(data, "MyPresentation")
    print(result)
except Exception as e:
    print(f"Error: {e}")
    # Common errors:
    # - Template not found
    # - Invalid JSON structure
    # - Missing required fields
    # - File permission issues
```

**Common Issues:**
- **Template not found**: Falls back to built-in template
- **Invalid JSON**: Returns detailed parsing error
- **Missing content**: Gracefully skips missing fields
- **File errors**: Clear error message with file path

## Environment Configuration

```python
import os

# Optional: Set custom paths
os.environ["DECK_TEMPLATE_FOLDER"] = "/path/to/templates"
os.environ["DECK_OUTPUT_FOLDER"] = "/path/to/output"
os.environ["DECK_TEMPLATE_NAME"] = "corporate"

# Then use normally
deck = get_deckbuilder_client()
```

## Complete Example

```python
from deckbuilder import get_deckbuilder_client

def create_quarterly_report():
    """Create a complete quarterly report presentation."""

    deck = get_deckbuilder_client()

    # Method 1: Step by step
    deck.create_presentation("corporate", "Q4_Report")

    # Add title slide
    title_data = {
        "presentation": {
            "slides": [{
                "type": "Title Slide",
                "title": "**Q4 2024 Results**",
                "subtitle": "Quarterly performance review"
            }]
        }
    }
    deck.add_slide_from_json(title_data)

    # Add content slides
    content_data = {
        "presentation": {
            "slides": [
                {
                    "type": "Title and Content",
                    "title": "Financial Highlights",
                    "content": [
                        "**Revenue**: $2.1M (+25% YoY)",
                        "*Profit Margin*: 18.5% (+2.3%)",
                        "***Cash Flow***: $450K positive"
                    ]
                },
                {
                    "type": "table",
                    "title": "Department Performance",
                    "table": {
                        "header_style": "dark_blue_white_text",
                        "row_style": "alternating_light_gray",
                        "data": [
                            ["**Department**", "*Revenue*", "___Target___"],
                            ["Sales", "$1.2M", "$1.0M"],
                            ["Marketing", "$300K", "$350K"],
                            ["Support", "$600K", "$750K"]
                        ]
                    }
                }
            ]
        }
    }
    deck.add_slide_from_json(content_data)

    # Save presentation
    result = deck.write_presentation("Q4_Report")
    return result

# Run it
result = create_quarterly_report()
print(result)
```

This covers all the essential functions you need for programmatic presentation generation. For advanced features like custom templates or content intelligence, see the specialized guides.

## Related Documentation

- **[Supported Templates](Supported_Templates.md)** - Complete list of available layouts and their status
- **[Placeholder Matching](Placeholder_Matching.md)** - How the hybrid template system works
- **[Template Discovery](Template_Discovery.md)** - Content-first design evolution and structured frontmatter
- **[Template Management](Deckbuilder_Template_Management.md)** - Custom template creation and CLI tools
- **[Content Intelligence](Deckbuilder_Content_Intelligence.md)** - AI-powered layout recommendations
