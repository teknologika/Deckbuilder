import asyncio
import json
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from deckbuilder.engine import get_deckbuilder_client  # noqa: E402
from deckbuilder.template_metadata import TemplateMetadataLoader  # noqa: E402

# Content-first tools moved to content_first_tools.py to keep core server focused


deck = get_deckbuilder_client()


load_dotenv()


# Create a dataclass for our application context
@dataclass
class DeckbuilderContext:
    """Context for the Deckbuilder MCP server."""

    deckbuilder_client: str


@asynccontextmanager
async def deckbuilder_lifespan(server: FastMCP) -> AsyncIterator[DeckbuilderContext]:
    """
    Manages the Deckbuilder client lifecycle.

    Args:
        server: The Deckbuilder server instance

    Yields:
        PresentationContext: The context containing the Deckbuilder client
    """

    # Create and return the Deckbuilder Client with the helper function in deckbuilder.py
    deckbuilder_client = get_deckbuilder_client()

    try:
        yield DeckbuilderContext(deckbuilder_client=deckbuilder_client)
    finally:
        # Explicit cleanup goes here if any is required
        pass


# Initialize FastMCP server with the Deckbuilder client as context
mcp = FastMCP(
    "deckbuilder",
    description="Token-efficient MCP server for PowerPoint presentation generation from files and markdown",
    lifespan=deckbuilder_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),  # nosec B104
    port=os.getenv("PORT", "8050"),
)


# Note: create_presentation() JSON tool removed - forces efficient file-based workflows
# The core Deckbuilder.create_presentation() engine method remains intact
# Use create_presentation_from_file() for token-efficient LLM workflows (15 tokens vs 2000+)


