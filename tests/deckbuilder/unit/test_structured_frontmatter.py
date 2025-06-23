"""
Unit tests for structured frontmatter system.
"""

import pytest
from unittest.mock import Mock, patch

# Test imports with graceful handling
try:
    from deckbuilder.structured_frontmatter import (
        StructuredFrontmatterRegistry,
        StructuredFrontmatterConverter,
        StructuredFrontmatterValidator,
    )

    HAS_STRUCTURED_FRONTMATTER = True
except ImportError:
    HAS_STRUCTURED_FRONTMATTER = False


@pytest.mark.skipif(not HAS_STRUCTURED_FRONTMATTER, reason="Structured frontmatter not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestStructuredFrontmatterRegistry:
    """Test cases for StructuredFrontmatterRegistry."""

    def test_initialization(self, default_template_json):
        """Test registry initialization."""
        registry = StructuredFrontmatterRegistry(default_template_json)
        assert registry.template_mapping == default_template_json

    def test_get_structure_patterns(self, structured_frontmatter_registry):
        """Test getting structure patterns."""
        patterns = structured_frontmatter_registry.get_structure_patterns()

        # Check expected layouts are present
        expected_layouts = [
            "Four Columns",
            "Four Columns With Titles",
            "Three Columns",
            "Three Columns With Titles",
            "Comparison",
            "Two Content",
            "Picture with Caption",
        ]

        for layout in expected_layouts:
            assert layout in patterns
            pattern = patterns[layout]
            assert "structure_type" in pattern
            assert "description" in pattern
            assert "yaml_pattern" in pattern
            assert "validation" in pattern
            assert "example" in pattern

    def test_get_structure_definition(self, structured_frontmatter_registry):
        """Test getting structure definition with mapping rules."""
        definition = structured_frontmatter_registry.get_structure_definition("Four Columns")

        assert "structure_type" in definition
        assert "mapping_rules" in definition
        assert "validation" in definition

        # Check that mapping rules are generated
        mapping_rules = definition["mapping_rules"]
        assert "title" in mapping_rules
        assert mapping_rules["title"] == "semantic:title"

    def test_supports_structured_frontmatter(self, structured_frontmatter_registry):
        """Test checking layout support."""
        # Should support known layouts
        assert structured_frontmatter_registry.supports_structured_frontmatter("Four Columns")
        assert structured_frontmatter_registry.supports_structured_frontmatter("Comparison")

        # Should not support unknown layouts
        assert not structured_frontmatter_registry.supports_structured_frontmatter("Unknown Layout")

    def test_get_supported_layouts(self, structured_frontmatter_registry):
        """Test getting list of supported layouts."""
        layouts = structured_frontmatter_registry.get_supported_layouts()

        assert isinstance(layouts, list)
        assert "Four Columns" in layouts
        assert "Comparison" in layouts
        assert len(layouts) > 0

    def test_get_example(self, structured_frontmatter_registry):
        """Test getting example frontmatter."""
        example = structured_frontmatter_registry.get_example("Four Columns")

        assert isinstance(example, str)
        assert "layout: Four Columns" in example
        assert "columns:" in example
        assert "---" in example  # YAML frontmatter markers

    def test_build_mapping_rules_four_columns(self, structured_frontmatter_registry):
        """Test building mapping rules for four columns layout."""
        mapping_rules = structured_frontmatter_registry._build_mapping_rules(
            "Four Columns With Titles"
        )

        assert "title" in mapping_rules
        assert mapping_rules["title"] == "semantic:title"

        # Check column mappings are generated
        for i in range(4):
            title_key = f"columns[{i}].title"
            content_key = f"columns[{i}].content"

            if title_key in mapping_rules:
                assert "title_col" in mapping_rules[title_key]
            if content_key in mapping_rules:
                assert "content_col" in mapping_rules[content_key]

    def test_build_mapping_rules_comparison(self, structured_frontmatter_registry):
        """Test building mapping rules for comparison layout."""
        mapping_rules = structured_frontmatter_registry._build_mapping_rules("Comparison")

        assert "title" in mapping_rules

        # Check left/right mappings
        expected_keys = [
            "comparison.left.title",
            "comparison.left.content",
            "comparison.right.title",
            "comparison.right.content",
        ]

        for key in expected_keys:
            if key in mapping_rules:
                if "left" in key:
                    assert "left" in mapping_rules[key]
                elif "right" in key:
                    assert "right" in mapping_rules[key]


@pytest.mark.skipif(not HAS_STRUCTURED_FRONTMATTER, reason="Structured frontmatter not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestStructuredFrontmatterConverter:
    """Test cases for StructuredFrontmatterConverter."""

    def test_initialization(self, default_template_json):
        """Test converter initialization."""
        converter = StructuredFrontmatterConverter(default_template_json)
        assert converter.layout_mapping == default_template_json
        assert converter.registry is not None

    def test_convert_four_columns_structured_to_placeholders(
        self, structured_frontmatter_converter, sample_structured_frontmatter
    ):
        """Test converting four columns structured frontmatter."""
        result = structured_frontmatter_converter.convert_structured_to_placeholders(
            sample_structured_frontmatter
        )

        assert "type" in result
        assert result["type"] == "Four Columns With Titles"

        # Check that title is converted
        assert "title" in result
        assert result["title"] == "Feature Comparison"

        # Check that columns are converted to placeholder names
        # Note: exact placeholder names depend on the mapping rules
        assert len([k for k in result.keys() if "col" in k]) > 0

    def test_convert_comparison_structured_to_placeholders(self, structured_frontmatter_converter):
        """Test converting comparison structured frontmatter."""
        comparison_data = {
            "layout": "Comparison",
            "title": "Solution Analysis",
            "comparison": {
                "left": {"title": "Current Solution", "content": "Proven reliability"},
                "right": {"title": "New Solution", "content": "Enhanced features"},
            },
        }

        result = structured_frontmatter_converter.convert_structured_to_placeholders(
            comparison_data
        )

        assert "type" in result
        assert result["type"] == "Comparison"
        assert "title" in result

        # Check left/right content is mapped
        left_keys = [k for k in result.keys() if "left" in k]
        right_keys = [k for k in result.keys() if "right" in k]

        assert len(left_keys) > 0
        assert len(right_keys) > 0

    def test_extract_value_by_path(self, structured_frontmatter_converter):
        """Test extracting values using dot notation paths."""
        data = {
            "comparison": {"left": {"title": "Left Title", "content": "Left Content"}},
            "columns": [
                {"title": "Col 1", "content": "Content 1"},
                {"title": "Col 2", "content": "Content 2"},
            ],
        }

        # Test nested object access
        assert (
            structured_frontmatter_converter._extract_value_by_path(data, "comparison.left.title")
            == "Left Title"
        )
        assert (
            structured_frontmatter_converter._extract_value_by_path(data, "comparison.left.content")
            == "Left Content"
        )

        # Test array access
        assert (
            structured_frontmatter_converter._extract_value_by_path(data, "columns[0].title")
            == "Col 1"
        )
        assert (
            structured_frontmatter_converter._extract_value_by_path(data, "columns[1].content")
            == "Content 2"
        )

        # Test non-existent paths
        assert (
            structured_frontmatter_converter._extract_value_by_path(data, "nonexistent.path")
            is None
        )
        assert (
            structured_frontmatter_converter._extract_value_by_path(data, "columns[5].title")
            is None
        )

    def test_parse_path_with_arrays(self, structured_frontmatter_converter):
        """Test parsing paths with array notation."""
        test_cases = [
            ("columns[0].title", ["columns", 0, "title"]),
            ("sections[1].content", ["sections", 1, "content"]),
            ("comparison.left.title", ["comparison", "left", "title"]),
            ("simple", ["simple"]),
            ("array[0]", ["array", 0]),
            ("nested[0].deep[1].value", ["nested", 0, "deep", 1, "value"]),
        ]

        for path, expected in test_cases:
            result = structured_frontmatter_converter._parse_path_with_arrays(path)
            assert result == expected, f"Failed for path: {path}"

    def test_convert_unsupported_layout(self, structured_frontmatter_converter):
        """Test conversion for unsupported layout."""
        unsupported_data = {"layout": "Unsupported Layout", "title": "Test Title"}

        result = structured_frontmatter_converter.convert_structured_to_placeholders(
            unsupported_data
        )

        # Should return original data if layout not supported
        assert result == unsupported_data

    def test_convert_missing_layout(self, structured_frontmatter_converter):
        """Test conversion when layout field is missing."""
        data_without_layout = {"title": "Test Title", "content": "Test Content"}

        result = structured_frontmatter_converter.convert_structured_to_placeholders(
            data_without_layout
        )

        # Should return original data if layout not specified
        assert result == data_without_layout


@pytest.mark.skipif(not HAS_STRUCTURED_FRONTMATTER, reason="Structured frontmatter not available")
@pytest.mark.unit
@pytest.mark.deckbuilder
class TestStructuredFrontmatterValidator:
    """Test cases for StructuredFrontmatterValidator."""

    def test_initialization(self):
        """Test validator initialization."""
        validator = StructuredFrontmatterValidator()
        assert validator.registry is not None

    def test_validate_four_columns_valid(
        self, structured_frontmatter_validator, sample_structured_frontmatter
    ):
        """Test validation of valid four columns frontmatter."""
        result = structured_frontmatter_validator.validate_structured_frontmatter(
            sample_structured_frontmatter, "Four Columns With Titles"
        )

        assert result["valid"] is True
        assert "errors" in result
        assert "warnings" in result
        assert len(result["errors"]) == 0

    def test_validate_four_columns_missing_required_field(self, structured_frontmatter_validator):
        """Test validation with missing required fields."""
        invalid_data = {
            "layout": "Four Columns With Titles"
            # Missing title and columns
        }

        result = structured_frontmatter_validator.validate_structured_frontmatter(
            invalid_data, "Four Columns With Titles"
        )

        assert result["valid"] is False
        assert len(result["errors"]) > 0

        # Check for specific required field errors
        error_messages = " ".join(result["errors"])
        assert "title" in error_messages or "columns" in error_messages

    def test_validate_four_columns_too_many_columns(self, structured_frontmatter_validator):
        """Test validation with too many columns."""
        data_with_too_many_columns = {
            "layout": "Four Columns With Titles",
            "title": "Test Title",
            "columns": [
                {"title": "Col 1", "content": "Content 1"},
                {"title": "Col 2", "content": "Content 2"},
                {"title": "Col 3", "content": "Content 3"},
                {"title": "Col 4", "content": "Content 4"},
                {"title": "Col 5", "content": "Content 5"},  # Too many
                {"title": "Col 6", "content": "Content 6"},  # Too many
            ],
        }

        result = structured_frontmatter_validator.validate_structured_frontmatter(
            data_with_too_many_columns, "Four Columns With Titles"
        )

        # Should have warnings about too many columns
        assert len(result["warnings"]) > 0
        warning_messages = " ".join(result["warnings"])
        assert "columns" in warning_messages

    def test_validate_comparison_valid(self, structured_frontmatter_validator):
        """Test validation of valid comparison frontmatter."""
        comparison_data = {
            "layout": "Comparison",
            "title": "Solution Analysis",
            "comparison": {
                "left": {"title": "Current", "content": "Current solution"},
                "right": {"title": "Proposed", "content": "Proposed solution"},
            },
        }

        result = structured_frontmatter_validator.validate_structured_frontmatter(
            comparison_data, "Comparison"
        )

        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_comparison_missing_side(self, structured_frontmatter_validator):
        """Test validation of comparison missing a side."""
        incomplete_comparison = {
            "layout": "Comparison",
            "title": "Incomplete Comparison",
            "comparison": {
                "left": {"title": "Left Side", "content": "Left content"}
                # Missing right side
            },
        }

        result = structured_frontmatter_validator.validate_structured_frontmatter(
            incomplete_comparison, "Comparison"
        )

        assert result["valid"] is False
        assert len(result["errors"]) > 0

        error_messages = " ".join(result["errors"])
        assert "right" in error_messages

    def test_validate_unsupported_layout(self, structured_frontmatter_validator):
        """Test validation of unsupported layout."""
        result = structured_frontmatter_validator.validate_structured_frontmatter(
            {"layout": "Unsupported"}, "Unsupported Layout"
        )

        assert result["valid"] is True  # Should pass with warning
        assert len(result["warnings"]) > 0

        warning_messages = " ".join(result["warnings"])
        assert "validation rules" in warning_messages or "available" in warning_messages

    def test_validate_column_structure(self, structured_frontmatter_validator):
        """Test validation of column structure details."""
        invalid_column_structure = {
            "layout": "Four Columns With Titles",
            "title": "Test Title",
            "columns": [
                {"title": "Valid Column", "content": "Valid content"},
                "Invalid column structure",  # Should be object
                {"title": "Missing content"},  # Missing content field
                {"content": "Missing title"},  # Missing title field
            ],
        }

        result = structured_frontmatter_validator.validate_structured_frontmatter(
            invalid_column_structure, "Four Columns With Titles"
        )

        # Should have errors and/or warnings about column structure
        assert len(result["errors"]) > 0 or len(result["warnings"]) > 0
