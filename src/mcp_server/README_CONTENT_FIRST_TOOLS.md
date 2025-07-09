# Content-First Tools

This directory contains the content-first analysis tools that were moved from the main MCP server to keep the core server focused on presentation generation.

## Files

### `content_first_tools.py`
Contains the content-first analysis tools that implement the intelligent presentation consultation workflow:

1. **`analyze_presentation_needs_tool()`** - Analyzes user's presentation needs and recommends structure
2. **`recommend_slide_approach_tool()`** - Recommends optimal slide layouts based on content and intent
3. **`optimize_content_for_layout_tool()`** - Optimizes content structure and generates ready-to-use YAML

### `main.py`
The streamlined MCP server containing only the core presentation generation tools:

1. **`create_presentation()`** - Create presentation from JSON data
2. **`create_presentation_from_file()`** - Create presentation from JSON or markdown files
3. **`create_presentation_from_markdown()`** - Create presentation from markdown content

## Why Were They Moved?

The content-first tools were moved to separate the core presentation generation functionality from the intelligent content analysis features. This provides:

- **Cleaner MCP server**: Focus on essential presentation generation
- **Preserved functionality**: Content-first tools available for future integration
- **Better maintainability**: Clear separation of concerns
- **Reduced complexity**: Simpler MCP server interface

## Future Integration

The content-first tools can be easily re-integrated into the MCP server by:

1. Adding the `@mcp.tool()` decorator back to each function
2. Adding the `ctx: Context` parameter back to each function signature
3. Importing the functions in `main.py`

## Content-First Workflow

The preserved workflow implements a content-first design philosophy:

```
1. analyze_presentation_needs_tool()
   ↓ (analyzes user intent and audience)
2. recommend_slide_approach_tool()
   ↓ (suggests optimal layouts with confidence scores)
3. optimize_content_for_layout_tool()
   ↓ (generates production-ready structured frontmatter)
4. create_presentation_from_markdown()
   ↓ (creates final PowerPoint presentation)
```

This approach transforms LLMs from layout pickers into intelligent presentation consultants.