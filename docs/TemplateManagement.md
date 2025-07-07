# Template Management Guide

## Overview

Deckbuilder supports custom PowerPoint templates through a comprehensive template management system. This guide covers the complete workflow from adding a new PowerPoint template to having it fully integrated and usable within Deckbuilder.

## Quick Start

```bash
# 1. Initialize template folder
deckbuilder init ./my-templates

# 2. Add your PowerPoint template
cp /path/to/corporate.pptx ./my-templates/corporate.pptx

# 3. Analyze and create mapping
deckbuilder template analyze corporate --verbose

# 4. Enhance with conventions (recommended)
deckbuilder template enhance corporate --use-conventions

# 5. Test your template
deckbuilder create example_presentation.md --template corporate
```

## Template Discovery System

Deckbuilder uses a **hierarchical template discovery system** through the PathManager:

### Context-Based Discovery
- **CLI Context**: CLI args → env vars → current directory (`./templates`)
- **MCP Context**: env vars → failure (no fallbacks for security)
- **Library Context**: constructor args → env vars → package assets

### Required Files
Templates consist of **2 required files**:
- `template_name.pptx` (PowerPoint template file)
- `template_name.json` (JSON mapping file)

## Complete Workflow: Adding a New Template

### Step 1: Initial Setup (One-time)

Initialize a template folder with default files and documentation:

```bash
deckbuilder init ./my-templates
```

This creates:
- `./my-templates/default.pptx` (PowerPoint template)
- `./my-templates/default.json` (JSON mapping)
- `Getting_Started.md` (comprehensive documentation)
- `example_presentation.md/.json` (working examples)

### Step 2: Add Your PowerPoint Template

Copy your PowerPoint template to the templates folder:

```bash
cp /path/to/your/corporate.pptx ./my-templates/corporate.pptx
```

### Step 3: Analyze Template Structure

Extract all slide layouts and placeholders from your template:

```bash
deckbuilder template analyze corporate --verbose
```

This generates:
- Detailed analysis of all slide layouts (typically 19 layouts)
- Placeholder structure and naming inconsistencies detection
- `corporate.g.json` file ready for editing

**Sample Output:**
```
🔍 Analyzing template: corporate
📊 Found 19 layouts
⚠️  Multiple placeholder naming patterns detected:
['Col 1', 'Col 2', 'Content Placeholder', 'Date Placeholder']
📄 Generated: corporate.g.json
```

### Step 4: Validate Template Health

Check for issues and get specific fix instructions:

```bash
deckbuilder template validate corporate
```

This provides:
- Template file accessibility check
- Placeholder naming convention validation
- Column layout consistency analysis
- Specific instructions for fixing issues in PowerPoint

### Step 5: Create JSON Mapping

You have two options for creating the JSON mapping:

#### Option A: Manual Editing

Edit the generated mapping file to add semantic placeholder names:

```bash
vim corporate.g.json
```

Example mapping structure:
```json
{
  "layouts": {
    "Four Columns": {
      "placeholders": {
        "0": "title",              // Main title
        "12": "col1_title",        // Column 1 title
        "13": "col1_content"       // Column 1 content
      }
    }
  },
  "aliases": {
    "four_cols": "Four Columns",   // User-friendly alias
    "4col": "Four Columns"         // Short alias
  }
}
```

Activate the mapping:
```bash
mv corporate.g.json corporate.json
```

#### Option B: Convention-Based Enhancement (Recommended)

Automatically apply standardized placeholder names:

```bash
deckbuilder template enhance corporate --use-conventions
```

This:
- Creates backup: `corporate_backup_TIMESTAMP.pptx`
- Applies semantic names: `title_top_1`, `content_col1_1`, `date_footer_1`
- Generates enhanced template: `corporate.g.pptx`
- Updates 150+ placeholders across all layouts

### Step 6: Generate Documentation

Create comprehensive template documentation:

```bash
deckbuilder template document corporate
```

This generates:
- Layout specifications with placeholder tables
- JSON and YAML usage examples
- Template management instructions
- Status tracking (mapping support, frontmatter compatibility)

### Step 7: Test Your Template

Test with example content:

```bash
deckbuilder create example_presentation.md --template corporate
```

Verify all layouts work correctly:
```bash
deckbuilder template validate corporate
```

## Convention-Based Naming System

