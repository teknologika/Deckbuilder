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
async def create_presentation(ctx: Context, json_data: str, fileName: str = "Sample_Presentation", templateName: str = "default") -> str:
    """Create a complete PowerPoint presentation from JSON data
    
    This tool accepts JSON data containing all slides and creates a complete presentation with automatic saving.
    Supports all slide types: title, content, table, and all available layouts with inline formatting.
    
    Args:
        ctx: MCP context
        json_data: JSON string containing presentation data with slides
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
                    }
                ]
            }
        }
    
    Supported slide types:
        - title: Title slide with title and subtitle
        - content: Content slide with rich text, bullets, headings
        - table: Table slide with full styling support
        - All PowerPoint layout types are supported via the template mapping
        
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
    """
    try:
        # Create presentation
        deck.create_presentation(templateName, fileName)
        
        # Add slides from JSON data
        result = deck.add_slide_from_json(json_data)
        
        # Automatically save the presentation
        write_result = deck.write_presentation(fileName)
        
        return f"Successfully created presentation: {fileName}. {write_result}"
    except Exception as e:
        return f"Error creating presentation: {str(e)}"

@mcp.tool()
async def create_presentation_from_markdown(ctx: Context, markdown_content: str, fileName: str = "Sample_Presentation", templateName: str = "default") -> str:
    """Create presentation from formatted markdown with frontmatter
    
    This tool accepts markdown content with frontmatter slide definitions and creates a complete presentation.
    Each slide is defined using YAML frontmatter followed by markdown content.
    This tool automatically saves the presentation to disk after creation.
    
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
        
        # Add all slides to the presentation
        for slide_data in slides:
            deck._add_slide(slide_data)
        
        # Automatically save the presentation to disk after creation
        write_result = deck.write_presentation(fileName)
            
        return f"Successfully created presentation with {len(slides)} slides from markdown. {write_result}"
    except Exception as e:
        return f"Error creating presentation from markdown: {str(e)}"
    

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
