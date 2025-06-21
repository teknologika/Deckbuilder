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
from content_analysis import analyze_presentation_needs
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
async def analyze_presentation_needs_tool(ctx: Context, user_input: str, audience: str = "general", constraints: str = None, presentation_goal: str = "inform") -> str:
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
        user_input: "I need to present our Q3 results to the board. We had 23% revenue growth, 
                    expanded to 3 new markets, but customer churn increased to 8%. I want to show 
                    we're growing but acknowledge the churn issue and present our retention strategy."
        audience: "board"
        presentation_goal: "report"
        
        Returns analysis with:
        - Content analysis (key messages, narrative arc, complexity level)
        - Audience considerations (expertise level, attention span, preferred format)
        - Recommended structure (slide sequence with purpose and timing)
        - Presentation strategy (opening/closing approach, engagement tactics)
    """
    try:
        analysis_result = analyze_presentation_needs(user_input, audience, constraints, presentation_goal)
        return json.dumps(analysis_result, indent=2)
    except Exception as e:
        return f"Error analyzing presentation needs: {str(e)}"

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
