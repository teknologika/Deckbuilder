# Convention-Based Naming System Design

## Overview

A standardized placeholder naming convention system that automatically generates consistent, semantic placeholder names across all PowerPoint templates. This system will replace the current mixed naming patterns with a unified approach that improves content intelligence and layout recommendations.

## Current Problem

Template analysis shows inconsistent placeholder naming patterns:
```
Multiple placeholder naming patterns detected:
['Col 1', 'Col 2', 'Col 3', 'Col 4', 'Content Placeholder', 'Date Placeholder',
'Footer Placeholder', 'Picture Placeholder', 'Slide Number', 'Text Placeholder', 'Vertical Text']
```

This inconsistency makes it difficult to:
- Implement reliable content matching algorithms
- Provide accurate layout recommendations
- Maintain semantic consistency across templates

## Proposed Solution: Convention-Based Naming

### Core Naming Convention

**Format**: `{ContentType}_{Position}_{Index}`

Where:
- **ContentType**: Semantic content type (title, content, image, number, etc.)
- **Position**: Spatial or logical position (top, left, center, col1, col2, etc.)
- **Index**: Unique identifier within layout (1, 2, 3, etc.)

### Standard Content Types

1. **title** - Main slide titles
2. **subtitle** - Secondary titles and subtitles
3. **content** - Main content areas (text, bullets, paragraphs)
4. **text** - Additional text areas
5. **image** - Image/picture placeholders
6. **number** - Numeric content (statistics, counts)
7. **date** - Date placeholders
8. **footer** - Footer content
9. **slide_number** - Slide numbering
10. **logo** - Logo/branding areas

### Position Indicators

**Spatial Positions**:
- `top`, `bottom`, `left`, `right`, `center`
- `top_left`, `top_right`, `bottom_left`, `bottom_right`

**Column Layouts**:
- `col1`, `col2`, `col3`, `col4` (for multi-column layouts)

**Comparison Layouts**:
- `left_side`, `right_side`

**List/Agenda Layouts**:
- `item1`, `item2`, `item3`, etc.

## Implementation Examples

### Current vs. Proposed Naming

| Current Name | Proposed Name | Layout Context |
|--------------|---------------|----------------|
| "Title 1" | `title_top_1` | All layouts |
| "Content Placeholder 2" | `content_main_1` | Single content |
| "Col 1 Title Placeholder 2" | `title_col1_1` | Multi-column |
| "Col 1 Text Placeholder 3" | `content_col1_1` | Multi-column |
| "Text Placeholder 2" | `content_left_1` | Comparison |
| "Content Placeholder 3" | `content_right_1` | Comparison |
| "Picture Placeholder 2" | `image_main_1` | Picture layouts |
| "Date Placeholder 3" | `date_footer_1` | All layouts |

### Layout-Specific Patterns

#### Four Columns With Titles
```
title_top_1          # Main slide title
title_col1_1         # Column 1 title
content_col1_1       # Column 1 content
title_col2_1         # Column 2 title
content_col2_1       # Column 2 content
title_col3_1         # Column 3 title
content_col3_1       # Column 3 content
title_col4_1         # Column 4 title
content_col4_1       # Column 4 content
date_footer_1        # Date
footer_bottom_1      # Footer text
slide_number_footer_1 # Slide number
```

#### Comparison Layout
```
title_top_1          # Main title
title_left_1         # Left side title
content_left_1       # Left side content
title_right_1        # Right side title
content_right_1      # Right side content
date_footer_1        # Date
footer_bottom_1      # Footer
slide_number_footer_1 # Slide number
```

#### Picture with Caption
```
title_top_1          # Main title
image_main_1         # Primary image
text_caption_1       # Image caption
date_footer_1        # Date
footer_bottom_1      # Footer
slide_number_footer_1 # Slide number
```

## Implementation Strategy

### Phase 1: Convention Engine
Create `src/deckbuilder/naming_conventions.py`:

```python
class NamingConvention:
    def generate_placeholder_name(self, layout_name: str, placeholder_idx: int,
                                 placeholder_type: str, spatial_context: dict) -> str:
        """Generate standardized placeholder name"""

    def detect_content_type(self, placeholder_type: str, layout_context: str) -> str:
        """Detect semantic content type from PowerPoint type"""

    def determine_position(self, layout_name: str, placeholder_idx: int,
                          total_placeholders: int) -> str:
        """Determine spatial/logical position"""
```

### Phase 2: Template Enhancement Integration
Integrate with existing `enhance` CLI command:

```bash
# Enhance with convention-based naming
python src/deckbuilder/cli_tools.py enhance default --use-conventions

# Preview convention changes without applying
python src/deckbuilder/cli_tools.py enhance default --preview-conventions
```

### Phase 3: Layout Intelligence Integration
Use consistent names for content matching:

```python
# layout_intelligence.json can now use predictable naming
{
  "content_patterns": {
    "title_top_1": ["main heading", "slide title", "primary message"],
    "content_col1_1": ["first point", "left column", "primary feature"],
    "content_col2_1": ["second point", "right column", "secondary feature"]
  }
}
```

## Benefits

1. **Predictable Content Placement**: Consistent naming enables reliable content-to-placeholder matching
2. **Improved Layout Intelligence**: Semantic names support better layout recommendations
3. **Template Interoperability**: Consistent naming across all templates
4. **Maintainable Codebase**: Reduces special cases and layout-specific logic
5. **User-Friendly**: Clear, descriptive names help users understand placeholder purposes

## Success Criteria

1. **Zero Naming Pattern Warnings**: Template analysis shows consistent naming across all layouts
2. **Semantic Clarity**: Placeholder names clearly indicate content type and position
3. **Backward Compatibility**: Existing JSON mappings continue to work
4. **Layout Intelligence Ready**: Names support content matching algorithms
5. **User Validation**: Template enhancement produces intuitive, descriptive placeholder names

## Next Steps

1. Design and implement the `NamingConvention` class
2. Integrate with CLI tools for testing and validation
3. Update existing templates using the new convention
4. Test with content intelligence system
5. Document the naming standard for template creators

---
*Generated as part of Phase 3: Content Intelligence & Layout Expansion*
