#!/bin/bash
# Launch MCP Inspector with Deckbuilder MCP Server
# This script sets up the required environment variables and launches the MCP Inspector

# Set the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Set required environment variables for Deckbuilder MCP server
export DECK_TEMPLATE_FOLDER="${PROJECT_ROOT}/src/deckbuilder/assets/templates"
export DECK_OUTPUT_FOLDER="${PROJECT_ROOT}/tests/output"
export DECK_TEMPLATE_NAME="default"
export TRANSPORT="stdio"

# Ensure output directory exists
mkdir -p "${DECK_OUTPUT_FOLDER}"

echo "🚀 Launching MCP Inspector for Deckbuilder server..."
echo "📁 Template folder: ${DECK_TEMPLATE_FOLDER}"
echo "📁 Output folder: ${DECK_OUTPUT_FOLDER}"
echo "📄 Template name: ${DECK_TEMPLATE_NAME}"
echo ""

# Check if template files exist
if [ ! -f "${DECK_TEMPLATE_FOLDER}/default.json" ]; then
    echo "❌ Error: Template mapping file not found at ${DECK_TEMPLATE_FOLDER}/default.json"
    echo "Please ensure the template files are in the correct location."
    exit 1
fi

if [ ! -f "${DECK_TEMPLATE_FOLDER}/default.pptx" ]; then
    echo "⚠️  Warning: Template PowerPoint file not found at ${DECK_TEMPLATE_FOLDER}/default.pptx"
    echo "The server may still work but presentations will use default layouts."
fi

# Check if MCP Inspector is available
if ! command -v npx &> /dev/null; then
    echo "❌ Error: npx is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

# Launch the MCP Inspector
echo "🔍 Starting MCP Inspector..."
echo "The inspector will open in your browser at http://localhost:5173"
echo "Press Ctrl+C to stop the server"
echo ""

# Change to project directory and launch
cd "${PROJECT_ROOT}" || exit 1
npx @modelcontextprotocol/inspector \
  uv \
  --directory /Users/bruce/GitHub/teknologika/Deckbuilder/src/mcp_server/main.py \
  run \
  deckbuilder-server \
  args...