# Table Styles Reference

Complete reference for all table styling options, colors, and configurations in Deckbuilder.

## Style Definitions

### Header Styles

Complete list of predefined header styles with exact color values:

| Style Name | Background Color | RGB | Text Color | RGB | Preview |
|------------|------------------|-----|------------|-----|---------|
| `dark_blue_white_text` | #4472C4 | 68, 114, 196 | #FFFFFF | 255, 255, 255 | ![Dark Blue](https://via.placeholder.com/100x30/4472C4/FFFFFF?text=Sample) |
| `light_blue_dark_text` | #D9EDFF | 217, 237, 255 | #333333 | 51, 51, 51 | ![Light Blue](https://via.placeholder.com/100x30/D9EDFF/333333?text=Sample) |
| `dark_gray_white_text` | #666666 | 102, 102, 102 | #FFFFFF | 255, 255, 255 | ![Dark Gray](https://via.placeholder.com/100x30/666666/FFFFFF?text=Sample) |
| `light_gray_dark_text` | #F2F2F2 | 242, 242, 242 | #333333 | 51, 51, 51 | ![Light Gray](https://via.placeholder.com/100x30/F2F2F2/333333?text=Sample) |
| `white_dark_text` | #FFFFFF | 255, 255, 255 | #333333 | 51, 51, 51 | ![White](https://via.placeholder.com/100x30/FFFFFF/333333?text=Sample) |
| `accent_color_white_text` | #4472C4 | 68, 114, 196 | #FFFFFF | 255, 255, 255 | ![Accent](https://via.placeholder.com/100x30/4472C4/FFFFFF?text=Sample) |

### Row Styles

Alternating row color patterns for data rows:

| Style Name | Primary Row | RGB | Alternate Row | RGB |
|------------|-------------|-----|---------------|-----|
| `alternating_light_gray` | #FFFFFF | 255, 255, 255 | #F8F8F8 | 248, 248, 248 |
| `alternating_light_blue` | #FFFFFF | 255, 255, 255 | #F0F8FF | 240, 248, 255 |
| `solid_white` | #FFFFFF | 255, 255, 255 | #FFFFFF | 255, 255, 255 |
| `solid_light_gray` | #F8F8F8 | 248, 248, 248 | #F8F8F8 | 248, 248, 248 |
| `no_fill` | Transparent | - | Transparent | - |

### Border Styles

Border configuration options:

| Style Name | Width (cm) | Color | RGB | Application |
|------------|------------|-------|-----|-------------|
| `thin_gray` | 0.025 | #A6A6A6 | 166, 166, 166 | All borders |
| `thick_gray` | 0.05 | #A6A6A6 | 166, 166, 166 | All borders |
| `header_only` | 0.025 | #A6A6A6 | 166, 166, 166 | Header row only |
| `outer_only` | 0.025 | #A6A6A6 | 166, 166, 166 | Perimeter only |
| `no_borders` | 0 | None | - | No borders |

## Configuration Options

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `table_data` | String | Markdown table content | `"| Header | Data |\n| Value | 123 |"` |

### Styling Parameters

| Parameter | Type | Default | Options | Description |
|-----------|------|---------|---------|-------------|
| `style` | String | `dark_blue_white_text` | See Header Styles | Header row appearance |
| `row_style` | String | `alternating_light_gray` | See Row Styles | Data row appearance |
| `border_style` | String | `thin_gray` | See Border Styles | Border appearance |

### Font Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `header_font_size` | Integer | 12 | 6-72 | Header font size (points) |
| `data_font_size` | Integer | 10 | 6-72 | Data font size (points) |

### Dimension Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `table_width` | Float | Auto | 5.0-25.0 | Total table width (cm) |
| `table_height` | Float | Auto | 3.0-20.0 | Total table height (cm) |
| `row_height` | Float | 0.6 | 0.3-5.0 | Uniform row height (cm) |
| `column_widths` | Array | Auto | [1.0-15.0] | Individual column widths (cm) |

### Custom Color Parameters

