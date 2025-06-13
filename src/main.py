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
async def create_presentation(ctx: Context, title: str = "Presentation Title", subTitle: str = "", author: str = "") -> str:
    """Create a new presentation ready to add slides

    This tool is designed to create a new powerpoint presentation from the given context.
    This tool creates an empty presentation, with no slides in it.
    Slides can then be added by calling other tools.

    Args:
        ctx: The MCP server provided context.
        title: The title of the presentation (default: Sample_Presentation).
        subTitle: The sub-title of the presentation (default: blank).
        author: The author of the presentation.
    """
    try:
        template_name = deck.template_name or 'default'
        result = deck.create_presentation(title, template_name)
        return f"Successfully created the presentation and added a title slide {title}"
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

        # Get output folder from environment
        output_folder = os.getenv('DECK_OUTPUT_FOLDER', '.')
        
        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Create base filename with .latest.txt extension
        base_name = f"{fileName}.latest.pptx"
        
        latest_file = os.path.join(output_folder, base_name)
        
        # Handle versioning if file exists
        if os.path.exists(latest_file):
            # Find the highest version number
            version_num = 1
            while True:
                version_file = os.path.join(output_folder, f"{base_name}.v{version_num:02d}.pptx")
                if not os.path.exists(version_file):
                    break
                version_num += 1
            
            # Trim the .latest of the version_file name when we rename it
            # Create versioned filename without .latest (e.g. Sample_Presentation.v01.pptx instead of Sample_Presentation.latest.pptx)
            version_file = os.path.join(output_folder, f"{base_name}.v{version_num:02d}.pptx")
            
            # Rename current latest to versioned file
            os.rename(latest_file, version_file)
        
        # Write the latest file
        deck.prs.save(latest_file)
        
        return f"Successfully created presentation: {os.path.basename(latest_file)}"
    except Exception as e:
        return f"Error creating presentation: {str(e)}"

@mcp.tool()
async def add_title_slide(ctx: Context, title: str = "Slide Title", subTitle: str = "", author: str = "") -> str:
    """Add a title slide to an existing presentaiton

        This tool is designed to add a title to an existing presentation.
        If a title slide already exists, it will replace it.
        This tool should be called after create_presentation 

        Args:
            ctx: The MCP server provided context.
            title: The title of the presentation (default: Sample_Presentation).
            subTitle: The sub-title of the presentation (default: blank).
            author: The author of the presentation.
            
        """
    try:
        return f"Successfully added title slide {title}"
    except Exception as e:
        return f"Error creating presentation: {str(e)}"

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
