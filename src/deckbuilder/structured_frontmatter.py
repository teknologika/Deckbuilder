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

from typing import Any, Dict, List, Optional, Union


class StructuredFrontmatterRegistry:
    """Registry of structured frontmatter patterns for different layout types"""

    def __init__(self, template_mapping: Optional[Dict] = None):
        """Initialize with template mapping from JSON file"""
        self.template_mapping = template_mapping or {}

    def get_structure_patterns(self):
        """Get structure patterns that define how to parse structured frontmatter"""
        return {
            "Four Columns With Titles": {
                "structure_type": "columns",
                "description": "Four-column comparison layout with individual titles and content",
                "yaml_pattern": {
                    "layout": "Four Columns With Titles",
                    "title": str,
                    "columns": [{"title": str, "content": str}],
                },
                "validation": {
                    "min_columns": 1,
                    "max_columns": 4,
                    "required_fields": ["title", "columns"],
                },
                "example": """---
                layout: Four Columns
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
                ---""",
            },
            "Three Columns With Titles": {
                "structure_type": "columns",
                "description": "Three-column layout with individual titles and content",
                "yaml_pattern": {
                    "layout": "Three Columns With Titles",
                    "title": str,
                    "columns": [{"title": str, "content": str}],
                },
                "validation": {
                    "min_columns": 1,
                    "max_columns": 3,
                    "required_fields": ["title", "columns"],
                },
                "example": """---
                layout: Three Columns With Titles
                title: Key Features
                columns:
                  - title: Performance
                    content: Fast processing with optimized algorithms
                  - title: Security
                    content: Enterprise-grade encryption and compliance
                  - title: Usability
                    content: Intuitive interface with minimal learning curve
                ---""",
            },
            "Three Columns": {
                "structure_type": "columns",
                "description": "Three-column layout with content only (no titles)",
                "yaml_pattern": {
                    "layout": "Three Columns",
                    "title": str,
                    "columns": [{"content": str}],
                },
                "validation": {
                    "min_columns": 1,
                    "max_columns": 3,
                    "required_fields": ["title", "columns"],
                },
                "example": """---
layout: Three Columns
title: Benefits Overview
columns:
  - content: Fast processing with optimized algorithms and sub-millisecond response times
  - content: Enterprise-grade encryption with SOC2 and GDPR compliance
  - content: Intuitive interface with minimal learning curve and comprehensive docs
---""",
            },
            "Four Columns": {
                "structure_type": "columns",
                "description": "Four-column layout with content only (no titles)",
                "yaml_pattern": {
                    "layout": "Four Columns",
                    "title": str,
                    "columns": [{"content": str}],
                },
                "validation": {
                    "min_columns": 1,
                    "max_columns": 4,
                    "required_fields": ["title", "columns"],
                },
                "example": """---
layout: Four Columns
title: Complete Feature Set
columns:
  - content: Fast processing with optimized algorithms and sub-millisecond response times
  - content: Enterprise-grade encryption with SOC2 and GDPR compliance
  - content: Intuitive interface with minimal learning curve and comprehensive docs
  - content: Transparent pricing with flexible plans and proven ROI
---""",
            },
            "Comparison": {
                "structure_type": "comparison",
                "description": "Side-by-side comparison layout for contrasting two options",
                "yaml_pattern": {
                    "layout": "Comparison",
                    "title": str,
                    "comparison": {
                        "left": {"title": str, "content": str},
                        "right": {"title": str, "content": str},
                    },
                },
                "mapping_rules": {"title": "semantic:title"},
                "validation": {
                    "required_fields": ["title", "comparison"],
                    "required_comparison_fields": ["left", "right"],
                },
                "example": """---
layout: Comparison
title: Solution Analysis
comparison:
  left:
    title: Traditional Approach
    content: Proven reliability with established workflows
  right:
    title: Modern Solution
    content: Advanced features with improved efficiency
---""",
            },
            "Two Content": {
                "structure_type": "sections",
                "description": "Side-by-side layout with two content areas",
                "yaml_pattern": {
                    "layout": "Two Content",
                    "title": str,
                    "sections": [{"title": str, "content": [str]}],
                },
                "mapping_rules": {"title": "semantic:title"},
                "validation": {
                    "required_fields": ["title", "sections"],
                    "min_sections": 2,
                    "max_sections": 2,
                },
                "example": """---
                layout: Two Content
                title: Before and After
                sections:
                  - title: Current State
                    content:
                      - Manual processes
                      - Time-consuming workflows
                  - title: Future State
                    content:
                      - Automated systems
                      - Streamlined operations
                ---""",
            },
            "Picture with Caption": {
                "structure_type": "media",
                "description": "Media slide with image placeholder and caption text",
                "yaml_pattern": {
                    "layout": "Picture with Caption",
                    "title": str,
                    "media": {
                        "image_path": str,  # NEW - Primary image source (optional)
                        "alt_text": str,  # NEW - Accessibility support (optional)
                        "caption": str,
                        "description": str,
                    },
                },
                "mapping_rules": {"title": "semantic:title"},
                "validation": {"required_fields": ["title", "media"]},
                "example": """---
                layout: Picture with Caption
                title: System Architecture
                media:
                  image_path: "assets/architecture_diagram.png"  # Primary image source
                  alt_text: "System architecture overview"       # Accessibility support
                  caption: High-level system architecture diagram
                  description: |
                    Main components include:
                    • Frontend: React-based interface
                    • API: RESTful services
                    • Database: PostgreSQL with Redis
                ---""",
            },
            "Agenda, 6 Textboxes": {
                "structure_type": "agenda",
                "description": "Six-item agenda layout with numbered items",
                "yaml_pattern": {
                    "layout": "Agenda, 6 Textboxes",
                    "title": str,
                    "agenda": [{"number": str, "item": str}],
                },
                "validation": {"required_fields": ["title", "agenda"], "max_items": 6},
                "example": """---
                layout: Agenda, 6 Textboxes
                title: Meeting Agenda
                agenda:
                  - number: "01"
                    item: Opening remarks
                  - number: "02"
                    item: Market analysis
                ---""",
            },
            "Title and 6-item Lists": {
                "structure_type": "lists",
                "description": "Six-item list layout with numbers, titles, and content",
                "yaml_pattern": {
                    "layout": "Title and 6-item Lists",
                    "title": str,
                    "lists": [{"number": str, "title": str, "content": str}],
                },
                "validation": {"required_fields": ["title", "lists"], "max_items": 6},
                "example": """---
                 layout: Title and 6-item Lists
                 title: Feature Overview
                 lists:
                   - number: "01"
                     title: Authentication
                     content: Secure login system
                 ---""",
            },
            "SWOT Analysis": {
                "structure_type": "analysis",
                "description": "SWOT analysis layout with four quadrants",
                "yaml_pattern": {
                    "layout": "SWOT Analysis",
                    "title": str,
                    "swot": {
                        "strengths": str,
                        "weaknesses": str,
                        "opportunities": str,
                        "threats": str,
                    },
                },
                "validation": {"required_fields": ["title", "swot"]},
                "example": """---
                layout: SWOT Analysis
                title: Strategic Analysis
                swot:
                  strengths: Strong market position
                  weaknesses: Limited resources
                  opportunities: New markets
                  threats: Competition
                ---""",
            },
        }

    def get_structure_definition(self, layout_name: str) -> Dict[str, Any]:
        """Get structure definition for a layout with dynamically built mapping rules"""
        patterns = self.get_structure_patterns()
        pattern = patterns.get(layout_name, {})

        if not pattern:
            return {}

        # Build mapping rules dynamically from template mapping
        mapping_rules = self._build_mapping_rules(layout_name)

        return {**pattern, "mapping_rules": mapping_rules}

    def _build_mapping_rules(self, layout_name: str) -> Dict[str, str]:
        """Build mapping rules dynamically from template JSON"""

        if not self.template_mapping:
            return {}

        layouts = self.template_mapping.get("layouts", {})
        layout_info = layouts.get(layout_name, {})
        placeholders = layout_info.get("placeholders", {})

        mapping_rules = {"title": "semantic:title"}  # Always use semantic for title

        if layout_name == "Four Columns With Titles":
            # Find column placeholders using convention-based patterns
            col_title_placeholders = []
            col_content_placeholders = []

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "title_col" in name_lower:
                    col_title_placeholders.append((_idx, placeholder_name))
                elif "content_col" in name_lower:
                    col_content_placeholders.append((_idx, placeholder_name))

            # Sort by placeholder index to get correct order
            col_title_placeholders.sort(key=lambda x: int(x[0]))
            col_content_placeholders.sort(key=lambda x: int(x[0]))

            # Build mapping rules for each column
            for i, (_idx, placeholder_name) in enumerate(col_title_placeholders[:4]):
                mapping_rules[f"columns[{i}].title"] = placeholder_name

            for i, (_idx, placeholder_name) in enumerate(col_content_placeholders[:4]):
                mapping_rules[f"columns[{i}].content"] = placeholder_name

        elif layout_name == "Comparison":
            # Find comparison placeholders using convention-based patterns
            left_placeholders = {}
            right_placeholders = {}

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "_left_" in name_lower:
                    if "title" in name_lower:
                        left_placeholders["title"] = placeholder_name
                    elif "content" in name_lower:
                        left_placeholders["content"] = placeholder_name
                elif "_right_" in name_lower:
                    if "title" in name_lower:
                        right_placeholders["title"] = placeholder_name
                    elif "content" in name_lower:
                        right_placeholders["content"] = placeholder_name

            # Map to comparison structure
            if "title" in left_placeholders:
                mapping_rules["comparison.left.title"] = left_placeholders["title"]
            if "content" in left_placeholders:
                mapping_rules["comparison.left.content"] = left_placeholders["content"]
            if "title" in right_placeholders:
                mapping_rules["comparison.right.title"] = right_placeholders["title"]
            if "content" in right_placeholders:
                mapping_rules["comparison.right.content"] = right_placeholders["content"]

        elif layout_name == "Two Content":
            # Find content placeholders using convention-based patterns
            content_placeholders = []

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "content_" in name_lower and ("_left_" in name_lower or "_right_" in name_lower):
                    if "_left_" in name_lower:
                        content_placeholders.append((0, placeholder_name))
                    elif "_right_" in name_lower:
                        content_placeholders.append((1, placeholder_name))

            content_placeholders.sort()

            # Map to sections
            for order, placeholder_name in content_placeholders:
                mapping_rules[f"sections[{order}].content"] = placeholder_name

        elif layout_name == "Three Columns With Titles":
            # Find column placeholders using convention-based patterns
            col_title_placeholders = []
            col_content_placeholders = []

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "title_col" in name_lower:
                    col_title_placeholders.append((_idx, placeholder_name))
                elif "content_col" in name_lower:
                    col_content_placeholders.append((_idx, placeholder_name))

            # Sort by placeholder index to get correct order
            col_title_placeholders.sort(key=lambda x: int(x[0]))
            col_content_placeholders.sort(key=lambda x: int(x[0]))

            # Build mapping rules for each column (max 3)
            for i, (_idx, placeholder_name) in enumerate(col_title_placeholders[:3]):
                mapping_rules[f"columns[{i}].title"] = placeholder_name

            for i, (_idx, placeholder_name) in enumerate(col_content_placeholders[:3]):
                mapping_rules[f"columns[{i}].content"] = placeholder_name

        elif layout_name == "Three Columns":
            # Find column content placeholders using convention-based patterns
            col_content_placeholders = []

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "content_col" in name_lower:
                    col_content_placeholders.append((_idx, placeholder_name))

            # Sort by placeholder index to get correct order
            col_content_placeholders.sort(key=lambda x: int(x[0]))

            # Build mapping rules for each column content (max 3)
            for i, (_idx, placeholder_name) in enumerate(col_content_placeholders[:3]):
                mapping_rules[f"columns[{i}].content"] = placeholder_name

        elif layout_name == "Four Columns":
            # Find column content placeholders using convention-based patterns
            col_content_placeholders = []

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "content_col" in name_lower:
                    col_content_placeholders.append((_idx, placeholder_name))

            # Sort by placeholder index to get correct order
            col_content_placeholders.sort(key=lambda x: int(x[0]))

            # Build mapping rules for each column content (max 4)
            for i, (_idx, placeholder_name) in enumerate(col_content_placeholders[:4]):
                mapping_rules[f"columns[{i}].content"] = placeholder_name

        elif layout_name == "Picture with Caption":
            # Find caption and image placeholders using convention-based patterns
            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "text_caption" in name_lower:
                    mapping_rules["media.caption"] = placeholder_name
                elif "image" in name_lower:
                    mapping_rules["media.image_path"] = placeholder_name

            # For Picture with Caption, description goes to the text area below image
            # Don't map to semantic:content to avoid conflicts with image placeholder

        elif layout_name == "Agenda, 6 Textboxes":
            # Find agenda item placeholders using convention-based patterns
            number_placeholders = []
            content_placeholders = []

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "number_item" in name_lower:
                    number_placeholders.append((_idx, placeholder_name))
                elif "content_item" in name_lower:
                    content_placeholders.append((_idx, placeholder_name))

            number_placeholders.sort(key=lambda x: int(x[0]))
            content_placeholders.sort(key=lambda x: int(x[0]))

            # Map agenda items
            for i, (_idx, placeholder_name) in enumerate(number_placeholders[:6]):
                mapping_rules[f"agenda[{i}].number"] = placeholder_name
            for i, (_idx, placeholder_name) in enumerate(content_placeholders[:6]):
                mapping_rules[f"agenda[{i}].item"] = placeholder_name

        elif layout_name == "Title and 6-item Lists":
            # Find list item placeholders using convention-based patterns
            number_placeholders = []
            content_placeholders = []
            title_placeholders = []

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "number_item" in name_lower:
                    number_placeholders.append((_idx, placeholder_name))
                elif "content_item" in name_lower:
                    content_placeholders.append((_idx, placeholder_name))
                elif "content_" in name_lower and "_1" in name_lower:
                    # These are the title placeholders for lists
                    title_placeholders.append((_idx, placeholder_name))

            number_placeholders.sort(key=lambda x: int(x[0]))
            content_placeholders.sort(key=lambda x: int(x[0]))
            title_placeholders.sort(key=lambda x: int(x[0]))

            # Map list items
            for i, (_idx, placeholder_name) in enumerate(number_placeholders[:6]):
                mapping_rules[f"lists[{i}].number"] = placeholder_name
            for i, (_idx, placeholder_name) in enumerate(content_placeholders[:6]):
                mapping_rules[f"lists[{i}].content"] = placeholder_name
            for i, (_idx, placeholder_name) in enumerate(title_placeholders[:6]):
                mapping_rules[f"lists[{i}].title"] = placeholder_name

        elif layout_name == "SWOT Analysis":
            # Find SWOT content placeholders using convention-based patterns
            swot_placeholders = []

            for _idx, placeholder_name in placeholders.items():
                name_lower = placeholder_name.lower()
                if "content_" in name_lower and "_1" not in name_lower:
                    # These are content placeholders like content_16, content_17, etc.
                    swot_placeholders.append((_idx, placeholder_name))

            swot_placeholders.sort(key=lambda x: int(x[0]))

            # Map SWOT quadrants (assuming they are in order:
            # strengths, weaknesses, opportunities, threats)
            swot_keys = ["strengths", "weaknesses", "opportunities", "threats"]
            for i, key in enumerate(swot_keys):
                if i < len(swot_placeholders):
                    mapping_rules[f"swot.{key}"] = swot_placeholders[i][1]

        return mapping_rules

    def supports_structured_frontmatter(self, layout_name: str) -> bool:
        """Check if layout supports structured frontmatter"""
        patterns = self.get_structure_patterns()
        return layout_name in patterns

    def get_supported_layouts(self) -> List[str]:
        """Get list of layouts that support structured frontmatter"""
        patterns = self.get_structure_patterns()
        return list(patterns.keys())

    def get_example(self, layout_name: str) -> Optional[str]:
        """Get example structured frontmatter for a layout"""
        definition = self.get_structure_definition(layout_name)
        return definition.get("example")


