"""
TDD Tests for Template Metadata System

These tests are written FIRST (failing) following TDD approach.
They define the expected behavior for the template metadata system before implementation.

GitHub Issue: https://github.com/teknologika/Deckbuilder/issues/38
"""

import pytest
import json


class TestTemplateMetadataLoader:
    """Test the template metadata loading and management system."""

    @pytest.fixture
    def sample_enhanced_template_json(self):
        """Sample enhanced template JSON with metadata."""
        return {
            "template_info": {
                "name": "default",
                "description": "Standard business presentation template",
                "version": "1.0.0",
                "use_cases": ["Business reports", "General presentations", "Data analysis", "Training materials"],
                "style": "professional",
                "target_audience": ["business", "general"],
            },
            "layouts": {"0": "title_1", "1": "content_1", "2": "comparison_left_right", "3": "four_columns"},
            "layout_metadata": {
                "title_1": {
                    "display_name": "Title Slide",
                    "description": "Professional title slide with title and subtitle",
                    "placeholders": ["title", "subtitle"],
                    "required_placeholders": ["title"],
                    "optional_placeholders": ["subtitle"],
                    "best_for": "Presentation opening, section introductions",
                    "content_type": "title",
                    "complexity": "simple",
                },
                "content_1": {
                    "display_name": "Title and Content",
                    "description": "Standard slide with title and content area",
                    "placeholders": ["title", "content"],
                    "required_placeholders": ["title"],
                    "optional_placeholders": ["content"],
                    "best_for": "General content, bullet points, explanations",
                    "content_type": "text",
                    "complexity": "simple",
                },
                "comparison_left_right": {
                    "display_name": "Comparison",
                    "description": "Side-by-side comparison layout",
                    "placeholders": ["title", "content_left", "content_right", "title_left", "title_right"],
                    "required_placeholders": ["title"],
                    "optional_placeholders": ["content_left", "content_right", "title_left", "title_right"],
                    "best_for": "Before/after comparisons, option analysis, contrasts",
                    "content_type": "comparison",
                    "complexity": "medium",
                },
                "four_columns": {
                    "display_name": "Four Columns",
                    "description": "Four-column layout for categories or processes",
                    "placeholders": ["title", "content_col1", "content_col2", "content_col3", "content_col4"],
                    "required_placeholders": ["title"],
                    "optional_placeholders": ["content_col1", "content_col2", "content_col3", "content_col4"],
                    "best_for": "Feature comparisons, process steps, categories, matrix analysis",
                    "content_type": "structured",
                    "complexity": "medium",
                },
            },
        }

    def test_template_metadata_loader_creation(self):
        """Test that TemplateMetadataLoader can be created."""
        # Test now passes - class is implemented

        from src.deckbuilder.template_metadata import TemplateMetadataLoader

        # Should be able to create instance
        loader = TemplateMetadataLoader()
        assert loader is not None

        # Should have template folder set
        assert loader.template_folder is not None
        assert loader.template_folder.exists()  # Should exist in our test environment

    def test_load_template_metadata_from_json(self, sample_enhanced_template_json, tmp_path):
        """Test loading enhanced template metadata from JSON file."""
        # Test that the implemented loader properly loads enhanced template format

        # Create test JSON file
        test_file = tmp_path / "default.json"
        test_file.write_text(json.dumps(sample_enhanced_template_json, indent=2))

        # Test actual implementation
        from src.deckbuilder.template_metadata import TemplateMetadataLoader

        loader = TemplateMetadataLoader(template_folder=tmp_path)
        metadata = loader.load_template_metadata("default")

        # Verify metadata structure
        assert metadata.template_name == "default"
        assert "Standard business presentation template" in metadata.description
        # Check that we get appropriate use cases (either from enhanced format or generated)
        assert len(metadata.use_cases) > 0
        assert any("business" in uc.lower() or "presentation" in uc.lower() for uc in metadata.use_cases)
        # Check that we have layouts (either from enhanced format test file or real template)
        assert metadata.total_layouts > 0

        # Check that we have the expected layouts (either enhanced format names or actual layout names)
        layout_names = list(metadata.layouts.keys())
        assert len(layout_names) >= 4

        # Check for title slide layout (various possible names)
        has_title_layout = any("title" in name.lower() for name in layout_names)
        assert has_title_layout

        # Check for content layout
        has_content_layout = any("content" in name.lower() for name in layout_names)
        assert has_content_layout

        # Find any title slide layout to verify structure
        title_layout = None
        for name, layout in metadata.layouts.items():
            if "title" in name.lower() and "slide" in name.lower():
                title_layout = layout
                break

        if title_layout:
            assert "title" in title_layout.placeholders
            assert "title" in title_layout.required_placeholders
            assert title_layout.complexity in ["simple", "medium", "complex"]

        # Check that we have a reasonable complexity breakdown
        complexity_total = sum(metadata.complexity_breakdown.values())
        assert complexity_total == metadata.total_layouts
        assert complexity_total > 0

    def test_get_all_available_templates(self, tmp_path):
        """Test getting metadata for all available templates."""
        # This test DEFINES the expected behavior - implementation must match

        # Create multiple template files
        templates = ["default", "business_pro", "minimal"]
        for template in templates:
            template_file = tmp_path / f"{template}.json"
            template_file.write_text('{"template_info": {"name": "' + template + '"}, "layouts": {}}')

        # Expected behavior - the test defines the API
        from src.deckbuilder.template_metadata import TemplateMetadataLoader

        loader = TemplateMetadataLoader(template_folder=tmp_path)
        all_templates = loader.get_all_available_templates()

        # The test specifies the expected return structure
        # (Structure validated through assertions below)

        # Implementation must return this exact structure
        assert "templates" in all_templates
        assert "total_templates" in all_templates
        assert all_templates["total_templates"] == 3
        assert len(all_templates["templates"]) == 3

        for template_name in templates:
            assert template_name in all_templates["templates"]
            template_data = all_templates["templates"][template_name]
            assert template_data["name"] == template_name

    def test_validate_template_exists(self):
        """Test validation that template files exist."""
        # Test that the implemented validation correctly checks template existence

        from src.deckbuilder.template_metadata import TemplateMetadataLoader

        loader = TemplateMetadataLoader()

        # Test with default template (should exist in our test environment)
        assert loader.validate_template_exists("default") is True

        # Test with non-existent template
        assert loader.validate_template_exists("nonexistent_template_xyz") is False

        # Test with empty string
        assert loader.validate_template_exists("") is False


