"""
Tests for Semantic Layout Aliases

Tests the new semantic alias pattern files that provide user-friendly
layout discovery while mapping to existing PowerPoint layouts.

Created: 2025-07-14
Related: Semantic layout aliases implementation
"""

import pytest

# json import removed - not used with disabled tests
from pathlib import Path


class TestSemanticAliases:
    """Test semantic alias pattern files for improved layout discoverability."""

    @pytest.fixture
    def semantic_aliases(self):
        """Map of semantic aliases to their target PowerPoint layouts."""
        return {
            "pros_and_cons": "Comparison",
            "before_and_after": "Comparison",
            "problem_solution": "Two Content",
            "timeline": "Title and Content",
            "process_steps": "Four Columns",
            "team_members": "Four Columns",
            "key_metrics": "Four Columns",
        }

    @pytest.fixture
    def patterns_dir(self):
        """Path to the structured frontmatter patterns directory."""
        return Path(__file__).parent.parent / "src" / "deckbuilder" / "structured_frontmatter_patterns"

    # Disabled pending Semantic alias redesign.
    # def test_semantic_alias_files_exist(self, semantic_aliases, patterns_dir):
    #     """Test that all semantic alias pattern files exist."""
    #     for alias_name in semantic_aliases.keys():
    #         pattern_file = patterns_dir / f"{alias_name}.json"
    #         assert pattern_file.exists(), f"Semantic alias file {alias_name}.json does not exist"

    # Disabled pending Semantic alias redesign.
    # def test_semantic_alias_file_structure(self, semantic_aliases, patterns_dir):
    #     """Test that semantic alias files have the correct JSON structure."""
    #     for alias_name, _target_layout in semantic_aliases.items():
    #         pattern_file = patterns_dir / f"{alias_name}.json"
    #
    #         # Load and parse JSON
    #         with open(pattern_file, "r") as f:
    #             pattern_data = json.load(f)
    #
    #         # Verify required fields
    #         assert "description" in pattern_data, f"{alias_name}.json missing description"
    #         assert "yaml_pattern" in pattern_data, f"{alias_name}.json missing yaml_pattern"
    #         assert "validation" in pattern_data, f"{alias_name}.json missing validation"
    #         assert "example" in pattern_data, f"{alias_name}.json missing example"
    #
    #         # Verify yaml_pattern uses semantic alias name
    #         yaml_pattern = pattern_data["yaml_pattern"]
    #         assert "layout" in yaml_pattern, f"{alias_name}.json yaml_pattern missing layout"
    #         assert yaml_pattern["layout"] == alias_name, f"{alias_name}.json layout should be {alias_name}, got {yaml_pattern['layout']}"

    # Disabled pending Semantic alias redesign.
    # def test_pros_and_cons_semantic_alias(self, patterns_dir):
    #     """Test pros_and_cons semantic alias specifically."""
    #     pattern_file = patterns_dir / "pros_and_cons.json"
    #
    #     with open(pattern_file, "r") as f:
    #         pattern_data = json.load(f)
    #
    #     # Should use semantic alias name as layout
    #     assert pattern_data["yaml_pattern"]["layout"] == "pros_and_cons"
    #
    #     # Should have appropriate description
    #     description = pattern_data["description"].lower()
    #     assert "advantages" in description or "disadvantages" in description or "pros" in description
    #
    #     # Should have required comparison fields
    #     validation = pattern_data["validation"]
    #     required_fields = validation["required_fields"]
    #     assert "title" in required_fields
    #     assert any("left" in field for field in required_fields)
    #     assert any("right" in field for field in required_fields)

    # Disabled pending Semantic alias redesign.
    # def test_before_and_after_semantic_alias(self, patterns_dir):
    #     """Test before_and_after semantic alias specifically."""
    #     pattern_file = patterns_dir / "before_and_after.json"
    #
    #     with open(pattern_file, "r") as f:
    #         pattern_data = json.load(f)
    #
    #     # Should use semantic alias name as layout
    #     assert pattern_data["yaml_pattern"]["layout"] == "before_and_after"
    #
    #     # Should have appropriate description
    #     description = pattern_data["description"].lower()
    #     assert "before" in description or "after" in description or "transformation" in description
    #
    #     # Should have example that demonstrates before/after usage
    #     example = pattern_data["example"]
    #     assert "before" in example.lower() or "after" in example.lower() or "current" in example.lower()

    # Disabled pending Semantic alias redesign.
    # def test_problem_solution_semantic_alias(self, patterns_dir):
    #     """Test problem_solution semantic alias specifically."""
    #     pattern_file = patterns_dir / "problem_solution.json"
    #
    #     with open(pattern_file, "r") as f:
    #         pattern_data = json.load(f)
    #
    #     # Should use semantic alias name as layout
    #     assert pattern_data["yaml_pattern"]["layout"] == "problem_solution"
    #
    #     # Should have appropriate description
    #     description = pattern_data["description"].lower()
    #     assert "problem" in description or "solution" in description or "issue" in description
    #
    #     # Should have left/right content fields
    #     validation = pattern_data["validation"]
    #     required_fields = validation["required_fields"]
    #     assert "title" in required_fields
    #     assert any("left" in field or "content" in field for field in required_fields)

    # Disabled pending Semantic alias redesign.
    # def test_timeline_semantic_alias(self, patterns_dir):
    #     """Test timeline semantic alias specifically."""
    #     pattern_file = patterns_dir / "timeline.json"
    #
    #     with open(pattern_file, "r") as f:
    #         pattern_data = json.load(f)
    #
    #     # Should use semantic alias name as layout
    #     assert pattern_data["yaml_pattern"]["layout"] == "timeline"
    #
    #     # Should have appropriate description
    #     description = pattern_data["description"].lower()
    #     assert "timeline" in description or "chronological" in description or "events" in description

    # Disabled pending Semantic alias redesign.
    # def test_process_steps_semantic_alias(self, patterns_dir):
    #     """Test process_steps semantic alias specifically."""
    #     pattern_file = patterns_dir / "process_steps.json"
    #
    #     with open(pattern_file, "r") as f:
    #         pattern_data = json.load(f)
    #
    #     # Should use semantic alias name as layout
    #     assert pattern_data["yaml_pattern"]["layout"] == "process_steps"
    #
    #     # Should have appropriate description
    #     description = pattern_data["description"].lower()
    #     assert "process" in description or "step" in description or "workflow" in description
    #
    #     # Should have four column content fields
    #     validation = pattern_data["validation"]
    #     required_fields = validation["required_fields"]
    #     assert "title" in required_fields
    #     column_fields = [f for f in required_fields if "col" in f]
    #     assert len(column_fields) == 4, f"Expected 4 column fields, got {len(column_fields)}"

    # Disabled pending Semantic alias redesign.
    # def test_team_members_semantic_alias(self, patterns_dir):
    #     """Test team_members semantic alias specifically."""
    #     pattern_file = patterns_dir / "team_members.json"
    #
    #     with open(pattern_file, "r") as f:
    #         pattern_data = json.load(f)
    #
    #     # Should use semantic alias name as layout
    #     assert pattern_data["yaml_pattern"]["layout"] == "team_members"
    #
    #     # Should have appropriate description
    #     description = pattern_data["description"].lower()
    #     assert "team" in description or "member" in description or "profile" in description
    #
    #     # Should have example that shows team member usage
    #     example = pattern_data["example"]
    #     assert "team" in example.lower() or "member" in example.lower()

    # Disabled pending Semantic alias redesign.
    # def test_key_metrics_semantic_alias(self, patterns_dir):
    #     """Test key_metrics semantic alias specifically."""
    #     pattern_file = patterns_dir / "key_metrics.json"
    #
    #     with open(pattern_file, "r") as f:
    #         pattern_data = json.load(f)
    #
    #     # Should use semantic alias name as layout
    #     assert pattern_data["yaml_pattern"]["layout"] == "key_metrics"
    #
    #     # Should have appropriate description
    #     description = pattern_data["description"].lower()
    #     assert "metric" in description or "kpi" in description or "performance" in description
    #
    #     # Should have example that shows metrics usage
    #     example = pattern_data["example"]
    #     assert "metric" in example.lower() or "kpi" in example.lower() or "performance" in example.lower()

    # Disabled pending Semantic alias redesign.
    # def test_semantic_aliases_have_unique_descriptions(self, semantic_aliases, patterns_dir):
    #     """Test that semantic aliases have unique, descriptive descriptions."""
    #     descriptions = []
    #
    #     for alias_name in semantic_aliases.keys():
    #         pattern_file = patterns_dir / f"{alias_name}.json"
    #
    #         with open(pattern_file, "r") as f:
    #             pattern_data = json.load(f)
    #
    #         description = pattern_data["description"]
    #         assert len(description) > 20, f"{alias_name} description too short: {description}"
    #         assert description not in descriptions, f"{alias_name} has duplicate description"
    #         descriptions.append(description)

    # Disabled pending Semantic alias redesign.
    # def test_semantic_aliases_have_valid_examples(self, semantic_aliases, patterns_dir):
    #     """Test that semantic alias examples are valid YAML frontmatter."""
    #     for alias_name, _target_layout in semantic_aliases.items():
    #         pattern_file = patterns_dir / f"{alias_name}.json"
    #
    #         with open(pattern_file, "r") as f:
    #             pattern_data = json.load(f)
    #
    #         example = pattern_data["example"]
    #
    #         # Should start and end with YAML frontmatter markers
    #         assert example.startswith("---"), f"{alias_name} example doesn't start with ---"
    #         assert example.endswith("---"), f"{alias_name} example doesn't end with ---"
    #
    #         # Should contain the semantic alias name as layout
    #         assert f"layout: {alias_name}" in example, f"{alias_name} example doesn't specify layout: {alias_name}"
    #
    #         # Should have a title
    #         assert "title:" in example, f"{alias_name} example missing title field"


