"""
Structured Frontmatter Processing

Handles structured frontmatter patterns and conversion for PowerPoint presentations.
Extracted from converter.py to provide clear separation of concerns.
"""

import re
from typing import Dict, Any, List, Optional
import json
from pathlib import Path


class StructuredFrontmatterRegistry:
    """Registry of structured frontmatter patterns for different layout types."""

    def __init__(self):
        self._patterns = self._load_patterns()

    def _load_patterns(self) -> Dict[str, Any]:
        """Loads structured frontmatter patterns from JSON files in a dedicated directory."""
        patterns_dir = Path(__file__).parent.parent / "structured_frontmatter_patterns"
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

        return {**pattern, "mapping_rules": pattern.get("mapping_rules", {})}

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

        # Check if this slide has table properties that will create a separate table object
        table_properties = ["column_widths", "row_height", "table_width", "style", "row_style", "border_style"]
        has_table_properties = any(prop in structured_data for prop in table_properties)

        # Process each field defined in yaml_pattern (except layout)
        for field_name, _field_type in yaml_pattern.items():
            if field_name == "layout":
                continue  # Skip layout field - already preserved above

            if field_name in structured_data:
                value = structured_data[field_name]

                # Convert arrays to newline-separated strings for content placeholders
                if isinstance(value, list):
                    value = "\n".join(str(item) for item in value)

                # Special handling for content field when table properties exist
                if field_name == "content" and has_table_properties and isinstance(value, str):
                    # Keep content as raw text when table properties exist
                    # The table object will handle the actual table creation
                    processed_value = value
                else:
                    # Process content to convert markdown to LLM-friendly JSON
                    processed_value = self._process_content_field(value)

                result[field_name] = processed_value

        # Preserve table-related properties that aren't in the yaml_pattern
        for prop in table_properties:
            if prop in structured_data and prop not in yaml_pattern:
                result[prop] = structured_data[prop]

        return result

    def _process_content_field(self, content: str) -> Any:
        """Process content field - detect and parse tables, lists, blockquotes, and headings"""
        if not content or not isinstance(content, str):
            return content

        content = content.strip()

        # Check if content contains a table (lines starting with |)
        if self._is_table_content(content):
            return self._parse_markdown_table(content)

        # Check if content contains lists or other markdown elements
        if self._is_structured_markdown_content(content):
            return self._parse_structured_markdown(content)

        # Process headings and other simple markdown content
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
                r"\\*\\*\\*___(.*?)___\\*\\*\\*",
                {"bold": True, "italic": True, "underline": True},
            ),  # ***___text___***
            (
                r"___\\*\\*\\*(.*?)\\*\\*\\*___",
                {"bold": True, "italic": True, "underline": True},
            ),  # ___***text***___
            (r"\\*\\*\\*(.*?)\\*\\*\\*", {"bold": True, "italic": True}),  # ***text***
            (r"___(.*?)___", {"underline": True}),  # ___text___
            (r"\\*\\*(.*?)\\*\\*", {"bold": True}),  # **text**
            (r"\\*(.*?)\\*", {"italic": True}),  # *text*
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
        """Process markdown headings - preserve markers for semantic processing, strip for legacy content"""
        if not content:
            return content

        # Check if content should preserve heading markers for semantic processing
        # This allows the rich content parser to detect and format headings properly
        lines = content.split("\n")
        has_headings = any(line.strip().startswith(("###### ", "##### ", "#### ", "### ", "## ", "# ")) for line in lines)

        # If content has headings, preserve them for semantic processing
        if has_headings:
            return content

        # Legacy behavior: strip heading markers from simple content
        processed_lines = []
        for line in lines:
            # Remove markdown heading prefixes (order matters - longest first)
            if line.strip().startswith("### "):
                processed_lines.append(line.strip()[4:])  # Remove "### "
            elif line.strip().startswith("## "):
                processed_lines.append(line.strip()[3:])  # Remove "## "
            elif line.strip().startswith("# "):
                processed_lines.append(line.strip()[2:])  # Remove "# "
            else:
                processed_lines.append(line)

        return "\n".join(processed_lines)

    def _is_structured_markdown_content(self, content: str) -> bool:
        """Check if content contains structured markdown elements like lists or blockquotes"""
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        # Check for bullet lists (- or *)
        bullet_lines = sum(1 for line in lines if line.startswith("- ") or line.startswith("* "))

        # Check for numbered lists (1. 2. 3.)
        numbered_lines = sum(1 for line in lines if self._is_numbered_list_line(line))

        # Check for blockquotes (>)
        blockquote_lines = sum(1 for line in lines if line.startswith("> "))

        # Return True if we have at least one structured element
        return bullet_lines > 0 or numbered_lines > 0 or blockquote_lines > 0

    def _is_numbered_list_line(self, line: str) -> bool:
        """Check if a line is a numbered list item (1. 2. 3. etc.)"""
        return bool(re.match(r"^\\d+\\.\\s+", line))

    def _parse_structured_markdown(self, content: str) -> str:
        """Parse structured markdown content with lists and blockquotes"""
        lines = content.split("\n")
        processed_lines = []

        for line in lines:
            original_line = line
            line = line.strip()

            # Process headings first (order matters - longest first)
            if line.startswith("### "):
                processed_lines.append(line[4:])  # Remove "### "
            elif line.startswith("## "):
                processed_lines.append(line[3:])  # Remove "## "
            elif line.startswith("# "):
                processed_lines.append(line[2:])  # Remove "# "
            # Process bullet lists
            elif line.startswith("- "):
                processed_lines.append("• " + line[2:])  # Replace "- " with "• "
            elif line.startswith("* "):
                processed_lines.append("• " + line[2:])  # Replace "* " with "• "
            # Process numbered lists
            elif self._is_numbered_list_line(line):
                processed_lines.append(line)  # Keep numbered lists as-is for now
            # Process blockquotes
            elif line.startswith("> "):
                processed_lines.append(line[2:])  # Remove "> "
            else:
                processed_lines.append(original_line)  # Keep original indentation for non-markdown lines

        return "\n".join(processed_lines)


# Legacy alias for backward compatibility
FrontmatterConverter = StructuredFrontmatterConverter