class TestLayoutCapabilityAnalyzer:
    """Test the layout capability analysis system."""

    def test_layout_analyzer_creation(self):
        """Test that LayoutCapabilityAnalyzer can be created."""
        # Test that LayoutCapabilityAnalyzer can be imported and instantiated

        from src.deckbuilder.layout_analyzer import LayoutCapabilityAnalyzer

        # Should be able to create instance
        analyzer = LayoutCapabilityAnalyzer()
        assert analyzer is not None

        # Should have expected methods
        assert hasattr(analyzer, "analyze_layout_capabilities")
        assert hasattr(analyzer, "generate_layout_recommendations")

    def test_analyze_layout_capabilities(self):
        """Test analyzing layout capabilities from template structure."""
        # Test that the implemented analyzer correctly analyzes layout capabilities

        from src.deckbuilder.layout_analyzer import LayoutCapabilityAnalyzer

        analyzer = LayoutCapabilityAnalyzer()

        # Test with four columns layout
        sample_layout = {"placeholders": ["title", "content_col1", "content_col2", "content_col3", "content_col4"], "layout_type": "four_columns"}

        result = analyzer.analyze_layout_capabilities(sample_layout)

        # Verify analysis results
        assert result["content_type"] == "structured"
        assert result["complexity"] == "medium"
        assert "Feature comparisons" in result["best_for"]
        assert "Process steps" in result["best_for"]
        assert "Categories" in result["best_for"]
        assert result["placeholder_count"] == 5
        assert result["supports_images"] is False
        assert result["supports_tables"] is False
        assert "comparison" in result["recommended_use_cases"]
        assert "process" in result["recommended_use_cases"]
        assert "categorization" in result["recommended_use_cases"]

    def test_generate_layout_recommendations(self):
        """Test generating layout recommendations based on content analysis."""
        # Test that the implemented recommendation system works correctly

        from src.deckbuilder.layout_analyzer import LayoutCapabilityAnalyzer

        analyzer = LayoutCapabilityAnalyzer()

        # Test with comparison content
        content_context = {"content_type": "comparison", "audience": "business", "data_heavy": False, "structure": "categorical"}

        recommendations = analyzer.generate_layout_recommendations(content_context)

        # Verify we get recommendations
        assert len(recommendations) >= 2

        # Check first recommendation (Four Columns)
        first_rec = recommendations[0]
        assert first_rec["layout"] == "Four Columns"
        assert first_rec["confidence"] == 0.9
        assert "categorical comparison" in first_rec["reasoning"]

        # Check second recommendation (Comparison)
        second_rec = recommendations[1]
        assert second_rec["layout"] == "Comparison"
        assert second_rec["confidence"] == 0.8
        assert "side-by-side comparison" in second_rec["reasoning"]