class TestSemanticAliasPatternLoader:
    """Test pattern loader integration with semantic aliases."""

    # Disabled pending Semantic alias redesign.
    # def test_pattern_loader_loads_semantic_aliases(self):
    #     """Test that PatternLoader loads semantic alias patterns."""
    #     from deckbuilder.templates.pattern_loader import PatternLoader
    #
    #     loader = PatternLoader()
    #     patterns = loader.load_patterns()
    #
    #     # Should include semantic aliases
    #     semantic_aliases = ["pros_and_cons", "before_and_after", "problem_solution", "timeline", "process_steps", "team_members", "key_metrics"]
    #
    #     for alias in semantic_aliases:
    #         assert alias in patterns, f"PatternLoader didn't load semantic alias: {alias}"
    #
    #         # Each alias should have proper structure
    #         pattern_data = patterns[alias]
    #         assert "description" in pattern_data
    #         assert "yaml_pattern" in pattern_data
    #         assert "validation" in pattern_data
    #         assert "example" in pattern_data

    # Disabled pending Semantic alias redesign.
    # def test_semantic_aliases_discoverable_through_mcp_tools(self):
    #     """Test that semantic aliases are discoverable through MCP template discovery."""
    #     import os
    #     from pathlib import Path
    #
    #     # Set up environment for MCP testing
    #     original_env = os.environ.copy()
    #
    #     try:
    #         os.environ["DECK_OUTPUT_FOLDER"] = "/tmp/test_output"
    #         os.environ["DECK_TEMPLATE_FOLDER"] = str(Path(__file__).parent.parent / "src" / "deckbuilder" / "assets" / "templates")
    #         os.environ["DECK_TEMPLATE_NAME"] = "default"
    #
    #         from deckbuilder.templates.pattern_loader import PatternLoader
    #
    #         # Load patterns through same system MCP tools use
    #         loader = PatternLoader()
    #         patterns = loader.load_patterns()
    #
    #         # Verify semantic aliases are discoverable
    #         semantic_aliases = ["pros_and_cons", "before_and_after", "problem_solution", "timeline", "process_steps", "team_members", "key_metrics"]
    #
    #         for alias in semantic_aliases:
    #             assert alias in patterns, f"Semantic alias {alias} not discoverable through pattern loader"
    #
    #             # Verify they have the structure MCP tools expect
    #             pattern = patterns[alias]
    #             assert "yaml_pattern" in pattern
    #             assert "layout" in pattern["yaml_pattern"]
    #
    #             # Verify they use semantic alias names
    #             layout_name = pattern["yaml_pattern"]["layout"]
    #             assert layout_name == alias, f"Pattern {alias} should use {alias} as layout name, got {layout_name}"
    #
    #     finally:
    #         # Restore environment
    #         os.environ.clear()
    #         os.environ.update(original_env)


