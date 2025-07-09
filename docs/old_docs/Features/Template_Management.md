# Template Management System Guide

## Overview

This guide walks you through using the Template Management System to analyze, enhance, and maintain PowerPoint templates. The system provides automated tools that eliminate manual PowerPoint editing and ensure consistent, professional template quality.

## Getting Started

### Prerequisites

1. **Activate Virtual Environment** (Required for all commands)
   ```bash
   # From project root
   cd /path/to/deck-builder-mcp
   source venv/bin/activate
   ```

2. **Verify Template Location**
   - Templates should be in `assets/templates/`
   - Default template: `assets/templates/default.pptx`

### Basic Workflow

The template management system follows a simple 4-step process:

1. **Analyze** → Extract template structure
2. **Enhance** → Apply convention-based naming
3. **Validate** → Check for issues
4. **Document** → Generate comprehensive docs

## Step-by-Step Guide

### Step 1: Analyze Template Structure

Start by analyzing your PowerPoint template to understand its current state:

```bash
# Basic analysis
python src/deckbuilder/cli_tools.py analyze default --verbose

# With custom paths
python src/deckbuilder/cli_tools.py --template-folder ./templates --output-folder ./output analyze mytemplate --verbose
```

**What this does:**
- Extracts all slide layouts (typically 19 layouts)
- Identifies placeholder names and types
- Detects naming inconsistencies
- Generates `template_output/default.g.json` for review

**Sample Output:**
```
🔍 Analyzing template: default
📊 Found 19 layouts
⚠️  Multiple placeholder naming patterns detected:
['Col 1', 'Col 2', 'Content Placeholder', 'Date Placeholder']
📄 Generated: template_output/default.g.json
```

### Step 2: Enhance Template with Convention-Based Naming

Apply standardized placeholder names automatically:

```bash
# Enhance with convention-based naming (recommended)
python src/deckbuilder/cli_tools.py enhance default --use-conventions

# Skip backup creation (for testing)
python src/deckbuilder/cli_tools.py enhance default --use-conventions --no-backup
```

**What this does:**
- Creates backup in `assets/templates/backups/`
- Applies standardized names like `title_top_1`, `content_col1_1`, `date_footer_1`
- Generates enhanced template: `assets/templates/default.g.pptx`
- Updates 150+ placeholders across all 19 layouts

**Sample Output:**
```
🔧 Enhancing template: default
📄 Backup created: assets/templates/backups/default_backup_20250623_141526.pptx
🎯 Using convention-based naming system...
✅ Enhancement complete!
   📊 Modified 150 placeholders across 19 layouts
   📄 Enhanced template saved: assets/templates/default.g.pptx
```

### Step 3: Validate Enhanced Template

Check that everything worked correctly:

```bash
# Validate template structure and mappings
python src/deckbuilder/cli_tools.py validate default

# Analyze enhanced template
python src/deckbuilder/cli_tools.py analyze default.g --verbose
```

**What to look for:**
- ✅ No more "Multiple placeholder naming patterns" warnings
- ✅ Consistent naming across all layouts
- ⚠️ Any remaining validation errors (usually minor layout structure issues)

### Step 4: Generate New JSON Mapping

Create a clean JSON mapping file from the enhanced template:

```bash
# Analyze enhanced template to generate mapping
python src/deckbuilder/cli_tools.py analyze default.g --verbose

# Copy generated mapping to become new default.json
cp template_output/default.g.g.json assets/templates/default.json
```

### Step 5: Generate Documentation

Create comprehensive documentation for your template:

```bash
# Generate template documentation
python src/deckbuilder/cli_tools.py document default

# Custom documentation path
python src/deckbuilder/cli_tools.py document default --doc-output ./my-docs/Template.md
```

**Generated Documentation Includes:**
- Layout summary table with placeholder counts
- Detailed specifications for each layout
- JSON mapping status
- Usage examples in both JSON and YAML formats
- Template management instructions

## Understanding Convention-Based Naming

The system applies a standardized naming pattern to all placeholders:

