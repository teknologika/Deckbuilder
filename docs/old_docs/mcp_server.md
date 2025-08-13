# MCP Server v1.2.0

The MCP Server provides intelligent content analysis and template recommendations for Claude Desktop. Enhanced in v1.2.0 with advanced template recommendation system and smart content optimization.

## What's New in v1.2.0

- **Smart Template Recommendations**: Analyzes your content to suggest the best templates and layouts
- **Content Analysis Engine**: Automatically detects content type, audience, and formality level
- **Intelligent Layout Suggestions**: Recommends optimal layouts within chosen templates
- **Enhanced MCP Tools**: More powerful content-first presentation assistance

## Available MCP Tools

### Template Intelligence
- `list_available_templates()`: Get comprehensive template metadata with usage recommendations
- `get_template_layouts()`: Detailed layout information for specific templates
- `recommend_template_for_content()`: Smart template recommendations based on content analysis
- `validate_presentation_file()`: Pre-generation validation with actionable feedback

### Content Processing
- `create_presentation_from_markdown()`: Generate presentations from Markdown with frontmatter
- `create_presentation_from_file()`: Process JSON or Markdown files directly (token-efficient)

## `main.py`

The `main.py` file is the main entry point for the MCP Server. It starts the server and loads the other modules.

## `content_analysis.py`

The `content_analysis.py` file contains the content analysis functionality. It provides methods for analyzing the content of a presentation and extracting key information.

## `content_optimization.py`

The `content_optimization.py` file contains the content optimization functionality. It provides methods for optimizing the content of a presentation for better readability and visual appeal.

## `layout_recommendations.py`

The `layout_recommendations.py` file contains the layout recommendation functionality. It provides methods for recommending layouts for a presentation based on its content.

## `tools.py`

The `tools.py` file contains various tools for the MCP Server, such as tools for working with images and text.
