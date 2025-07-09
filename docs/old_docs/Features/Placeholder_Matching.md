# Placeholder Matching System

## Overview

The placeholder matching system enables reliable content mapping to PowerPoint template layouts using a combination of semantic detection and JSON configuration files. This hybrid approach ensures that basic slide content (titles, subtitles, content) works reliably with any PowerPoint template, while still supporting advanced customization through JSON mappings for complex layouts.

**Key Features:**
- **Semantic Detection**: Automatically finds title, subtitle, and content placeholders using PowerPoint's built-in types
- **Template Independence**: Basic slide creation works with any PowerPoint template without configuration
- **JSON Mapping**: Advanced layouts can be customized using template-specific mapping files
- **Reliable Content Placement**: Combines the best of both approaches for robust slide generation

## Architecture Overview

### Core Components

- **Template Analyzer** (`src/mcp_server/tools.py`): Extracts layout and placeholder information from PPTX files
- **Semantic Detection** (`placeholder_types.py`): Identifies placeholder types using PowerPoint's built-in semantic types
- **JSON Mapping System**: Dynamic layout configuration using template-specific JSON files
- **Unified Mapping Logic** (`deckbuilder.py`): Combines semantic detection with JSON mappings for reliable content placement
- **Template Packages**: PPTX file + JSON configuration file pairs
- **Backward Compatibility**: Maintains existing API while adding flexibility

### File Structure

        templates

        ├── default.pptx     # PowerPoint template file
        ├── default.json     # Layout configuration for default.pptx
        ├── corporate.pptx   # Corporate template
        ├── corporate.json   # Layout configuration for corporate.pptx
        └── custom.pptx      # Custom template
        └── custom.json      # Layout configuration for custom.pptx

### Template Generation Workflow

1. **Extract Template Structure**: Run `python tests/test_tools.py` to analyze a PowerPoint template
2. **Generate Raw Mapping**: Creates `templateName.g.json` with extracted layout and placeholder information
3. **Activate Mapping**: Rename `templateName.g.json` to `templateName.json` when ready to use

### Template Loading Logic

- Template name: `default` → Load `default.pptx` + `default.json`
- Template name: `corporate` → Load `corporate.pptx` + `corporate.json`
- **Automatic Default Copying**: The default Template and JSON files are automatically copied from `src/` to template folder on first use
- **Fallback Strategy**: If JSON file doesn't exist, falls back gracefully with basic layout support
- **File Pairing**: JSON filename always must match the PPTX filename (just different extension)

## Implementation

### Template Analyzer (`src/mcp_server/tools.py`)

The `TemplateAnalyzer` class provides:
- **Layout Discovery**: Extracts actual PowerPoint layout names (e.g., "Title Slide", "Title and Content")
- **Placeholder Detection**: Identifies placeholder indices and names from PowerPoint templates
- **JSON Generation**: Creates structured mapping files ready for customization
- **Environment Integration**: Uses `DECK_TEMPLATE_FOLDER` and `DECK_OUTPUT_FOLDER` environment variables

### Key Features

- **Human & LLM Readable**: JSON format with clear layout and placeholder descriptions
- **Automatic Discovery**: Extracts actual names from PowerPoint templates instead of using generic placeholders
- **Flexible Mapping**: Support for any layout structure with customizable placeholder assignments
- **Template Portability**: Each template comes with its own configuration file.
- **Extensible**: Easy to add new layout types and templates without code changes

## Usage Examples

### Template Analysis

```bash
# Generate mapping for a PowerPoint template
python tests/test_tools.py

# This creates templateName.g.json with extracted structure
```

### Basic Content (Semantic Detection)
These fields work reliably with any PowerPoint template using semantic detection:

```python
# Title slide using semantic detection
slide_data = {
    "type": "Title Slide",
    "title": "My Presentation Title",    # Automatically finds title placeholder
    "subtitle": "Subtitle Text"          # Automatically finds subtitle placeholder
}

# Content slide using semantic detection
slide_data = {
    "type": "Title and Content",
    "title": "Content Slide Title",      # Automatically finds title placeholder
    "content": [                         # Automatically finds content placeholder
        "First bullet point",
        "Second bullet point"
    ]
}
```

### Advanced Layout Usage (JSON Mapping)
For custom layout fields, use the JSON mapping system:

```python
slide_data = {
    "type": "Four Columns",                         # Uses actual PowerPoint layout name
    "title": "Comparison Matrix",                   # Uses semantic detection
    "Col 1 Title Placeholder 2" : "Feature A",      # Uses JSON mapping to placeholder 13
    "Col 1 Text Placeholder 3" : "Details about A", # Uses JSON mapping to placeholder 14
    "Col 2 Title Placeholder 4": "Feature B",       # Uses JSON mapping to placeholder 15
    "Col 2 Text Placeholder 5": "Details about B",  # Uses JSON mapping to placeholder 16
    # ... etc
}
```

