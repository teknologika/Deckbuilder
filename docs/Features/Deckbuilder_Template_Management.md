# Deckbuilder Template Management Guide

**For users who want to customize PowerPoint templates or create their own.**

This guide covers template analysis, validation, enhancement, and custom template creation. Use this when the default template doesn't meet your needs.

## Overview

Deckbuilder uses two files to define templates:
- **`template.pptx`** - The PowerPoint template file with layouts and styling
- **`template.json`** - Mapping file that tells Deckbuilder which placeholders to use

The CLI tools help you analyze existing templates and create these mapping files automatically.

## Quick Setup

```bash
# Analyze an existing PowerPoint template
python src/deckbuilder/cli_tools.py analyze my_template --verbose

# Generate documentation for the template
python src/deckbuilder/cli_tools.py document my_template

# Validate template structure and mappings
python src/deckbuilder/cli_tools.py validate my_template
```

## CLI Tools Reference

### `analyze` - Extract Template Structure

Analyzes a PowerPoint template and generates a JSON mapping file.

```bash
python src/deckbuilder/cli_tools.py analyze TEMPLATE_NAME [options]
```

**Options:**
- `--verbose` - Include detailed placeholder information
- `--template-folder PATH` - Custom template folder (default: auto-detected)
- `--output-folder PATH` - Custom output folder (default: auto-detected)

**What it does:**
1. Opens the PowerPoint template file
2. Extracts all slide layouts and their placeholders
3. Identifies placeholder types (title, content, image, etc.)
4. Generates a `.g.json` file with the structure
5. Reports validation issues and naming inconsistencies

**Example:**
```bash
# Basic analysis
python src/deckbuilder/cli_tools.py analyze corporate

# Detailed analysis with custom paths
python src/deckbuilder/cli_tools.py analyze corporate --verbose --template-folder ./templates
```

**Output:**
- **`corporate.g.json`** - Generated mapping file (ready for editing)
- **Console output** - Analysis summary and validation issues

### `document` - Generate Template Documentation

Creates comprehensive documentation for a template.

```bash
python src/deckbuilder/cli_tools.py document TEMPLATE_NAME [options]
```

**Options:**
- `--doc-output PATH` - Custom documentation output path

**What it generates:**
- Layout specifications with placeholder tables
- JSON and YAML usage examples
- Template management instructions
- Status tracking (mapping support, frontmatter compatibility)

**Example:**
```bash
python src/deckbuilder/cli_tools.py document corporate
# Creates: corporate_template_documentation.md
```

### `validate` - Check Template Health

Validates template structure and JSON mappings.

```bash
python src/deckbuilder/cli_tools.py validate TEMPLATE_NAME
```

**Validation checks:**
- ✅ Template file accessibility
- ✅ JSON mapping structure completeness
- ✅ Placeholder naming conventions
- ✅ Column layout consistency (Col 1, Col 2, Col 3, Col 4)
- ✅ Comparison layout structure (left/right placeholders)

**Example output:**
```
✓ Template file found: corporate.pptx
✓ JSON mapping file found: corporate.json
⚠ Warning: Layout 'Four Columns' has inconsistent column numbering
⚠ Warning: Missing placeholder for 'Col 3 Content'
✓ All layouts have title placeholders
```

### `enhance` - Improve Template Placeholders

Modifies PowerPoint template files to improve placeholder names.

```bash
python src/deckbuilder/cli_tools.py enhance TEMPLATE_NAME [options]
```

**Options:**
- `--mapping-file PATH` - Use specific mapping file
- `--no-backup` - Skip backup creation
- `--use-conventions` - Apply convention-based naming

**What it does:**
1. Creates backup of original template (`.backup.pptx`)
2. Opens PowerPoint template master slides
3. Renames placeholders to semantic names
4. Saves enhanced template (`.g.pptx`)

**Example:**
```bash
# Enhance with convention-based naming
python src/deckbuilder/cli_tools.py enhance corporate --use-conventions

# Use custom mapping file
python src/deckbuilder/cli_tools.py enhance corporate --mapping-file ./custom_mapping.json
```

## Working with Custom Templates

### Step 1: Prepare Your PowerPoint Template

Create or obtain a PowerPoint template (`.pptx` file) with the layouts you need:

1. **Open PowerPoint** and create a new presentation
2. **Go to View → Slide Master** to edit layouts
3. **Add/modify layouts** as needed
4. **Name placeholders clearly** (optional - CLI tools can fix this)
5. **Save as template** (`.pptx` file)

### Step 2: Analyze the Template

```bash
# Analyze your template
python src/deckbuilder/cli_tools.py analyze my_template --verbose

# This creates: my_template.g.json
```

**Sample output (`my_template.g.json`):**
```json
{
    "template_info": {
        "name": "My Custom Template",
        "version": "1.0",
        "created": "2025-01-26"
    },
    "layouts": {
        "Title Slide": {
            "index": 0,
            "placeholders": {
                "0": "Title 1",
                "1": "Subtitle 2"
            }
        },
        "Title and Content": {
            "index": 1,
            "placeholders": {
                "0": "Title 1",
                "14": "Content Placeholder 2"
            }
        },
        "Four Columns": {
            "index": 7,
            "placeholders": {
                "0": "Title 1",
                "12": "Col 1 Title 2",
                "13": "Col 1 Content 3",
                "14": "Col 2 Title 4",
                "15": "Col 2 Content 5"
            }
        }
    },
    "aliases": {
        "title": "Title Slide",
        "content": "Title and Content"
    }
}
```

