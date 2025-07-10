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
    description="MCP server for PowerPoint presentation generation from JSON and Markdown",
    lifespan=deckbuilder_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),  # nosec B104
    port=os.getenv("PORT", "8050"),
)


@mcp.tool()
async def create_presentation(
    ctx: Context,
    json_data: dict,
    fileName: str = "Sample_Presentation",
    templateName: str = "default",
) -> str:
    """Create a complete PowerPoint presentation from JSON data

    This tool accepts JSON data containing all slides and creates a complete presentation
    with automatic saving. Supports all slide types: title, content, table, and all
    available layouts with inline formatting.

    IMPORTANT: Use the provided JSON data exactly as given by the user. Do not modify,
    reformat, or adjust the JSON structure unless the tool fails with specific errors
    that require fixes.

    Args:
        ctx: MCP context
        json_data: JSON object containing presentation data with slides (use as-is)
        fileName: Output filename (default: Sample_Presentation)
        templateName: Template to use (default: default)

    Example JSON format:
        {
            "presentation": {
                "slides": [
                    {
                        "type": "title",
                        "title": "**My Title** with *formatting*",
                        "subtitle": "Subtitle with ___underline___"
                    },
                    {
                        "type": "content",
                        "title": "Content Slide",
                        "content": [
                            "**Bold** bullet point",
                            "*Italic* text with ___underline___",
                            "***Bold italic*** combination"
                        ]
                    },
                    {
                        "type": "table",
                        "title": "Table Example",
                        "table": {
                            "header_style": "dark_blue_white_text",
                            "row_style": "alternating_light_gray",
                            "data": [
                                ["**Header 1**", "*Header 2*", "___Header 3___"],
                                ["Data 1", "Data 2", "Data 3"]
                            ]
                        }
                    },
                    {
                        "type": "Picture with Caption",
                        "title": "Image Example",
                        "image_1": "path/to/image.png",
                        "text_caption_1": "**Professional** image with *automatic* fallback"
                    }
                ]
            }
        }

    Supported slide types:
        - title: Title slide with title and subtitle
        - content: Content slide with rich text, bullets, headings
        - table: Table slide with full styling support
        - Picture with Caption: Image slides with automatic PlaceKitten fallback
        - All PowerPoint layout types are supported via the template mapping

    Image support:
        - Direct image insertion via image_1, image_2, etc. fields
        - Automatic PlaceKitten fallback for missing images
        - Professional styling: grayscale filter + smart cropping
        - Intelligent face detection and rule-of-thirds composition
        - Optimized caching for performance

    Inline formatting support:
        - **bold** - Bold text
        - *italic* - Italic text
        - ___underline___ - Underlined text
        - ***bold italic*** - Combined bold and italic
        - ***___all three___*** - Bold, italic, and underlined

    Table styling options:
        - header_style: dark_blue_white_text, light_blue_dark_text, etc.
        - row_style: alternating_light_gray, solid_white, etc.
        - border_style: thin_gray, thick_gray, no_borders, etc.
        - custom_colors: Custom hex color overrides

    IMPORTANT: Do NOT include markdown table separator lines (|---|---|---|) in table data.
    Only include actual table rows with content.

    USER CONTENT POLICY: When users provide JSON or markdown content (pasted or referenced),
    use it exactly as provided. Do not modify, reformat, or "improve" the structure unless
    the tool fails with specific errors requiring fixes. Respect the user's formatting choices.
    """
    try:
        # Convert JSON data to canonical format if needed
        if "presentation" in json_data and "slides" in json_data["presentation"]:
            # Handle Claude Desktop format: {"presentation": {"slides": [...]}}
            canonical_data = json_data["presentation"]
        elif "slides" not in json_data:
            # If json_data is not already in canonical format, wrap it
            canonical_data = {"slides": [json_data] if isinstance(json_data, dict) else json_data}
        else:
            canonical_data = json_data

        # Convert Claude Desktop slide format to canonical format
        if "slides" in canonical_data:
            for slide in canonical_data["slides"]:
                # Convert 'type' to 'layout' and map to proper layout names
                if "type" in slide:
                    slide_type = slide.pop("type")
                    # Map Claude Desktop types to actual layout names
                    type_to_layout = {
                        "title": "Title Slide",
                        "content": "Title and Content",
                        "table": "Title and Content",  # Tables use Title and Content layout
                        "Picture with Caption": "Picture with Caption",
                        "comparison": "Comparison",
                        "two_content": "Two Content",
                        "section_header": "Section Header",
                        "title_only": "Title Only",
                        "blank": "Blank",
                    }
                    slide["layout"] = type_to_layout.get(slide_type, "Title and Content")

                # Move direct fields to placeholders
                placeholders = slide.get("placeholders", {})
                direct_fields = [
                    "title",
                    "subtitle",
                    "content",
                    "text",
                    "image_1",
                    "text_caption_1",
                ]
                for field in direct_fields:
                    if field in slide and field not in placeholders:
                        field_value = slide[field]
                        # Handle content arrays - convert to string
                        if field == "content" and isinstance(field_value, list):
                            field_value = "\n".join(field_value)
                        placeholders[field] = field_value
                        # Don't remove the field from slide yet - let the engine handle it

                # Ensure placeholders dict exists
                if placeholders:
                    slide["placeholders"] = placeholders

        # Create presentation using the new API
        result = deck.create_presentation(canonical_data, fileName, templateName)

        return f"Successfully created presentation: {fileName}. {result}"
    except Exception as e:
        return f"Error creating presentation: {str(e)}"


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
