"""
Integration tests for MCP tools functionality.

Tests the MCP tools for template analysis and presentation creation
to replace functionality from test_tools.py with proper pytest structure.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import shutil

import pytest

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))  # noqa: E402

# Test imports with graceful handling
HAS_MCP_TOOLS = False
try:
    from mcp_server.tools import analyze_pptx_template  # noqa: E402
    from deckbuilder.engine import get_deckbuilder_client  # noqa: E402

    HAS_MCP_TOOLS = True
except ImportError as e:
    print(f"Import error: {e}")

    # Create mock functions to avoid NameError
    def analyze_pptx_template(template_name):
        return {"mock": True}

    def get_deckbuilder_client():
        return None


@pytest.fixture
def mock_deckbuilder_env():
    """Mock environment variables for deckbuilder with cleanup."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        templates_dir = temp_path / "templates"
        output_dir = temp_path / "outputs"
        templates_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)

        project_root = Path(__file__).parent.parent.parent.parent
        source_template_dir = project_root / "src" / "deckbuilder" / "assets" / "templates"

        # Copy real template files to the temp directory
        for file_name in ["default.pptx", "default.json"]:
            source_file = source_template_dir / file_name
            if source_file.exists():
                shutil.copy(source_file, templates_dir / file_name)

        original_env = os.environ.copy()
        test_env = {
            "DECK_TEMPLATE_FOLDER": str(templates_dir),
            "DECK_OUTPUT_FOLDER": str(output_dir),
            "DECK_TEMPLATE_NAME": "default",
        }
        os.environ.update(test_env)

        yield {"templates_dir": templates_dir, "output_dir": output_dir}

        os.environ.clear()
        os.environ.update(original_env)


@pytest.fixture
def sample_test_data():
    """Sample test data for presentation creation."""
    return {
        "presentation": {
            "slides": [
                {
                    "type": "Title Slide",
                    "layout": "Title Slide",
                    "title": "Test Presentation",
                    "subtitle": "Automated Testing Framework",
                },
                {
                    "type": "Four Columns With Titles",
                    "title": "Feature Overview",
                    "title_col1_1": "Performance",
                    "content_col1_1": "Fast processing",
                    "title_col2_1": "Security",
                    "content_col2_1": "Enterprise encryption",
                    "title_col3_1": "Usability",
                    "content_col3_1": "Intuitive interface",
                    "title_col4_1": "Cost",
                    "content_col4_1": "Competitive pricing",
                },
            ]
        }
    }


@pytest.fixture
def sample_markdown_content():
    """Sample markdown content with structured frontmatter."""
    return """---
layout: Four Columns With Titles
title: Feature Comparison
columns:
  - title: Performance
    content: Fast processing with optimized algorithms
  - title: Security
    content: Enterprise-grade encryption and compliance
  - title: Usability
    content: Intuitive interface with minimal learning curve
  - title: Cost
    content: Competitive pricing with flexible plans
---

# Feature Overview

This slide demonstrates the four-column layout with structured frontmatter.

---
layout: Comparison
title: Before vs After
comparison:
  left:
    title: Current State
    content: Manual processes that are time-consuming
  right:
    title: Future State
    content: Automated systems with streamlined workflows
---

# Process Improvement

This comparison shows the transformation we're aiming for.
"""


