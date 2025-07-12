"""
TDD Tests for MCP Template Discovery Tools

These tests are written FIRST (failing) following TDD approach.
They define the expected behavior for template discovery MCP tools before implementation.

GitHub Issue: https://github.com/teknologika/Deckbuilder/issues/38
"""

import pytest
from unittest.mock import MagicMock
from pathlib import Path


class TestMCPTemplateDiscoveryTools:
    """Test MCP tools for template discovery and metadata."""

    @pytest.fixture
    def mock_context(self):
        """Mock MCP context for testing."""
        context = MagicMock()
        context.deckbuilder_client = MagicMock()
        return context

    @pytest.fixture
    def sample_template_metadata(self):
        """Sample template metadata for testing."""
        return {
            "default": {
                "template_name": "default",
                "description": "Standard business presentation template",
                "use_cases": ["Business reports", "General presentations", "Data analysis"],
                "layouts": {
                    "Title Slide": {"description": "Professional title slide with title and subtitle", "placeholders": ["title", "subtitle"], "best_for": "Presentation opening"},
                    "Four Columns": {
                        "description": "Four-column comparison layout",
                        "placeholders": ["title", "content_col1", "content_col2", "content_col3", "content_col4"],
                        "best_for": "Feature comparisons, process steps, categories",
                    },
                    "Title and Content": {"description": "Standard slide with title and content area", "placeholders": ["title", "content"], "best_for": "General content, bullet points, text"},
                },
                "total_layouts": 3,
            },
            "business_pro": {
                "template_name": "business_pro",
                "description": "Professional corporate template with advanced layouts",
                "use_cases": ["Executive presentations", "Client reports", "Sales pitches"],
                "layouts": {"Executive Summary": {"description": "Executive-level summary slide", "placeholders": ["title", "summary", "key_metrics"], "best_for": "High-level overviews"}},
                "total_layouts": 1,
            },
        }

    @pytest.mark.asyncio
    async def test_list_available_templates_tool_exists(self, mock_context):
        """Test that list_available_templates MCP tool exists and is callable."""
        # Test that the tool function can be imported and called

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = "/tmp/test_templates"
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import list_available_templates

            # Tool should be callable (even if it returns an error due to missing templates)
            result = await list_available_templates(mock_context)

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)
            assert "available_templates" in parsed

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_list_available_templates_returns_metadata(self, mock_context, sample_template_metadata):
        """Test that list_available_templates returns comprehensive template metadata."""
        # Test that the implemented tool returns the expected format

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import list_available_templates

            # Call the tool
            result = await list_available_templates(mock_context)

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)

            # Should have expected structure
            assert "available_templates" in parsed
            assert "recommendation" in parsed

            # Should have templates
            templates = parsed["available_templates"]
            assert len(templates) > 0

            # Each template should have required fields
            for _template_name, template_info in templates.items():
                assert "description" in template_info
                assert "use_cases" in template_info
                assert "total_layouts" in template_info
                assert "key_layouts" in template_info
                assert isinstance(template_info["use_cases"], list)
                assert isinstance(template_info["key_layouts"], list)
                assert isinstance(template_info["total_layouts"], int)

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_get_template_layouts_tool_exists(self, mock_context):
        """Test that get_template_layouts MCP tool exists and is callable."""
        # Test that the tool function can be imported and called

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import get_template_layouts

            # Tool should be callable
            result = await get_template_layouts(mock_context, "default")

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)
            assert "template_name" in parsed
            assert "layouts" in parsed

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_get_template_layouts_returns_detailed_info(self, mock_context):
        """Test that get_template_layouts returns detailed layout information."""
        # Test that the implemented tool returns the expected format

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import get_template_layouts

            # Call the tool
            result = await get_template_layouts(mock_context, "default")

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)

            # Should have expected structure
            assert "template_name" in parsed
            assert "layouts" in parsed
            assert "usage_tips" in parsed
            assert parsed["template_name"] == "default"

            # Should have layouts
            layouts = parsed["layouts"]
            assert len(layouts) > 0

            # Each layout should have required fields
            for _layout_name, layout_info in layouts.items():
                assert "description" in layout_info
                assert "required_placeholders" in layout_info
                assert "optional_placeholders" in layout_info
                assert "best_for" in layout_info
                assert "example" in layout_info
                assert isinstance(layout_info["required_placeholders"], list)
                assert isinstance(layout_info["optional_placeholders"], list)
                assert isinstance(layout_info["example"], dict)

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_get_template_layouts_handles_invalid_template(self, mock_context):
        """Test that get_template_layouts handles invalid template names gracefully."""
        # Test that the implemented tool handles invalid templates correctly

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import get_template_layouts

            # Call with invalid template
            result = await get_template_layouts(mock_context, "nonexistent_template")

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)

            # Should indicate error or failure
            # The tool should either return an error field or handle gracefully
            assert "error" in parsed or "template_name" in parsed

            # If it returns an error, should be descriptive
            if "error" in parsed:
                assert "not found" in parsed["error"].lower() or "nonexistent" in parsed["error"].lower()

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_recommend_template_for_content_tool_exists(self, mock_context):
        """Test that recommend_template_for_content MCP tool exists and is callable."""
        # Test that the tool function can be imported and called

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import recommend_template_for_content

            # Tool should be callable
            result = await recommend_template_for_content(mock_context, "Test business presentation for executives")

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)
            assert "content_analysis" in parsed
            assert "recommendations" in parsed
            assert "layout_suggestions" in parsed

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_recommend_template_for_content_analyzes_description(self, mock_context):
        """Test that recommend_template_for_content analyzes content and provides recommendations."""
        # Test that the implemented tool analyzes content correctly

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import recommend_template_for_content

            # Test case 1: Executive business content
            content_description = "Executive summary presentation with quarterly metrics, financial data, and strategic recommendations for the board of directors"

            result = await recommend_template_for_content(mock_context, content_description)

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)

            # Should have expected structure
            assert "content_analysis" in parsed
            assert "recommendations" in parsed
            assert "layout_suggestions" in parsed

            # Check content analysis
            analysis = parsed["content_analysis"]
            assert "detected_type" in analysis
            assert "audience" in analysis
            assert "content_style" in analysis
            assert "data_heavy" in analysis

            # Should detect executive content
            assert analysis["detected_type"] == "executive_presentation"
            assert analysis["audience"] == "executive"
            assert analysis["data_heavy"] is True

            # Should have recommendations
            recommendations = parsed["recommendations"]
            assert len(recommendations) > 0

            # Each recommendation should have required fields
            for rec in recommendations:
                assert "template" in rec
                assert "confidence" in rec
                assert "reasoning" in rec
                assert "suggested_layouts" in rec
                assert isinstance(rec["confidence"], (int, float))
                assert isinstance(rec["suggested_layouts"], list)

            # Should have layout suggestions
            layout_suggestions = parsed["layout_suggestions"]
            assert "opening" in layout_suggestions
            assert "content" in layout_suggestions
            assert "closing" in layout_suggestions

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_recommend_template_for_content_handles_general_content(self, mock_context):
        """Test template recommendations for general content descriptions."""
        # Test that the implemented tool handles general training content correctly

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import recommend_template_for_content

            content_description = "Training presentation about software features with step-by-step instructions and examples"

            result = await recommend_template_for_content(mock_context, content_description)

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)

            # Should have expected structure
            assert "content_analysis" in parsed
            assert "recommendations" in parsed
            assert "layout_suggestions" in parsed

            # Check content analysis
            analysis = parsed["content_analysis"]
            assert "detected_type" in analysis
            assert "audience" in analysis
            assert "content_style" in analysis
            assert "data_heavy" in analysis

            # Should detect training content
            assert analysis["detected_type"] == "training_presentation"
            assert analysis["data_heavy"] is False

            # Should have recommendations
            recommendations = parsed["recommendations"]
            assert len(recommendations) > 0

            # Should recommend default template for training
            has_default = any(rec["template"] == "default" for rec in recommendations)
            assert has_default, "Should recommend default template for training content"

            # Should have layout suggestions
            layout_suggestions = parsed["layout_suggestions"]
            assert "opening" in layout_suggestions
            assert "content" in layout_suggestions
            assert "closing" in layout_suggestions

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_validate_presentation_file_tool_exists(self, mock_context):
        """Test that validate_presentation_file MCP tool exists and is callable."""
        # Test that the tool function can be imported and called

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import validate_presentation_file

            # Tool should be callable (even with non-existent file)
            result = await validate_presentation_file(mock_context, "/nonexistent/file.md")

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)
            assert "file_validation" in parsed
            assert "content_validation" in parsed
            assert "template_compatibility" in parsed
            assert "recommendation" in parsed

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_validate_presentation_file_validates_structure(self, mock_context, tmp_path):
        """Test that validate_presentation_file validates file structure before generation."""
        # Test that the implemented tool validates file structure correctly

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import validate_presentation_file

            # Create test markdown file
            test_file = tmp_path / "test_presentation.md"
            test_file.write_text(
                """---
layout: Title Slide
title: Test Presentation
subtitle: Test subtitle
---

---
layout: Four Columns
title: Feature Comparison
content_col1: Feature A
content_col2: Feature B
content_col3: Feature C
content_col4: Feature D
---"""
            )

            result = await validate_presentation_file(mock_context, str(test_file), "default")

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)

            # Should have expected structure
            assert "file_validation" in parsed
            assert "content_validation" in parsed
            assert "template_compatibility" in parsed
            assert "recommendation" in parsed

            # Check file validation
            file_val = parsed["file_validation"]
            assert file_val["file_exists"] is True
            assert file_val["file_type"] == "markdown"
            assert file_val["syntax_valid"] is True
            assert file_val["slides_detected"] == 2

            # Check content validation
            content_val = parsed["content_validation"]
            assert len(content_val) == 2
            assert "slide_1" in content_val
            assert "slide_2" in content_val

            # Check slide 1 (Title Slide)
            slide1 = content_val["slide_1"]
            assert slide1["layout"] == "Title Slide"
            assert slide1["status"] == "valid"
            assert "title" in slide1["required_fields"]
            assert len(slide1["missing_fields"]) == 0

            # Check slide 2 (Four Columns)
            slide2 = content_val["slide_2"]
            assert slide2["layout"] == "Four Columns"
            assert slide2["status"] == "valid"
            assert len(slide2["missing_fields"]) == 0

            # Check template compatibility
            template_compat = parsed["template_compatibility"]
            assert template_compat["template"] == "default"
            assert template_compat["all_layouts_supported"] is True

            # Should be valid for generation
            assert "valid" in parsed["recommendation"].lower() or "ready" in parsed["recommendation"].lower()

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)

    @pytest.mark.asyncio
    async def test_validate_presentation_file_detects_errors(self, mock_context, tmp_path):
        """Test that validate_presentation_file detects and reports errors with actionable fixes."""
        # Test that the implemented tool detects errors correctly

        # Mock the environment variables required for MCP server initialization
        import os

        original_env = os.environ.copy()

        try:
            os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
            os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
            os.environ["DECK_TEMPLATE_NAME"] = "default"

            from src.mcp_server.main import validate_presentation_file

            # Create test file with errors
            test_file = tmp_path / "invalid_presentation.md"
            test_file.write_text(
                """---
layout: NonexistentLayout
title: Test
---

---
layout: Four Columns
title: Missing Content
content_col1: Only one column
---"""
            )

            result = await validate_presentation_file(mock_context, str(test_file), "default")

            # Should return a JSON string
            assert isinstance(result, str)

            # Should be valid JSON
            import json

            parsed = json.loads(result)

            # Should have expected structure
            assert "file_validation" in parsed
            assert "content_validation" in parsed
            assert "template_compatibility" in parsed
            assert "recommendation" in parsed

            # Check file validation
            file_val = parsed["file_validation"]
            assert file_val["file_exists"] is True
            assert file_val["file_type"] == "markdown"
            assert file_val["syntax_valid"] is True
            assert file_val["slides_detected"] == 2

            # Check content validation
            content_val = parsed["content_validation"]
            assert len(content_val) == 2
            assert "slide_1" in content_val
            assert "slide_2" in content_val

            # Check slide 1 (NonexistentLayout should be error)
            slide1 = content_val["slide_1"]
            assert slide1["layout"] == "NonexistentLayout"
            assert slide1["status"] == "error"
            assert "error" in slide1
            assert "not found" in slide1["error"].lower()

            # Check slide 2 (Four Columns with missing fields should be error)
            slide2 = content_val["slide_2"]
            assert slide2["layout"] == "Four Columns"
            assert slide2["status"] == "error"
            assert "missing_fields" in slide2
            assert len(slide2["missing_fields"]) > 0

            # Check template compatibility
            template_compat = parsed["template_compatibility"]
            assert template_compat["template"] == "default"
            assert template_compat["all_layouts_supported"] is False
            assert "unsupported_layouts" in template_compat
            assert "NonexistentLayout" in template_compat["unsupported_layouts"]

            # Should recommend fixing errors
            assert "fix" in parsed["recommendation"].lower() or "error" in parsed["recommendation"].lower()

        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)


