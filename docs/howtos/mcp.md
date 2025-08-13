# Run as MCP server (Claude Desktop)

Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "deckbuilder": {
      "command": "deckbuilder-server",
      "env": {
        "DECK_TEMPLATE_FOLDER": "/path/to/Templates",
        "DECK_TEMPLATE_NAME": "default",
        "DECK_OUTPUT_FOLDER": "/path/to/Output",
        "DECK_PROOFING_LANGUAGE": "en-AU",
        "DECK_DEFAULT_FONT": "Calibri"
      }
    }
  }
}
```