The enhance command applies standardized naming patterns that provide consistency across all templates:

### Naming Patterns
- `title_top_1` - Main title placeholder
- `subtitle_1` - Subtitle placeholder
- `content_1` - Primary content area
- `content_col1_1` - First column content
- `content_col2_1` - Second column content
- `title_col1_1` - First column title
- `image_center_1` - Centered image placeholder
- `image_1` - Primary image placeholder
- `text_caption_1` - Caption text
- `date_footer_1` - Footer date placeholder
- `footer_footer_1` - Footer content
- `slide_number_footer_1` - Slide number

### Benefits
- **Predictable**: Always know what `title_top_1` means
- **Semantic**: Names describe content purpose and location
- **Consistent**: Same patterns across all templates
- **Maintainable**: Easy to update and extend
- **Automated**: No manual placeholder naming required

## Advanced Template Management

### Batch Processing Multiple Templates

Process multiple templates at once:

```bash
for template in corporate minimal modern; do
    deckbuilder template enhance $template --use-conventions
    deckbuilder template document $template
done
```

### Template File Organization

Recommended file structure:

```
templates/
├── corporate.pptx          # Your PowerPoint template
├── corporate.json          # Active mapping
├── corporate.g.pptx        # Enhanced template (use this!)
├── corporate.g.json        # Generated mapping (backup)
├── backups/                # Automatic backups
│   └── corporate_backup_TIMESTAMP.pptx
└── Getting_Started.md      # Documentation
```

### Environment Configuration

Make template configuration permanent:

```bash
# Add to .bash_profile or .bashrc
export DECK_TEMPLATE_FOLDER="/path/to/templates"
export DECK_OUTPUT_FOLDER="/path/to/output"
export DECK_TEMPLATE_NAME="corporate"
```

## Using Your New Template

### CLI Usage

```bash
# Use your new template
deckbuilder create presentation.md --template corporate

# With custom output location
deckbuilder create presentation.md --template corporate --output ./presentations/
```

### MCP Server Configuration

Configure the MCP server to use your template:

```json
{
  "mcpServers": {
    "deckbuilder": {
      "env": {
        "DECK_TEMPLATE_FOLDER": "/path/to/templates",
        "DECK_TEMPLATE_NAME": "corporate"
      }
    }
  }
}
```

### Python API Usage

```python
from deckbuilder import Deckbuilder

# Initialize with custom template
db = Deckbuilder(
    template_folder="/path/to/templates",
    template_name="corporate"
)

# Create presentation
result = db.create_presentation_from_markdown(
    content, 
    "MyPresentation"
)
```

## Template Validation and Troubleshooting

### Common Issues and Solutions

#### Placeholder Naming Inconsistencies
**Problem**: Multiple naming patterns in template
**Solution**: Use `deckbuilder template enhance corporate --use-conventions`

#### Missing Layout Mappings
**Problem**: Some layouts not generating correctly
**Solution**: Run `deckbuilder template validate corporate` for specific guidance

#### PowerPoint Template Corruption
**Problem**: Template file cannot be opened
**Solution**: Check backup files in `backups/` folder

### Validation Commands

```bash
# Check template health
deckbuilder template validate corporate

# Verify all layouts work
deckbuilder template analyze corporate --verbose

# Test with sample content
deckbuilder create example_presentation.md --template corporate
```

## Template Compatibility

### Supported Features
- All PowerPoint slide layouts (typically 19 layouts)
- Complex multi-column layouts
- Image placeholders with automatic fallbacks
- Table layouts with custom styling
- Footer elements (date, slide numbers, custom text)
- Master slide formatting preservation

### Layout Types
- **Single Content**: Title and Content, Section Header, Big Number
- **Multi-Column**: Two Content, Three/Four Columns (with/without titles)
- **Specialized**: Comparison, SWOT Analysis, Agenda layouts
- **Media**: Picture with Caption, Content with Caption
- **Orientation**: Vertical Title and Text, Title and Vertical Text

### Structured Frontmatter Support
Templates automatically support structured frontmatter patterns for:
- Column layouts with semantic field mapping
- Comparison layouts with left/right structure
- SWOT analysis with quadrant mapping
- Custom layout intelligence integration

This comprehensive template management system ensures that any PowerPoint template can be quickly integrated into Deckbuilder with full feature support and consistent user experience.