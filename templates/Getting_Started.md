# Getting Started with Deckbuilder

Welcome to Deckbuilder! This guide will help you create professional PowerPoint "
"presentations from Markdown or JSON files.

## Quick Start (3 Steps)

1. **Create your content**
   ```bash
   # Try the example file
   deckbuilder create examples/test_presentation.md
   ```

2. **View your presentation**
   Open the generated `.pptx` file in PowerPoint or LibreOffice

3. **Customize for your needs**
   Edit the example files or create your own content

## File Formats: Markdown vs JSON

Deckbuilder supports two input formats to fit different workflows:

### Markdown with Frontmatter (Recommended)
- **Best for**: Content authors, quick editing, version control
- **Syntax**: YAML frontmatter + Markdown content
- **Example**: `examples/test_presentation.md`

### JSON Format
- **Best for**: Programmatic generation, automation, complex structures
- **Syntax**: Structured JSON with rich content
- **Example**: `examples/test_presentation.json`

## Supported Layouts (13 Available)

Your template currently supports **13 layouts**. Here's how to use each:

### 1. Title Slide
Perfect for presentation openings and section breaks

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Title Slide
---
# Your Presentation Title
## Your subtitle here
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Title Slide",
  "title": "Your Presentation Title",
  "subtitle": "Your subtitle here"
}
```

### 2. Title and Content
Standard content slides with bullets and paragraphs

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Title and Content
---
# Slide Title

Your content here with:
- Bullet point one
- Bullet point two
- **Bold** and *italic* formatting
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Title and Content",
  "title": "Slide Title",
  "rich_content": [
    {
      "paragraph": "Your content here with:"
    },
    {
      "bullets": ["Bullet point one", "Bullet point two", "**Bold** and *italic* formatting"],
      "bullet_levels": [1, 1, 1]
    }
  ]
}
```

### 3. Section Header
Section dividers for organizing your presentation

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Section Header
---
# Section: **Implementation** Phase

This section covers the development and deployment stages.
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Section Header",
  "title": "Section: **Implementation** Phase",
  "rich_content": [
    {
      "paragraph": "This section covers the development and deployment stages."
    }
  ]
}
```

### 4. Two Content
Side-by-side content comparison

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Two Content
title: Comparison Title
sections:
  - title: Left Side
    content:
      - "Point A"
      - "Point B"
  - title: Right Side
    content:
      - "Point C"
      - "Point D"
---
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Two Content",
  "title": "Comparison Title",
  "content_left_1": ["Point A", "Point B"],
  "content_right_1": ["Point C", "Point D"]
}
```

### 5. Comparison
Side-by-side comparison for contrasting two options

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Comparison
title: Option Analysis
comparison:
  left:
    title: Option A
    content: "Cost effective with rapid deployment"
  right:
    title: Option B
    content: "Advanced features with future-proof design"
---
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Comparison",
  "title": "Option Analysis",
  "title_left_1": "Option A",
  "content_left_1": "Cost effective with rapid deployment",
  "title_right_1": "Option B",
  "content_right_1": "Advanced features with future-proof design"
}
```

### 6. Four Columns
Four-column layout for feature comparisons

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Four Columns
title: Feature Comparison
columns:
  - title: Performance
    content: "Fast processing with optimized algorithms"
  - title: Security
    content: "Enterprise-grade encryption and compliance"
  - title: Usability
    content: "Intuitive interface with minimal learning"
  - title: Cost
    content: "Competitive pricing with flexible plans"
---
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Four Columns",
  "title": "Feature Comparison",
  "title_col1_1": "Performance",
  "content_col1_1": "Fast processing with optimized algorithms",
  "title_col2_1": "Security",
  "content_col2_1": "Enterprise-grade encryption and compliance",
  "title_col3_1": "Usability",
  "content_col3_1": "Intuitive interface with minimal learning",
  "title_col4_1": "Cost",
  "content_col4_1": "Competitive pricing with flexible plans"
}
```

### 7. Three Columns With Titles
Three-column layout with individual titles

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Three Columns With Titles
title: Key Features
columns:
  - title: Performance
    content: "Fast processing with optimized algorithms"
  - title: Security
    content: "Enterprise-grade encryption and compliance"
  - title: Usability
    content: "Intuitive interface with minimal learning"
---
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Three Columns With Titles",
  "title": "Key Features",
  "title_col1_1": "Performance",
  "content_col1_1": "Fast processing with optimized algorithms",
  "title_col2_1": "Security",
  "content_col2_1": "Enterprise-grade encryption and compliance",
  "title_col3_1": "Usability",
  "content_col3_1": "Intuitive interface with minimal learning"
}
```

### 8. Three Columns
Three-column layout with content only

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Three Columns
title: Benefits Overview
columns:
  - content: "Fast processing with optimized algorithms"
  - content: "Enterprise-grade encryption and compliance"
  - content: "Intuitive interface with minimal learning"
---
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Three Columns",
  "title": "Benefits Overview",
  "content_col1_1": "Fast processing with optimized algorithms",
  "content_col2_1": "Enterprise-grade encryption and compliance",
  "content_col3_1": "Intuitive interface with minimal learning"
}
```

### 9. Picture with Caption
Media slides with image and caption (includes PlaceKitten fallback)

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Picture with Caption
title: System Architecture
media:
  image_path: "assets/architecture.png"  # Auto-fallback to PlaceKitten
  alt_text: "System architecture diagram"
  caption: "High-level system architecture"
  description: "Main components and their interactions"