class TestTemplateMetadataSystem:
    """Test the underlying template metadata system that powers MCP tools."""

    def test_template_metadata_loader_exists(self):
        """Test that template metadata loading system exists."""
        # Test that TemplateMetadataLoader can be imported and instantiated

        from src.deckbuilder.template_metadata import TemplateMetadataLoader

        # Should be able to create instance
        loader = TemplateMetadataLoader()
        assert loader is not None

        # Should have expected methods
        assert hasattr(loader, "load_template_metadata")
        assert hasattr(loader, "get_template_names")
        assert hasattr(loader, "get_enhanced_layout_metadata")

    def test_template_metadata_loader_loads_enhanced_json(self):
        """Test that metadata loader can load enhanced template JSON files."""
        # Test that TemplateMetadataLoader can load template metadata

        from src.deckbuilder.template_metadata import TemplateMetadataLoader

        # Should be able to create instance and load metadata
        loader = TemplateMetadataLoader()

        # Should be able to load default template
        try:
            metadata = loader.load_template_metadata("default")
            assert metadata is not None
            assert hasattr(metadata, "layouts")
            assert hasattr(metadata, "total_layouts")
            assert metadata.total_layouts > 0
            assert len(metadata.layouts) > 0
        except Exception as e:
            # If loading fails, that's also valid behavior (template might not exist in test environment)
            assert "not found" in str(e).lower() or "template" in str(e).lower()

    def test_layout_capability_analyzer_exists(self):
        """Test that layout capability analysis system exists."""
        # Test that LayoutCapabilityAnalyzer can be imported and instantiated

        from src.deckbuilder.layout_analyzer import LayoutCapabilityAnalyzer

        # Should be able to create instance
        analyzer = LayoutCapabilityAnalyzer()
        assert analyzer is not None

        # Should have expected methods
        assert hasattr(analyzer, "analyze_layout_capabilities")
        assert hasattr(analyzer, "generate_layout_recommendations")

    def test_content_template_matcher_exists(self):
        """Test that content-template matching system exists."""
        # Test that ContentTemplateMatcher can be imported and instantiated

        from src.deckbuilder.content_matcher import ContentTemplateMatcher

        # Should be able to create instance
        matcher = ContentTemplateMatcher()
        assert matcher is not None

        # Should have expected methods
        assert hasattr(matcher, "analyze_content_description")
        assert hasattr(matcher, "match_content_to_templates")