| Parameter | Type | Format | Description |
|-----------|------|--------|-------------|
| `custom_colors.header_bg` | String | `#RRGGBB` | Header background color |
| `custom_colors.header_text` | String | `#RRGGBB` | Header text color |
| `custom_colors.primary_row` | String | `#RRGGBB` | Primary row background |
| `custom_colors.alt_row` | String | `#RRGGBB` | Alternate row background |
| `custom_colors.border_color` | String | `#RRGGBB` | Border color |

## Usage Patterns

### Basic Configuration
```yaml
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
```

### Custom Styling
```yaml
style: white_dark_text
custom_colors:
  header_bg: "#2E5984"
  header_text: "#FFFFFF"
  primary_row: "#F8F8F8"
  alt_row: "#E8E8E8"
  border_color: "#CCCCCC"
```

### Dimension Control
```yaml
table_width: 18.0
column_widths: [5.0, 4.0, 4.0, 5.0]
row_height: 0.8
header_font_size: 14
data_font_size: 11
```

## Color Format Specifications

### Hex Color Format
- **Required format**: `#RRGGBB` (6 characters)
- **Valid examples**: `#FF0000`, `#00FF00`, `#0000FF`
- **Invalid examples**: `FF0000`, `#F00`, `red`, `rgb(255,0,0)`

### Transparency Support
- **Current limitation**: RGBA colors not fully supported
- **Workaround**: Use `no_fill` row style for transparency
- **Future enhancement**: Full RGBA support planned

### Popular Color Combinations

**Corporate Professional:**
```yaml
custom_colors:
  header_bg: "#1F4E79"      # Corporate blue
  header_text: "#FFFFFF"    # White text
  primary_row: "#F8F8F8"    # Light gray
  border_color: "#D0D0D0"   # Light gray border
```

**Minimal Grayscale:**
```yaml
custom_colors:
  header_bg: "#E5E5E5"      # Very light gray
  header_text: "#333333"    # Dark gray text
  primary_row: "#FFFFFF"    # Pure white
  alt_row: "#FAFAFA"        # Almost white
  border_color: "#CCCCCC"   # Medium gray border
```

**High Contrast:**
```yaml
custom_colors:
  header_bg: "#000000"      # Pure black
  header_text: "#FFFFFF"    # Pure white
  primary_row: "#FFFFFF"    # White rows
  border_color: "#333333"   # Dark gray border
```

**Brand Colors Example:**
```yaml
custom_colors:
  header_bg: "#8B0000"      # Dark red brand
  header_text: "#FFFFFF"    # White text
  primary_row: "#FFF5F5"    # Very light red tint
  alt_row: "#FFE8E8"        # Light red tint
  border_color: "#8B0000"   # Match header
```

### Color Limitations

**❌ Not Currently Supported:**
- Data row text color (only header text customizable)
- RGBA transparency (`rgba(255,255,255,0.5)`)
- Named colors (`red`, `blue`, `white`)
- HSL colors (`hsl(120, 100%, 50%)`)
- Gradient colors

**✅ Workarounds Available:**
- Use `row_style: no_fill` for transparent backgrounds
- Use appropriate header styles for white/dark text
- Use `border_style: no_borders` for custom overlay designs

### Color Accessibility

**Recommended Contrast Ratios:**
- Header text: Minimum 4.5:1 contrast with background
- Data text: Currently limited to preset combinations
- Border visibility: Ensure borders contrast with row backgrounds

**Safe High-Contrast Combinations:**
- `#000000` background + `#FFFFFF` text (21:1 ratio)
- `#4472C4` background + `#FFFFFF` text (5.74:1 ratio)
- `#666666` background + `#FFFFFF` text (6.26:1 ratio)

**Avoid Low-Contrast Combinations:**
- `#F0F0F0` background + `#CCCCCC` text (1.61:1 ratio) ❌

## Layout Integration

### Compatible Layouts

Tables work with these slide layouts:

| Layout | Table Placement | Content Integration |
|--------|-----------------|-------------------|
| `Table Only` | Full slide | Table only |
| `Table with Content Above` | Below content | Text above table |
| `Table with Content Above and Below` | Middle | Text above and below |
| `Table with Content Left` | Right side | Text on left |
| `Content Table Content Table Content` | Multiple tables | Mixed content |