---
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Picture with Caption",
  "title": "System Architecture",
  "image_1": "assets/architecture.png",
  "text_caption_1": "High-level system architecture"
}
```

### 10. Title Only
Simple title slides for minimal content

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Title Only
---
# Title Only Layout: **Bold** *Italic* ___Underline___
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Title Only",
  "title": "Title Only Layout: **Bold** *Italic* ___Underline___"
}
```

### 11. Blank
Blank layout for custom content

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Blank
---
# Custom Content

This layout provides maximum flexibility for custom designs.
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Blank",
  "title": "Custom Content",
  "rich_content": [
    {
      "paragraph": "This layout provides maximum flexibility for custom designs."
    }
  ]
}
```

### 12. Content with Caption
Content with additional caption area

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: Content with Caption
---
# Content with Caption

Main content goes here:
- Primary information
- Secondary details

Caption area with additional context.
```

**JSON Syntax (in .json files):**
```json
{
  "type": "Content with Caption",
  "title": "Content with Caption",
  "rich_content": [
    {
      "paragraph": "Main content goes here:"
    },
    {
      "bullets": ["Primary information", "Secondary details"],
      "bullet_levels": [1, 1]
    },
    {
      "paragraph": "Caption area with additional context."
    }
  ]
}
```

### 13. table
Table layout with styling options (alias for Title and Content)

**Frontmatter Syntax (in .md files):**
```yaml
---
layout: table
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
---
# Table Slide

| **Feature** | *Status* | ___Priority___ |
| Authentication | **Complete** | *High* |
| User Management | ***In Progress*** | ___Medium___ |
| Reporting | *Planned* | **Low** |
```

**JSON Syntax (in .json files):**
```json
{
  "type": "table",
  "style": "dark_blue_white_text",
  "row_style": "alternating_light_gray",
  "border_style": "thin_gray",
  "title": "Table Slide",
  "table": {
    "data": [
      ["**Feature**", "*Status*", "___Priority___"],
      ["Authentication", "**Complete**", "*High*"],
      ["User Management", "***In Progress***", "___Medium___"],
      ["Reporting", "*Planned*", "**Low**"]
    ],
    "header_style": "dark_blue_white_text",
    "row_style": "alternating_light_gray",
    "border_style": "thin_gray"
  }
}
```

## Advanced Features

### PlaceKitten Image Support
When images are missing or invalid, Deckbuilder automatically generates professional "
"placeholder images:
- **Grayscale styling** for business presentations
- **Smart cropping** with face detection and rule-of-thirds composition
- **Automatic caching** for performance optimization
- **Professional appearance** suitable for client presentations

### Inline Formatting
Use these formatting options in any text content:
- **Bold text**: `**text**` or `***text***`
- *Italic text*: `*text*` or `***text***`
- ___Underlined text___: `___text___`
- **_Combined formatting_**: `**_bold italic_**`

### Table Support
Create tables with professional styling:
```yaml
---
layout: table
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
---
```

## CLI Commands Reference

### Essential Commands
```bash
# Create presentation from Markdown
deckbuilder create presentation.md

# Create from JSON
deckbuilder create presentation.json

# Generate PlaceKitten images
deckbuilder image 800 600 --filter grayscale --output placeholder.jpg

# List available templates
deckbuilder templates

# Analyze template structure
deckbuilder analyze default --verbose
```

### Template Management
```bash
# Initialize new template folder
deckbuilder init ~/my-templates

# Validate template and mappings
deckbuilder validate default

# Document template capabilities
deckbuilder document default --output template_docs.md

# Enhance template placeholders
deckbuilder enhance default
```

## Troubleshooting

### Common Issues

**"Template folder not found"**
```bash
# Solution: Initialize template folder
deckbuilder init ./templates
```

**"Layout not supported"**
- Check the supported layouts list above
- Use `deckbuilder analyze default` to see available layouts
- Ensure correct spelling and capitalization

**"Image not found"**
- Don't worry! PlaceKitten will generate a professional placeholder
- Check image path is relative to presentation file
- Supported formats: JPG, PNG, WebP

**"JSON validation error"**
- Validate JSON syntax with online tools
- Check required fields for each layout type
- Compare with working examples in `examples/test_presentation.json`

### Getting Help
```bash
# Show help for any command
deckbuilder --help
deckbuilder create --help

# Show current configuration
deckbuilder config

# List available templates
deckbuilder templates
```

## Next Steps

1. **Explore the examples**: Study `examples/test_presentation.md` and "
"   `examples/test_presentation.json`
2. **Try different layouts**: Experiment with the {layout_count} supported layouts
3. **Add your content**: Replace example content with your own
4. **Customize styling**: Explore table styles and formatting options
5. **Share your presentations**: Generated `.pptx` files work in PowerPoint, "
"   LibreOffice, and Google Slides

## Advanced Usage

### Batch Processing
```bash
# Process multiple files
for file in *.md; do deckbuilder create "$file"; done
```

### Environment Configuration
```bash
# Set permanent template folder
export DECK_TEMPLATE_FOLDER="~/my-templates"
export DECK_OUTPUT_FOLDER="~/presentations"
export DECK_TEMPLATE_NAME="default"
```

### Integration with Version Control
- Markdown files work excellently with Git
- Track presentation content changes easily
- Collaborate on presentations using familiar tools

---

**Generated by Deckbuilder CLI** • Template Version: 1.0 • {datetime.now().strftime('%Y-%m-%d')}

Happy presenting! 🚀