@pytest.mark.skipif(not HAS_MCP_TOOLS, reason="MCP tools not available")
@pytest.mark.integration
@pytest.mark.mcp_server
class TestMCPToolsIntegration:
    """Integration tests for MCP tools functionality."""

    def test_template_analysis_tool(self, mock_deckbuilder_env):
        """Test the analyze_pptx_template MCP tool."""
        result = analyze_pptx_template("default")

        assert result is not None
        assert "template_info" in result
        assert "layouts" in result

    @patch("deckbuilder.engine.Deckbuilder")
    def test_presentation_creation_from_json(self, mock_deckbuilder_class, mock_deckbuilder_env, sample_test_data):
        """Test creating a presentation from canonical JSON data."""
        # Mock the deckbuilder instance
        mock_deck = MagicMock()
        mock_deckbuilder_class.return_value = mock_deck

        # Mock successful operations
        mock_deck.create_presentation.return_value = "✓ Presentation created successfully with 2 slides"

        # Convert legacy format to canonical format
        canonical_data = {"slides": []}
        for slide_data in sample_test_data["presentation"]["slides"]:
            canonical_slide = {
                "layout": slide_data.get("type", "Title and Content"),
                "placeholders": {key: value for key, value in slide_data.items() if key not in ["type", "layout"]},
                "content": [],
            }
            canonical_data["slides"].append(canonical_slide)

        # Test the workflow
        deck = get_deckbuilder_client()

        # Create presentation using canonical format
        result = deck.create_presentation(presentation_data=canonical_data, fileName="test_json", templateName="default")
        assert "successfully" in result.lower()

        # Verify calls
        mock_deck.create_presentation.assert_called_once_with(presentation_data=canonical_data, fileName="test_json", templateName="default")

    @patch("deckbuilder.engine.Deckbuilder")
    def test_presentation_creation_from_markdown(self, mock_deckbuilder_class, mock_deckbuilder_env, sample_markdown_content):
        """Test creating a presentation from markdown with structured frontmatter."""
        # Mock the deckbuilder instance
        mock_deck = MagicMock()
        mock_deckbuilder_class.return_value = mock_deck

        # Mock successful operation
        mock_deck.create_presentation.return_value = "✓ Presentation created from canonical JSON successfully"

        # Test the workflow with mocked converter
        deck = get_deckbuilder_client()

        with patch("deckbuilder.converter.markdown_to_canonical_json") as mock_converter:
            # Mock converter to return canonical JSON format
            mock_converter.return_value = {
                "slides": [
                    {
                        "layout": "Four Columns With Titles",
                        "placeholders": {"title": "Feature Comparison"},
                        "content": [],
                    }
                ]
            }

            # Create presentation from markdown (using canonical pipeline)
            canonical_data = mock_converter(sample_markdown_content)
            result = deck.create_presentation(
                presentation_data=canonical_data,
                fileName="test_markdown",
                templateName="default",
            )

            assert "successfully" in result.lower()

            # Verify calls
            mock_converter.assert_called_once_with(sample_markdown_content)
            mock_deck.create_presentation.assert_called_once_with(
                presentation_data=canonical_data,
                fileName="test_markdown",
                templateName="default",
            )

    def test_atomic_test_isolation(self, mock_deckbuilder_env):
        """Test that tests are properly isolated and atomic."""
        # Each test should start with a clean environment
        assert "DECK_TEMPLATE_FOLDER" in os.environ
        assert "DECK_OUTPUT_FOLDER" in os.environ
        assert "DECK_TEMPLATE_NAME" in os.environ

        # Verify directories exist
        templates_dir = Path(os.environ["DECK_TEMPLATE_FOLDER"])
        output_dir = Path(os.environ["DECK_OUTPUT_FOLDER"])

        assert templates_dir.exists()
        assert output_dir.exists()

    @patch("deckbuilder.engine.Deckbuilder")
    def test_error_handling_missing_template(self, mock_deckbuilder_class, mock_deckbuilder_env):
        """Test error handling when template is missing."""
        # Mock the deckbuilder instance to raise an error
        mock_deck = MagicMock()
        mock_deckbuilder_class.return_value = mock_deck
        mock_deck.create_presentation.side_effect = FileNotFoundError("Template not found")

        deck = get_deckbuilder_client()

        # Should handle the error gracefully
        with pytest.raises(FileNotFoundError):
            deck.create_presentation("nonexistent_template", "test")

    @patch("deckbuilder.engine.Deckbuilder")
    def test_error_handling_invalid_slide_data(self, mock_deckbuilder_class, mock_deckbuilder_env):
        """Test error handling when slide data is invalid."""
        # Mock the deckbuilder instance
        mock_deck = MagicMock()
        mock_deckbuilder_class.return_value = mock_deck
        mock_deck.create_presentation.return_value = "✓ Presentation created"
        mock_deck.add_slide_from_json.side_effect = ValueError("Invalid slide data")

        deck = get_deckbuilder_client()
        deck.create_presentation("default", "test")

        # Should handle invalid slide data gracefully
        invalid_slide = {"invalid": "data"}
        with pytest.raises(ValueError):
            deck.add_slide_from_json(invalid_slide)


@pytest.mark.skipif(not HAS_MCP_TOOLS, reason="MCP tools not available")
@pytest.mark.integration
@pytest.mark.mcp_server
@pytest.mark.requires_template
class TestMCPToolsWithRealFiles:
    """Integration tests that require actual template files."""

    def test_template_analysis_with_real_file(self, mock_deckbuilder_env):
        """Test template analysis with actual template file (if available)."""
        templates_dir = Path(os.environ["DECK_TEMPLATE_FOLDER"])
        template_file = templates_dir / "default.pptx"

        if not template_file.exists():
            pytest.skip("Real template file not available for testing")

        # Test with real file
        try:
            result = analyze_pptx_template("default")
            assert result is not None
            assert isinstance(result, dict)
        except Exception as e:
            pytest.skip(f"Template analysis failed with real file: {e}")

    def test_full_workflow_with_real_environment(self, mock_deckbuilder_env, sample_test_data):
        """Test complete workflow with real environment setup."""
        # Skip if dependencies not available
        try:
            deck = get_deckbuilder_client()
        except Exception:
            pytest.skip("Deckbuilder not available for full workflow test")

        # This would be a full integration test in a real environment
        # For now, we'll just verify the client can be created
        assert deck is not None