class TestSemanticAliasLayoutIntelligence:
    """Test layout intelligence integration with semantic aliases."""

    # Disabled pending Semantic alias redesign.
    # def test_layout_intelligence_includes_semantic_aliases(self):
    #     """Test that layout_intelligence.json includes semantic alias metadata."""
    #     intelligence_file = Path(__file__).parent.parent / "src" / "deckbuilder" / "layout_intelligence.json"
    #
    #     with open(intelligence_file, "r") as f:
    #         intelligence_data = json.load(f)
    #
    #     # Should have semantic aliases section
    #     assert "semantic_aliases" in intelligence_data["recommendation_engine"]
    #
    #     semantic_aliases = intelligence_data["recommendation_engine"]["semantic_aliases"]
    #
    #     # Should map all our semantic aliases
    #     expected_aliases = {
    #         "pros_and_cons": "Comparison",
    #         "before_and_after": "Comparison",
    #         "problem_solution": "Two Content",
    #         "timeline": "Title and Content",
    #         "process_steps": "Four Columns",
    #         "team_members": "Four Columns",
    #         "key_metrics": "Four Columns",
    #     }
    #
    #     for alias, target in expected_aliases.items():
    #         assert alias in semantic_aliases, f"Semantic alias {alias} not in layout intelligence"
    #         assert semantic_aliases[alias] == target, f"Semantic alias {alias} maps to {semantic_aliases[alias]}, expected {target}"

    # Disabled pending Semantic alias redesign.
    # def test_layout_intelligence_has_semantic_alias_layouts(self):
    #     """Test that layout_intelligence.json has layout compatibility for semantic aliases."""
    #     intelligence_file = Path(__file__).parent.parent / "src" / "deckbuilder" / "layout_intelligence.json"
    #
    #     with open(intelligence_file, "r") as f:
    #         intelligence_data = json.load(f)
    #
    #     layout_compatibility = intelligence_data["layout_compatibility"]
    #
    #     # Should have entries for semantic aliases
    #     semantic_aliases = ["pros_and_cons", "before_and_after", "problem_solution", "timeline", "process_steps", "team_members", "key_metrics"]
    #
    #     for alias in semantic_aliases:
    #         assert alias in layout_compatibility, f"Layout compatibility missing for {alias}"
    #
    #         alias_config = layout_compatibility[alias]
    #
    #         # Should have required structure
    #         assert "optimal_for" in alias_config
    #         assert "semantic_alias_for" in alias_config
    #         assert "placeholders" in alias_config
    #         assert "content_hints" in alias_config
    #         assert "confidence_factors" in alias_config
    #
    #         # Should reference the target layout
    #         target_layout = alias_config["semantic_alias_for"]
    #         assert target_layout in ["Comparison", "Two Content", "Title and Content", "Four Columns"]

    # Disabled pending Semantic alias redesign.
    # def test_layout_intelligence_updated_date(self):
    #     """Test that layout_intelligence.json has updated date for semantic aliases."""
    #     intelligence_file = Path(__file__).parent.parent / "src" / "deckbuilder" / "layout_intelligence.json"
    #
    #     with open(intelligence_file, "r") as f:
    #         intelligence_data = json.load(f)
    #
    #     # Should have updated date reflecting semantic alias implementation
    #     last_updated = intelligence_data["layout_intelligence"]["last_updated"]
    #     assert last_updated == "2025-07-14", f"Layout intelligence last_updated should be 2025-07-14, got {last_updated}"