### Naming Format
```
{ContentType}_{Position}_{Index}
```

### Examples
| Old Name | New Convention Name | Purpose |
|----------|-------------------|----------|
| "Title 1" | `title_top_1` | Main slide title |
| "Col 1 Text Placeholder 3" | `content_col1_1` | First column content |
| "Date Placeholder 3" | `date_footer_1` | Footer date |
| "Content Placeholder 2" | `content_1` | General content area |

### Benefits
- **Predictable**: Always know what `title_top_1` means
- **Semantic**: Names describe content purpose
- **Consistent**: Same patterns across all templates
- **Maintainable**: Easy to update and extend

## Troubleshooting Common Issues

### Template Not Found
```bash
❌ Template file not found: assets/templates/mytemplate.pptx
```
**Solution:** Verify template exists and use correct name (without .pptx extension)

### Permission Errors
```bash
❌ Failed to save enhanced template: Permission denied
```
**Solution:** Close PowerPoint if template is open, check file permissions

### Virtual Environment Issues
```bash
ModuleNotFoundError: No module named 'pptx'
```
**Solution:** Activate virtual environment: `source venv/bin/activate`

### Mapping File Missing
```bash
❌ Mapping file not found: default.json. Run 'analyze' first to generate mapping.
```
**Solution:** Run analyze command first to generate the mapping file

## Advanced Usage

### Custom Template Folders
```bash
# Work with templates in different locations
python src/deckbuilder/cli_tools.py --template-folder ./my-templates --output-folder ./my-output analyze corporate --verbose
```

### Batch Processing Multiple Templates
```bash
# Process multiple templates
for template in corporate minimal modern; do
    python src/deckbuilder/cli_tools.py enhance $template --use-conventions
    python src/deckbuilder/cli_tools.py document $template
done
```

### Development and Testing
```bash
# Analyze without generating files (dry run)
python src/deckbuilder/cli_tools.py analyze default --verbose

# Enhance without backup (for rapid testing)
python src/deckbuilder/cli_tools.py enhance default --use-conventions --no-backup
```

## File Organization

After running the template management system, you'll have:

```
assets/templates/
├── default.pptx              # Original template
├── default.g.pptx            # Enhanced template (use this!)
├── default.json              # JSON mapping for enhanced template
├── backups/                  # Automatic backups
│   ├── default_backup_20250623_141526.pptx
│   └── ...

template_output/
├── default.g.json            # Raw analysis for editing
├── default.g.g.json          # Analysis of enhanced template
└── ...

docs/Features/
├── Default_Template.md        # Generated documentation
└── ...
```

## Integration with Presentation Engine

Once you have an enhanced template:

1. **Update Engine Configuration:** Change default template from `default.pptx` to `default.g.pptx`
2. **Test with MCP Tools:** Verify presentations generate correctly
3. **Use New Mapping:** The enhanced `default.json` provides reliable content placement

## Best Practices

1. **Always Create Backups:** Use default backup creation for production templates
2. **Test Thoroughly:** Validate enhanced templates before deploying
3. **Document Changes:** Generate documentation after any template modifications
4. **Use Version Control:** Commit enhanced templates and mappings to git
5. **Convention Over Configuration:** Prefer `--use-conventions` over manual naming

## Next Steps

After completing template enhancement:

1. **Update Engine:** Switch presentation engine to use enhanced template
2. **Test Comprehensive Layouts:** Verify all 19 layouts work correctly
3. **Content Intelligence:** Leverage standardized names for layout recommendations
4. **Documentation:** Keep template documentation up to date

---

## TODO

- [ ] Add support for bulk template processing
- [ ] Implement template comparison tools
- [ ] Add convention compliance scoring
- [ ] Create template migration utilities
- [ ] Add support for custom naming conventions
- [ ] Implement template versioning system
- [ ] Add automated testing for enhanced templates
- [ ] Create template quality metrics dashboard
- [ ] Add support for template themes and branding
- [ ] Implement rollback functionality for enhancements