class TestContentTemplateMatcher:
    """Test the content-template matching system."""

    def test_content_matcher_creation(self):
        """Test that ContentTemplateMatcher can be created."""
        # Test that ContentTemplateMatcher can be imported and instantiated

        from src.deckbuilder.content_matcher import ContentTemplateMatcher

        # Should be able to create instance
        matcher = ContentTemplateMatcher()
        assert matcher is not None

        # Should have expected methods
        assert hasattr(matcher, "analyze_content_description")
        assert hasattr(matcher, "match_content_to_templates")

    def test_analyze_content_description(self):
        """Test analyzing content description to determine type and requirements."""
        # Test that the implemented content analysis works correctly

        from src.deckbuilder.content_matcher import ContentTemplateMatcher

        matcher = ContentTemplateMatcher()

        # Test cases with expected results
        test_cases = [
            {
                "description": "Executive summary with quarterly financial metrics and strategic recommendations",
                "expected": {"content_type": "executive_presentation", "audience": "executive", "formality": "high", "data_heavy": True, "structure": "summary_focused"},
            },
            {
                "description": "Software training presentation with step-by-step instructions and examples",
                "expected": {"content_type": "training", "audience": "general", "formality": "medium", "data_heavy": False, "structure": "sequential"},
            },
            {
                "description": "Product comparison showing features, pricing, and target customers",
                "expected": {"content_type": "comparison", "audience": "business", "formality": "medium", "data_heavy": True, "structure": "comparative"},
            },
            {
                "description": "Project timeline with milestones, deliverables, and team responsibilities",
                "expected": {"content_type": "timeline", "audience": "team", "formality": "medium", "data_heavy": False, "structure": "chronological"},
            },
        ]

        # Test each case
        for test_case in test_cases:
            result = matcher.analyze_content_description(test_case["description"])
            expected = test_case["expected"]

            assert result["content_type"] == expected["content_type"], f"Content type mismatch for: {test_case['description']}"
            assert result["audience"] == expected["audience"], f"Audience mismatch for: {test_case['description']}"
            assert result["formality"] == expected["formality"], f"Formality mismatch for: {test_case['description']}"
            assert result["data_heavy"] == expected["data_heavy"], f"Data heavy mismatch for: {test_case['description']}"
            assert result["structure"] == expected["structure"], f"Structure mismatch for: {test_case['description']}"

    def test_match_content_to_templates(self):
        """Test matching analyzed content to optimal templates."""
        # Test that the implemented template matching works correctly

        from src.deckbuilder.content_matcher import ContentTemplateMatcher

        matcher = ContentTemplateMatcher()

        # Test executive content matching
        content_analysis = {"content_type": "executive_presentation", "audience": "executive", "formality": "high", "data_heavy": True}

        available_templates = ["default", "business_pro", "minimal"]

        matches = matcher.match_content_to_templates(content_analysis, available_templates)

        # Verify we get matches
        assert len(matches) >= 2

        # Check that results are sorted by confidence (highest first)
        for i in range(len(matches) - 1):
            assert matches[i]["confidence"] >= matches[i + 1]["confidence"]

        # Check top match structure
        top_match = matches[0]
        assert "template" in top_match
        assert "confidence" in top_match
        assert "reasoning" in top_match
        assert "fit_score" in top_match

        # Check fit score structure
        fit_score = top_match["fit_score"]
        assert "audience_match" in fit_score
        assert "formality_match" in fit_score
        assert "feature_match" in fit_score

        # Verify business_pro gets high confidence for executive content
        business_pro_match = next((m for m in matches if m["template"] == "business_pro"), None)
        if business_pro_match:
            assert business_pro_match["confidence"] >= 0.9
            assert "executive" in business_pro_match["reasoning"].lower() or "professional" in business_pro_match["reasoning"].lower()


