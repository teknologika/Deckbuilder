#!/bin/bash
# Build Examples Script
# 
# This script runs the complete build process for example files:
# 1. Runs all tests to ensure examples are working
# 2. Generates master files for packaging
# 3. Reports build status
#
# Usage: ./scripts/build_examples.sh

set -e  # Exit on any error

echo "🔨 Starting Deckbuilder Examples Build Process"
echo "============================================="

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not detected, attempting to activate..."
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ Virtual environment not found. Please run: python -m venv .venv && source .venv/bin/activate"
        exit 1
    fi
fi

# Step 1: Run all tests
echo ""
echo "🧪 Step 1: Running comprehensive test suite..."
echo "---------------------------------------------"
python tests/test_structured_frontmatter_examples.py

# Check test results
if [[ $? -eq 0 ]]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed. Fix issues before generating master files."
    exit 1
fi

# Step 2: Generate master files
echo ""
echo "📦 Step 2: Generating master example files..."
echo "---------------------------------------------"
python scripts/generate_master_examples.py

# Check generation results
if [[ $? -eq 0 ]]; then
    echo "✅ Master files generated successfully!"
else
    echo "❌ Master file generation failed."
    exit 1
fi

# Step 3: Report final status
echo ""
echo "🎯 Build Complete!"
echo "=================="
echo "📄 Generated Files:"
echo "   • master_examples.json (ready for packaging)"
echo "   • master_examples.md (ready for packaging)"
echo ""
echo "🚀 Examples are ready for distribution!"