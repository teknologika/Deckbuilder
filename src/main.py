from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import json
import os

from deckbuilder import Deckbuilder
from deckbuilder import get_deckbuilder_client
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
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8050")
)

@mcp.tool()
async def create_presentation(ctx: Context, templateName: str, fileName: str) -> str:
    """Create a new presentation ready to add slides

    This tool is designed to create a new powerpoint presentation from the given context.
    This tool creates an empty presentation, with no slides in it.
    Slides are then be added by calling other tools.
    This does NOT add a title slide, you will need to call add_title_slide to do that.

    Args:
        ctx: The MCP server provided context.
        title: The title of the presentation (default: Sample_Presentation).
        subTitle: The sub-title of the presentation (default: blank).
        templateName: The name of the tempate to use (default: default)
        author: The author of the presentation.
    """
    try:
        result = deck.create_presentation(templateName, fileName)
        return f"Successfully created the presentation: {fileName}"
    except Exception as e:
        return f"Error creating presentation: {str(e)}"

@mcp.tool()
async def write_presentation(ctx: Context, fileName: str = "Sample_Presentation" ) -> str:
    """Writes the presentation to disk

    This tool is designed to save the current presentation that has been created to a file.

    Args:
        ctx: The MCP server provided context.
        fileName: The name of the file that this server should create (default: Sample_Presentation).
    """
    try:
        return deck.write_presentation(fileName)
    except Exception as e:
        return f"Error creating presentation: {str(e)}"

@mcp.tool()
async def add_title_slide(ctx: Context, json_data) -> str:
    """Add a Title slide to the presentation using JSON data
    
    This tool accepts a JSON string containing slide information and adds it to the current presentation.
    
    Args:
        ctx: The MCP server provided context.
        json_data: JSON string containing slide data with title, content, etc.
        
    Example JSON format for the Title slide:
        {
            "type": "title",
            "title": "My Title",
            "subtitle": "My subtitle"
        } 
    """
    try:
        return deck.add_slide_from_json(json_data)
    except Exception as e:
        return f"Error adding slide from JSON: {str(e)}"

@mcp.tool()
async def add_content_slide(ctx: Context, json_data) -> str:
    """Add a Content slide to the presentation using JSON data
    
    This tool accepts a JSON string containing slide information and adds it to the current presentation.
    
    Args:
        ctx: The MCP server provided context.
        json_data: JSON string containing slide data with title, content, etc.
        
    Example JSON format for the Content slide:
        {
            "type": "content",
            "title": "Content Slide title",
            "content": [
                "Content line one.",
                "Content line two.",
                "Content line three.",
                "Content line four."
            ]
        }
    """
    try:
        return deck.add_slide_from_json(json_data)
    except Exception as e:
        return f"Error adding slide from JSON: {str(e)}"

@mcp.tool()
async def add_table_slide(ctx: Context, json_data) -> str:
    """Add a Table slide to the presentation using JSON data with custom styling support
    
    This tool accepts a JSON string containing table slide information and adds it to the current presentation.
    Supports custom styling through predefined style names and color overrides.
    
    Args:
        ctx: The MCP server provided context.
        json_data: JSON string containing table slide data with styling options.
        
    Example JSON format for the Table slide:
        {
            "type": "table",
            "title": "Sales Report",
            "table": {
                "header_style": "dark_blue_white_text",
                "row_style": "alternating_light_gray", 
                "border_style": "thin_gray",
                "custom_colors": {
                    "header_bg": "#2E5984",
                    "header_text": "#FFFFFF",
                    "alt_row": "#F0F8FF"
                },
                "data": [
                    ["Name", "Sales", "Region"],
                    ["John Smith", "$125,000", "North"],
                    ["Sarah Johnson", "$98,500", "South"]
                ]
            }
        }
        
    Available header_style options:
        - "dark_blue_white_text" - Dark blue background, white text
        - "light_blue_dark_text" - Light blue background, dark text
        - "dark_gray_white_text" - Dark gray background, white text
        - "light_gray_dark_text" - Light gray background, dark text
        - "white_dark_text" - White background, dark text
        - "accent_color_white_text" - Theme accent color background, white text
        
    Available row_style options:
        - "alternating_light_gray" - White/light gray alternating rows
        - "alternating_light_blue" - White/light blue alternating rows
        - "solid_white" - All white rows
        - "solid_light_gray" - All light gray rows
        - "no_fill" - Transparent/no background
        
    Available border_style options:
        - "thin_gray" - Thin gray borders all around
        - "thick_gray" - Thick gray borders
        - "header_only" - Border only under header
        - "outer_only" - Border only around table perimeter
        - "no_borders" - No borders
        
    Custom color overrides (hex codes):
        - "header_bg" - Header background color
        - "header_text" - Header text color
        - "alt_row" - Alternating row background color
        - "border_color" - Border color
    """
    try:
        return deck.add_slide_from_json(json_data)
    except Exception as e:
        return f"Error adding table slide from JSON: {str(e)}"

