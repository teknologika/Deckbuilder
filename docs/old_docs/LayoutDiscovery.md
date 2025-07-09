# Layout Discovery and Validation System

## Overview

Deckbuilder's MCP server uses a sophisticated multi-layered system to determine what slide layouts are supported and how to process markdown content. This guide explains how layout discovery works, validation processes, and the relationship between different system components.

## Architecture Overview

The layout discovery system operates through **four complementary layers**:

1. **Template JSON Mappings** - Core layout definitions and placeholder mappings
2. **Layout Intelligence System** - Content-first semantic recommendations  
3. **Structured Frontmatter Registry** - Clean YAML authoring patterns
4. **Fallback Mechanisms** - Graceful degradation when layouts are missing

## Layer 1: Template JSON Mappings (Primary Source)

### Location and Structure
- **File**: `/src/deckbuilder/assets/templates/default.json`
- **Purpose**: Defines the authoritative list of supported layouts
- **Format**: JSON mapping from layout names to PowerPoint slide layout indices

### Current Layout Support
The default template currently supports **19 layouts**:

#### Core Layouts
- `Title Slide` - Title and subtitle presentation
- `Title and Content` - Standard content slide
- `Section Header` - Section divider slide
- `Title Only` - Title-only slide
- `Blank` - Empty slide for custom content

#### Multi-Column Layouts
- `Two Content` - Left/right content areas
- `Three Columns` - Triple column layout
- `Three Columns With Titles` - Triple columns with headers
- `Four Columns` - Quadruple column layout  
- `Four Columns With Titles` - Quadruple columns with headers

#### Specialized Layouts
- `Comparison` - Side-by-side comparison
- `SWOT Analysis` - Four-quadrant SWOT matrix
- `Agenda, 6 Textboxes` - Six-item agenda layout
- `Title and 6-item Lists` - Six-section content layout
- `Big Number` - Large metric display

#### Media Layouts
- `Content with Caption` - Content with description
- `Picture with Caption` - Image with caption
- `Title and Vertical Text` - Vertical text orientation
- `Vertical Title and Text` - Alternative vertical layout

### Template Mapping Structure

```json
{
  "template_info": {
    "name": "Default",
    "version": "1.0"
  },
  "layouts": {
    "Title and Content": {
      "index": 1,
      "placeholders": {
        "0": "title_top_1",
        "1": "content_1",
        "10": "date_footer_1",
        "11": "footer_footer_1",
        "12": "slide_number_footer_1"
      }
    }
  },
  "aliases": {
    "content": "Title and Content",
    "bullets": "Title and Content"
  }
}
```

### Layout Discovery Process

1. **Template Manager** loads JSON mappings from configured template folder
2. **Layout Registry** builds internal index of available layouts
3. **Alias Resolution** maps user-friendly names to canonical layout names
4. **Placeholder Mapping** provides semantic field names for content placement

## Layer 2: Layout Intelligence System

### Location and Purpose
- **File**: `/src/deckbuilder/layout_intelligence.json`
- **Purpose**: Content-first semantic layout recommendations
- **Integration**: Used by MCP tools for intelligent layout selection

### Intelligence Categories

#### Intent Recognition Patterns
- **Comparison**: Side-by-side analysis content
- **Features**: Product/service feature lists
- **Process**: Step-by-step workflows
- **Analysis**: Data analysis and insights
- **Timeline**: Chronological content
- **Team**: People and role information

#### Content Type Mapping
```json
{
  "comparison_content": {
    "recommended_layouts": ["Comparison", "Two Content"],
    "confidence_factors": {
      "vs_keywords": 0.8,
      "side_by_side_structure": 0.9
    }
  },
  "column_content": {
    "recommended_layouts": ["Four Columns", "Three Columns"],
    "detection_patterns": ["numbered_lists", "parallel_structure"]
  }
}
```

#### Optimization Hints
- Content restructuring suggestions
- Layout-specific formatting recommendations
- Audience consideration factors
- Presentation flow optimization

## Layer 3: Structured Frontmatter Registry

### Location and Purpose
- **File**: `/src/deckbuilder/structured_frontmatter.py`
- **Purpose**: Clean YAML syntax validation and conversion
- **Coverage**: 12 layouts with structured patterns

### Supported Structured Patterns

#### Multi-Column Layouts
```yaml
# Four Columns
layout: Four Columns
title: "Column Layout Example"
columns:
  - content: "Column 1 content"
  - content: "Column 2 content"
  - content: "Column 3 content" 
  - content: "Column 4 content"
```

#### Comparison Layout
```yaml
# Comparison
layout: Comparison  
title: "Comparison Example"
comparison:
  left:
    title: "Option A"
    content: "Left side details"
  right:
    title: "Option B" 
    content: "Right side details"
```

#### SWOT Analysis
```yaml
# SWOT Analysis
layout: SWOT Analysis
swot:
  strengths: ["Strength 1", "Strength 2"]
  weaknesses: ["Weakness 1", "Weakness 2"]  
  opportunities: ["Opportunity 1", "Opportunity 2"]
  threats: ["Threat 1", "Threat 2"]
```

### Pattern Validation Process

1. **YAML Parsing** - Validates frontmatter syntax
2. **Pattern Matching** - Checks against registered structured patterns
3. **Field Validation** - Ensures required fields are present
4. **Content Conversion** - Transforms YAML to canonical JSON format
5. **Placeholder Mapping** - Maps fields to template placeholders

## Layer 4: Fallback Mechanisms

### Template Manager Fallbacks
When template loading fails:
- Falls back to basic mapping with "Title and Content" and "Title Slide"
- Provides minimal viable layout set
- Logs warnings about missing template files