### How It Works Behind the Scenes
```python
# For "title" field - uses semantic detection
if field_name == "title":
    for placeholder in slide.placeholders:
        if is_title_placeholder(placeholder.placeholder_format.type):
            # Found! Apply content to this placeholder
            break

# For "col_1_title" field - uses JSON mapping
else:
    if field_name in field_to_index:  # "col_1_title" maps to index 13
        placeholder_idx = field_to_index[field_name]  # Get index 13
        for placeholder in slide.placeholders:
            if placeholder.placeholder_format.idx == placeholder_idx:
                # Found! Apply content to placeholder at index 13
                break
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
        "0": "Title 1",
        "13": "Col 1 Title Placeholder 2",
        "14": "Col 1 Text Placeholder 3",
        "15": "Col 2 Title Placeholder 4",
        "16": "Col 2 Text Placeholder 5",
        "17": "Col 3 Title Placeholder 6",
        "18": "Col 3 Text Placeholder 7",
        "19": "Col 4 Title Placeholder 8",
        "20": "Col 4 Text Placeholder 9",
        "10": "Date Placeholder 10",
        "11": "Footer Placeholder 11",
        "12": "Slide Number Placeholder 12"
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

The system combines semantic detection with JSON mappings for reliable content placement:

#### Layout Selection
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

#### Content Placement with Semantic Detection
```python
def _apply_content_to_mapped_placeholders(self, slide, slide_data, layout_name):
    # Process each field in slide_data using semantic detection
    for field_name, field_value in slide_data.items():
        target_placeholder = None

        # Handle title placeholders using semantic detection
        if field_name == "title":
            for placeholder in slide.placeholders:
                if is_title_placeholder(placeholder.placeholder_format.type):
                    target_placeholder = placeholder
                    break

        # Handle subtitle placeholders using semantic detection
        elif field_name == "subtitle":
            for placeholder in slide.placeholders:
                if is_subtitle_placeholder(placeholder.placeholder_format.type):
                    target_placeholder = placeholder
                    break

        # Handle content placeholders using semantic detection
        elif field_name == "content":
            for placeholder in slide.placeholders:
                if is_content_placeholder(placeholder.placeholder_format.type):
                    target_placeholder = placeholder
                    break

        # Handle other fields using JSON mapping
        else:
            # Try to find by exact field name match in JSON mapping
            if field_name in field_to_index:
                placeholder_idx = field_to_index[field_name]
                for placeholder in slide.placeholders:
                    if placeholder.placeholder_format.idx == placeholder_idx:
                        target_placeholder = placeholder
                        break

        if target_placeholder:
            # Apply content based on placeholder's semantic type
            self._apply_content_by_semantic_type(target_placeholder, field_name, field_value, slide_data)
```

### How Content Placement Works

The system uses a two-tier approach for reliable content placement:

#### 1. Semantic Detection (Primary)
For common slide fields (`title`, `subtitle`, `content`), the system uses PowerPoint's built-in semantic placeholder types:

```python
# From placeholder_types.py
TITLE_PLACEHOLDERS = {
    PP_PLACEHOLDER_TYPE.TITLE,         # Standard slide title
    PP_PLACEHOLDER_TYPE.CENTER_TITLE,  # Centered title (title slides)
    PP_PLACEHOLDER_TYPE.VERTICAL_TITLE # Vertical orientation title
}

SUBTITLE_PLACEHOLDERS = {
    PP_PLACEHOLDER_TYPE.SUBTITLE       # Subtitle text
}

CONTENT_PLACEHOLDERS = {
    PP_PLACEHOLDER_TYPE.BODY,          # Main content area
    PP_PLACEHOLDER_TYPE.VERTICAL_BODY  # Vertical text content
}
```

**Benefits:**
- **Template Independent**: Works with any PowerPoint template
- **Reliable**: Uses PowerPoint's built-in semantic types
- **Automatic**: No manual mapping required for basic content

#### 2. JSON Mapping (Secondary)
For custom layout fields (like column content), the system falls back to JSON mappings:

- `"0": "Title 1"` = placeholder index 0 contains PowerPoint's actual name
- `"13": "Col 1 Title Placeholder 2"` = placeholder index 13 maps to first column title
- `"14": "Col 1 Text Placeholder 3"` = placeholder index 14 maps to first column content

**Usage:**
```python
slide_data = {
    "type": "Four Columns",
    "title": "Comparison Matrix",           # Uses semantic detection
    "col_1_title": "Feature A",            # Uses JSON mapping to index 13
    "col_1_content": "Details about A",    # Uses JSON mapping to index 14
    # ... etc
}
```

### Generated vs. Customized Names

**Generated Output** (from `src/mcp_server/tools.py`):
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

## Troubleshooting

### Common Issues

#### 1. Titles Not Appearing
**Problem**: Title content isn't showing up in slides
**Solution**: The system now uses semantic detection - ensure your slide_data uses the field name `"title"`:

```python
# ✅ Correct - uses semantic detection
slide_data = {"type": "Title and Content", "title": "My Title"}

