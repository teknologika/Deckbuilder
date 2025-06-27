# List Content Specification

## Overview
This specification defines how to add bulleted and numbered list support to the deck builder MCP, with nested objects support and presentation-wide color theming.

## JSON Structure for Content Lists

### Simple Backwards Compatible Approach

```json
{
  "type": "content",
  "title": "Slide Title",
  "content": [
    "Intro text",
    {
      "type": "list",
      "bullet_style": "circle",
      "items": [
        "Item 1",
        {
          "text": "Item 2 with subs",
          "sub_items": ["Sub 1", "Sub 2"]
        }
      ]
    },
    "Closing text"
  ]
}
```

### Presentation Creation with Colors

```json
{
  "create_presentation": {
    "templateName": "default",
    "title": "My Presentation",
    "author": "User",
    "presentation_colors": {
      "bullet_color": "#4472C4",
      "text_color": "#333333"
    }
  }
}
```

## Key Features

1. **Nested Objects**: Support for text mixed with lists within paragraphs
2. **Circle Bullets**: Default/prioritized bullet style
3. **Presentation-wide Colors**: Set once at presentation creation, applied to all lists
4. **Backwards Compatibility**: Still handle simple string arrays
5. **Mixed Content**: Text and lists can be interspersed

## Bullet Styles

- `circle` - Prioritized style (○)
- `round` - Standard bullet (•)
- `square` - Square bullet (▪)
- `arrow` - Arrow bullet (➤)
- `diamond` - Diamond bullet (♦)

## Implementation Notes

- Default bullet style: `circle` if none specified
- Support 2 levels of nesting (main items + sub_items)
- Presentation colors set at presentation creation level, applied to all lists throughout the presentation
- Mixed content array allows text and lists to be interspersed
- Backwards compatible with existing simple string array format

## Example Usage

```json
{
  "type": "content",
  "title": "Project Benefits",
  "content": [
    "Our new system provides several key advantages:",
    {
      "type": "list",
      "bullet_style": "circle",
      "items": [
        "Improved efficiency and automation",
        {
          "text": "Enhanced user experience with",
          "sub_items": [
            "Intuitive interface design",
            "Faster response times"
          ]
        },
        "Reduced operational costs"
      ]
    },
    "These improvements will deliver immediate value to our organization."
  ]
}
```

*Note: Bullet colors would be set during presentation creation and applied automatically to all lists.*
