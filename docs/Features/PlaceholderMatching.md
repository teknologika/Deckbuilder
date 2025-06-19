#  This is a early desing for pushing content into placehodlers in deckbuilder

## Architecture Overview

### Core Components

- Template Packages: PPTX file + JSON configuration file
- Layout Configuration: JSON schema describing available layouts
- Layout Manager: Dynamic layout loading and validation
- Backward Compatibility: Maintains existing API while adding flexibility

### File Structure

templates/
├── default.pptx               # PowerPoint template file
├── default.json               # Layout configuration for default.pptx
├── corporate.pptx             # Corporate template
├── corporate.json             # Layout configuration for corporate.pptx
└── custom.pptx                # Custom template
└── custom.json                # Layout configuration for custom.pptx

### Template Loading Logic

- Template name: default → Load default.pptx + default.json
- Template name: corporate → Load corporate.pptx + corporate.json

If JSON file doesn't exist, fall back to current hardcoded layouts
JSON filename always matches PPTX filename (just different extension)
This approach is much cleaner and easier to manage. Each template is a pair of files with matching names, making it obvious which configuration goes with which template.

The rest of the design remains the same - same JSON schema, same API, same backward compatibility. Does this simplified file structure work better for your needs?

## Implementation Strategy

# New Classes

- TemplateManager: Handles template loading and validation
- LayoutConfig: Parses and validates layout configurations
- DynamicLayoutHandler: Maps content to layout placeholders

# Key Features

- Human & LLM Readable: JSON format with clear descriptions
- Flexible Placeholders: Support for different content types (text, content, images)
- Validation: Ensures template and config compatibility
- Backward Compatibility: Existing code continues to work, with content in both Markdown and json 
- Extensible: Easy to add new layout types and templates

# API Usage Examples

# Current usage (still works)
slide_data = {"type": "content", "title": "My Slide", "content": "..."}

# New advanced usage
slide_data = {
    "type": "five_column",
    "title": "Comparison Matrix",
    "col1_header": "Feature A",
    "col1_content": "Details about A",
    "col2_header": "Feature B", 
    "col2_content": "Details about B",
    # ... etc
}

# Benefits

- Template Flexibility: Each template can define its own layouts
- Rich Descriptions: Self-documenting for humans and LLMs
- Type Safety: Validates content against expected placeholders
- Easy Extension: Add new layouts without code changes
- Template Portability: Share templates with their configurations

# Template Loading Logic

- Template name: default → Load default.pptx + default.json
- Template name: corporate → Load corporate.pptx + corporate.json
- If JSON file doesn't exist, fall back to defailt.json then if that fails current hardcoded layouts
- JSON filename always matches PPTX filename (just different extension)

# Proposed Json Schema

{
  "template_info": {
    "name": "Default Template",
    "version": "1.0"
  },
  "layouts": {
    "title": {
      "index": 0,
      "placeholders": {
        "0": "title",
        "1": "subtitle"
      }
    },
    "content": {
      "index": 1,
      "placeholders": {
        "0": "title",
        "1": "content"
      }
    },
    "five_column": {
      "index": 8,
      "placeholders": {
        "0": "title",
        "1": "col1_header",
        "2": "col1_content",
        "3": "col2_header",
        "4": "col2_content",
        "5": "col3_header",
        "6": "col3_content",
        "7": "col4_header",
        "8": "col4_content",
        "9": "col5_header",
        "10": "col5_content"
      }
    }
  },
  "aliases": {
    "table": "content",
    "bullets": "content"
  }
}

# proposed Implementation

# Direct mapping: placeholder index -> field name
placeholder_idx = int(placeholder_key)  # "0" -> 0
field_name = placeholder_config[placeholder_key]  # "title"

if field_name in slide_data:
    placeholder = slide.placeholders[placeholder_idx]
    self._fill_placeholder(placeholder, slide_data[field_name])
Much cleaner! The format is now:

"0": "title" = placeholder index 0 maps to slide_data field "title"
"1": "content" = placeholder index 1 maps to slide_data field "content"

Here's how the code would use "9": "col5_header":

# Code Implementation

def _add_slide(self, slide_data):
    slide_type = slide_data.get("type", "content")
    layout_config = self.template_manager.get_layout_config(slide_type)
    
    # Create slide
    slide_layout = self.prs.slide_layouts[layout_config["index"]]
    slide = self.prs.slides.add_slide(slide_layout)
    
    # Fill placeholders
    for placeholder_idx_str, field_name in layout_config["placeholders"].items():
        placeholder_idx = int(placeholder_idx_str)  # "9" -> 9
        
        if field_name in slide_data:  # Check if "col5_header" exists in slide_data
            try:
                placeholder = slide.placeholders[placeholder_idx]  # Get placeholder 9
                field_value = slide_data[field_name]  # Get value for "col5_header"
                self._fill_placeholder(placeholder, field_value)
            except (IndexError, KeyError):
                # Handle missing placeholder gracefully
                print(f"Warning: Placeholder {placeholder_idx} not found in layout")
# Usage Example

Simplified JSON with Custom Names

{
  "five_column": {
    "index": 8,
    "placeholders": {
      "0": "title",
      "1": "col1_header",    # This matches what you named in PowerPoint
      "2": "col1_content",   # This matches what you named in PowerPoint
      "9": "col5_header"     # This matches what you named in PowerPoint
    }
  }
}