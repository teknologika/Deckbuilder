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
                            pattern_data["yaml_pattern"] = self._convert_str_to_type(pattern_data["yaml_pattern"])
                        all_patterns[layout_name] = pattern_data
                    else:
                        print(f"Warning: Skipping {json_file} due to missing 'layout' in 'yaml_pattern'.")
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
                "text": "text",
                "subtitle": "subtitle",
                "text_caption": "text_caption",
                "image": "image",
                "title_top": "title_top",
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
            # No structured definition available, but still process content fields
            result = dict(structured_data)
            # Process common content fields even for non-structured layouts
            for field_name in [
                "title",
                "subtitle",
                "content",
                "text",
                "content_left",
                "content_right",
            ]:
                if field_name in result:
                    result[field_name] = self._process_content_field(result[field_name])
            return result

        # Extract fields directly from yaml_pattern instead of using mapping_rules
        yaml_pattern = structure_def.get("yaml_pattern", {})
        result = {}

        # Preserve the layout field from structured_data
        if "layout" in structured_data:
            result["layout"] = structured_data["layout"]

        # Process each field defined in yaml_pattern (except layout)
        for field_name, _field_type in yaml_pattern.items():
            if field_name == "layout":
                continue  # Skip layout field - already preserved above

            if field_name in structured_data:
                value = structured_data[field_name]

                # Convert arrays to newline-separated strings for content placeholders
                if isinstance(value, list):
                    value = "\n".join(str(item) for item in value)

                # Process content to convert markdown to LLM-friendly JSON
                processed_value = self._process_content_field(value)
                result[field_name] = processed_value

        return result

    def _process_content_field(self, content: str) -> Any:
        """Process content field - detect and parse tables, process headings, otherwise return content as-is"""
        if not content or not isinstance(content, str):
            return content

        content = content.strip()

        # Check if content contains a table (lines starting with |)
        if self._is_table_content(content):
            return self._parse_markdown_table(content)

        # Process headings and other markdown content
        processed_content = self._process_markdown_headings(content)
        return processed_content

    def _is_table_content(self, content: str) -> bool:
        """Check if content contains table markdown syntax"""
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        # A table needs at least 2 lines and contain pipe characters
        if len(lines) < 2:
            return False

        # Check if we have lines that look like table rows
        table_lines = 0
        for line in lines:
            if (line.startswith("|") and line.endswith("|")) or ("|" in line and not line.startswith("---")):
                table_lines += 1

        return table_lines >= 2

    def _parse_markdown_table(self, content: str) -> dict:
        """Extract table from markdown and apply default styling config"""
        table_data = {
            "type": "table",
            "data": [],
            "header_style": "dark_blue_white_text",
            "row_style": "alternating_light_gray",
            "border_style": "thin_gray",
            "custom_colors": {},
        }

        lines = [line.strip() for line in content.split("\n") if line.strip()]

        for line in lines:
            # Skip separator lines (markdown table separators)
            # Check for lines that are only separators (with or without pipes)
            clean_line = line.replace("|", "").replace("-", "").replace(":", "").replace("=", "").strip()
            if line.startswith("---") or line.startswith("===") or clean_line == "" or ("|" in line and all(c in "|-:= " for c in line)):
                continue

            if line.startswith("|") and line.endswith("|"):
                # Parse table row with inline formatting
                cells = [cell.strip() for cell in line[1:-1].split("|")]
                formatted_cells = []
                for cell in cells:
                    formatted_cells.append({"text": cell, "formatted": self._parse_inline_formatting(cell)})
                table_data["data"].append(formatted_cells)
            elif "|" in line and not line.startswith("|"):
                # Handle tables without outer pipes with inline formatting
                cells = [cell.strip() for cell in line.split("|")]
                formatted_cells = []
                for cell in cells:
                    formatted_cells.append({"text": cell, "formatted": self._parse_inline_formatting(cell)})
                table_data["data"].append(formatted_cells)

        return table_data

    def _parse_inline_formatting(self, text):
        """Parse inline formatting and return structured formatting data"""
        if not text:
            return [{"text": "", "format": {}}]

        # Patterns in order of precedence (longest patterns first to avoid conflicts)
        patterns = [
            (
                r"\*\*\*___(.*?)___\*\*\*",
                {"bold": True, "italic": True, "underline": True},
            ),  # ***___text___***
            (
                r"___\*\*\*(.*?)\*\*\*___",
                {"bold": True, "italic": True, "underline": True},
            ),  # ___***text***___
            (r"\*\*\*(.*?)\*\*\*", {"bold": True, "italic": True}),  # ***text***
            (r"___(.*?)___", {"underline": True}),  # ___text___
            (r"\*\*(.*?)\*\*", {"bold": True}),  # **text**
            (r"\*(.*?)\*", {"italic": True}),  # *text*
        ]

        # Find all matches and their positions
        all_matches = []
        for pattern, format_dict in patterns:
            for match in re.finditer(pattern, text):
                all_matches.append((match.start(), match.end(), match.group(1), format_dict))

        # Sort matches by position
        all_matches.sort(key=lambda x: x[0])

        # Remove overlapping matches (keep the first one found)
        filtered_matches = []
        last_end = 0
        for start, end, content, format_dict in all_matches:
            if start >= last_end:
                filtered_matches.append((start, end, content, format_dict))
                last_end = end

        # Build the formatted text segments
        segments = []
        last_pos = 0

        for start, end, content, format_dict in filtered_matches:
            # Add plain text before the formatted text
            if start > last_pos:
                plain_text = text[last_pos:start]
                if plain_text:
                    segments.append({"text": plain_text, "format": {}})

            # Add formatted text
            segments.append({"text": content, "format": format_dict})
            last_pos = end

        # Add any remaining plain text
        if last_pos < len(text):
            remaining_text = text[last_pos:]
            if remaining_text:
                segments.append({"text": remaining_text, "format": {}})

        # If no formatting found, return the original text
        if not segments:
            segments = [{"text": text, "format": {}}]

        return segments

    def _process_markdown_headings(self, content: str) -> str:
        """Process markdown headings by removing ## and ### prefixes"""
        if not content:
            return content

        lines = content.split("\n")
        processed_lines = []

        for line in lines:
            # Remove markdown heading prefixes
            if line.strip().startswith("## "):
                processed_lines.append(line.strip()[3:])  # Remove "## "
            elif line.strip().startswith("### "):
                processed_lines.append(line.strip()[4:])  # Remove "### "
            else:
                processed_lines.append(line)

        return "\n".join(processed_lines)

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

    Handles both pure structured frontmatter and frontmatter + content pairs.
    """
    # Import ContentProcessor to handle frontmatter + content parsing
    from .content_processor import ContentProcessor

    # Use ContentProcessor to properly parse frontmatter + content
    processor = ContentProcessor()
    slides = processor.parse_markdown_with_frontmatter(markdown_content)

    canonical_slides = []

    for slide_data in slides:
        # Convert slide data to canonical format
        slide_layout = slide_data.get("type") or slide_data.get("layout", "Title and Content")

        # Create canonical slide structure
        slide_obj = {
            "layout": slide_layout,
            "style": slide_data.get("style", "default_style"),
            "placeholders": {},
            "content": [],
        }

        # Add title if present
        if "title" in slide_data:
            slide_obj["placeholders"]["title"] = slide_data["title"]

        # Add subtitle if present
        if "subtitle" in slide_data:
            slide_obj["placeholders"]["subtitle"] = slide_data["subtitle"]

        # Convert rich content to canonical format and put it in placeholders
        if "rich_content" in slide_data:
            content_blocks = []
            for block in slide_data["rich_content"]:
                if "heading" in block:
                    content_blocks.append({"type": "heading", "text": block["heading"]})
                elif "paragraph" in block:
                    content_blocks.append({"type": "paragraph", "text": block["paragraph"]})
                elif "bullets" in block:
                    bullet_items = []
                    bullets = block["bullets"]
                    bullet_levels = block.get("bullet_levels", [1] * len(bullets))
                    for bullet, level in zip(bullets, bullet_levels):
                        bullet_items.append({"text": bullet, "level": level})
                    content_blocks.append({"type": "bullets", "items": bullet_items})

            if content_blocks:
                # Put content blocks in the placeholders so slide builder can find them
                slide_obj["placeholders"]["content"] = content_blocks

        # Add other placeholder fields from frontmatter (exclude internal fields)
        for key, value in slide_data.items():
            if key not in [
                "type",
                "rich_content",
                "style",
                "layout",
                "title_formatted",
                "subtitle_formatted",
            ]:
                # Don't duplicate title and subtitle since they're already handled above
                if key not in ["title", "subtitle"] or key not in slide_obj["placeholders"]:
                    slide_obj["placeholders"][key] = value

        canonical_slides.append(slide_obj)

    return {"slides": canonical_slides}
