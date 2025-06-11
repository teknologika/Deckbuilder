# deck-builder-mcp
MCP Server for building powerpoint presentations

## Configuration

Add this to your Claude Desktop config file:

```json
"mcp-deckbuilder": {
  "command": "/Users/bruce/GitHub/teknologika/deck-builder-mcp/.venv/bin/python",
  "args": ["/Users/bruce/GitHub/teknologika/deck-builder-mcp/src/main.py"],
  "env": {
    "TRANSPORT": "stdio",
    "DECK_TEMPLATE_FOLDER": "/Users/bruce/Documents/Deckbuilder/Templates",
    "DECK_TEMPLATE_NAME": "defailt",
    "DECK_OUTPUT_FOLDER": "/Users/bruce/Documents/Deckbuilder"
  }
}
```