@mcp.tool()
async def create_presentation_from_file(
    ctx: Context,
    file_path: str,
    fileName: str = "Sample_Presentation",
    templateName: str = "default",
) -> str:
    """Create a complete PowerPoint presentation from JSON or markdown file

    This tool reads presentation data directly from a local file without passing
    content through the context window.
    Supports both JSON files (.json) and markdown files (.md) with frontmatter.
    Automatically detects file type and processes accordingly.

    IMPORTANT: Process the file content exactly as provided. Do not modify the JSON
    structure or markdown formatting unless the tool fails with specific errors
    that require fixes.

    Args:
        ctx: MCP context
        file_path: Absolute path to JSON or markdown file (process content as-is)
        fileName: Output filename (default: Sample_Presentation)
        templateName: Template to use (default: default)

    Supported file types:
        - .json files: JSON format with presentation data
        - .md files: Markdown with frontmatter slide definitions

    Example usage:
        file_path: "/path/to/test_comprehensive_layouts.json"
        file_path: "/path/to/presentation.md"

    Benefits:
        - No token usage for large presentation files
        - Direct file system access
        - Supports both JSON and markdown formats
        - Automatic file type detection
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"

        # Determine file type and process accordingly
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == ".json":
            # Read JSON file
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            # Convert JSON data to canonical format if needed
            if "slides" not in json_data:
                canonical_data = {"slides": [json_data] if isinstance(json_data, dict) else json_data}
            else:
                canonical_data = json_data

            # Create presentation using the new API
            result = deck.create_presentation(canonical_data, fileName, templateName)

            return f"Successfully created presentation from JSON file: {file_path}. {result}"

        elif file_extension == ".md":
            # Read markdown file
            with open(file_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()

            # Convert markdown to canonical JSON format
            from deckbuilder.converter import markdown_to_canonical_json

            canonical_data = markdown_to_canonical_json(markdown_content)

            # Create presentation using the new API
            result = deck.create_presentation(canonical_data, fileName, templateName)

            return f"Successfully created presentation from markdown file: " f"{file_path} with {len(canonical_data['slides'])} slides. {result}"

        else:
            return f"Error: Unsupported file type '{file_extension}'. Supported types: .json, .md"

    except json.JSONDecodeError as e:
        return f"Error parsing JSON file: {str(e)}"
    except Exception as e:
        return f"Error creating presentation from file: {str(e)}"


@mcp.tool()
async def create_presentation_from_markdown(
    ctx: Context,
    markdown_content: str,
    fileName: str = "Sample_Presentation",
    templateName: str = "default",
) -> str:
    """Create presentation from formatted markdown with frontmatter

    This tool accepts markdown content with frontmatter slide definitions and
    creates a complete presentation.
    Each slide is defined using YAML frontmatter followed by markdown content.
    This tool automatically saves the presentation to disk after creation.

    IMPORTANT: Use the provided markdown content exactly as given by the user. Do not
    modify the frontmatter structure, markdown formatting, or content unless the tool
    fails with specific errors that require fixes.

    Args:
        ctx: MCP context
        markdown_content: Markdown string with frontmatter (use as-is)
        fileName: Output filename (default: Sample_Presentation)
        templateName: Template/theme to use (default: default)

    Example markdown format:
        ---
        layout: title
        ---
        # Main Title
        ## Subtitle

        ---
        layout: content
        ---
        # Key Points

        ## Overview
        This section covers the main features of our product.

        - Advanced analytics dashboard
        - Real-time data processing
        - Seamless API integration

        The system scales automatically based on demand.

        ---
        layout: table
        style: dark_blue_white_text
        ---
        # Sales Report
        | Name | Sales | Region |
        | John Smith | $125,000 | North |
        | Sarah Johnson | $98,500 | South |

        ---
        layout: Picture with Caption
        title: System **Architecture** Overview
        media:
          image_path: "diagrams/system_architecture.png"
          alt_text: "System architecture diagram showing microservices"
          caption: "***Scalable*** microservices with *intelligent* load balancing"
        ---

    Supported layouts:
        - title: Title slide with title and subtitle
        - content: Content slide with rich text support (headings, paragraphs, bullets)
        - table: Table slide with styling options
        - Picture with Caption: Image slides with PlaceKitten fallback support

    Image features:
        - Smart fallback: Missing images automatically use PlaceKitten placeholders
        - Professional styling: Grayscale filter + intelligent cropping
        - Face detection: Optimized cropping for portrait images
        - Performance: Intelligent caching system for repeated use
        - Accessibility: Alt text support for screen readers

    Table styling options:
        - style: Header style (dark_blue_white_text, light_blue_dark_text, etc.)
        - row_style: Row style (alternating_light_gray, solid_white, etc.)
        - border_style: Border style (thin_gray, thick_gray, no_borders, etc.)
        - custom_colors: Custom color overrides (header_bg, header_text, alt_row, border_color)
    """
    try:
        # Convert markdown to canonical JSON format
        from deckbuilder.converter import markdown_to_canonical_json

        canonical_data = markdown_to_canonical_json(markdown_content)

        # Create presentation using the new API
        result = deck.create_presentation(canonical_data, fileName, templateName)

        return f"Successfully created presentation with {len(canonical_data['slides'])} slides " f"from markdown. {result}"
    except Exception as e:
        return f"Error creating presentation from markdown: {str(e)}"


@mcp.tool()
async def list_available_templates(ctx: Context) -> str:
    """List all available presentation templates with metadata for intelligent selection
    
    This tool provides comprehensive template discovery for content-first workflows.
    Returns template metadata including descriptions, use cases, and layout capabilities
    to enable smart template selection without expensive trial-and-error.
    
    Token efficiency: ~50 tokens input → comprehensive template metadata output
    
    Returns:
        JSON string with template metadata in the format:
        {
            "available_templates": {
                "template_name": {
                    "description": "Template description",
                    "use_cases": ["use case 1", "use case 2"],
                    "total_layouts": number,
                    "key_layouts": ["layout 1", "layout 2"]
                }
            },
            "recommendation": "Usage guidance for template selection"
        }
    
    Use cases:
        - Template discovery for new presentations
        - Content-template matching for optimal results
        - Understanding layout capabilities before generation
        - Avoiding expensive template trial-and-error cycles
    """
    try:
        # Initialize template metadata loader
        loader = TemplateMetadataLoader()
        
        # Get template names first
        template_names = loader.get_template_names()
        
        if not template_names:
            return json.dumps({
                "available_templates": {},
                "recommendation": "No templates found. Check template folder configuration."
            })
        
        # Transform to expected format defined by TDD test
        available_templates = {}
        
        for template_name in template_names:
            try:
                # Load full metadata for each template
                metadata = loader.load_template_metadata(template_name)
                
                # Extract key layouts (first few layout names)
                key_layouts = list(metadata.layouts.keys())[:3]
                
                available_templates[template_name] = {
                    "description": metadata.description,
                    "use_cases": metadata.use_cases[:3],  # First 3 use cases
                    "total_layouts": metadata.total_layouts,
                    "key_layouts": key_layouts
                }
            except Exception as e:
                # If we can't load metadata for a template, include it with basic info
                available_templates[template_name] = {
                    "description": f"Template: {template_name}",
                    "use_cases": ["General presentations"],
                    "total_layouts": 0,
                    "key_layouts": []
                }
        
        # Generate recommendation based on available templates
        if "default" in available_templates and "business_pro" in available_templates:
            recommendation = "Use 'default' for general presentations, 'business_pro' for executive content"
        elif "default" in available_templates:
            recommendation = "Use 'default' template for most presentation needs"
        else:
            template_names = list(available_templates.keys())
            recommendation = f"Available templates: {', '.join(template_names)}"
        
        result = {
            "available_templates": available_templates,
            "recommendation": recommendation
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        error_result = {
            "error": f"Failed to load template metadata: {str(e)}",
            "available_templates": {},
            "recommendation": "Check template folder configuration and try again"
        }
        return json.dumps(error_result, indent=2)


@mcp.tool()
async def get_template_layouts(ctx: Context, template_name: str) -> str:
    """Get detailed layout information for a specific template
    
    This tool provides comprehensive layout details for a template including
    placeholder requirements, usage examples, and best practices for markdown authoring.
    
    Token efficiency: ~20 tokens input → detailed layout specifications
    
    Args:
        ctx: MCP context
        template_name: Name of template to analyze (e.g., 'default', 'business_pro')
    
    Returns:
        JSON string with detailed layout information in the format:
        {
            "template_name": "template_name",
            "layouts": {
                "Layout Name": {
                    "description": "Layout description",
                    "required_placeholders": ["field1", "field2"],
                    "optional_placeholders": ["field3"],
                    "best_for": "Usage recommendations",
                    "example": {
                        "field1": "Example content 1",
                        "field2": "Example content 2"
                    }
                }
            },
            "usage_tips": "General usage guidance"
        }
    
    Use cases:
        - Understanding placeholder requirements for markdown authoring
        - Getting realistic examples for specific layouts
        - Learning best practices for template usage
        - Troubleshooting placeholder naming issues
    """
    try:
        # Initialize template metadata loader
        loader = TemplateMetadataLoader()
        
        # Check if template exists
        if not loader.validate_template_exists(template_name):
            # Get available templates for helpful error message
            available_templates = loader.get_template_names()
            
            error_result = {
                "error": f"Template '{template_name}' not found",
                "available_templates": available_templates,
                "suggestion": "Use list_available_templates() to see all available options"
            }
            return json.dumps(error_result, indent=2)
        
        # Load template metadata
        metadata = loader.load_template_metadata(template_name)
        
        # Transform to expected format with examples
        layouts_info = {}
        
        for layout_name, layout_meta in metadata.layouts.items():
            # Generate realistic examples for this layout
            example = _generate_layout_example(layout_name, layout_meta.placeholders)
            
            layouts_info[layout_name] = {
                "description": layout_meta.description,
                "required_placeholders": layout_meta.required_placeholders,
                "optional_placeholders": layout_meta.optional_placeholders,
                "best_for": layout_meta.best_for,
                "example": example
            }
        
        result = {
            "template_name": template_name,
            "layouts": layouts_info,
            "usage_tips": "Use placeholders exactly as specified. Title is required for all layouts."
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        error_result = {
            "error": f"Failed to load template layouts: {str(e)}",
            "template_name": template_name,
            "suggestion": "Check template name and try again"
        }
        return json.dumps(error_result, indent=2)


def _generate_layout_example(layout_name: str, placeholders: list) -> dict:
    """Generate realistic examples for layout placeholders dynamically."""
    
    examples = {}
    
    # Generate examples based on semantic placeholder names
    for placeholder in placeholders:
        placeholder_lower = placeholder.lower()
        
        # Dynamic title examples
        if placeholder_lower == "title":
            examples[placeholder] = _get_title_example_for_layout(layout_name)
        elif placeholder_lower == "subtitle":
            examples[placeholder] = "Subtitle with key message"
        elif placeholder_lower.startswith("title_col"):
            col_num = placeholder_lower.split("_col")[-1] if "_col" in placeholder_lower else "1"
            examples[placeholder] = f"Column {col_num} Title"
        
        # Dynamic content examples
        elif placeholder_lower == "content":
            examples[placeholder] = _get_content_example_for_layout(layout_name)
        elif placeholder_lower.startswith("content_col"):
            col_num = placeholder_lower.split("_col")[-1] if "_col" in placeholder_lower else "1"
            examples[placeholder] = f"Feature {col_num} details"
        elif placeholder_lower == "content_left":
            examples[placeholder] = "Left side content details"
        elif placeholder_lower == "content_right":
            examples[placeholder] = "Right side content details"
        elif "top_left" in placeholder_lower:
            examples[placeholder] = "Strengths content"
        elif "top_right" in placeholder_lower:
            examples[placeholder] = "Weaknesses content"
        elif "bottom_left" in placeholder_lower:
            examples[placeholder] = "Opportunities content"
        elif "bottom_right" in placeholder_lower:
            examples[placeholder] = "Threats content"
        
        # Image and media examples
        elif "image" in placeholder_lower or "picture" in placeholder_lower:
            examples[placeholder] = "path/to/image.png"
        elif "caption" in placeholder_lower:
            examples[placeholder] = "Image caption or description"
        
        # Other semantic types
        elif "summary" in placeholder_lower:
            examples[placeholder] = "Executive summary content"
        elif "bullet" in placeholder_lower:
            examples[placeholder] = "• Bullet point 1\n• Bullet point 2"
        
        # Fallback for unrecognized patterns
        else:
            examples[placeholder] = f"Content for {placeholder}"
    
    return examples


def _get_title_example_for_layout(layout_name: str) -> str:
    """Generate appropriate title examples based on layout context."""
    layout_lower = layout_name.lower()
    
    if "comparison" in layout_lower:
        return "Feature Comparison"
    elif "four" in layout_lower and "column" in layout_lower:
        return "Four Key Areas"
    elif "three" in layout_lower and "column" in layout_lower:
        return "Three Main Points"
    elif "swot" in layout_lower:
        return "SWOT Analysis"
    elif "agenda" in layout_lower:
        return "Meeting Agenda"
    elif "picture" in layout_lower:
        return "Visual Overview"
    elif "title" in layout_lower and "slide" in layout_lower:
        return "My Presentation Title"
    else:
        return "Slide Title"


def _get_content_example_for_layout(layout_name: str) -> str:
    """Generate appropriate content examples based on layout context."""
    layout_lower = layout_name.lower()
    
    if "section" in layout_lower:
        return "Section introduction and overview"
    elif "content" in layout_lower and "caption" in layout_lower:
        return "Main content with supporting details"
    elif "big" in layout_lower and "number" in layout_lower:
        return "85%"  # For big number layouts
    else:
        return "Main content with bullet points and details"


async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == "sse":
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