### Step 3: Edit the Mapping (Optional)

Edit the `.g.json` file to:
- Add user-friendly aliases
- Map placeholders to semantic names
- Add custom configurations

```json
{
    "layouts": {
        "Four Columns": {
            "index": 7,
            "placeholders": {
                "0": "title",              // Main title
                "12": "col1_title",        // Column 1 title
                "13": "col1_content",      // Column 1 content
                "14": "col2_title",        // Column 2 title
                "15": "col2_content"       // Column 2 content
            }
        }
    },
    "aliases": {
        "four_cols": "Four Columns",       // User-friendly alias
        "4col": "Four Columns"             // Short alias
    }
}
```

### Step 4: Activate the Template

Rename the mapping file to activate it:
```bash
# Rename generated file to active mapping
mv my_template.g.json my_template.json
```

### Step 5: Use Your Template

```python
from deckbuilder import get_deckbuilder_client

deck = get_deckbuilder_client()

# Use your custom template
presentation_data = {
    "presentation": {
        "slides": [
            {
                "type": "Title Slide",
                "title": "**My Custom Presentation**",
                "subtitle": "Using my custom template"
            },
            {
                "type": "four_cols",  # Using alias
                "title": "Feature Comparison",
                "col1_title": "Performance",
                "col1_content": "**Fast** and reliable",
                "col2_title": "Security",
                "col2_content": "***Enterprise-grade***"
            }
        ]
    }
}

result = deck.create_presentation_from_json(
    presentation_data,
    "CustomPresentation",
    "my_template"  # Your template name
)
```

## Template File Organization

Deckbuilder looks for templates in this order:

1. **`DECK_TEMPLATE_FOLDER`** environment variable path
2. **`./assets/templates/`** relative to project root
3. **Built-in templates** in the package

**Recommended structure:**
```
templates/
├── my_template.pptx          # PowerPoint template
├── my_template.json          # Active mapping
├── my_template.g.json        # Generated mapping (backup)
├── corporate.pptx            # Another template
├── corporate.json            # Another mapping
└── backups/                  # Enhanced template backups
    ├── my_template.backup.pptx
    └── corporate.backup.pptx
```

## Advanced Features

### Convention-Based Naming

The `enhance` command can apply semantic naming conventions:

```bash
python src/deckbuilder/cli_tools.py enhance my_template --use-conventions
```

**Naming patterns:**
- `title_top_1` - Main title placeholder
- `content_col1_1` - First column content
- `content_col2_1` - Second column content
- `image_center_1` - Centered image placeholder
- `date_footer_1` - Footer date placeholder

### Validation and Fix Instructions

The `validate` command provides specific fix instructions:

```bash
python src/deckbuilder/cli_tools.py validate my_template
```

**Sample output:**
```
⚠ Layout 'Four Columns' issues:
  → Col 1 Content: Rename 'Col 1 Text Placeholder 3' to 'Col 1 Content 3'
  → Col 2 Content: Rename 'Col 2 Text Placeholder 5' to 'Col 2 Content 5'

Fix in PowerPoint:
1. Open template in PowerPoint
2. Go to View → Slide Master
3. Select 'Four Columns' layout
4. Use Selection Pane to rename placeholders
5. Save template
```

### Backup and Recovery

Template enhancement automatically creates backups:

```
templates/backups/
├── my_template_backup_20250126_143022.pptx  # Original backup
└── my_template.g.pptx                       # Enhanced version
```

**Recovery:**
```bash
# Restore from backup if needed
cp templates/backups/my_template_backup_20250126_143022.pptx templates/my_template.pptx
```

## Troubleshooting

### Template Not Found
```
Error: Template file not found: my_template.pptx
```
**Fix:** Check template folder path and file name

### Invalid JSON Mapping
```
Error: JSON mapping file contains errors
```
**Fix:** Run `validate` command to see specific issues

### Placeholder Mismatch
```
Warning: Placeholder 'col1_content' not found in layout
```
**Fix:** Check placeholder names in PowerPoint vs JSON mapping

### Permission Errors
```
Error: Cannot write to template file
```
**Fix:** Ensure template file isn't open in PowerPoint

## Best Practices

1. **Start with analysis**: Always run `analyze` before customizing
2. **Validate regularly**: Use `validate` to catch issues early
3. **Keep backups**: Never modify original templates directly
4. **Use semantic names**: Make placeholder names human-readable
5. **Document your templates**: Generate docs for team reference
6. **Test thoroughly**: Validate with actual content before production use

This covers everything you need for custom template management. The CLI tools handle the complex PowerPoint manipulation automatically, so you can focus on design and content structure.

## Related Documentation

- **[Placeholder Matching](Placeholder_Matching.md)** - Deep dive into the hybrid template system architecture
- **[Convention Based Naming](Convention_Based_Naming.md)** - Naming conventions and multi-tier detection system
- **[Supported Templates](Supported_Templates.md)** - Status of all 50+ planned business layouts
- **[Default Template](Default_Template.md)** - Specifications for the built-in template
- **[Template Management](Template_Management.md)** - Original template management system design
