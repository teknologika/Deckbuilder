#!/usr/bin/env python3
"""
Robust Convention-Based Naming System for PowerPoint Template Placeholders

Provides standardized, semantic placeholder naming using multi-tier detection
with graceful fallbacks for template variations and missing elements.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class PlaceholderContext:
    """Context information for placeholder naming decisions"""

    layout_name: str
    placeholder_idx: str
    placeholder_type: Optional[str] = None
    total_placeholders: int = 0
    existing_names: List[str] = None
    powerpoint_type: Optional[int] = None


@dataclass
class SemanticInfo:
    """Semantic information for a placeholder"""

    content_type: str
    position: str
    index: int = 1
    confidence: float = 1.0  # How confident we are in this detection


class NamingConvention:
    """
    Robust convention-based placeholder naming system with multi-tier detection.

    Handles template variations gracefully and provides semantic names even when
    footer elements or other placeholders are missing.

    Format: {ContentType}_{Position}_{Index}
    Example: title_top_1, content_col1_1, date_footer_1
    """

    def __init__(self):
        self.layout_mappings = self._build_layout_mappings()
        self.powerpoint_type_map = self._build_powerpoint_type_map()
        self.universal_patterns = self._build_universal_patterns()

    def generate_placeholder_name(self, context: PlaceholderContext) -> str:
        """
        Generate standardized placeholder name using multi-tier detection.

        Args:
            context: PlaceholderContext with layout and placeholder information

        Returns:
            Standardized placeholder name with confidence score
        """
        semantic_info = self._detect_semantic_info(context)

        # Generate name from semantic info
        if semantic_info.position and semantic_info.position != "main":
            return f"{semantic_info.content_type}_{semantic_info.position}_{semantic_info.index}"
        else:
            return f"{semantic_info.content_type}_{semantic_info.index}"

    def _detect_semantic_info(self, context: PlaceholderContext) -> SemanticInfo:
        """Multi-tier detection with confidence scoring"""

        # Tier 1: Exact layout + index mapping (highest confidence)
        if semantic_info := self._tier1_exact_mapping(context):
            semantic_info.confidence = 1.0
            return semantic_info

        # Tier 2: PowerPoint built-in types (high confidence)
        if semantic_info := self._tier2_powerpoint_types(context):
            semantic_info.confidence = 0.9
            return semantic_info

        # Tier 3: Universal patterns (medium confidence)
        if semantic_info := self._tier3_universal_patterns(context):
            semantic_info.confidence = 0.7
            return semantic_info

        # Tier 4: Layout-based inference (lower confidence)
        if semantic_info := self._tier4_layout_inference(context):
            semantic_info.confidence = 0.5
            return semantic_info

        # Tier 5: Generic fallback (lowest confidence)
        return self._tier5_generic_fallback(context)

    def _tier1_exact_mapping(self, context: PlaceholderContext) -> Optional[SemanticInfo]:
        """Tier 1: Exact layout + index mapping"""
        layout_key = self._normalize_layout_name(context.layout_name)

        if layout_key not in self.layout_mappings:
            return None

        mapping = self.layout_mappings[layout_key]
        idx = context.placeholder_idx

        # Check required placeholders first
        if idx in mapping.get("required", {}):
            info = mapping["required"][idx]
            return SemanticInfo(content_type=info["type"], position=info["position"], index=1)

        # Check optional placeholders (like footer elements)
        if idx in mapping.get("optional", {}):
            info = mapping["optional"][idx]
            return SemanticInfo(content_type=info["type"], position=info["position"], index=1)

        return None

    def _tier2_powerpoint_types(self, context: PlaceholderContext) -> Optional[SemanticInfo]:
        """Tier 2: PowerPoint built-in placeholder types"""
        if context.powerpoint_type is None:
            return None

        type_mapping = self.powerpoint_type_map.get(context.powerpoint_type)
        if not type_mapping:
            return None

        # Determine position based on layout and index
        position = self._infer_position_from_layout(context)

        return SemanticInfo(content_type=type_mapping["type"], position=position, index=1)

    def _tier3_universal_patterns(self, context: PlaceholderContext) -> Optional[SemanticInfo]:
        """Tier 3: Universal patterns that work across layouts"""
        idx = context.placeholder_idx

        # Universal pattern: Index 0 is almost always the main title
        if idx == "0":
            return SemanticInfo(content_type="title", position="top", index=1)

        # Universal pattern: Footer elements (may not exist in all templates)
        if idx in ["10", "11", "12"]:
            footer_types = {"10": "date", "11": "footer", "12": "slide_number"}
            return SemanticInfo(content_type=footer_types[idx], position="footer", index=1)

        # Universal pattern: Index 1 is often main content
        if idx == "1":
            return SemanticInfo(content_type="content", position="main", index=1)

        return None

    def _tier4_layout_inference(self, context: PlaceholderContext) -> Optional[SemanticInfo]:
        """Tier 4: Infer from layout structure and index patterns"""
        layout_name = context.layout_name.lower()
        idx = int(context.placeholder_idx) if context.placeholder_idx.isdigit() else 0

        # Column layouts: Infer column position from index
        if "column" in layout_name:
            return self._infer_column_semantic(context, idx)

        # Comparison layouts: Infer left/right from index
        if "comparison" in layout_name:
            return self._infer_comparison_semantic(context, idx)

        # Picture layouts: Infer picture vs caption
        if "picture" in layout_name or "caption" in layout_name:
            return self._infer_picture_semantic(context, idx)

        # Agenda/list layouts: Infer item position
        if "agenda" in layout_name or "6" in layout_name:
            return self._infer_agenda_semantic(context, idx)

        return None

    def _tier5_generic_fallback(self, context: PlaceholderContext) -> SemanticInfo:
        """Tier 5: Generic fallback naming"""
        return SemanticInfo(
            content_type="content",
            position="main",
            index=int(context.placeholder_idx) if context.placeholder_idx.isdigit() else 1,
            confidence=0.1,
        )

    def _infer_column_semantic(self, context: PlaceholderContext, idx: int) -> Optional[SemanticInfo]:
        """Infer semantic info for column layouts"""
        # Four columns: title=13,15,17,19 content=14,16,18,20
        # Three columns: title=13,15,17 content=14,16,18

        if idx in [13, 14]:  # Column 1
            content_type = "title" if idx == 13 else "content"
            return SemanticInfo(content_type=content_type, position="col1", index=1)
        elif idx in [15, 16]:  # Column 2
            content_type = "title" if idx == 15 else "content"
            return SemanticInfo(content_type=content_type, position="col2", index=1)
        elif idx in [17, 18]:  # Column 3
            content_type = "title" if idx == 17 else "content"
            return SemanticInfo(content_type=content_type, position="col3", index=1)
        elif idx in [19, 20]:  # Column 4 (four columns only)
            content_type = "title" if idx == 19 else "content"
            return SemanticInfo(content_type=content_type, position="col4", index=1)

        return None

    def _infer_comparison_semantic(self, context: PlaceholderContext, idx: int) -> Optional[SemanticInfo]:
        """Infer semantic info for comparison layouts"""
        if idx in [1, 2]:  # Left side
            content_type = "title" if idx == 1 else "content"
            return SemanticInfo(content_type=content_type, position="left", index=1)
        elif idx in [3, 4]:  # Right side
            content_type = "title" if idx == 3 else "content"
            return SemanticInfo(content_type=content_type, position="right", index=1)

        return None

    def _infer_picture_semantic(self, context: PlaceholderContext, idx: int) -> Optional[SemanticInfo]:
        """Infer semantic info for picture layouts"""
        if idx == 1:
            return SemanticInfo(content_type="image", position="main", index=1)
        elif idx == 2:
            return SemanticInfo(content_type="text", position="caption", index=1)

        return None

    def _infer_agenda_semantic(self, context: PlaceholderContext, idx: int) -> Optional[SemanticInfo]:
        """Infer semantic info for agenda layouts"""
        # Agenda items mapping based on actual template structure
        agenda_mapping = {
            28: ("number", "item1"),
            18: ("content", "item1"),
            29: ("number", "item2"),
            20: ("content", "item2"),
            30: ("number", "item3"),
            22: ("content", "item3"),
            31: ("number", "item4"),
            19: ("content", "item4"),
            32: ("number", "item5"),
            21: ("content", "item5"),
            33: ("number", "item6"),
            34: ("content", "item6"),
        }

        if idx in agenda_mapping:
            content_type, position = agenda_mapping[idx]
            return SemanticInfo(content_type=content_type, position=position, index=1)

        return None

    def _infer_position_from_layout(self, context: PlaceholderContext) -> str:
        """Infer position based on layout type and index"""
        idx = context.placeholder_idx
        layout_name = context.layout_name.lower()

        if idx == "0":
            return "top"
        elif idx in ["10", "11", "12"]:
            return "footer"
        elif "column" in layout_name:
            return "col1"  # Default to first column
        elif "comparison" in layout_name:
            return "left"  # Default to left side
        else:
            return "main"

    def _normalize_layout_name(self, layout_name: str) -> str:
        """Normalize layout name for mapping lookup"""
        return layout_name.lower().replace(" ", "_")

    def _build_layout_mappings(self) -> Dict[str, Dict]:
        """Build comprehensive layout mappings with required/optional elements"""
        return {
            "title_slide": {
                "required": {
                    "0": {"type": "title", "position": "top"},
                    "1": {"type": "subtitle", "position": "main"},
                },
                "optional": {
                    "10": {"type": "date", "position": "footer"},
                    "11": {"type": "footer", "position": "footer"},
                    "12": {"type": "slide_number", "position": "footer"},
                },
            },
            "title_and_content": {
                "required": {
                    "0": {"type": "title", "position": "top"},
                    "1": {"type": "content", "position": "main"},
                },
                "optional": {
                    "10": {"type": "date", "position": "footer"},
                    "11": {"type": "footer", "position": "footer"},
                    "12": {"type": "slide_number", "position": "footer"},
                },
            },
            "section_header": {
                "required": {
                    "0": {"type": "title", "position": "top"},
                    "1": {"type": "text", "position": "main"},
                },
                "optional": {
                    "10": {"type": "date", "position": "footer"},
                    "11": {"type": "footer", "position": "footer"},
                    "12": {"type": "slide_number", "position": "footer"},
                },
            },
            "two_content": {
                "required": {
                    "0": {"type": "title", "position": "top"},
                    "1": {"type": "content", "position": "left"},
                    "2": {"type": "content", "position": "right"},
                },
                "optional": {
                    "10": {"type": "date", "position": "footer"},
                    "11": {"type": "footer", "position": "footer"},
                    "12": {"type": "slide_number", "position": "footer"},
                },
            },
            "comparison": {
                "required": {
                    "0": {"type": "title", "position": "top"},
                    "1": {"type": "title", "position": "left"},
                    "2": {"type": "content", "position": "left"},
                    "3": {"type": "title", "position": "right"},
                    "4": {"type": "content", "position": "right"},
                },
                "optional": {
                    "10": {"type": "date", "position": "footer"},
                    "11": {"type": "footer", "position": "footer"},
                    "12": {"type": "slide_number", "position": "footer"},
                },
            },
            "three_columns_with_titles": {
                "required": {
                    "0": {"type": "title", "position": "top"},
                    "13": {"type": "title", "position": "col1"},
                    "14": {"type": "content", "position": "col1"},
                    "15": {"type": "title", "position": "col2"},
                    "16": {"type": "content", "position": "col2"},
                    "17": {"type": "title", "position": "col3"},
                    "18": {"type": "content", "position": "col3"},
                },
                "optional": {
                    "10": {"type": "date", "position": "footer"},
                    "11": {"type": "footer", "position": "footer"},
                    "12": {"type": "slide_number", "position": "footer"},
                },
            },
            "four_columns_with_titles": {
                "required": {
                    "0": {"type": "title", "position": "top"},
                    "13": {"type": "title", "position": "col1"},
                    "14": {"type": "content", "position": "col1"},
                    "15": {"type": "title", "position": "col2"},
                    "16": {"type": "content", "position": "col2"},
                    "17": {"type": "title", "position": "col3"},
                    "18": {"type": "content", "position": "col3"},
                    "19": {"type": "title", "position": "col4"},
                    "20": {"type": "content", "position": "col4"},
                },
                "optional": {
                    "10": {"type": "date", "position": "footer"},
                    "11": {"type": "footer", "position": "footer"},
                    "12": {"type": "slide_number", "position": "footer"},
                },
            },
            "picture_with_caption": {
                "required": {
                    "0": {"type": "title", "position": "top"},
                    "1": {"type": "image", "position": "main"},
                    "2": {"type": "text", "position": "caption"},
                },
                "optional": {
                    "10": {"type": "date", "position": "footer"},
                    "11": {"type": "footer", "position": "footer"},
                    "12": {"type": "slide_number", "position": "footer"},
                },
            },
            # Additional layouts can be added here
        }

    def _build_powerpoint_type_map(self) -> Dict[int, Dict[str, str]]:
        """Build mapping of PowerPoint placeholder types to semantic types"""
        # Note: These constants would come from python-pptx PP_PLACEHOLDER enum
        return {
            1: {"type": "title"},  # PP_PLACEHOLDER.TITLE
            2: {"type": "content"},  # PP_PLACEHOLDER.BODY
            3: {"type": "text"},  # PP_PLACEHOLDER.TEXT
            4: {"type": "date"},  # PP_PLACEHOLDER.DATE
            5: {"type": "slide_number"},  # PP_PLACEHOLDER.SLIDE_NUMBER
            6: {"type": "footer"},  # PP_PLACEHOLDER.FOOTER
            7: {"type": "subtitle"},  # PP_PLACEHOLDER.SUBTITLE
            18: {"type": "image"},  # PP_PLACEHOLDER.PICTURE
        }

    def _build_universal_patterns(self) -> Dict[str, Dict]:
        """Build universal patterns that work across all layouts"""
        return {
            "title_indices": ["0"],
            "footer_indices": ["10", "11", "12"],
            "main_content_indices": ["1"],
        }

    def convert_template_to_conventions(self, template_analysis: Dict) -> Dict:
        """
        Convert existing template analysis to use convention-based naming.

        Args:
            template_analysis: Template analysis from CLI tools

        Returns:
            Updated analysis with convention-based placeholder names
        """
        converted_analysis = template_analysis.copy()
        layouts = converted_analysis.get("layouts", {})

        for layout_name, layout_info in layouts.items():
            placeholders = layout_info.get("placeholders", {})
            converted_placeholders = {}

            for idx, _current_name in placeholders.items():
                context = PlaceholderContext(
                    layout_name=layout_name,
                    placeholder_idx=idx,
                    total_placeholders=len(placeholders),
                    existing_names=list(placeholders.values()),
                )

                convention_name = self.generate_placeholder_name(context)
                converted_placeholders[idx] = convention_name

            layout_info["placeholders"] = converted_placeholders

        return converted_analysis

    def validate_naming_consistency(self, template_analysis: Dict) -> Dict:
        """
        Validate naming consistency and detect improvement opportunities.

        Returns:
            Validation results with consistency scores and recommendations
        """
        layouts = template_analysis.get("layouts", {})
        validation_results = {
            "consistency_score": 0.0,
            "convention_compliance": 0.0,
            "issues": [],
            "recommendations": [],
            "pattern_analysis": {},
        }

        # Analyze current naming patterns
        all_names = []
        convention_names = []

        for layout_name, layout_info in layouts.items():
            placeholders = layout_info.get("placeholders", {})
            all_names.extend(placeholders.values())

            # Generate convention names for comparison
            for idx in placeholders.keys():
                context = PlaceholderContext(
                    layout_name=layout_name,
                    placeholder_idx=idx,
                    total_placeholders=len(placeholders),
                )
                convention_name = self.generate_placeholder_name(context)
                convention_names.append(convention_name)

        # Calculate compliance scores
        if all_names:
            convention_compliant = sum(1 for name in all_names if self._follows_convention_format(name))
            validation_results["convention_compliance"] = convention_compliant / len(all_names)

        # Generate recommendations
        if validation_results["convention_compliance"] < 0.8:
            validation_results["recommendations"].append("Consider using 'enhance --use-conventions' to apply standardized naming")

        # Detect naming patterns
        patterns = {}
        for name in all_names:
            pattern = self._extract_naming_pattern(name)
            patterns[pattern] = patterns.get(pattern, 0) + 1

        validation_results["pattern_analysis"] = patterns

        return validation_results

    def _follows_convention_format(self, placeholder_name: str) -> bool:
        """Check if placeholder name follows convention format"""
        # Convention format: {ContentType}_{Position}_{Index} or {ContentType}_{Index}
        pattern = r"^(title|subtitle|content|text|image|number|date|footer|slide_number)_" r"([a-z0-9]+_)?\d+$"
        return bool(re.match(pattern, placeholder_name.lower()))

    def _extract_naming_pattern(self, placeholder_name: str) -> str:
        """Extract naming pattern from placeholder name"""
        # Simplify name to pattern (e.g., "Title 1" -> "Title N")
        return re.sub(r"\d+", "N", placeholder_name)


def test_naming_convention():
    """Test the robust naming convention system"""
    convention = NamingConvention()

    test_cases = [
        # Test Four Columns layout
        PlaceholderContext("Four Columns With Titles", "13"),
        PlaceholderContext("Four Columns With Titles", "14"),
        PlaceholderContext("Four Columns With Titles", "0"),
        PlaceholderContext("Four Columns With Titles", "10"),  # Optional footer
        # Test unknown layout
        PlaceholderContext("Custom Layout", "1"),
        PlaceholderContext("Custom Layout", "5"),
        # Test minimal template (no footer)
        PlaceholderContext("Simple Title", "0"),
        PlaceholderContext("Simple Title", "1"),
    ]

    print("Testing Robust Naming Convention:")
    print("=" * 50)

    for context in test_cases:
        name = convention.generate_placeholder_name(context)
        semantic_info = convention._detect_semantic_info(context)
        print(f"Layout: {context.layout_name}")
        print(f"Index: {context.placeholder_idx}")
        print(f"Generated: {name}")
        print(f"Confidence: {semantic_info.confidence:.1f}")
        print("-" * 30)


if __name__ == "__main__":
    test_naming_convention()
