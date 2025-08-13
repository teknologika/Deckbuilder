import re
import yaml


class ContentProcessor:
    """Handles markdown parsing, frontmatter processing, and content formatting."""

    def __init__(self):
        """Initialize the content processor."""
        pass

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
        """Parse frontmatter using PatternLoader system only"""
        from ..templates.pattern_loader import PatternLoader

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

        # Check if this layout has a pattern file
        pattern_loader = PatternLoader()
        pattern_data = pattern_loader.get_pattern_for_layout(layout_name)

        if pattern_data:
            # Validate required fields
            validation_rules = pattern_data.get("validation", {})
            required_fields = validation_rules.get("required_fields", [])

            missing_fields = []
            for field in required_fields:
                if field not in parsed:
                    missing_fields.append(field)

            if missing_fields:
                print(f"Warning in structured frontmatter: Missing required fields: {missing_fields}")

            # Pattern files define the correct structure directly
            # No conversion needed - the pattern file structure matches expected placeholder names
            return parsed

        # Regular frontmatter processing - still process content fields
        from .frontmatter_to_json_converter import FrontmatterConverter

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
                else:
                    # Keep H1 in content since we already have a frontmatter title
                    content_lines.append(line)
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

                if not current_block or current_block.get("type") != "bullets":
                    if current_block:
                        blocks.append(current_block)
                    current_block = {"type": "bullets", "items": []}

                # Map indentation to bullet levels (0 indent = level 1, 2+ spaces = level 2, etc.)
                level = 1 if indent_level < 2 else 2
                current_block["items"].append({"text": bullet_text, "level": level})

            elif line.startswith("###### "):  # H6 heading
                if current_block:
                    blocks.append(current_block)
                current_block = {"type": "heading", "text": line[7:].strip(), "level": 6}

            elif line.startswith("##### "):  # H5 heading
                if current_block:
                    blocks.append(current_block)
                current_block = {"type": "heading", "text": line[6:].strip(), "level": 5}

            elif line.startswith("#### "):  # H4 heading
                if current_block:
                    blocks.append(current_block)
                current_block = {"type": "heading", "text": line[5:].strip(), "level": 4}

            elif line.startswith("### "):  # H3 heading
                if current_block:
                    blocks.append(current_block)
                current_block = {"type": "heading", "text": line[4:].strip(), "level": 3}

            elif line.startswith("## "):  # H2 heading
                if current_block:
                    blocks.append(current_block)
                current_block = {"type": "heading", "text": line[3:].strip(), "level": 2}

            elif line.startswith("# "):  # H1 heading
                if current_block:
                    blocks.append(current_block)
                current_block = {"type": "heading", "text": line[2:].strip(), "level": 1}

            else:  # Regular paragraph
                if not current_block or current_block.get("type") != "paragraph":
                    if current_block:
                        blocks.append(current_block)
                    current_block = {"type": "paragraph", "text": line}
                else:
                    current_block["text"] += " " + line

        if current_block:
            blocks.append(current_block)

        return blocks

    def _parse_inline_formatting(self, text):
        """Parse inline formatting and return structured formatting data"""
        from .formatter import ContentFormatter

        formatter = ContentFormatter()
        return formatter.parse_inline_formatting(text)
