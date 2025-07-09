# MCP Server Tests

This directory contains comprehensive tests for the Deckbuilder MCP server that **actually call the real MCP server**.

## Test Files

### ✅ Working Tests

1. **`test_mcp_simple.py`** - Basic error reproduction and success tests
   - ✅ Reproduces original "Slide 1 must have a 'layout' field" error
   - ✅ Tests successful presentation creation
   - ✅ Uses real MCP protocol

2. **`test_mcp_subset.py`** - Comprehensive tests with smaller datasets
   - ✅ JSON content test (3 slides)
   - ✅ JSON file test (small file)
   - ✅ Markdown content test (2 slides)
   - ✅ Error handling test
   - ✅ Fast execution (avoids timeouts)

3. **`test_mcp_pytest.py`** - Pytest-compatible test structure
   - ✅ Proper pytest fixtures
   - ✅ All 5 test scenarios covered
   - ✅ Async-aware (needs pytest-asyncio for pytest runner)
   - ✅ Works standalone

### 🔄 In Development

4. **`test_mcp_final.py`** - Full master file tests
   - ⚠️  Uses large master files (may timeout)
   - ✅ Comprehensive coverage
   - 🔄 Needs optimization for large datasets

## How to Run Tests

### Individual Test Files
```bash
# Quick error reproduction test
python tests/mcp_server/test_mcp_simple.py

# Comprehensive subset tests
python tests/mcp_server/test_mcp_subset.py

# Pytest-style tests (standalone)
python tests/mcp_server/test_mcp_pytest.py
```

### With Pytest (requires pytest-asyncio)
```bash
# Install pytest-asyncio first
pip install pytest-asyncio

# Run pytest tests
python -m pytest tests/mcp_server/test_mcp_pytest.py -v --asyncio-mode=auto
```

## Test Coverage

All tests cover the **4 main MCP tools**:

1. **`create_presentation`** - Direct JSON data
2. **`create_presentation_from_file`** - JSON file path
3. **`create_presentation_from_markdown`** - Direct markdown content
4. **`create_presentation_from_file`** - Markdown file path

Plus **error handling** for invalid data (missing layout fields).

## Test Results

✅ **Successfully reproduces original error**: "Slide 1 must have a 'layout' field"
✅ **Successfully creates presentations** when valid data is provided
✅ **Actually calls MCP server** using real MCP protocol
✅ **Tests all MCP tools** with different input methods
✅ **Validates error handling** for invalid inputs

## MCP Inspector

Use the MCP Inspector for interactive testing:

```bash
# Launch inspector
./scripts/launch_mcp_inspector.sh

# Or manually
npx @modelcontextprotocol/inspector python src/mcp_server/main.py
```

## Environment Requirements

All tests require these environment variables (automatically set by test files):

- `DECK_TEMPLATE_FOLDER` - Path to template files
- `DECK_OUTPUT_FOLDER` - Path for output files  
- `DECK_TEMPLATE_NAME` - Template name (default: "default")
- `TRANSPORT` - MCP transport type (default: "stdio")

## Template Files Required

Tests require these files to exist:
- `src/deckbuilder/assets/templates/default.json` - Template mapping
- `src/deckbuilder/assets/templates/default.pptx` - PowerPoint template (optional)

## Test Output

Generated presentations are saved to:
- `tests/output/` directory
- Named with test name and timestamp
- Format: `test_name.YYYY-MM-DD_HHMM.g.pptx`