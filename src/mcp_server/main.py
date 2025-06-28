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

# Import content-first tools (will be implemented later)
try:
    from .content_analysis import analyze_presentation_needs
    from .content_optimization import optimize_content_for_layout
    from .layout_recommendations import recommend_slide_approach
except ImportError:
    # Placeholder functions for when these modules don't exist yet
    def analyze_presentation_needs(*args, **kwargs):
        return "Content analysis tool not implemented yet"

    def recommend_slide_approach(*args, **kwargs):
        return "Layout recommendation tool not implemented yet"

    def optimize_content_for_layout(*args, **kwargs):
        return "Content optimization tool not implemented yet"


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
    description="MCP server for creation of powerpoint decks",
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
        # Create presentation
        deck.create_presentation(templateName, fileName)

        # Add slides from JSON data
        deck.add_slide_from_json(json_data)

        # Automatically save the presentation
        write_result = deck.write_presentation(fileName)

        return f"Successfully created presentation: {fileName}. {write_result}"
    except Exception as e:
        return f"Error creating presentation: {str(e)}"


@mcp.tool()
async def analyze_presentation_needs_tool(
    ctx: Context,
    user_input: str,
    audience: str = "general",
    constraints: str = None,
    presentation_goal: str = "inform",
) -> str:
    """
    Analyze user's presentation needs and recommend structure.

    Content-first approach: Understand communication goals before suggesting layouts.
    Acts as intelligent presentation consultant, not layout picker.

    Args:
        ctx: MCP context
        user_input: Raw description of what they want to present
        audience: Target audience ("board", "team", "customers", "technical", "general")
        constraints: Time/slide constraints ("10 minutes", "5 slides max", "data-heavy")
        presentation_goal: Primary goal ("persuade", "inform", "report", "update", "train")

    Returns:
        JSON string with content analysis and structural recommendations

    Example:
        user_input: "I need to present our Q3 results to the board. We had 23% revenue
                    growth, expanded to 3 new markets, but customer churn increased to 8%.
                    I want to show we're growing but acknowledge the churn issue and present
                    our retention strategy."
        audience: "board"
        presentation_goal: "report"

        Returns analysis with:
        - Content analysis (key messages, narrative arc, complexity level)
        - Audience considerations (expertise level, attention span, preferred format)
        - Recommended structure (slide sequence with purpose and timing)
        - Presentation strategy (opening/closing approach, engagement tactics)
    """
    try:
        analysis_result = analyze_presentation_needs(
            user_input, audience, constraints, presentation_goal
        )
        return json.dumps(analysis_result, indent=2)
    except Exception as e:
        return f"Error analyzing presentation needs: {str(e)}"


@mcp.tool()
async def recommend_slide_approach_tool(
    ctx: Context, content_piece: str, message_intent: str, presentation_context: str = None
) -> str:
    """
    Recommend optimal slide layouts based on specific content and communication intent.

    Content-first approach: Analyzes what you want to communicate with this specific
    content piece and recommends the most effective slide layouts.

    Args:
        ctx: MCP context
        content_piece: Specific content to present (e.g., "We increased revenue 25%,
                       expanded to 3 markets, but churn rose to 8%")
        message_intent: What you want this content to communicate (e.g.,
                        "show growth while acknowledging challenges")
        presentation_context: Optional JSON string from analyze_presentation_needs_tool output

    Returns:
        JSON string with layout recommendations, confidence scores, and content suggestions

    Example:
        content_piece: "Our mobile app has these key features: real-time notifications,
                       offline mode, cloud sync, and advanced analytics dashboard"
        message_intent: "showcase the comprehensive feature set to potential customers"

        Returns recommendations like:
        - Four Columns layout (confidence: 0.90) for feature comparison grid
        - Title and Content layout (confidence: 0.75) for traditional feature list
        - Content structuring suggestions and YAML preview

    This tool bridges the gap between content analysis (Tool #1) and content optimization (Tool #3)
    by providing specific layout guidance for individual content pieces.
    """
    try:
        # Parse presentation context if provided
        context_dict = None
        if presentation_context:
            try:
                context_dict = json.loads(presentation_context)
            except json.JSONDecodeError:
                # If parsing fails, continue without context
                pass

        # Get layout recommendations
        recommendations = recommend_slide_approach(content_piece, message_intent, context_dict)

        return json.dumps(recommendations, indent=2)

    except Exception as e:
        return f"Error recommending slide approach: {str(e)}"