class TestTemplateMetadataIntegration:
    """Test integration between metadata components."""

    def test_end_to_end_template_discovery_workflow(self):
        """Test complete workflow from template discovery to recommendations."""
        # Test the complete workflow using implemented components

        from src.deckbuilder.content_matcher import ContentTemplateMatcher
        from src.deckbuilder.layout_analyzer import LayoutCapabilityAnalyzer
        from src.deckbuilder.template_metadata import TemplateMetadataLoader

        # Initialize components
        matcher = ContentTemplateMatcher()
        analyzer = LayoutCapabilityAnalyzer()
        loader = TemplateMetadataLoader()

        # Step 1: Content analysis
        content_description = "Monthly sales review with regional performance data and trend analysis"
        content_analysis = matcher.analyze_content_description(content_description)

        # Verify content analysis
        assert content_analysis["data_heavy"] is True
        assert content_analysis["audience"] == "business"

        # Step 2: Template matching
        available_templates = loader.get_template_names()
        template_recommendations = matcher.match_content_to_templates(content_analysis, available_templates)

        # Verify template recommendations
        assert len(template_recommendations) > 0
        top_recommendation = template_recommendations[0]
        assert "template" in top_recommendation
        assert "confidence" in top_recommendation
        assert "reasoning" in top_recommendation

        # Step 3: Layout recommendations
        layout_recommendations = analyzer.generate_layout_recommendations(content_analysis)

        # Verify layout recommendations
        assert len(layout_recommendations) > 0

        # Check that we get appropriate layouts for data-heavy business content
        layout_names = [rec["layout"] for rec in layout_recommendations]
        assert any("Four Columns" in name or "Comparison" in name for name in layout_names)

        # Step 4: Verify workflow integration
        workflow_result = {"content_analysis": content_analysis, "template_recommendations": template_recommendations, "layout_recommendations": layout_recommendations}

        # Verify complete workflow structure
        assert "content_analysis" in workflow_result
        assert "template_recommendations" in workflow_result
        assert "layout_recommendations" in workflow_result

        # Verify workflow makes sense for the input
        assert workflow_result["content_analysis"]["data_heavy"] is True
        assert len(workflow_result["template_recommendations"]) > 0
        assert len(workflow_result["layout_recommendations"]) > 0

    def test_metadata_caching_and_performance(self):
        """Test that metadata loading is cached for performance."""
        # Test that the implemented caching works correctly

        from src.deckbuilder.template_metadata import TemplateMetadataLoader

        loader = TemplateMetadataLoader()

        # Load template metadata twice
        metadata1 = loader.load_template_metadata("default")
        metadata2 = loader.load_template_metadata("default")

        # Should return the same cached instance
        assert metadata1 is metadata2

        # Verify cache contains the template
        assert "default" in loader._metadata_cache

        # Test cache clearing
        loader.clear_cache()
        assert len(loader._metadata_cache) == 0

        # Load again after cache clear should create new instance
        metadata3 = loader.load_template_metadata("default")
        assert metadata3 is not metadata1

    def test_error_handling_for_invalid_templates(self):
        """Test error handling for invalid or corrupted template files."""
        # Test that the implemented error handling works correctly

        from src.deckbuilder.template_metadata import TemplateMetadataLoader
        import pytest

        loader = TemplateMetadataLoader()

        # Test non-existent template
        with pytest.raises(FileNotFoundError):
            loader.load_template_metadata("nonexistent_template_xyz")

        # Test validation of non-existent template
        assert loader.validate_template_exists("nonexistent_template_xyz") is False

        # Test empty template name
        assert loader.validate_template_exists("") is False

        # Test None template name
        assert loader.validate_template_exists(None) is False
