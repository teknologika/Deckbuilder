from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import json
import os


from deckbuilder import get_deckbuilder_client

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
async def create_presentation(ctx: Context, fileName: str = "Sample_Presentation") -> str:
    """Create a new presentation ready to add slides

    This tool is designed to create a new powerpoint presentation from the given context.
    This tool creates an empty presentation, with no slides in it.
    Slides can then be added by calling other tools.

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
        base_name = fileName
        latest_file = os.path.join(output_folder, f"{base_name}.latest.txt")
        
        # Handle versioning if file exists
        if os.path.exists(latest_file):
            # Find the highest version number
            version_num = 1
            while True:
                version_file = os.path.join(output_folder, f"{base_name}.v{version_num:02d}.txt")
                if not os.path.exists(version_file):
                    break
                version_num += 1
            
            # Trim the .latest of the version_file name when we rename it
            # Create versioned filename without .latest (e.g. Sample_Presentation.v01.txt instead of Sample_Presentation.latest.v01.txt)
            version_file = os.path.join(output_folder, f"{base_name}.v{version_num:02d}.txt")
            
            # Rename current latest to versioned file
            os.rename(latest_file, version_file)
        
        # Create new latest file
        with open(latest_file, 'w') as f:
            f.write(f"Presentation: {fileName}\n")
            f.write(f"Created: {os.path.basename(latest_file)}\n")
            f.write("This is a test presentation file.\n")
        
        return f"Successfully created presentation: {os.path.basename(latest_file)}"
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