@mcp.tool()
async def optimize_content_for_layout_tool(
    ctx: Context, content: str, chosen_layout: str, slide_context: str = None
) -> str:
    """
    Optimize content structure and generate ready-to-use YAML for immediate presentation creation.

    Final step in content-first workflow: Takes raw content and chosen layout, then optimizes
    the content structure and generates production-ready YAML that can be used directly
    with create_presentation_from_markdown.

    Args:
        ctx: MCP context
        content: Raw content to optimize (e.g., "Our platform offers real-time
                 analytics, automated reporting, custom dashboards, and API integration")
        chosen_layout: Layout to optimize for (e.g., "Four Columns" from
                       recommend_slide_approach_tool)
        slide_context: Optional JSON string with context from previous tools
                       (analyze_presentation_needs, recommend_slide_approach)

    Returns:
        JSON string with optimized YAML structure, gap analysis, and presentation tips

    Example:
        content: "Traditional approach costs $50K annually with 2-week deployment
                 vs our solution at $30K with same-day setup"
        chosen_layout: "Comparison"

        Returns:
        - optimized_content.yaml_structure: Ready-to-use YAML for create_presentation_from_markdown
        - gap_analysis: Content fit assessment and recommendations
        - presentation_tips: Delivery guidance and timing estimates
        - image_recommendations: Suggested visual content with PlaceKitten fallback support

    Complete Content-First Workflow:
    1. analyze_presentation_needs_tool() -> overall structure
    2. recommend_slide_approach_tool() -> layout recommendations
    3. optimize_content_for_layout_tool() -> production-ready YAML ✅ THIS TOOL
    4. create_presentation_from_markdown() -> final PowerPoint
    """
    try:
        # Parse slide context if provided
        context_dict = None
        if slide_context:
            try:
                context_dict = json.loads(slide_context)
            except json.JSONDecodeError:
                # If parsing fails, continue without context
                pass

        # Optimize content for the chosen layout
        optimization_result = optimize_content_for_layout(content, chosen_layout, context_dict)

        return json.dumps(optimization_result, indent=2)

    except Exception as e:
        return f"Error optimizing content for layout: {str(e)}"


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

            # Create presentation from JSON
            deck.create_presentation(templateName, fileName)
            deck.add_slide_from_json(json_data)
            write_result = deck.write_presentation(fileName)

            return f"Successfully created presentation from JSON file: {file_path}. {write_result}"

        elif file_extension == ".md":
            # Read markdown file
            with open(file_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()

            # Create presentation from markdown
            slides = deck.parse_markdown_with_frontmatter(markdown_content)
            deck.create_presentation(templateName, fileName)

            for slide_data in slides:
                deck._add_slide(slide_data)

            write_result = deck.write_presentation(fileName)

            return (
                f"Successfully created presentation from markdown file: "
                f"{file_path} with {len(slides)} slides. {write_result}"
            )

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
        slides = deck.parse_markdown_with_frontmatter(markdown_content)

        # Create presentation
        deck.create_presentation(templateName, fileName)

        # Add all slides to the presentation
        for slide_data in slides:
            deck._add_slide(slide_data)

        # Automatically save the presentation to disk after creation
        write_result = deck.write_presentation(fileName)

        return (
            f"Successfully created presentation with {len(slides)} slides "
            f"from markdown. {write_result}"
        )
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
