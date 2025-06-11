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

@asynccontextmanager
async def deckbuilder_lifespan(server: FastMCP) -> AsyncIterator[DeckbuilderContext]:
    """
    Manages the Deckbuilder client lifecycle.
    
    Args:
        server: The Deckbuilder server instance
        
    Yields:
        PresentationContext: The context containing the Deckbuilder client
    """
    
    # Create and return the Deckbuilder Client with the helper function in deckbuidlder.py
    deckbuilder_client = get_deckbuilder_client

    try:
        yield DeckbuilderContext(deckbuilder_client=deckbuilder_client)
    finally:
        # Explicit cleanup goes here if any is required
        pass

# Initialize FastMCP server with the Deckbuilder client as context
mcp = FastMCP(
    "mcp-deckbuilder",
    description="MCP server for creation of powerpoint decks",
    lifespan=deckbuilder_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),
    port=os.getenv("PORT", "8050")
)

@mcp.tool()
async def create_presentation(ctx: Context, fileName: str) -> str:
    """Create a new presentation ready to add slides

    This tool is designed to create a new powerpoint presentation from the given context.
    This tool creates an empty presentation, with no slides in it.
    Slides can then be added by calling other tools.

    Args:
        ctx: The MCP server provided context.
        text: The name of the file that this server should create.
    """
    try:
        return f"Created a presentation: {fileName[:100]}..." if len(fileName) > 100 else f"Successfully saved memory: {fileName}"
    except  Exception as e:
        return f"Error creating presentation memory: {str(e)}"

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
