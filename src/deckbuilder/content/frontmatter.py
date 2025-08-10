"""
Structured Frontmatter System for Clean YAML Layout Authoring

This module provides clean, human-readable YAML structures that abstract away
PowerPoint placeholder names while maintaining full functionality. It includes:

1. Registry of structured patterns for different layout types
2. Bidirectional conversion between structured YAML and placeholder mappings
3. Validation system for structured frontmatter
4. Fallback handling when structured parsing fails

Based on the Template Discovery System specification (Option C).
"""

from typing import Any, Dict, Optional


class StructuredFrontmatterConverter:
    """Convert structured frontmatter to placeholder mappings (one-way only) - DEPRECATED

    This class is deprecated and maintained only for backward compatibility.
    New code should use PatternLoader directly from templates.pattern_loader.
    """

    def __init__(self, layout_mapping: Optional[Dict] = None):
        self.layout_mapping = layout_mapping or {}
        # Import here to avoid circular imports
        from ..templates.pattern_loader import PatternLoader

        self.pattern_loader = PatternLoader()

    def convert_structured_to_placeholders(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert structured frontmatter to placeholder field names - DEPRECATED

        Pattern files now define the correct structure directly.
        This method just returns the original data for backward compatibility.
        """

        layout_name = structured_data.get("layout")
        if not layout_name:
            return structured_data

        # Check if pattern exists for validation only
        pattern_data = self.pattern_loader.get_pattern_for_layout(layout_name)
        if pattern_data:
            # Pattern files define the correct structure directly
            # No conversion needed - return original data
            return structured_data

        # No pattern found, return original data for backward compatibility
        return structured_data


class StructuredFrontmatterValidator:
    """Validate structured frontmatter against layout requirements - DEPRECATED

    This class is deprecated. Pattern validation is now handled by PatternLoader.
    """

    def __init__(self):
        # Import here to avoid circular imports
        from ..templates.pattern_loader import PatternLoader

        self.pattern_loader = PatternLoader()

    def validate_structured_frontmatter(self, data: Dict[str, Any], layout_name: str) -> Dict[str, Any]:
        """Validate structured frontmatter against layout requirements - DEPRECATED"""

        pattern_data = self.pattern_loader.get_pattern_for_layout(layout_name)
        if not pattern_data:
            return {
                "valid": True,
                "warnings": ["No validation rules available for this layout"],
                "errors": [],
            }

        validation_rules = pattern_data.get("validation", {})
        result = {"valid": True, "warnings": [], "errors": []}

        # Check required fields
        required_fields = validation_rules.get("required_fields", [])
        for field in required_fields:
            if field not in data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: '{field}'")

        return result


def get_structured_frontmatter_help(layout_name: Optional[str] = None, template_mapping: Optional[Dict] = None) -> Dict[str, Any]:
    """Get help information for structured frontmatter - DEPRECATED

    This function is deprecated. Use PatternLoader directly for pattern information.
    """
    from ..templates.pattern_loader import PatternLoader

    pattern_loader = PatternLoader()

    if layout_name:
        pattern_data = pattern_loader.get_pattern_for_layout(layout_name)
        if not pattern_data:
            return {
                "error": f"Layout '{layout_name}' does not support structured frontmatter",
                "supported_layouts": pattern_loader.get_layout_names(),
            }

        return {
            "layout": layout_name,
            "description": pattern_data.get("description", ""),
            "example": pattern_data.get("example", ""),
            "validation_rules": pattern_data.get("validation", {}),
        }
    else:
        # General help
        patterns = pattern_loader.load_patterns()
        return {
            "supported_layouts": pattern_loader.get_layout_names(),
            "layout_info": {
                name: {
                    "description": pattern_data.get("description", ""),
                }
                for name, pattern_data in patterns.items()
            },
            "usage": ("Use 'layout: <LayoutName>' in frontmatter, then follow the pattern " "format for that layout"),
        }