### Slide Builder Fallbacks  
When layout validation fails:
- Uses semantic detection for title/content/subtitle placeholders
- Attempts content placement using placeholder type inference
- Defaults to "Title and Content" for unknown layouts

### Layout Recommendation Fallbacks
When content analysis fails:
- Defaults to "Title and Content" for text content
- Uses "Picture with Caption" for image-heavy content
- Provides generic layout suggestions

## How Markdown Layout Requests Are Processed

### Process Flow

1. **Frontmatter Parsing**
   ```yaml
   layout: "Four Columns"
   title: "Example Title"
   ```

2. **Structured Pattern Check**
   - Structured Frontmatter Registry validates if layout supports clean YAML syntax
   - If supported, applies pattern-specific validation rules

3. **Template Mapping Lookup**
   - Template Manager loads corresponding layout from `default.json`
   - Resolves layout aliases (e.g., "content" → "Title and Content")

4. **Layout Validation**
   - Slide Builder validates layout exists in PowerPoint template
   - Checks placeholder availability and accessibility

5. **Content Processing**
   - Applies semantic detection for title/content/subtitle placement
   - Uses placeholder mapping for field-to-placeholder assignment
   - Handles content formatting and inline markdown

6. **Fallback Application**
   - If layout not found, uses "Title and Content" with warnings
   - If placeholders missing, attempts semantic detection
   - Logs detailed error information for debugging

### Example Processing

```yaml
# Input markdown frontmatter
layout: Two Content
title: "Side by Side Example"
sections:
  - title: "Left Side"
    content: ["Left content here"]
  - title: "Right Side"  
    content: ["Right content here"]
```

**Processing Steps:**
1. Parse YAML frontmatter ✓
2. Check structured pattern for "Two Content" ✓
3. Validate required fields (title, sections) ✓
4. Load template mapping for "Two Content" ✓
5. Map to placeholders: title→0, left content→1, right content→2 ✓
6. Generate slide with proper content placement ✓

## Validation and Error Handling

### Layout Name Validation
```python
def validate_layout_name(layout_name, template_manager):
    """Validate if layout name is supported"""
    available_layouts = template_manager.get_available_layouts()
    
    if layout_name in available_layouts:
        return True, layout_name
    
    # Check aliases
    canonical_name = template_manager.resolve_alias(layout_name)
    if canonical_name:
        return True, canonical_name
        
    return False, None
```

### Error Types and Messages

#### Unknown Layout
```
Error: Layout "Custom Layout" not found in template.
Available layouts: Title Slide, Title and Content, ...
Did you mean: "Title and Content"?
```

#### Missing Required Fields
```
Error: Structured frontmatter for "Four Columns" missing required field "columns".
Expected structure:
  layout: Four Columns
  title: "Title text"
  columns:
    - content: "Column 1"
    - content: "Column 2"
```

#### Template Loading Failure
```
Warning: Template file not accessible, using fallback layouts.
Available: Title Slide, Title and Content
```

## Current Limitations and Improvement Opportunities

### Missing Features

1. **Layout Discovery MCP Tool**
   - No programmatic way for clients to discover supported layouts
   - Users must rely on documentation or trial-and-error

2. **Dynamic Layout Loading**
   - System only loads from single template file
   - No support for multiple template sources

3. **Layout Capability Reporting**
   - No way to query what features each layout supports
   - Limited validation feedback for complex layouts

4. **Real-time Validation**
   - No pre-submission layout validation
   - Errors only discovered during processing

### Recommended Improvements

#### 1. Add Layout Discovery MCP Tool
```python
@server.tool(name="get_supported_layouts")
async def get_supported_layouts():
    """Return list of all supported layouts with descriptions"""
    layouts = template_manager.get_available_layouts()
    return {
        "layouts": layouts,
        "total_count": len(layouts),
        "template_name": template_manager.template_name
    }
```

#### 2. Layout Validation Tool
```python  
@server.tool(name="validate_layout_request")
async def validate_layout_request(layout_name: str, frontmatter: dict):
    """Validate layout request before processing"""
    # Validate layout exists
    # Check required fields
    # Verify content structure
    # Return validation results
```

#### 3. Layout Capability Tool
```python
@server.tool(name="get_layout_capabilities") 
async def get_layout_capabilities(layout_name: str):
    """Return layout features and requirements"""
    # Field requirements
    # Content type support  
    # Special features
    # Usage examples
```

## Integration with Documentation

### SupportedTemplates.md Relationship
- **Documentation**: Lists 19 implemented + 30+ planned layouts
- **Reality**: Only layouts in `default.json` are actually supported  
- **Status**: Documentation accurately reflects current implementation

### Structured Frontmatter Coverage
- **Template Mappings**: 19 layouts supported
- **Structured Patterns**: 12 layouts with clean YAML syntax
- **Gap**: 7 layouts only support direct placeholder field mapping

### Missing Structured Patterns
Layouts that need structured frontmatter patterns:
- Title Slide, Title and Content, Section Header
- Title Only, Blank, Content with Caption  
- Title and Vertical Text, Vertical Title and Text, Big Number

## Best Practices for Layout Usage

### Content-First Approach
1. **Analyze Content Structure** - What story are you telling?
2. **Consider Audience Needs** - How will they consume information?  
3. **Choose Layout Semantically** - Match layout to content purpose
4. **Use Layout Intelligence** - Leverage MCP recommendation tools

### Fallback-Aware Design
1. **Always Specify Layout** - Don't rely on auto-detection
2. **Validate Layout Names** - Check against supported list
3. **Use Structured Frontmatter** - When available for cleaner syntax
4. **Test Edge Cases** - Verify behavior with minimal content

This comprehensive layout discovery system ensures reliable content processing while providing multiple pathways for layout selection and validation.