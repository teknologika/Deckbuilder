import yaml
import re
from typing import Dict, Any, List, Optional, Union

import json
from pathlib import Path

# from .template_manager import TemplateManage


class StructuredFrontmatterRegistry:
    """Registry of structured frontmatter patterns for different layout types."""

    def __init__(self):
        self._patterns = self._load_patterns()

    def _load_patterns(self) -> Dict[str, Any]:
        """Loads structured frontmatter patterns from JSON files in a dedicated directory."""
        patterns_dir = Path(__file__).parent / "structured_frontmatter_patterns"
        all_patterns = {}
        for json_file in patterns_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    pattern_data = json.load(f)
                    layout_name = pattern_data.get("yaml_pattern", {}).get("layout")
                    if layout_name:
                        # Convert string placeholders back to type objects for validation
                        if "yaml_pattern" in pattern_data:
                            pattern_data["yaml_pattern"] = self._convert_str_to_type(
                                pattern_data["yaml_pattern"]
                            )
                        all_patterns[layout_name] = pattern_data
                    else:
                        print(
                            f"Warning: Skipping {json_file} due to missing 'layout' in 'yaml_pattern'."
                        )
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {json_file}: {e}")
            except Exception as e:
                print(f"Error loading pattern from {json_file}: {e}")
        return all_patterns

    def _convert_str_to_type(self, data: Any) -> Any:
        """Recursively converts string representations of types (e.g., 'str') to actual type objects."""
        if isinstance(data, dict):
            return {k: self._convert_str_to_type(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_str_to_type(item) for item in data]
        elif isinstance(data, str):
            if data == "str":
                return str
            elif data == "int":
                return int
            elif data == "bool":
                return bool
            # Add other types as needed
            return data
        return data

    def get_structure_patterns(self) -> Dict[str, Any]:
        """Returns the loaded structured frontmatter patterns."""
        return self._patterns

    def get_structure_definition(self, layout_name: str) -> Dict[str, Any]:
        """Get structure definition for a layout with dynamically built mapping rules"""
        patterns = self.get_structure_patterns()
        pattern = patterns.get(layout_name, {})

        if not pattern:
            # Default mapping rules for unrecognized layouts
            default_mapping_rules = {
                "title": "title",
                "content": "content",
            }
            return {"mapping_rules": default_mapping_rules}

        # Build mapping rules dynamically from template mapping
        # mapping_rules = self._build_mapping_rules(layout_name) # Removed

        return {**pattern, "mapping_rules": pattern.get("mapping_rules", {})}

    # Removed _build_mapping_rules method

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

    def __init__(self):
        self.registry = StructuredFrontmatterRegistry()

    def convert_structured_to_placeholders(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert structured frontmatter to placeholder field names"""

        layout_name = structured_data.get("layout")
        if not layout_name:
            # Fallback for cases where layout_name might be missing (e.g., malformed frontmatter)
            # In this case, we can't apply structured mapping, so return original data
            return structured_data

        structure_def = self.registry.get_structure_definition(layout_name)
        if not structure_def:
            # No structured definition available, return original data for backward compatibility
            return structured_data

        # Create result with type field for supported layouts
        result = {"type": layout_name}

        # Copy title and subtitle if present
        if "title" in structured_data:
            result["title"] = structured_data["title"]
        if "subtitle" in structured_data:
            result["subtitle"] = structured_data["subtitle"]

        mapping_rules = structure_def.get("mapping_rules", {})

        # Process each mapping rule
        for structured_path, placeholder_target in mapping_rules.items():
            value = self._extract_value_by_path(structured_data, structured_path)
            if value is not None:
                # Convert arrays to newline-separated strings for content placeholders
                if isinstance(value, list):
                    value = "\n".join(str(item) for item in value)
                # In the new canonical model, we directly use the target name
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


class FrontmatterConverter(StructuredFrontmatterConverter):
    """Converter to be used in the new converter module"""

    pass


def markdown_to_canonical_json(markdown_content: str) -> Dict[str, Any]:
    """
    Converts a Markdown string with frontmatter into the canonical JSON presentation model.
    This will be the single entry point for all .md files.
    """
    # 1. Split content into slides using "---" as a delimiter for both frontmatter and content
    # This regex handles cases where there might be leading/trailing newlines around the ---.
    # It also ensures that the first block is treated as frontmatter if it starts with ---
    blocks = re.split(r"""^---\s*$\n""", markdown_content, flags=re.MULTILINE)

    canonical_slides = []

    # The first block is usually empty if the markdown starts with ---
    # Or it's the content if there's no frontmatter
    start_index = 0
    if blocks and not blocks[0].strip() and len(blocks) > 1:
        start_index = 1  # Skip the initial empty block if frontmatter exists

    for i in range(start_index, len(blocks), 2):
        frontmatter_raw = blocks[i].strip()
        body_raw = blocks[i + 1].strip() if (i + 1) < len(blocks) else ""

        frontmatter = yaml.safe_load(frontmatter_raw) or {}  # Ensure frontmatter is a dict

        # 3. Use FrontmatterConverter to handle structured frontmatter
        converter = FrontmatterConverter()
        placeholder_mappings = converter.convert_structured_to_placeholders(frontmatter)

        # Initialize Canonical Slide Object with layout from placeholder_mappings
        slide_obj = {
            "layout": placeholder_mappings.get(
                "type", "Title and Content"
            ),  # Use 'type' from converted mappings
            "style": frontmatter.get("style", "default_style"),
            "placeholders": placeholder_mappings,  # ,
            # "content": [],  # Legacy?
        }

        # Remove 'type' from placeholders as it's now in 'layout'
        if "type" in slide_obj["placeholders"]:
            del slide_obj["placeholders"]["type"]

        # 5. Parse the Markdown body into structured content blocks
        # This logic will need to be robust, identifying headings, lists, tables, etc.
        # and converting them into the structured `content` array.
        # e.g., lines starting with '#' become 'heading' objects.
        # e.g., lines starting with '-' become 'bullets' objects.

        lines = body_raw.strip().split("\n")
        for line in lines:
            if line.startswith("#"):
                level = len(line.split(" ")[0])
                slide_obj["content"].append(
                    {"type": "heading", "level": level, "text": line.lstrip("# ")}
                )
            elif line.startswith("-"):
                # This is a simplified bullet implementation. A more robust
                # implementation would group consecutive bullet points.
                slide_obj["content"].append(
                    {"type": "bullets", "items": [{"level": 1, "text": line.lstrip("- ")}]}
                )
            elif "|" in line:
                # This is a simplified table implementation.
                pass  # Table parsing will be implemented later
            else:
                slide_obj["content"].append({"type": "paragraph", "text": line})

        canonical_slides.append(slide_obj)

    return {"slides": canonical_slides}