# ❌ Wrong - won't be recognized
slide_data = {"type": "Title and Content", "slide_title": "My Title"}
```

#### 2. Custom Fields Not Working
**Problem**: Custom layout fields (like column content) aren't appearing
**Solution**: Check that your JSON mapping includes the correct field names:

```json
{
  "Four Columns": {
    "placeholders": {
      "13": "col_1_title",    // Must match slide_data field name exactly
      "14": "col_1_content"   // Must match slide_data field name exactly
    }
  }
}
```

#### 3. Wrong Placeholder Selected
**Problem**: Content appears in unexpected placeholders
**Solution**: The system prioritizes semantic detection. For troubleshooting:

1. Check if you're using reserved field names (`title`, `subtitle`, `content`)
2. Use `python tests/test_tools.py` to regenerate template mappings
3. Verify placeholder indices in the generated `.g.json` file

### Debugging Tips

1. **Check Template Structure**: Run `python tests/test_tools.py` to see actual placeholder indices and names
2. **Semantic vs JSON**: Remember that `title`, `subtitle`, and `content` use semantic detection, other fields use JSON mapping
3. **Field Name Matching**: Custom field names must exactly match the JSON mapping keys
4. **Template Loading**: Ensure both `.pptx` and `.json` files exist in the template folder

## Content Intelligence Storage Design

### Design Decision: Separate Layout Intelligence System

**Options Considered:**
1. **Enhanced Template JSON**: Extend existing `default.json` with semantic metadata
2. **Separate Content Intelligence JSON**: New `layout_intelligence.json` file ✅ **SELECTED**
3. **Embedded Content Patterns**: YAML-based content matching rules
4. **Database/Vector Store**: Advanced semantic matching with embeddings

**Decision: Option 2 - Separate Content Intelligence JSON**

**Rationale:**
- **Separation of Concerns**: Technical template data vs semantic intelligence remain distinct
- **Easy to Extend**: Add new layouts without touching core template structure
- **LLM-Friendly**: Rich descriptive content optimized for content analysis
- **Maintainable**: Content experts can edit without touching placeholder mappings
- **Backwards Compatible**: Existing template system unchanged

### Layout Intelligence Architecture

The content-first MCP tools will use a separate `src/layout_intelligence.json` file containing semantic information about each layout:

```json
{
  "Comparison": {
    "semantic_tags": ["contrast", "versus", "choice", "alternative", "decision"],
    "content_triggers": ["vs", "versus", "compared to", "old way", "new approach", "before", "after"],
    "ideal_for": {
      "content_types": ["decision making", "feature comparison", "method analysis"],
      "audience": ["stakeholders", "decision makers", "executives"],
      "presentation_goals": ["persuade", "inform", "evaluate options"]
    },
    "use_cases": [
      "Traditional vs Modern Architecture",
      "Our Solution vs Competitors",
      "Before vs After Implementation"
    ],
    "strengths": ["clear contrast", "easy comparison", "decision support"],
    "limitations": ["only two options", "not suitable for complex data"],
    "recommendation_confidence": {
      "high": "when content contains comparative language",
      "medium": "when presenting two distinct concepts",
      "low": "when more than two options need comparison"
    }
  },
  "Four Columns": {
    "semantic_tags": ["features", "matrix", "categories", "breakdown"],
    "content_triggers": ["features", "aspects", "categories", "components", "pillars"],
    "ideal_for": {
      "content_types": ["feature showcase", "categorical breakdown", "comparison matrix"],
      "audience": ["technical teams", "product managers", "general audience"],
      "presentation_goals": ["inform", "educate", "showcase capabilities"]
    },
    "use_cases": [
      "Product Feature Comparison",
      "Service Offering Breakdown",
      "Strategic Pillar Overview"
    ],
    "strengths": ["organized information", "easy scanning", "comprehensive overview"],
    "limitations": ["limited detail per section", "requires even content distribution"],
    "recommendation_confidence": {
      "high": "when content has 4 distinct categories or features",
      "medium": "when content can be logically grouped into 4 sections",
      "low": "when content doesn't naturally divide into 4 parts"
    }
  }
}
```

### Integration with Content-First MCP Tools

The layout intelligence system will support the content-first workflow:

1. **`analyze_presentation_needs()`**: Uses semantic tags to understand content themes
2. **`recommend_slide_approach()`**: Matches content triggers to suggest optimal layouts
3. **`optimize_content_for_layout()`**: Uses use cases and examples to structure content

### Content Matching Strategy

**Multi-Level Matching:**
1. **Keyword Triggers**: Direct phrase matching (`"vs"` → Comparison layout)
2. **Semantic Tags**: Content theme analysis (`"decision making"` → Comparison layout)
3. **Audience Consideration**: Stakeholder-appropriate recommendations
4. **Goal Alignment**: Presentation objective matching (persuade vs inform)
5. **Content Structure**: Natural content organization patterns

### Extensibility

**Adding New Layouts:**
1. Add layout to `default.json` (technical structure)
2. Add layout to `layout_intelligence.json` (semantic information)
3. Update `SupportedTemplates.md` (documentation)
4. Content-first tools automatically gain new layout awareness

This design enables intelligent content-to-layout matching while maintaining clean separation between technical template structure and semantic content intelligence.