class StructuredFrontmatterConverter:
    """Convert structured frontmatter to placeholder mappings (one-way only)"""

    def __init__(self, layout_mapping: Optional[Dict] = None):
        self.layout_mapping = layout_mapping or {}
        self.registry = StructuredFrontmatterRegistry(layout_mapping)

    def convert_structured_to_placeholders(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert structured frontmatter to placeholder field names"""

        layout_name = structured_data.get("layout")
        if not layout_name:
            return structured_data

        structure_def = self.registry.get_structure_definition(layout_name)
        if not structure_def:
            # No structured definition available, return original data for backward compatibility
            return structured_data

        # Create result with type field for supported layouts
        result = {"type": layout_name}

        # Copy title if present
        if "title" in structured_data:
            result["title"] = structured_data["title"]

        mapping_rules = structure_def.get("mapping_rules", {})

        # Process each mapping rule
        for structured_path, placeholder_target in mapping_rules.items():
            value = self._extract_value_by_path(structured_data, structured_path)
            if value is not None:
                if placeholder_target.startswith("semantic:"):
                    # Use semantic field name directly
                    semantic_field = placeholder_target.split(":", 1)[1]
                    result[semantic_field] = value
                else:
                    # Use exact placeholder name
                    result[placeholder_target] = value

        return result

    def _extract_value_by_path(self, data: Dict[str, Any], path: str) -> Any:
        """Extract value from nested dict using dot notation path with array support"""

        # Handle array indexing like "columns[0].title"
        if "[" in path and "]" in path:
            return self._extract_array_value(data, path)

        # Handle simple dot notation like "comparison.left.title"
        keys = path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None

        return current

    def _extract_array_value(self, data: Dict[str, Any], path: str) -> Any:
        """Extract value from array using path like 'columns[0].title'"""

        # Parse "columns[0].title" into parts
        parts = self._parse_path_with_arrays(path)

        # Navigate through the data structure
        current = data
        for part in parts:
            if isinstance(part, int):
                if isinstance(current, list) and len(current) > part:
                    current = current[part]
                else:
                    return None
            elif isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def _set_value_by_path(self, data: Dict[str, Any], path: str, value: Any) -> None:
        """Set value in nested dict using dot notation path with array support"""

        if "[" in path and "]" in path:
            self._set_array_value(data, path, value)
            return

        keys = path.split(".")
        current = data

        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Set the final value
        current[keys[-1]] = value

    def _set_array_value(self, data: Dict[str, Any], path: str, value: Any) -> None:
        """Set value in array structure, creating arrays as needed"""

        parts = self._parse_path_with_arrays(path)
        current = data

        # Navigate through all but the last part, creating structure as needed
        for i, part in enumerate(parts[:-1]):
            if isinstance(part, int):
                # Current should be a list, ensure it exists and has enough elements
                if not isinstance(current, list):
                    current = []
                while len(current) <= part:
                    current.append({})
                current = current[part]
            else:
                # Current should be a dict
                if part not in current:
                    # Look ahead to see if next part is an array index
                    next_part = parts[i + 1] if i + 1 < len(parts) else None
                    if isinstance(next_part, int):
                        current[part] = []
                    else:
                        current[part] = {}
                current = current[part]

        # Set the final value
        final_part = parts[-1]
        if isinstance(final_part, int):
            if not isinstance(current, list):
                current = []
            while len(current) <= final_part:
                current.append(None)
            current[final_part] = value
        else:
            current[final_part] = value

    def _parse_path_with_arrays(self, path: str) -> List[Union[str, int]]:
        """Parse path like 'columns[0].title' into ['columns', 0, 'title']"""

        parts = []
        current_part = ""
        i = 0

        while i < len(path):
            if path[i] == "[":
                # Add the current part if it exists
                if current_part:
                    parts.append(current_part)
                    current_part = ""

                # Find the closing bracket and extract the index
                j = i + 1
                while j < len(path) and path[j] != "]":
                    j += 1

                if j < len(path):
                    index_str = path[i + 1 : j]
                    try:
                        index = int(index_str)
                        parts.append(index)
                    except ValueError:
                        # If it's not a number, treat as string key
                        parts.append(index_str)

                    i = j + 1
                    # Skip the dot after the bracket if it exists
                    if i < len(path) and path[i] == ".":
                        i += 1
                else:
                    # Malformed path, just add the bracket as text
                    current_part += path[i]
                    i += 1
            elif path[i] == ".":
                if current_part:
                    parts.append(current_part)
                    current_part = ""
                i += 1
            else:
                current_part += path[i]
                i += 1

        # Add any remaining part
        if current_part:
            parts.append(current_part)

        return parts


class StructuredFrontmatterValidator:
    """Validate structured frontmatter against layout requirements"""

    def __init__(self):
        self.registry = StructuredFrontmatterRegistry()

    def validate_structured_frontmatter(
        self, data: Dict[str, Any], layout_name: str
    ) -> Dict[str, Any]:
        """Validate structured frontmatter against layout requirements"""

        structure_def = self.registry.get_structure_definition(layout_name)
        if not structure_def:
            return {
                "valid": True,
                "warnings": ["No validation rules available for this layout"],
                "errors": [],
            }

        validation_rules = structure_def.get("validation", {})
        result = {"valid": True, "warnings": [], "errors": []}

        # Check required fields
        required_fields = validation_rules.get("required_fields", [])
        for field in required_fields:
            if field not in data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: '{field}'")

        # Layout-specific validation
        if layout_name in ["Four Columns", "Four Columns With Titles"] and "columns" in data:
            self._validate_four_columns(data, validation_rules, result)
        elif layout_name == "Comparison" and "comparison" in data:
            self._validate_comparison(data, validation_rules, result)
        elif layout_name == "Two Content" and "sections" in data:
            self._validate_two_content(data, validation_rules, result)

        return result

    def _validate_four_columns(
        self, data: Dict[str, Any], rules: Dict[str, Any], result: Dict[str, Any]
    ) -> None:
        """Validate Four Columns specific structure"""
        columns = data.get("columns", [])

        min_cols = rules.get("min_columns", 1)
        max_cols = rules.get("max_columns", 4)

        if len(columns) < min_cols:
            result["valid"] = False
            result["errors"].append(f"Expected at least {min_cols} columns, got {len(columns)}")
        elif len(columns) > max_cols:
            result["warnings"].append(
                f"Expected at most {max_cols} columns, got {len(columns)} "
                f"(extra columns will be ignored)"
            )

        # Validate each column structure
        for i, column in enumerate(columns):
            if not isinstance(column, dict):
                result["errors"].append(
                    f"Column {i + 1} must be an object with 'title' and 'content'"
                )
                continue

            if "title" not in column:
                result["warnings"].append(f"Column {i + 1} missing 'title' field")
            if "content" not in column:
                result["warnings"].append(f"Column {i + 1} missing 'content' field")

    def _validate_comparison(
        self, data: Dict[str, Any], rules: Dict[str, Any], result: Dict[str, Any]
    ) -> None:
        """Validate Comparison specific structure"""
        comparison = data.get("comparison", {})

        required_sides = rules.get("required_comparison_fields", ["left", "right"])
        for side in required_sides:
            if side not in comparison:
                result["valid"] = False
                result["errors"].append(f"Missing required comparison side: '{side}'")
            else:
                side_data = comparison[side]
                if not isinstance(side_data, dict):
                    result["errors"].append(f"Comparison '{side}' must be an object")
                else:
                    if "title" not in side_data:
                        result["warnings"].append(f"Comparison '{side}' missing 'title' field")
                    if "content" not in side_data:
                        result["warnings"].append(f"Comparison '{side}' missing 'content' field")

    def _validate_two_content(
        self, data: Dict[str, Any], rules: Dict[str, Any], result: Dict[str, Any]
    ) -> None:
        """Validate Two Content specific structure"""
        sections = data.get("sections", [])

        min_sections = rules.get("min_sections", 2)
        max_sections = rules.get("max_sections", 2)

        if len(sections) < min_sections:
            result["valid"] = False
            result["errors"].append(
                f"Expected at least {min_sections} sections, got {len(sections)}"
            )
        elif len(sections) > max_sections:
            result["warnings"].append(
                f"Expected at most {max_sections} sections, got {len(sections)} "
                f"(extra sections will be ignored)"
            )


def get_structured_frontmatter_help(
    layout_name: str = None, template_mapping: Dict = None
) -> Dict[str, Any]:
    """Get help information for structured frontmatter"""

    registry = StructuredFrontmatterRegistry(template_mapping)

    if layout_name:
        # Specific layout help
        definition = registry.get_structure_definition(layout_name)
        if not definition:
            return {
                "error": f"Layout '{layout_name}' does not support structured frontmatter",
                "supported_layouts": registry.get_supported_layouts(),
            }

        return {
            "layout": layout_name,
            "description": definition["description"],
            "structure_type": definition["structure_type"],
            "example": definition["example"],
            "validation_rules": definition.get("validation", {}),
            "mapping_rules": definition["mapping_rules"],
        }
    else:
        # General help
        patterns = registry.get_structure_patterns()
        return {
            "supported_layouts": registry.get_supported_layouts(),
            "layout_info": {
                name: {
                    "description": definition["description"],
                    "structure_type": definition["structure_type"],
                }
                for name, definition in patterns.items()
            },
            "usage": (
                "Use 'layout: <LayoutName>' in frontmatter, then follow the structured "
                "format for that layout"
            ),
        }
