# Deckbuilder Quick Start Guide

**Goal**: Create professional PowerPoint presentations in one shot from JSON or Markdown.

## What You Need to Know

Deckbuilder is designed for **one-shot presentation creation** - you provide your content, and it generates a complete PowerPoint file automatically. No complex setup required.

### Two Simple Ways to Create Presentations:

1. **JSON Format** - Precise control with structured data
2. **Markdown + YAML** - Natural writing with simple formatting

## Installation & Setup

```python
# Install Deckbuilder
pip install -r requirements.txt

# Import and create client
from deckbuilder import get_deckbuilder_client
deck = get_deckbuilder_client()
```

**Environment Setup** (optional - uses defaults if not set):
```bash
export DECK_TEMPLATE_FOLDER="/path/to/templates"  # Default: built-in template
export DECK_OUTPUT_FOLDER="/path/to/output"       # Default: current directory
```

## Method 1: JSON Format

Perfect for programmatic generation or when you have structured data.

### Simple Example

```python
from deckbuilder import get_deckbuilder_client

# Get the client
deck = get_deckbuilder_client()

# Your presentation data
presentation_data = {
    "presentation": {
        "slides": [
            {
                "type": "Title Slide",
                "title": "**My Presentation**",
                "subtitle": "Created with Deckbuilder"
            },
            {
                "type": "Title and Content",
                "title": "Key Points",
                "content": [
                    "**First point** - Something important",
                    "*Second point* - Something interesting",
                    "***Third point*** - Something critical"
                ]
            },
            {
                "type": "table",
                "title": "Project Status",
                "table": {
                    "header_style": "dark_blue_white_text",
                    "row_style": "alternating_light_gray",
                    "data": [
                        ["**Task**", "*Status*", "___Owner___"],
                        ["Design", "**Complete**", "Alice"],
                        ["Development", "***In Progress***", "Bob"],
                        ["Testing", "*Planned*", "Carol"]
                    ]
                }
            }
        ]
    }
}

# Create the presentation (one command does everything)
result = deck.create_presentation_from_json(
    presentation_data,
    fileName="MyPresentation",
    templateName="default"
)

print(result)  # "Successfully created presentation: MyPresentation.2025-01-26_1430.g.pptx"
```

### Supported Slide Types

```python
# Title slide
{
    "type": "Title Slide",
    "title": "Your Title Here",
    "subtitle": "Your Subtitle"
}

# Content slide with bullets and paragraphs
{
    "type": "Title and Content",
    "title": "Slide Title",
    "content": [
        "Bullet point one",
        "Bullet point two",
        "Regular paragraph text"
    ]
}

# Table slide with styling
{
    "type": "table",
    "title": "Table Title",
    "table": {
        "header_style": "dark_blue_white_text",  # or "light_blue_dark_text"
        "row_style": "alternating_light_gray",   # or "solid_white"
        "data": [
            ["Header 1", "Header 2", "Header 3"],
            ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
            ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]
        ]
    }
}

# Section divider
{
    "type": "Section Header",
    "title": "Section Title",
    "subtitle": "Section Description"
}
```

## Method 2: Markdown + YAML (Recommended)

Perfect for natural writing. Use YAML frontmatter to specify layouts, then write content in markdown.

### Simple Example

```python
markdown_content = """
---
layout: Title Slide
---
# **My Presentation**
## Created with *Deckbuilder*

---
layout: Title and Content
---
# Key Benefits

## Why Choose Our Solution
Our platform offers significant advantages over traditional approaches.

- **Performance** - 3x faster processing
- **Reliability** - 99.9% uptime guarantee
- **Security** - Enterprise-grade encryption
- **Support** - 24/7 expert assistance

Contact us today to learn more about implementation.

---
layout: table
style: dark_blue_white_text
row_style: alternating_light_gray
---
# Implementation Timeline

| **Phase** | *Duration* | ___Status___ |
| Planning | 2 weeks | **Complete** |
| Development | 6 weeks | ***In Progress*** |
| Testing | 2 weeks | *Scheduled* |
| Deployment | 1 week | ___Pending___ |
"""

# Create presentation from markdown
deck = get_deckbuilder_client()
result = deck.create_presentation_from_markdown(
    markdown_content,
    fileName="MyMarkdownPresentation",
    templateName="default"
)

print(result)
```

### Content Formatting

**Inline Formatting** (works in both JSON and Markdown):
- `**bold text**` → **bold text**
- `*italic text*` → *italic text*
- `___underlined text___` → ___underlined text___
- `***bold italic***` → ***bold italic***
- `***___all three___***` → ***bold italic underlined***

**Content Types**:
- `# Heading` → Section heading (larger text)
- `## Subheading` → Subsection heading
- `Regular paragraph` → Normal paragraph text
- `- Bullet point` → Bullet list item
- Tables use standard markdown syntax

## Advanced Layouts (Structured Frontmatter)

For more complex layouts, use structured YAML:

```yaml
---
layout: Four Columns
title: Feature Comparison
columns:
  - title: Performance
    content: "**Lightning fast** processing with optimized algorithms"
  - title: Security
    content: "***Enterprise-grade*** encryption and compliance"
  - title: Usability
    content: "*Intuitive* interface with minimal learning curve"
  - title: Value
    content: "___Transparent___ pricing with proven ROI"
---

---
layout: Comparison
title: Solution Analysis
comparison:
  left:
    title: Current Approach
    content: "**Legacy** system with *limited* scalability"
  right:
    title: Our Solution
    content: "***Modern*** architecture with ___unlimited___ growth potential"
---
```

## Output Files

All presentations are saved with timestamps:
- **Format**: `{fileName}.{YYYY-MM-DD_HHMM}.g.pptx`
- **Example**: `MyPresentation.2025-01-26_1430.g.pptx`
- **Location**: `DECK_OUTPUT_FOLDER` or current directory

## Common Patterns

### Multi-slide JSON Presentation
```python
slides_data = {
    "presentation": {
        "slides": [
            {"type": "Title Slide", "title": "**Quarterly Review**", "subtitle": "Q4 2024 Results"},
            {"type": "Section Header", "title": "Executive Summary"},
            {"type": "Title and Content", "title": "Key Metrics", "content": ["Revenue: **$2.1M**", "Growth: ***25%***"]},
            {"type": "Section Header", "title": "Detailed Analysis"},
            {"type": "table", "title": "Department Performance", "table": {...}}
        ]
    }
}

deck.create_presentation_from_json(slides_data, "QuarterlyReview")
```

### Multi-slide Markdown Presentation
```markdown
---
layout: Title Slide
---
# **Quarterly Review**
## Q4 2024 Results

---
layout: Section Header
---
# Executive Summary

---
layout: Title and Content
---
# Key Metrics
- Revenue: **$2.1M**
- Growth: ***25%***

---
layout: Section Header
---
# Detailed Analysis
```

## That's It!

You now know everything needed for one-shot presentation creation. The system handles:
- ✅ Template loading and management
- ✅ Content formatting and styling
- ✅ Slide layout selection
- ✅ File output with timestamps
- ✅ Error handling and fallbacks

**Next Steps**:
- See [Core API Reference](Deckbuilder_Core_API.md) for all available functions
- See [Template Management](Deckbuilder_Template_Management.md) for custom templates
- See [Supported Templates](Supported_Templates.md) for complete layout library status
- See [Placeholder Matching](Placeholder_Matching.md) for template system architecture