### Content Positioning

Smart positioning based on existing slide content:

```yaml
# Table positioning is automatic based on:
# 1. Existing content placeholder text
# 2. Content length and line count
# 3. Bullet points and formatting
# 4. Available slide space
```

## Performance Considerations

### Optimal Configurations

| Table Size | Recommended Settings | Performance Impact |
|------------|---------------------|-------------------|
| Small (≤3x3) | Any styling | Minimal |
| Medium (≤6x6) | Standard borders, moderate fonts | Low |
| Large (≤10x10) | Thin borders, smaller fonts | Medium |
| Very Large (>10x10) | No borders, minimal styling | High |

### Memory Usage

| Feature | Memory Impact | Recommendation |
|---------|---------------|----------------|
| Custom colors | Low | Use freely |
| Complex borders | Medium | Consider `no_borders` for large tables |
| Large dimensions | High | Use reasonable table sizes |
| Multiple tables per slide | High | Limit to 2-3 tables per slide |

## Migration Guide

### From Basic to Advanced Styling

**Step 1**: Start with presets
```yaml
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
```

**Step 2**: Add custom colors
```yaml
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
custom_colors:
  header_bg: "#1F4E79"
```

**Step 3**: Fine-tune dimensions
```yaml
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
custom_colors:
  header_bg: "#1F4E79"
table_width: 20.0
column_widths: [6.0, 4.0, 5.0, 5.0]
header_font_size: 13
```

### Legacy Compatibility

| Old Parameter | New Parameter | Migration |
|---------------|---------------|-----------|
| `header_style` | `style` | Direct replacement |
| `data` | `table_data` | Convert to markdown format |
| `rows` | `table_data` | Convert to markdown format |

## API Reference

### JSON Configuration Format

```json
{
  "placeholders": {
    "table_data": "| Header | Data |\n| Value | 123 |",
    "style": "dark_blue_white_text",
    "row_style": "alternating_light_gray",
    "border_style": "thin_gray",
    "header_font_size": 12,
    "data_font_size": 10,
    "table_width": 18.0,
    "column_widths": [4.5, 4.5, 4.5, 4.5],
    "row_height": 0.7,
    "custom_colors": {
      "header_bg": "#4472C4",
      "header_text": "#FFFFFF",
      "primary_row": "#FFFFFF",
      "alt_row": "#F8F8F8",
      "border_color": "#A6A6A6"
    }
  }
}
```

### Python Library Usage

```python
from deckbuilder import Deckbuilder

table_config = {
    "style": "dark_blue_white_text",
    "row_style": "alternating_light_gray",
    "border_style": "thin_gray",
    "header_font_size": 14,
    "data_font_size": 11,
    "custom_colors": {
        "header_bg": "#2E5984"
    }
}

# Apply to slide data
slide_data = {
    "layout": "Table Only",
    "placeholders": {
        "table_data": "| Product | Sales |\n| Widget | $1000 |",
        **table_config
    }
}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Colors not applying | Invalid hex format | Use `#RRGGBB` format |
| Table too wide | Default auto-sizing | Set `table_width` explicitly |
| Text unreadable | Font too small | Increase `header_font_size` and `data_font_size` |
| Borders missing | Invalid border style | Use valid `border_style` name |
| Poor contrast | Color combination | Check accessibility guidelines |

### Validation Rules

- Hex colors must start with `#` and be 6 characters
- Font sizes must be between 6-72 points
- Dimensions must be positive numbers
- Column count must match table data columns
- Style names must match predefined options exactly

### Debug Tips

1. **Test with minimal config** first
2. **Add one styling option** at a time
3. **Validate hex colors** with online tools
4. **Check table markdown** syntax
5. **Use browser developer tools** to inspect generated content

## Related Documentation

- [Table Styling Guide](../howtos/table-styling.md) - How-to guide with examples
- [Structured Frontmatter Patterns](./frontmatter-patterns.md) - Layout options
- [Color Accessibility Guide](../howtos/accessibility.md) - Color contrast guidelines
- [Brand Customization](../howtos/brand-customization.md) - Corporate styling