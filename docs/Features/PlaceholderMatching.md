# Placeholder Matching System

## Overview

The placeholder matching system enables dynamic content mapping to PowerPoint template layouts using JSON configuration files. This system automatically analyzes PowerPoint templates and generates mapping configurations that can be customized for precise content placement.

## Architecture Overview

### Core Components

- **Template Analyzer** (`tools.py`): Extracts layout and placeholder information from PPTX files
- **JSON Mapping System**: Dynamic layout configuration using template-specific JSON files  
- **Layout Manager**: Loads and applies JSON mappings at runtime
- **Template Packages**: PPTX file + JSON configuration file pairs
- **Backward Compatibility**: Maintains existing API while adding flexibility

### File Structure

templates/
├── default.pptx               # PowerPoint template file
├── default.json               # Layout configuration for default.pptx
├── corporate.pptx             # Corporate template
├── corporate.json             # Layout configuration for corporate.pptx
└── custom.pptx                # Custom template
└── custom.json                # Layout configuration for custom.pptx

### Template Generation Workflow

1. **Extract Template Structure**: Run `python tests/test_tools.py` to analyze a PowerPoint template
2. **Generate Raw Mapping**: Creates `templateName.g.json` with extracted layout and placeholder information
3. **Customize Mapping**: Edit the `.g.json` file to map placeholder indices to meaningful names
4. **Activate Mapping**: Rename `templateName.g.json` to `templateName.json` when ready to use

### Template Loading Logic

- Template name: `default` → Load `default.pptx` + `default.json`
- Template name: `corporate` → Load `corporate.pptx` + `corporate.json`
- **Automatic Copying**: Template and JSON files are automatically copied from `src/` to template folder on first use
- **Fallback Strategy**: If JSON file doesn't exist, falls back gracefully with basic layout support
- **File Pairing**: JSON filename always matches PPTX filename (just different extension)

## Implementation

### Template Analyzer (`tools.py`)

The `TemplateAnalyzer` class provides:
- **Layout Discovery**: Extracts actual PowerPoint layout names (e.g., "Title Slide", "Title and Content")
- **Placeholder Detection**: Identifies placeholder indices and names from PowerPoint templates
- **JSON Generation**: Creates structured mapping files ready for customization
- **Environment Integration**: Uses `DECK_TEMPLATE_FOLDER` and `DECK_OUTPUT_FOLDER` environment variables

### Key Features

- **Human & LLM Readable**: JSON format with clear layout and placeholder descriptions
- **Automatic Discovery**: Extracts actual names from PowerPoint templates instead of using generic placeholders
- **Flexible Mapping**: Support for any layout structure with customizable placeholder assignments
- **Template Portability**: Each template comes with its own configuration file
- **Backward Compatibility**: Existing slide creation code continues to work unchanged
- **Extensible**: Easy to add new layout types and templates without code changes

## Usage Examples

### Template Analysis

```bash
# Generate mapping for a PowerPoint template
python tests/test_tools.py

# This creates templateName.g.json with extracted structure
```

### Current API (still works)
```python
slide_data = {"type": "content", "title": "My Slide", "content": "..."}
```

### Advanced Layout Usage
```python
slide_data = {
    "type": "Four Columns",  # Uses actual PowerPoint layout name
    "title": "Comparison Matrix",
    "col_1_title": "Feature A",
    "col_1_content": "Details about A",
    "col_2_title": "Feature B", 
    "col_2_content": "Details about B",
    # ... etc
}
```

### Template Creation Workflow

1. **Create PowerPoint Template**: Design your template with named placeholders
2. **Generate Mapping**: `python tests/test_tools.py` to create `.g.json` file  
3. **Customize Mapping**: Edit placeholder assignments in the `.g.json` file
4. **Activate Template**: Rename `.g.json` to `.json` and place with `.pptx` file
5. **Use Template**: Reference by name in `create_presentation(templateName)`

## JSON Schema

The system uses the following JSON structure for template mappings:

```json
{
  "template_info": {
    "name": "Default Template",
    "version": "1.0"
  },
  "layouts": {
    "Title Slide": {
      "index": 0,
      "placeholders": {
        "0": "title",
        "1": "subtitle"
      }
    },
    "Title and Content": {
      "index": 1,
      "placeholders": {
        "0": "title",
        "1": "content"
      }
    },
    "Four Columns": {
      "index": 11,
      "placeholders": {
        "0": "title",
        "13": "col_1_title",
        "14": "col_1_content",
        "15": "col_2_title",
        "16": "col_2_content",
        "17": "col_3_title",
        "18": "col_3_content",
        "19": "col_4_title",
        "20": "col_4_content"
      }
    }
  },
  "aliases": {
    "content": "Title and Content",
    "title": "Title Slide",
    "table": "Title and Content",
    "bullets": "Title and Content"
  }
}
```

### Schema Elements

- **template_info**: Metadata about the template
- **layouts**: Maps PowerPoint layout names to their configuration
  - **index**: PowerPoint layout index in the template
  - **placeholders**: Maps placeholder indices to field names
- **aliases**: Maps user-friendly names to actual layout names

## Implementation Details

### Current Implementation in `deckbuilder.py`

The system is fully implemented and working:

```python
def _add_slide(self, slide_data):
    # Get slide type and determine layout using JSON mapping
    slide_type = slide_data.get("type", "content")
    
    # Use layout mapping if available
    if self.layout_mapping:
        aliases = self.layout_mapping.get("aliases", {})
        layouts = self.layout_mapping.get("layouts", {})
        
        # Get layout name from aliases
        layout_name = aliases.get(slide_type, slide_type)
        
        # Get layout index
        layout_info = layouts.get(layout_name, {})
        layout_index = layout_info.get("index", 1)
    else:
        # Fallback
        layout_index = 1
    
    slide_layout = self.prs.slide_layouts[layout_index]
    slide = self.prs.slides.add_slide(slide_layout)
```

### Placeholder Mapping

Direct mapping from placeholder index to field name:
- `"0": "title"` = placeholder index 0 maps to `slide_data["title"]`
- `"1": "content"` = placeholder index 1 maps to `slide_data["content"]`
- `"13": "col_1_title"` = placeholder index 13 maps to `slide_data["col_1_title"]`

### Generated vs. Customized Names

**Generated Output** (from `tools.py`):
```json
{
  "Four Columns": {
    "index": 11,
    "placeholders": {
      "0": "Title 1",                    // PowerPoint's actual name
      "13": "col_1_title",               // PowerPoint's actual name  
      "14": "col_1_content"              // PowerPoint's actual name
    }
  }
}
```

**Customized Mapping** (user edited):
```json
{
  "Four Columns": {
    "index": 11,
    "placeholders": {
      "0": "title",                      // Simplified for slide_data
      "13": "feature_name",              // Semantic field name
      "14": "feature_description"        // Semantic field name  
    }
  }
}
```