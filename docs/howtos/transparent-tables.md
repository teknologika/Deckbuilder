# Transparent Tables with White Borders

Guide for creating transparent tables with white text and horizontal-only borders - perfect for overlay designs and dark backgrounds.

## Current Limitations

⚠️ **Some features are not yet implemented:**
- Horizontal-only borders (only `header_only` available)
- Data row text color control (only header text customizable)
- Full RGBA transparency support

## What You Can Achieve Now

### Option 1: Transparent Background + Custom Colors
```yaml
---
layout: Table Only
title: "Transparent Table Design"
style: white_dark_text
row_style: no_fill              # Transparent backgrounds
border_style: no_borders        # Remove all borders for custom styling
header_font_size: 14
data_font_size: 12
custom_colors:
  header_bg: "#00000000"        # Try transparent (may not work)
  header_text: "#FFFFFF"        # White header text
  # Note: Data row text color not customizable yet
table_data: |
  | Metric | Q1 | Q2 | Q3 |
  | Revenue | $125K | $132K | $145K |
  | Growth | +12% | +15% | +18% |
---
```

### Option 2: Minimal White Design
```yaml
---
layout: Table Only
title: "Clean White Table"
style: white_dark_text
row_style: solid_white
border_style: header_only       # Only header borders
header_font_size: 14
data_font_size: 12
custom_colors:
  header_bg: "#FFFFFF"
  header_text: "#000000"        # Black text on white
  border_color: "#FFFFFF"       # White borders
table_data: |
  | Metric | Value | Status |
  | Revenue | $250K | ✓ Target Met |
  | Customers | 1,245 | ↗ Growing |
---
```

### Option 3: Dark Background Optimized
```yaml
---
layout: Table Only
title: "Dark Background Table"
style: dark_gray_white_text      # Dark header, white text
row_style: no_fill               # Transparent data rows
border_style: thin_gray          # Minimal borders
header_font_size: 14
data_font_size: 12
custom_colors:
  header_bg: "#333333"           # Dark gray header
  header_text: "#FFFFFF"         # White header text
  border_color: "#666666"        # Gray borders (visible on dark)
table_data: |
  | Team | Status | Progress |
  | Frontend | Active | 85% |
  | Backend | Testing | 92% |
  | Design | Complete | 100% |
---
```

## Workarounds for Missing Features

### Horizontal-Only Borders
**Current limitation**: No horizontal-only border option
**Workaround**: Use `header_only` for minimal borders
```yaml
border_style: header_only  # Closest to horizontal-only
custom_colors:
  border_color: "#FFFFFF"  # White borders
```

### White Data Row Text
**Current limitation**: Data row text color not customizable
**Workaround**: Use CSS post-processing or image overlays
```yaml
# This will need to be added to the system:
# custom_colors:
#   data_text: "#FFFFFF"  # Not yet supported
```

### Full Transparency
**Current limitation**: RGBA colors not fully supported
**Workaround**: Use `no_fill` row style
```yaml
row_style: no_fill  # Makes backgrounds transparent
```

## Recommended Combinations

### For Dark Presentations
```yaml
style: dark_gray_white_text
row_style: no_fill
border_style: header_only
custom_colors:
  header_bg: "#404040"
  header_text: "#FFFFFF"
  border_color: "#808080"
```

### For Light Overlays
```yaml
style: white_dark_text
row_style: solid_white
border_style: outer_only
custom_colors:
  header_bg: "#F8F8F8"
  border_color: "#E0E0E0"
```

### For Minimal Design
```yaml
style: light_gray_dark_text
row_style: no_fill
border_style: no_borders
header_font_size: 12
data_font_size: 11
```

## Future Enhancements Needed

To fully support your transparent table requirements, these features should be added:

### 1. Enhanced Border Control
```yaml
# Proposed syntax:
borders:
  top: { width: 0.5, color: "#FFFFFF" }
  bottom: { width: 0.5, color: "#FFFFFF" }
  left: { width: 0 }
  right: { width: 0 }
  
# Or simpler:
border_style: horizontal_white
```

### 2. Data Row Text Color
```yaml
# Proposed syntax:
custom_colors:
  data_text: "#FFFFFF"        # White text for data rows
  data_text_alt: "#F0F0F0"    # Slightly different for alt rows
```

### 3. Full RGBA Support
```yaml
# Proposed syntax:
custom_colors:
  header_bg: "rgba(0,0,0,0.8)"    # Semi-transparent black
  primary_row: "rgba(255,255,255,0.1)"  # Barely visible white
```

### 4. Border Side Control
```yaml
# Proposed syntax:
border_sides: ["top", "bottom"]  # Only horizontal borders
border_color: "#FFFFFF"
border_width: 1.0
```

## CSS Post-Processing Alternative

If you need immediate transparent tables with white text, consider post-processing:

```python
# Pseudo-code for post-processing approach:
def apply_white_text_overlay(pptx_file):
    # 1. Extract table XML
    # 2. Find all data row text runs
    # 3. Set color to white (#FFFFFF)
    # 4. Remove backgrounds
    # 5. Set horizontal borders only
    pass
```

## Request These Features

To get these transparency features implemented:

1. **Create feature request** with specific requirements
2. **Provide use cases** for transparent tables
3. **Share design mockups** showing desired appearance
4. **Contribute to implementation** if possible

Example feature request:
```markdown
## Feature Request: Enhanced Table Transparency

### Requirements:
- Horizontal-only borders with custom colors
- Data row text color control
- Full RGBA transparency support
- Border side control (top/bottom/left/right)

### Use Cases:
- Tables over background images
- Dark presentation themes
- Minimal design aesthetics
- Brand-specific styling

### Priority: High
Tables are core presentation elements that need full styling control.
```

## Best Practices with Current System

1. **Test thoroughly** - Transparency behavior may vary
2. **Use contrasting colors** - Ensure readability
3. **Keep it simple** - Complex transparency can reduce readability
4. **Consider alternatives** - Images or shapes for complex designs
5. **Validate accessibility** - Check color contrast ratios

## Related Documentation

- [Table Styling Guide](./table-styling.md) - Complete styling options
- [Table Styles Reference](../reference/table-styles.md) - All available styles
- [Custom Colors Guide](./custom-colors.md) - Color specification formats