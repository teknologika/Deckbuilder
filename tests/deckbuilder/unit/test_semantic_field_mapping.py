#!/usr/bin/env python3
"""
Test Semantic Field Mapping (CORRECT Expected Behavior)

Tests the EXPECTED template mapping behavior for Issue #31:
- Semantic field names in template JSON
- Proper placeholder mapping
- Consistent naming conventions

These tests SHOULD FAIL initially, then pass after template updates.
"""

import json
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))


class TestSemanticFieldMapping:
    """Test CORRECT semantic field mapping in templates"""

    def setup_method(self):
        """Setup for each test"""
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.template_path = self.project_root / "src" / "deckbuilder" / "assets" / "templates" / "default.json"

    def test_template_has_semantic_two_content_fields(self):
        """Test that Two Content layout has semantic field names"""

        with open(self.template_path, "r") as f:
            template_data = json.load(f)

        two_content_layout = template_data["layouts"]["Two Content"]
        placeholders = two_content_layout["placeholders"]

        print("\nTWO CONTENT PLACEHOLDERS:")
        for idx, name in placeholders.items():
            print(f"  {idx}: {name}")

        # EXPECTED: Semantic field names (not _1 suffix)
        expected_fields = {"content_left": False, "content_right": False}

        for placeholder_name in placeholders.values():
            if placeholder_name == "content_left":
                expected_fields["content_left"] = True
            elif placeholder_name == "content_right":
                expected_fields["content_right"] = True

        print("Expected semantic fields found:")
        for field, found in expected_fields.items():
            print(f"  {field}: {'✅' if found else '❌'}")

        # These SHOULD pass after template update
        assert expected_fields["content_left"], "Missing semantic field: content_left"
        assert expected_fields["content_right"], "Missing semantic field: content_right"

        # Should NOT have confusing _1 suffix
        confusing_fields = ["content_left_1", "content_right_1"]
        for placeholder_name in placeholders.values():
            assert placeholder_name not in confusing_fields, f"Found confusing field name: {placeholder_name}"

    def test_template_has_semantic_four_columns_fields(self):
        """Test that Four Columns layout has semantic field names"""

        with open(self.template_path, "r") as f:
            template_data = json.load(f)

        four_columns_layout = template_data["layouts"]["Four Columns"]
        placeholders = four_columns_layout["placeholders"]

        print("\nFOUR COLUMNS PLACEHOLDERS:")
        for idx, name in placeholders.items():
            print(f"  {idx}: {name}")

        # EXPECTED: Semantic field names
        expected_fields = {
            "content_col1": False,
            "content_col2": False,
            "content_col3": False,
            "content_col4": False,
        }

        for placeholder_name in placeholders.values():
            if placeholder_name in expected_fields:
                expected_fields[placeholder_name] = True

        print("Expected semantic fields found:")
        for field, found in expected_fields.items():
            print(f"  {field}: {'✅' if found else '❌'}")

        # These SHOULD pass after template update
        for field_name, found in expected_fields.items():
            assert found, f"Missing semantic field: {field_name}"

        # Should NOT have confusing _1 suffix
        confusing_fields = ["content_col1_1", "content_col2_1", "content_col3_1", "content_col4_1"]
        for placeholder_name in placeholders.values():
            assert placeholder_name not in confusing_fields, f"Found confusing field name: {placeholder_name}"

    def test_template_has_semantic_comparison_fields(self):
        """Test that Comparison layout has semantic field names"""

        with open(self.template_path, "r") as f:
            template_data = json.load(f)

        comparison_layout = template_data["layouts"]["Comparison"]
        placeholders = comparison_layout["placeholders"]

        print("\nCOMPARISON PLACEHOLDERS:")
        for idx, name in placeholders.items():
            print(f"  {idx}: {name}")

        # EXPECTED: Semantic field names
        expected_fields = {
            "title_left": False,
            "content_left": False,
            "title_right": False,
            "content_right": False,
        }

        for placeholder_name in placeholders.values():
            if placeholder_name in expected_fields:
                expected_fields[placeholder_name] = True

        print("Expected semantic fields found:")
        for field, found in expected_fields.items():
            print(f"  {field}: {'✅' if found else '❌'}")

        # These SHOULD pass after template update
        for field_name, found in expected_fields.items():
            assert found, f"Missing semantic field: {field_name}"

        # Should NOT have confusing _1 suffix
        confusing_fields = ["title_left_1", "content_left_1", "title_right_1", "content_right_1"]
        for placeholder_name in placeholders.values():
            assert placeholder_name not in confusing_fields, f"Found confusing field name: {placeholder_name}"

    def test_template_consistent_naming_pattern(self):
        """Test that all layouts follow consistent semantic naming pattern"""

        with open(self.template_path, "r") as f:
            template_data = json.load(f)

        layouts_to_check = ["Two Content", "Four Columns", "Comparison", "Three Columns"]

        for layout_name in layouts_to_check:
            if layout_name not in template_data["layouts"]:
                continue

            layout = template_data["layouts"][layout_name]
            placeholders = layout["placeholders"]

            print(f"\n{layout_name.upper()} NAMING PATTERN:")

            for placeholder_name in placeholders.values():
                print(f"  {placeholder_name}")

                # Should NOT have _1 suffix for semantic content/title fields
                if placeholder_name.startswith("content_"):
                    # Skip footer and system placeholders (these can have _1)
                    if not placeholder_name.startswith(("date_", "footer_", "slide_number_", "content_item", "content_1")):
                        # Semantic content fields should not end with _1
                        if placeholder_name in [
                            "content_left_1",
                            "content_right_1",
                            "content_col1_1",
                            "content_col2_1",
                            "content_col3_1",
                            "content_col4_1",
                        ]:
                            raise AssertionError(f"Confusing field name in {layout_name}: {placeholder_name} (should be semantic)")

                if placeholder_name.startswith("title_") and placeholder_name in [
                    "title_left_1",
                    "title_right_1",
                    "title_col1_1",
                    "title_col2_1",
                    "title_col3_1",
                    "title_col4_1",
                ]:
                    raise AssertionError(f"Confusing field name in {layout_name}: {placeholder_name} (should be semantic)")

                # Should use semantic names
                if "content" in placeholder_name:
                    semantic_patterns = [
                        "content_left",
                        "content_right",
                        "content_col1",
                        "content_col2",
                        "content_col3",
                        "content_col4",
                        "content_1",
                    ]
                    footer_patterns = ["date_", "footer_", "slide_number_"]

                    is_semantic = any(placeholder_name == pattern for pattern in semantic_patterns)
                    is_footer = any(placeholder_name.startswith(pattern) for pattern in footer_patterns)

                    if not is_footer:
                        assert is_semantic or placeholder_name == "content_1", f"Non-semantic content field in {layout_name}: {placeholder_name}"

    def test_no_placeholder_id_confusion(self):
        """Test that placeholder names don't confuse PowerPoint IDs with logical names"""

        with open(self.template_path, "r") as f:
            template_data = json.load(f)

        four_columns_layout = template_data["layouts"]["Four Columns"]
        placeholders = four_columns_layout["placeholders"]

        print("\nFOUR COLUMNS PLACEHOLDER MAPPING:")
        for placeholder_id, field_name in placeholders.items():
            print(f"  Placeholder ID {placeholder_id} → {field_name}")

        # The current confusing mapping that should be FIXED:
        # "14": "content_col1_1" - ID 14 doesn't match col1
        # "16": "content_col2_1" - ID 16 doesn't match col2
        # "18": "content_col3_1" - ID 18 doesn't match col3
        # "20": "content_col4_1" - ID 20 doesn't match col4

        # EXPECTED: Logical semantic names (ignore PowerPoint internal IDs)
        expected_mapping = {
            "14": "content_col1",  # First column
            "16": "content_col2",  # Second column
            "18": "content_col3",  # Third column
            "20": "content_col4",  # Fourth column
        }

        for placeholder_id, expected_name in expected_mapping.items():
            if placeholder_id in placeholders:
                actual_name = placeholders[placeholder_id]
                print(f"  Expected: {placeholder_id} → {expected_name}")
                print(f"  Actual:   {placeholder_id} → {actual_name}")

                # This SHOULD pass after template update
                assert actual_name == expected_name, f"Placeholder {placeholder_id} should map to {expected_name}, got {actual_name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
