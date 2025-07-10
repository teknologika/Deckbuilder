import re
import yaml


class ContentProcessor:
    """Handles markdown parsing, frontmatter processing, and content formatting."""

    def __init__(self, layout_mapping=None):
        """
        Initialize the content processor.

        Args:
            layout_mapping: Optional layout mapping dictionary
        """
        self.layout_mapping = layout_mapping

    def parse_markdown_with_frontmatter(self, markdown_content: str) -> list:
        """
        Parse markdown content with frontmatter into slide data.

        Args:
            markdown_content: Markdown string with frontmatter slide definitions

        Returns:
            List of slide dictionaries ready for _add_slide()
        """
        slides = []

        # Split content by frontmatter boundaries
        slide_blocks = re.split(r"^---\s*$", markdown_content, flags=re.MULTILINE)

        i = 0
        while i < len(slide_blocks):
            # Skip empty blocks
            if not slide_blocks[i].strip():
                i += 1
                continue

            # Look for frontmatter + content pairs
            if i + 1 < len(slide_blocks):
                try:
                    frontmatter_raw = slide_blocks[i].strip()
                    content_raw = slide_blocks[i + 1].strip() if i + 1 < len(slide_blocks) else ""

                    # Parse frontmatter with structured frontmatter support
                    slide_config = self._parse_structured_frontmatter(frontmatter_raw)

                    # Parse markdown content into slide data
                    slide_data = self._parse_slide_content(content_raw, slide_config)
                    slides.append(slide_data)

                    i += 2  # Skip both frontmatter and content blocks
                except yaml.YAMLError:
                    # If YAML parsing fails, treat as regular content
                    content_raw = slide_blocks[i].strip()
                    slide_data = self._parse_slide_content(content_raw, {})
                    slides.append(slide_data)
                    i += 1
            else:
                # Single block without frontmatter
                content_raw = slide_blocks[i].strip()
                slide_data = self._parse_slide_content(content_raw, {})
                slides.append(slide_data)
                i += 1

        return slides

    def _parse_structured_frontmatter(self, frontmatter_content: str) -> dict:
        """Parse structured frontmatter and convert to placeholder mappings"""
        from .converter import StructuredFrontmatterConverter

        try:
            parsed = yaml.safe_load(frontmatter_content)
        except yaml.YAMLError:
            # Fallback to safe parsing for special characters
            return self._parse_frontmatter_safe(frontmatter_content)

        # Handle case where YAML parsing returns a string (malformed YAML)
        if not isinstance(parsed, dict):
            return self._parse_frontmatter_safe(frontmatter_content)

        layout_name = parsed.get("layout")
        if not layout_name:
            return parsed

        # Check if this is structured frontmatter
        converter = StructuredFrontmatterConverter()

        if converter.registry.supports_structured_frontmatter(layout_name):
            # Simple validation using JSON pattern validation rules
            structure_def = converter.registry.get_structure_definition(layout_name)
            validation_rules = structure_def.get("validation", {})
            required_fields = validation_rules.get("required_fields", [])

            # Check required fields
            missing_fields = []
            for field in required_fields:
                if field not in parsed:
                    missing_fields.append(field)

            if missing_fields:
                print(f"Warning in structured frontmatter: Missing required fields: {missing_fields}")

            # Convert to placeholder mappings
            converted = converter.convert_structured_to_placeholders(parsed)
            return converted

        # Regular frontmatter processing - still process content fields
        from .converter import FrontmatterConverter

        converter_instance = FrontmatterConverter()

        # Process common content fields even for non-structured layouts
        result = dict(parsed)
        for field_name in ["title", "subtitle", "content", "text", "content_left", "content_right"]:
            if field_name in result:
                result[field_name] = converter_instance._process_content_field(result[field_name])

        return result

    def _parse_frontmatter_safe(self, frontmatter_raw: str) -> dict:
        """
        Parse frontmatter safely by handling special characters that break YAML.

        This method processes frontmatter line by line to handle values with
        markdown formatting characters (*, _, etc.) that would break YAML parsing.
        """
        config = {}
        for line in frontmatter_raw.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                config[key] = value

        return config

    def _parse_slide_content(self, content: str, config: dict) -> dict:
        """Convert markdown content + config into slide data dict with mixed content support"""
        slide_data = {
            "type": config.get("layout", "Title and Content"),
            **config,  # Include all frontmatter as slide properties
        }

        # Apply formatting to frontmatter fields
        if "title" in slide_data and slide_data["title"]:
            slide_data["title_formatted"] = self._parse_inline_formatting(slide_data["title"])
        if "subtitle" in slide_data and slide_data["subtitle"]:
            slide_data["subtitle_formatted"] = self._parse_inline_formatting(slide_data["subtitle"])

        if not content.strip():
            return slide_data

        lines = content.split("\n")

        # Extract title (first # header)
        title_found = False
        content_lines = []

        for line in lines:
            if line.startswith("# ") and not title_found:
                title_text = line[2:].strip()
                # Only use markdown title if no frontmatter title exists
                if "title" not in config or not config.get("title"):
                    slide_data["title"] = title_text
                    slide_data["title_formatted"] = self._parse_inline_formatting(title_text)
                title_found = True
            elif line.startswith("## ") and slide_data["type"] == "title":
                subtitle_text = line[3:].strip()
                slide_data["subtitle"] = subtitle_text
                slide_data["subtitle_formatted"] = self._parse_inline_formatting(subtitle_text)
            else:
                content_lines.append(line)

        # Parse mixed content based on slide type
        # Note: Tables are now parsed in converter.py and come as JSON objects in placeholders
        if slide_data["type"] != "title":  # Content slides get rich content
            rich_content = self._parse_rich_content("\n".join(content_lines))
            if rich_content:
                slide_data["rich_content"] = rich_content

        return slide_data

    def _parse_rich_content(self, content: str) -> list:
        """Parse mixed markdown content into structured content blocks with better hierarchy"""
        blocks = []
        lines = content.split("\n")
        current_block = None

        for line in lines:
            original_line = line
            line = line.strip()
            if not line:
                continue

            # Handle nested bullet points by preserving indentation
            if line.startswith("- ") or line.startswith("* "):
                # Determine indentation level
                indent_level = len(original_line) - len(original_line.lstrip())
                bullet_text = line[2:].strip()

                if not current_block or "bullets" not in current_block:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {"bullets": [], "bullet_levels": []}

                current_block["bullets"].append(bullet_text)
                # Map indentation to bullet levels (0 indent = level 1, 2+ spaces = level 2, etc.)
                level = 1 if indent_level < 2 else 2
                current_block["bullet_levels"].append(level)

            elif line.startswith("## "):  # Subheading
                if current_block:
                    blocks.append(current_block)
                current_block = {"heading": line[3:].strip(), "level": 2}

            elif line.startswith("### "):  # Sub-subheading
                if current_block:
                    blocks.append(current_block)
                current_block = {"heading": line[4:].strip(), "level": 3}

            else:  # Regular paragraph
                if not current_block or "paragraph" not in current_block:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {"paragraph": line}
                else:
                    current_block["paragraph"] += " " + line

        if current_block:
            blocks.append(current_block)

        return blocks

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
