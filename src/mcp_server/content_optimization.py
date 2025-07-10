"""
Content Optimization Engine for Content-First Presentation Intelligence

This module implements Tool #3: optimize_content_for_layout() which takes user content
and a chosen layout, then optimizes the content structure and generates ready-to-use
YAML for immediate presentation creation.

Design Philosophy: Transform raw content into presentation-ready structure that
maximizes communication effectiveness within the chosen layout constraints.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class ContentOptimizationResult:
    """Result of content optimization with YAML and analysis"""

    yaml_structure: str
    content_mapping: Dict[str, str]
    formatting_applied: List[str]
    title_generated: str


@dataclass
class GapAnalysis:
    """Analysis of how well content fits the chosen layout"""

    content_fit: str  # excellent|good|fair|poor
    missing_elements: List[str]
    recommendations: List[str]
    layout_utilization: float


class ContentOptimizationEngine:
    """
    Optimizes raw content for specific PowerPoint layouts and generates ready-to-use YAML.

    The final step in the content-first workflow that transforms analyzed content
    into presentation-ready structured frontmatter.
    """

    def __init__(self):
        """Initialize with layout templates and optimization rules"""
        self.layout_templates = self._build_layout_templates()
        self.formatting_rules = self._build_formatting_rules()

    def optimize_content_for_layout(self, content: str, chosen_layout: str, slide_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Optimize content structure and generate ready-to-use YAML.

        Args:
            content: Raw content to optimize
            chosen_layout: Layout selected from recommend_slide_approach
            slide_context: Optional context from previous tools

        Returns:
            Dictionary with optimized YAML, gap analysis, and presentation tips
        """
        # Clean and prepare content
        cleaned_content = self._clean_content(content)

        # Generate optimized content structure
        optimization_result = self._optimize_content_structure(cleaned_content, chosen_layout, slide_context)

        # Perform gap analysis
        gap_analysis = self._analyze_content_layout_fit(cleaned_content, chosen_layout, optimization_result)

        # Generate presentation tips
        presentation_tips = self._generate_presentation_tips(chosen_layout, gap_analysis, slide_context)

        return {
            "optimized_content": {
                "yaml_structure": optimization_result.yaml_structure,
                "content_mapping": optimization_result.content_mapping,
                "formatting_applied": optimization_result.formatting_applied,
                "title_generated": optimization_result.title_generated,
            },
            "gap_analysis": {
                "content_fit": gap_analysis.content_fit,
                "missing_elements": gap_analysis.missing_elements,
                "recommendations": gap_analysis.recommendations,
                "layout_utilization": gap_analysis.layout_utilization,
            },
            "presentation_tips": presentation_tips,
        }

    def _clean_content(self, content: str) -> str:
        """Clean and normalize the input content.
        The _clean_content method is intended to standardize and clean raw input content.
           Its specific goals are:

           1. Normalize Whitespace: It removes leading/trailing whitespace from the
           entire content and collapses multiple newline characters followed by
           whitespace into a single double newline, aiming to reduce "excessive" whitespace.

           2. Normalize Quotes: It replaces various Unicode or "smart" quote characters
           (both single and double) with their standard ASCII equivalents.

           3. Remove em dashes.

        """
        # Remove excessive whitespace
        cleaned = re.sub(r"\n\s*\n", "\n\n", content.strip())

        # Normalize quotes
        cleaned = re.sub(r'["""]', '"', cleaned)
        cleaned = re.sub(r"[''']", "'", cleaned)

        # Normalize em dashes to hyphens
        cleaned = re.sub(r"—", "-", cleaned)

        return cleaned

    def _optimize_content_structure(self, content: str, chosen_layout: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content structure for the chosen layout."""
        layout_handler = self._get_layout_handler(chosen_layout)

        if layout_handler:
            return layout_handler(content, slide_context)
        else:
            # Fallback to basic Title and Content layout
            return self._optimize_for_title_and_content(content, slide_context)

    def _get_layout_handler(self, layout: str):
        """Get the appropriate optimization handler for the layout."""
        handlers = {
            "Four Columns": self._optimize_for_four_columns,
            "Four Columns With Titles": self._optimize_for_four_columns_with_titles,
            "Three Columns": self._optimize_for_three_columns,
            "Three Columns With Titles": self._optimize_for_three_columns_with_titles,
            "Comparison": self._optimize_for_comparison,
            "Two Content": self._optimize_for_two_content,
            "Title and Content": self._optimize_for_title_and_content,
            "Section Header": self._optimize_for_section_header,
            "Title Slide": self._optimize_for_title_slide,
            "SWOT Analysis": self._optimize_for_swot_analysis,
            "Agenda, 6 Textboxes": self._optimize_for_agenda_6_textboxes,
        }
        return handlers.get(layout)

    def _optimize_for_four_columns(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Four Columns layout."""
        # Extract title
        title = self._extract_or_generate_title(content, slide_context)

        # Parse content into 4 columns
        columns = self._parse_content_into_columns(content, 4)

        # Apply formatting
        formatted_columns = []
        formatting_applied = []

        for col in columns:
            formatted_col = self._apply_content_formatting(col)
            formatted_columns.append(formatted_col)
            if formatted_col != col:
                formatting_applied.append("content optimization")

        # Generate YAML
        yaml_structure = self._generate_four_columns_yaml(title, formatted_columns)

        # Create content mapping
        content_mapping = {
            "title": title,
            **{f"column_{i + 1}": col for i, col in enumerate(formatted_columns)},
        }

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _optimize_for_comparison(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Comparison layout."""
        title = self._extract_or_generate_title(content, slide_context)

        # Parse content into left/right comparison
        left_content, right_content = self._parse_content_into_comparison(content)

        # Apply formatting
        left_formatted = self._apply_content_formatting(left_content["content"])
        right_formatted = self._apply_content_formatting(right_content["content"])

        formatting_applied = []
        if left_formatted != left_content["content"] or right_formatted != right_content["content"]:
            formatting_applied.append("comparison content optimization")

        # Generate YAML
        yaml_structure = self._generate_comparison_yaml(title, left_content["title"], left_formatted, right_content["title"], right_formatted)

        content_mapping = {
            "title": title,
            "left_title": left_content["title"],
            "left_content": left_formatted,
            "right_title": right_content["title"],
            "right_content": right_formatted,
        }

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _optimize_for_two_content(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Two Content layout."""
        title = self._extract_or_generate_title(content, slide_context)

        # Parse into two sections
        sections = self._parse_content_into_columns(content, 2)

        # Apply formatting
        formatted_sections = []
        formatting_applied = []

        for section in sections:
            formatted_section = self._apply_content_formatting(section)
            formatted_sections.append(formatted_section)
            if formatted_section != section:
                formatting_applied.append("section content optimization")

        # Generate YAML
        yaml_structure = self._generate_two_content_yaml(title, formatted_sections)

        content_mapping = {
            "title": title,
            "content_left": formatted_sections[0] if len(formatted_sections) > 0 else "",
            "content_right": formatted_sections[1] if len(formatted_sections) > 1 else "",
        }

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _optimize_for_title_and_content(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Title and Content layout."""
        title = self._extract_or_generate_title(content, slide_context)

        # Extract main content (everything after title)
        main_content = self._extract_main_content(content, title)

        # Apply formatting and structure
        formatted_content = self._apply_content_formatting(main_content)
        formatted_content = self._structure_as_bullets(formatted_content)

        formatting_applied = ["bullet point structuring"] if formatted_content != main_content else []

        # Generate YAML
        yaml_structure = self._generate_title_and_content_yaml(title, formatted_content)

        content_mapping = {"title": title, "content": formatted_content}

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _optimize_for_section_header(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Section Header layout."""
        title = self._extract_or_generate_title(content, slide_context)
        subtitle = self._extract_subtitle_or_summary(content)

        # Generate YAML
        yaml_structure = self._generate_section_header_yaml(title, subtitle)

        content_mapping = {"title": title, "subtitle": subtitle}

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=["section header formatting"],
            title_generated=title,
        )

    def _optimize_for_title_slide(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Title Slide layout."""
        title = self._extract_or_generate_title(content, slide_context)
        subtitle = self._extract_subtitle_or_summary(content)

        # Generate YAML
        yaml_structure = self._generate_title_slide_yaml(title, subtitle)

        content_mapping = {"title": title, "subtitle": subtitle}

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=["title slide formatting"],
            title_generated=title,
        )

    def _optimize_for_four_columns_with_titles(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Four Columns With Titles layout."""
        title = self._extract_or_generate_title(content, slide_context)
        columns = self._parse_content_into_columns(content, 4)

        # Apply formatting
        formatted_columns = []
        column_titles = []
        formatting_applied = []

        for i, col in enumerate(columns):
            # Extract title and content from column
            if ":" in col:
                parts = col.split(":", 1)
                col_title = parts[0].strip()
                col_content = parts[1].strip()
            else:
                col_title = f"Category {i + 1}"
                col_content = col

            formatted_col = self._apply_content_formatting(col_content)
            formatted_columns.append(formatted_col)
            column_titles.append(col_title)

            if formatted_col != col_content:
                formatting_applied.append("content optimization")

        # Generate YAML
        yaml_structure = self._generate_four_columns_with_titles_yaml(title, column_titles, formatted_columns)

        content_mapping = {
            "title": title,
            **{f"title_col{i + 1}": col_title for i, col_title in enumerate(column_titles)},
            **{f"content_col{i + 1}": col for i, col in enumerate(formatted_columns)},
        }

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _optimize_for_three_columns(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Three Columns layout."""
        title = self._extract_or_generate_title(content, slide_context)
        columns = self._parse_content_into_columns(content, 3)

        # Apply formatting
        formatted_columns = []
        formatting_applied = []

        for col in columns:
            formatted_col = self._apply_content_formatting(col)
            formatted_columns.append(formatted_col)
            if formatted_col != col:
                formatting_applied.append("content optimization")

        # Generate YAML
        yaml_structure = self._generate_three_columns_yaml(title, formatted_columns)

        content_mapping = {
            "title": title,
            **{f"content_col{i + 1}": col for i, col in enumerate(formatted_columns)},
        }

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _optimize_for_three_columns_with_titles(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Three Columns With Titles layout."""
        title = self._extract_or_generate_title(content, slide_context)
        columns = self._parse_content_into_columns(content, 3)

        # Apply formatting and extract titles
        formatted_columns = []
        column_titles = []
        formatting_applied = []

        for i, col in enumerate(columns):
            if ":" in col:
                parts = col.split(":", 1)
                col_title = parts[0].strip()
                col_content = parts[1].strip()
            else:
                col_title = f"Category {i + 1}"
                col_content = col

            formatted_col = self._apply_content_formatting(col_content)
            formatted_columns.append(formatted_col)
            column_titles.append(col_title)

            if formatted_col != col_content:
                formatting_applied.append("content optimization")

        # Generate YAML
        yaml_structure = self._generate_three_columns_with_titles_yaml(title, column_titles, formatted_columns)

        content_mapping = {
            "title": title,
            **{f"title_col{i + 1}": col_title for i, col_title in enumerate(column_titles)},
            **{f"content_col{i + 1}": col for i, col in enumerate(formatted_columns)},
        }

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _optimize_for_swot_analysis(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for SWOT Analysis layout."""
        title = self._extract_or_generate_title(content, slide_context)

        # Parse SWOT content into quadrants
        swot_content = self._parse_content_into_swot_quadrants(content)

        # Apply formatting
        formatted_swot = {}
        formatting_applied = []

        for quadrant, content_text in swot_content.items():
            formatted_content = self._apply_content_formatting(content_text)
            formatted_swot[quadrant] = formatted_content
            if formatted_content != content_text:
                formatting_applied.append("SWOT content optimization")

        # Generate YAML
        yaml_structure = self._generate_swot_analysis_yaml(title, formatted_swot)

        content_mapping = {
            "title": title,
            **formatted_swot,
        }

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _optimize_for_agenda_6_textboxes(self, content: str, slide_context: Optional[Dict]) -> ContentOptimizationResult:
        """Optimize content for Agenda, 6 Textboxes layout."""
        title = self._extract_or_generate_title(content, slide_context)

        # Parse content into 6 agenda items
        agenda_items = self._parse_content_into_agenda_items(content, 6)

        # Apply formatting
        formatted_items = []
        formatting_applied = []

        for item in agenda_items:
            formatted_item = self._apply_content_formatting(item)
            formatted_items.append(formatted_item)
            if formatted_item != item:
                formatting_applied.append("agenda item optimization")

        # Generate YAML
        yaml_structure = self._generate_agenda_6_textboxes_yaml(title, formatted_items)

        content_mapping = {
            "title": title,
            **{f"content_item{i + 1}": item for i, item in enumerate(formatted_items)},
        }

        return ContentOptimizationResult(
            yaml_structure=yaml_structure,
            content_mapping=content_mapping,
            formatting_applied=formatting_applied,
            title_generated=title,
        )

    def _extract_or_generate_title(self, content: str, slide_context: Optional[Dict]) -> str:
        """Extract title from content or generate from context."""
        # Try to extract from first line if it looks like a title
        lines = content.strip().split("\n")
        first_line = lines[0].strip() if lines else ""

        # Check if first line is title-like
        if len(first_line) < 80 and not first_line.endswith(".") and len(first_line.split()) <= 8:
            return first_line

        # Try to generate from slide context
        if slide_context and "message_intent" in slide_context:
            intent = slide_context["message_intent"]
            # Extract key words from intent
            key_words = [word for word in intent.split() if len(word) > 3][:3]
            if key_words:
                return " ".join(word.capitalize() for word in key_words)

        # Extract key terms from content
        content_words = re.findall(r"\b[A-Za-z]{4,}\b", content)
        if content_words:
            # Take first few significant words
            title_words = content_words[:3]
            return " ".join(word.capitalize() for word in title_words)

        return "Content Overview"

    def _parse_content_into_columns(self, content: str, num_columns: int) -> List[str]:
        """Parse content into specified number of columns."""
        # Look for explicit list items first
        bullet_items = re.findall(r"[-*•]\s*([^\n]+)", content)
        if len(bullet_items) >= num_columns:
            return bullet_items[:num_columns]

        # Look for numbered list items
        numbered_items = re.findall(r"\d+\)\s*([^\n]+)", content)
        if len(numbered_items) >= num_columns:
            return numbered_items[:num_columns]

        # Try comma-separated items
        comma_parts = [part.strip() for part in content.split(",")]
        if len(comma_parts) >= num_columns:
            return comma_parts[:num_columns]

        # Try colon-separated items
        colon_items = re.findall(r"([^:]+):\s*([^,\n]+)", content)
        if len(colon_items) >= num_columns:
            return [f"{item[0]}: {item[1]}" for item in colon_items[:num_columns]]

        # Split by sentences/phrases
        sentences = re.split(r"[.!?]+", content)
        clean_sentences = [s.strip() for s in sentences if s.strip()]

        if len(clean_sentences) >= num_columns:
            return clean_sentences[:num_columns]

        # Fallback: split content into equal parts
        words = content.split()
        if len(words) < num_columns * 3:  # Too few words
            # Pad with placeholder content
            result = [content] if words else []
            while len(result) < num_columns:
                result.append(f"Additional content for column {len(result) + 1}")
            return result

        # Split words roughly equally
        words_per_column = len(words) // num_columns
        columns = []
        for i in range(num_columns):
            start = i * words_per_column
            end = start + words_per_column if i < num_columns - 1 else len(words)
            columns.append(" ".join(words[start:end]))

        return columns

    def _parse_content_into_comparison(self, content: str) -> Tuple[Dict[str, str], Dict[str, str]]:
        """Parse content into left/right comparison structure."""
        # Look for explicit vs/versus patterns
        vs_match = re.search(r"(.+?)\s+(?:vs|versus|compared to)\s+(.+)", content, re.IGNORECASE)
        if vs_match:
            left_content = vs_match.group(1).strip()
            right_content = vs_match.group(2).strip()

            return (
                {"title": self._extract_comparison_title(left_content), "content": left_content},
                {"title": self._extract_comparison_title(right_content), "content": right_content},
            )

        # Look for contrasting words
        contrast_patterns = [
            r"(.+?)\s+(?:but|however|while)\s+(.+)",
            r"(.+?)\s+(?:whereas|although)\s+(.+)",
        ]

        for pattern in contrast_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                left_content = match.group(1).strip()
                right_content = match.group(2).strip()

                return (
                    {"title": "Current Approach", "content": left_content},
                    {"title": "Alternative Approach", "content": right_content},
                )

        # Split content in half
        sentences = re.split(r"[.!?]+", content)
        clean_sentences = [s.strip() for s in sentences if s.strip()]

        mid_point = len(clean_sentences) // 2
        left_content = ". ".join(clean_sentences[:mid_point])
        right_content = ". ".join(clean_sentences[mid_point:])

        return (
            {"title": "Option A", "content": left_content},
            {"title": "Option B", "content": right_content},
        )

    def _extract_comparison_title(self, content: str) -> str:
        """Extract a short title from comparison content."""
        words = content.split()[:3]
        return " ".join(word.capitalize() for word in words)

    def _extract_main_content(self, content: str, title: str) -> str:
        """Extract main content excluding the title."""
        if title and title in content:
            # Remove title from content
            content_without_title = content.replace(title, "", 1).strip()
            return content_without_title if content_without_title else content
        return content

    def _extract_subtitle_or_summary(self, content: str) -> str:
        """Extract subtitle or create a summary."""
        # Look for a second line that could be a subtitle
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        if len(lines) >= 2:
            second_line = lines[1]
            if len(second_line) < 100:  # Reasonable subtitle length
                return second_line

        # Create a summary from content
        sentences = re.split(r"[.!?]+", content)
        clean_sentences = [s.strip() for s in sentences if s.strip()]

        if clean_sentences:
            # Take first sentence as summary, limited length
            summary = clean_sentences[0]
            if len(summary) > 100:
                summary = summary[:97] + "..."
            return summary

        return "Overview"

    def _apply_content_formatting(self, content: str) -> str:
        """Apply smart formatting to content."""
        if not content:
            return content

        # Emphasize key numbers and percentages
        content = re.sub(r"(\d+%)", r"**\1**", content)
        content = re.sub(r"(\$[\d,]+)", r"**\1**", content)

        # Emphasize superlatives and strong words
        strong_words = [
            "best",
            "fastest",
            "highest",
            "lowest",
            "most",
            "least",
            "critical",
            "important",
            "key",
        ]
        for word in strong_words:
            content = re.sub(rf"\b({word})\b", r"**\1**", content, flags=re.IGNORECASE)

        return content

    def _structure_as_bullets(self, content: str) -> str:
        """Structure content as bullet points if appropriate."""
        # If already has bullets, keep as is
        if re.search(r"^\s*[-*•]", content, re.MULTILINE):
            return content

        # Split sentences and convert to bullets
        sentences = re.split(r"[.!?]+", content)
        clean_sentences = [s.strip() for s in sentences if s.strip() and len(s) > 10]

        if len(clean_sentences) >= 2:
            return "\n".join(f"- {sentence}" for sentence in clean_sentences)

        return content

    def _parse_content_into_swot_quadrants(self, content: str) -> Dict[str, str]:
        """Parse content into SWOT analysis quadrants."""
        default_swot = {
            "content_top_left": "**Strengths**: Market position and capabilities",
            "content_top_right": "**Weaknesses**: Areas for improvement",
            "content_bottom_left": "**Opportunities**: Market and growth potential",
            "content_bottom_right": "**Threats**: External challenges and risks",
        }

        # Look for explicit SWOT keywords
        content_lower = content.lower()
        swot_content = {}

        if "strength" in content_lower:
            strength_match = re.search(r"strength[s]?[:\-\s]*([^\n]+)", content, re.IGNORECASE)
            if strength_match:
                swot_content["content_top_left"] = f"**Strengths**: {strength_match.group(1).strip()}"

        if "weakness" in content_lower:
            weakness_match = re.search(r"weakness[es]*[:\-\s]*([^\n]+)", content, re.IGNORECASE)
            if weakness_match:
                swot_content["content_top_right"] = f"**Weaknesses**: {weakness_match.group(1).strip()}"

        if "opportunit" in content_lower:
            opportunity_match = re.search(r"opportunit[y|ies]*[:\-\s]*([^\n]+)", content, re.IGNORECASE)
            if opportunity_match:
                swot_content["content_bottom_left"] = f"**Opportunities**: {opportunity_match.group(1).strip()}"

        if "threat" in content_lower:
            threat_match = re.search(r"threat[s]*[:\-\s]*([^\n]+)", content, re.IGNORECASE)
            if threat_match:
                swot_content["content_bottom_right"] = f"**Threats**: {threat_match.group(1).strip()}"

        # Fill in missing quadrants with defaults
        for key, default_value in default_swot.items():
            if key not in swot_content:
                swot_content[key] = default_value

        return swot_content

    def _parse_content_into_agenda_items(self, content: str, num_items: int) -> List[str]:
        """Parse content into agenda items."""
        # Look for numbered or bulleted items
        numbered_items = re.findall(r"\d+[.\)\-\s]+([^\n]+)", content)
        if len(numbered_items) >= num_items:
            return numbered_items[:num_items]

        bullet_items = re.findall(r"[-*•]\s*([^\n]+)", content)
        if len(bullet_items) >= num_items:
            return bullet_items[:num_items]

        # Split by sentences
        sentences = re.split(r"[.!?]+", content)
        clean_sentences = [s.strip() for s in sentences if s.strip()]

        if len(clean_sentences) >= num_items:
            return clean_sentences[:num_items]

        # Generate default agenda items
        items = []
        for i in range(num_items):
            if i < len(clean_sentences):
                items.append(f"{i + 1:02d} - {clean_sentences[i]}")
            else:
                items.append(f"{i + 1:02d} - Agenda item {i + 1}")

        return items

    # YAML Generation Methods (Updated for Direct Field Format)
    def _generate_four_columns_yaml(self, title: str, columns: List[str]) -> str:
        """Generate YAML for Four Columns layout using direct field format."""
        # Ensure we have 4 columns
        while len(columns) < 4:
            columns.append(f"Content for column {len(columns) + 1}")

        return f"""---
layout: Four Columns
title: {title}
content_col1: "{columns[0]}"
content_col2: "{columns[1]}"
content_col3: "{columns[2]}"
content_col4: "{columns[3]}"
---"""

    def _generate_comparison_yaml(self, title: str, left_title: str, left_content: str, right_title: str, right_content: str) -> str:
        """Generate YAML for Comparison layout using direct field format."""
        return f"""---
layout: Comparison
title: {title}
title_left: {left_title}
content_left: "{left_content}"
title_right: {right_title}
content_right: "{right_content}"
---"""

    def _generate_two_content_yaml(self, title: str, sections: List[str]) -> str:
        """Generate YAML for Two Content layout using direct field format."""
        section1 = sections[0] if len(sections) > 0 else "Content for first section"
        section2 = sections[1] if len(sections) > 1 else "Content for second section"

        return f"""---
layout: Two Content
title: {title}
content_left: |
  {section1}
content_right: |
  {section2}
---"""

    def _generate_title_and_content_yaml(self, title: str, content: str) -> str:
        """Generate YAML for Title and Content layout using direct field format."""
        return f"""---
layout: Title and Content
title: {title}
content: "{content}"
---"""

    def _generate_section_header_yaml(self, title: str, subtitle: str) -> str:
        """Generate YAML for Section Header layout."""
        return f"""---
layout: Section Header
title: {title}
subtitle: {subtitle}
---"""

    def _generate_title_slide_yaml(self, title: str, subtitle: str) -> str:
        """Generate YAML for Title Slide layout."""
        return f"""---
layout: Title Slide
title: {title}
subtitle: {subtitle}
---"""

    def _generate_four_columns_with_titles_yaml(self, title: str, column_titles: List[str], columns: List[str]) -> str:
        """Generate YAML for Four Columns With Titles layout."""
        # Ensure we have 4 columns and titles
        while len(columns) < 4:
            columns.append(f"Content for column {len(columns) + 1}")
        while len(column_titles) < 4:
            column_titles.append(f"Category {len(column_titles) + 1}")

        return f"""---
layout: Four Columns With Titles
title: {title}
title_col1: "{column_titles[0]}"
content_col1: "{columns[0]}"
title_col2: "{column_titles[1]}"
content_col2: "{columns[1]}"
title_col3: "{column_titles[2]}"
content_col3: "{columns[2]}"
title_col4: "{column_titles[3]}"
content_col4: "{columns[3]}"
---"""

    def _generate_three_columns_yaml(self, title: str, columns: List[str]) -> str:
        """Generate YAML for Three Columns layout."""
        # Ensure we have 3 columns
        while len(columns) < 3:
            columns.append(f"Content for column {len(columns) + 1}")

        return f"""---
layout: Three Columns
title: {title}
content_col1: "{columns[0]}"
content_col2: "{columns[1]}"
content_col3: "{columns[2]}"
---"""

    def _generate_three_columns_with_titles_yaml(self, title: str, column_titles: List[str], columns: List[str]) -> str:
        """Generate YAML for Three Columns With Titles layout."""
        # Ensure we have 3 columns and titles
        while len(columns) < 3:
            columns.append(f"Content for column {len(columns) + 1}")
        while len(column_titles) < 3:
            column_titles.append(f"Category {len(column_titles) + 1}")

        return f"""---
layout: Three Columns With Titles
title: {title}
title_col1: "{column_titles[0]}"
content_col1: "{columns[0]}"
title_col2: "{column_titles[1]}"
content_col2: "{columns[1]}"
title_col3: "{column_titles[2]}"
content_col3: "{columns[2]}"
---"""

    def _generate_swot_analysis_yaml(self, title: str, swot_content: Dict[str, str]) -> str:
        """Generate YAML for SWOT Analysis layout."""
        return f"""---
layout: SWOT Analysis
title: {title}
content_top_left: "{swot_content['content_top_left']}"
content_top_right: "{swot_content['content_top_right']}"
content_bottom_left: "{swot_content['content_bottom_left']}"
content_bottom_right: "{swot_content['content_bottom_right']}"
---"""

    def _generate_agenda_6_textboxes_yaml(self, title: str, agenda_items: List[str]) -> str:
        """Generate YAML for Agenda, 6 Textboxes layout."""
        # Ensure we have 6 items
        while len(agenda_items) < 6:
            agenda_items.append(f"{len(agenda_items) + 1:02d} - Agenda item {len(agenda_items) + 1}")

        return f"""---
layout: Agenda, 6 Textboxes
title: {title}
content_item1: "{agenda_items[0]}"
content_item2: "{agenda_items[1]}"
content_item3: "{agenda_items[2]}"
content_item4: "{agenda_items[3]}"
content_item5: "{agenda_items[4]}"
content_item6: "{agenda_items[5]}"
---"""

    def _analyze_content_layout_fit(self, content: str, chosen_layout: str, optimization_result: ContentOptimizationResult) -> GapAnalysis:
        """Analyze how well the content fits the chosen layout."""
        # Analyze content characteristics
        # content_length = len(content.split())  # Future: use for length analysis
        # layout_requirements = self._get_layout_requirements(chosen_layout)
        # Future: use for validation

        # Assess content fit
        fit_score = self._calculate_fit_score(content, chosen_layout, optimization_result)

        if fit_score >= 0.8:
            content_fit = "excellent"
        elif fit_score >= 0.6:
            content_fit = "good"
        elif fit_score >= 0.4:
            content_fit = "fair"
        else:
            content_fit = "poor"

        # Identify missing elements
        missing_elements = self._identify_missing_elements(content, chosen_layout)

        # Generate recommendations
        recommendations = self._generate_fit_recommendations(content_fit, missing_elements, chosen_layout)

        # Calculate layout utilization
        layout_utilization = min(fit_score, 1.0)

        return GapAnalysis(
            content_fit=content_fit,
            missing_elements=missing_elements,
            recommendations=recommendations,
            layout_utilization=layout_utilization,
        )

    def _calculate_fit_score(self, content: str, layout: str, optimization_result: ContentOptimizationResult) -> float:
        """Calculate a fit score between content and layout."""
        score = 0.5  # Base score

        # Bonus for having appropriate content structure
        if layout == "Four Columns":
            content_elements = len(optimization_result.content_mapping) - 1  # Exclude title
            if content_elements >= 4:
                score += 0.3
            elif content_elements >= 3:
                score += 0.2
            elif content_elements >= 2:
                score += 0.1

        elif layout == "Comparison":
            if "left_content" in optimization_result.content_mapping and "right_content" in optimization_result.content_mapping:
                score += 0.3
                # Bonus for balanced content
                left_len = len(optimization_result.content_mapping["left_content"].split())
                right_len = len(optimization_result.content_mapping["right_content"].split())
                if 0.5 <= left_len / max(right_len, 1) <= 2.0:
                    score += 0.2

        elif layout in ["Title and Content", "Section Header", "Title Slide"]:
            # These layouts are very flexible
            score += 0.3

        # Bonus for appropriate content length
        word_count = len(content.split())
        if 50 <= word_count <= 200:  # Sweet spot for slide content
            score += 0.2
        elif 20 <= word_count <= 300:  # Acceptable range
            score += 0.1

        return min(score, 1.0)

    def _identify_missing_elements(self, content: str, layout: str) -> List[str]:
        """Identify elements missing for optimal layout utilization."""
        missing = []

        if layout == "Four Columns":
            content_elements = len(self._parse_content_into_columns(content, 4))
            if content_elements < 4:
                missing.append(f"Need {4 - content_elements} more content elements for full utilization")

        elif layout == "Comparison":
            if not any(word in content.lower() for word in ["vs", "versus", "compared", "against", "but", "however"]):
                missing.append("Content lacks clear comparison elements")

        # Check for visual elements that could enhance the slide
        if not re.search(r"\d+%|\$[\d,]+", content):
            if layout in ["Four Columns", "Title and Content"]:
                missing.append("Consider adding metrics or data points for impact")

        return missing

    def _generate_fit_recommendations(self, content_fit: str, missing_elements: List[str], layout: str) -> List[str]:
        """Generate recommendations for improving content-layout fit."""
        recommendations = []

        if content_fit == "poor":
            recommendations.append("Consider switching to a simpler layout like 'Title and Content'")
        elif content_fit == "fair":
            recommendations.append("Content structure could be improved for better layout utilization")

        if missing_elements:
            recommendations.extend([f"Suggestion: {element}" for element in missing_elements])

        # Layout-specific recommendations
        if layout == "Four Columns" and content_fit in ["fair", "poor"]:
            recommendations.append("Try organizing content into 4 distinct categories or points")
        elif layout == "Comparison" and content_fit in ["fair", "poor"]:
            recommendations.append("Highlight the contrasting elements more clearly")

        return recommendations

    def _generate_presentation_tips(self, layout: str, gap_analysis: GapAnalysis, slide_context: Optional[Dict]) -> Dict[str, str]:
        """Generate presentation delivery tips."""
        tips = {}

        # Layout-specific delivery guidance
        if layout == "Four Columns":
            tips["delivery_guidance"] = "Present columns in logical order, allow time for audience to " "process each section"
        elif layout == "Comparison":
            tips["delivery_guidance"] = "Guide audience through left side first, then right, conclude with recommendation"
        elif layout == "Title and Content":
            tips["delivery_guidance"] = "Use title to set context, walk through content points systematically"
        else:
            tips["delivery_guidance"] = "Keep focus on key message, use slide as visual support"

        # Audience adaptation
        if slide_context and "audience" in slide_context:
            audience = slide_context["audience"]
            if audience == "board":
                tips["audience_adaptation"] = "Focus on high-level insights, minimize technical details"
            elif audience == "technical":
                tips["audience_adaptation"] = "Include technical details, be prepared for deep-dive questions"
            else:
                tips["audience_adaptation"] = "Balance detail level, check for understanding"
        else:
            tips["audience_adaptation"] = "Adapt detail level based on audience expertise"

        # Timing estimate
        word_count = sum(len(mapping.split()) for mapping in gap_analysis.__dict__.values() if isinstance(mapping, str))
        if word_count < 50:
            tips["timing_estimate"] = "1-2 minutes"
        elif word_count < 100:
            tips["timing_estimate"] = "2-3 minutes"
        else:
            tips["timing_estimate"] = "3-4 minutes"

        return tips

    def _get_layout_requirements(self, layout: str) -> Dict[str, Any]:
        """Get requirements and characteristics for each layout."""
        return {
            "Four Columns": {"min_elements": 2, "max_elements": 4, "flexibility": "medium"},
            "Comparison": {"min_elements": 2, "max_elements": 2, "flexibility": "low"},
            "Two Content": {"min_elements": 1, "max_elements": 2, "flexibility": "high"},
            "Title and Content": {
                "min_elements": 1,
                "max_elements": "unlimited",
                "flexibility": "very_high",
            },
            "Section Header": {"min_elements": 1, "max_elements": 2, "flexibility": "high"},
            "Title Slide": {"min_elements": 1, "max_elements": 2, "flexibility": "high"},
        }.get(layout, {"min_elements": 1, "max_elements": "unlimited", "flexibility": "high"})

    def _build_layout_templates(self) -> Dict[str, Dict]:
        """Build templates for different layouts."""
        return {
            "Four Columns": {
                "required_fields": ["title", "columns"],
                "optimal_content_length": "20-40 words per column",
            },
            "Comparison": {
                "required_fields": ["title", "left", "right"],
                "optimal_content_length": "30-60 words per side",
            },
        }

    def _build_formatting_rules(self) -> Dict[str, List[str]]:
        """Build formatting rules for different content types."""
        return {
            "numbers": ["**{number}**"],
            "percentages": ["**{percentage}**"],
            "currency": ["**{amount}**"],
            "emphasis": ["**{word}**"],
        }


# Helper function for easy import
def optimize_content_for_layout(content: str, chosen_layout: str, slide_context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Convenience function for optimizing content for a specific layout.

    Args:
        content: Raw content to optimize
        chosen_layout: Layout selected from recommend_slide_approach
        slide_context: Optional context from previous tools

    Returns:
        Dictionary with optimized YAML, gap analysis, and presentation tips
    """
    engine = ContentOptimizationEngine()
    return engine.optimize_content_for_layout(content, chosen_layout, slide_context)