@mcp.tool()
async def create_presentation_from_markdown(ctx: Context, markdown_content: str, fileName: str = "Sample_Presentation", templateName: str = "default") -> str:
    """Create presentation from formatted markdown with frontmatter
    
    This tool accepts markdown content with frontmatter slide definitions and creates a complete presentation.
    Each slide is defined using YAML frontmatter followed by markdown content.
    This tool does not save the presentation. After you call this tool call write_presentation
    
    Args:
        ctx: MCP context
        markdown_content: Markdown string with frontmatter slide definitions
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
    
    Supported layouts:
        - title: Title slide with title and subtitle
        - content: Content slide with rich text support (headings, paragraphs, bullets)
        - table: Table slide with styling options
        
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
        
        # Add all slides
        for slide_data in slides:
            deck._add_slide(slide_data)
            
        return f"Successfully created presentation with {len(slides)} slides from markdown"
    except Exception as e:
        return f"Error creating presentation from markdown: {str(e)}"
    
@mcp.tool()
async def add_slide(ctx: Context, json_data) -> str:
    """Add a slide to the presentation using JSON data
    
    This tool accepts a JSON string containing slide information and adds it to the current presentation.
    
    Args:
        ctx: The MCP server provided context.
        json_data: JSON string containing slide data with title, content, etc.
        
    Example JSON formats:
        Single slide: "slides": [{"title": "My Title", "content": "My content"}]
        Multiple slides:
             "slides": [
            {
                "type": "title",
                "title": "My Title",
                "subtitle": "My subtitle"
            },
            {
                "type": "content",
                "title": "Content Slide title",
                "content": [
                    "Content line one.",
                    "Content line two.",
                    "Content line three.",
                    "Content line four."
                ]
            }

    Supported slide layouts, and sample json for each
        Title slide:
            {
                "type": "title",
                "title": "My Title",
                "subtitle": "My subtitle"
            } 
        Content slide:
            {
                "type": "content",
                "title": "Content Slide title",
                "content": [
                    "Content line one.",
                    "Content line two.",
                    "Content line three.",
                    "Content line four."
                ]
            }
        Table slide:
            {
                "type": "table",
                "title": "Key Metrics",
                "table": {
                    "rows": [
                        ["Metric", "Q2 2024", "Q1 2024", "YoY Change"],
                        ["Revenue", "$12.5M", "$11.2M", "+11.6%"],
                        ["Operating Margin", "28.4%", "26.8%", "+1.6pp"],
                        ["Customer Base", "145K", "128K", "+13.3%"],
                        ["Employee Count", "520", "480", "+8.3%"]
                    ]
                }
    """
    try:
        return deck.add_slide_from_json(json_data)
    except Exception as e:
        return f"Error adding slide from JSON: {str(e)}"

async def main():
    transport = os.getenv("TRANSPORT", "sse")
    if transport == 'sse':
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())
