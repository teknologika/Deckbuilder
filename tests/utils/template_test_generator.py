"""
Template Test Generator

Auto-generates test files from template JSON structures, including both
JSON presentation format and markdown with structured frontmatter.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Import content generator
from .content_generator import ContentGenerator, ContentLength, ContentType


@dataclass
class GeneratedTestFile:
    """Information about a generated test file."""

    file_path: Path
    layout_name: str
    file_type: str  # 'json' or 'markdown'
    content_preview: str


@dataclass
class TestGenerationReport:
    """Report of test file generation."""

    template_name: str
    total_layouts: int
    generated_files: List[GeneratedTestFile]
    coverage_report: Dict[str, bool]
    generation_time: datetime

    @property
    def coverage_percentage(self) -> float:
        """Calculate layout coverage percentage."""
        if self.total_layouts == 0:
            return 0.0
        covered_layouts = sum(1 for covered in self.coverage_report.values() if covered)
        return (covered_layouts / self.total_layouts) * 100


class TemplateTestGenerator:
    """Auto-generate test files from template JSON structures."""

    def __init__(self, content_generator: Optional[ContentGenerator] = None):
        """
        Initialize template test generator.

        Args:
            content_generator: ContentGenerator instance, creates new one if None
        """
        self.content_generator = content_generator or ContentGenerator(seed=42)
        self.supported_layouts = {
            "Title Slide": self._generate_title_slide,
            "Title and Content": self._generate_title_content,
            "Section Header": self._generate_section_header,
            "Four Columns With Titles": self._generate_four_columns_with_titles,
            "Four Columns": self._generate_four_columns,
            "Three Columns With Titles": self._generate_three_columns_with_titles,
            "Three Columns": self._generate_three_columns,
            "Comparison": self._generate_comparison,
            "Two Content": self._generate_two_content,
            "Picture with Caption": self._generate_picture_with_caption,
            "Title and Vertical Text": self._generate_title_vertical_text,
            "Vertical Title and Text": self._generate_vertical_title_text,
            "Agenda, 6 Textboxes": self._generate_agenda_6_textboxes,
            "Title and 6-item Lists": self._generate_title_6_item_lists,
            "Big Number": self._generate_big_number,
            "SWOT Analysis": self._generate_swot_analysis,
            "Title Only": self._generate_title_only,
            "Blank": self._generate_blank,
            "Content with Caption": self._generate_content_with_caption,
        }

    def generate_test_files(
        self,
        template_json_path: Path,
        output_dir: Path,
        content_type: ContentType = ContentType.BUSINESS,
        content_length: ContentLength = ContentLength.MEDIUM,
    ) -> TestGenerationReport:
        """
        Generate test files from template JSON.

        Args:
            template_json_path: Path to template JSON file
            output_dir: Output directory for generated test files
            content_type: Type of content to generate
            content_length: Length of content to generate

        Returns:
            TestGenerationReport with generation results
        """
        # Load template JSON
        with open(template_json_path, "r", encoding="utf-8") as f:
            template_data = json.load(f)

        template_name = template_data.get("template_info", {}).get("name", "unknown")
        layouts = template_data.get("layouts", {})

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate test files
        generated_files = []
        coverage_report = {}

        # Generate JSON test file
        json_file = self._generate_json_test_file(
            template_name, layouts, output_dir, content_type, content_length
        )
        if json_file:
            generated_files.append(json_file)

        # Generate Markdown test file
        md_file = self._generate_markdown_test_file(
            template_name, layouts, output_dir, content_type, content_length
        )
        if md_file:
            generated_files.append(md_file)

        # Generate coverage report
        for layout_name in layouts.keys():
            coverage_report[layout_name] = layout_name in self.supported_layouts

        return TestGenerationReport(
            template_name=template_name,
            total_layouts=len(layouts),
            generated_files=generated_files,
            coverage_report=coverage_report,
            generation_time=datetime.now(),
        )

    def _generate_json_test_file(
        self,
        template_name: str,
        layouts: Dict[str, Any],
        output_dir: Path,
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Optional[GeneratedTestFile]:
        """Generate JSON test file."""
        slides = []

        # Generate slides for each supported layout
        for layout_name, layout_info in layouts.items():
            if layout_name in self.supported_layouts:
                slide_data = self.supported_layouts[layout_name](
                    layout_name, layout_info, content_type, content_length
                )
                if slide_data:
                    slides.append(slide_data)

        if not slides:
            return None

        # Create presentation structure
        presentation_data = {"presentation": {"slides": slides}}

        # Save JSON file
        json_filename = f"{template_name.lower().replace(' ', '_')}_test.json"
        json_path = output_dir / json_filename

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(presentation_data, f, indent=2, ensure_ascii=False)

        # Create preview
        preview = f"Generated {len(slides)} slides for layouts: {', '.join([s.get('layout', 'Unknown') for s in slides[:3]])}..."

        return GeneratedTestFile(
            file_path=json_path, layout_name="multiple", file_type="json", content_preview=preview
        )

    def _generate_markdown_test_file(
        self,
        template_name: str,
        layouts: Dict[str, Any],
        output_dir: Path,
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Optional[GeneratedTestFile]:
        """Generate Markdown test file with structured frontmatter."""
        markdown_sections = []

        # Generate markdown sections for each supported layout
        for layout_name, layout_info in layouts.items():
            if layout_name in self.supported_layouts:
                md_section = self._generate_markdown_section(
                    layout_name, layout_info, content_type, content_length
                )
                if md_section:
                    markdown_sections.append(md_section)

        if not markdown_sections:
            return None

        # Combine sections
        markdown_content = "\n\n".join(markdown_sections)

        # Save Markdown file
        md_filename = f"{template_name.lower().replace(' ', '_')}_test.md"
        md_path = output_dir / md_filename

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        # Create preview
        preview = f"Generated markdown with {len(markdown_sections)} layout sections"

        return GeneratedTestFile(
            file_path=md_path,
            layout_name="multiple",
            file_type="markdown",
            content_preview=preview,
        )

    def _generate_markdown_section(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> str:
        """Generate markdown section for a layout."""
        # Get structured frontmatter for the layout
        if layout_name in ["Four Columns With Titles", "Four Columns"]:
            return self._generate_columns_markdown(layout_name, 4, content_type, content_length)
        elif layout_name in ["Three Columns With Titles", "Three Columns"]:
            return self._generate_columns_markdown(layout_name, 3, content_type, content_length)
        elif layout_name == "Comparison":
            return self._generate_comparison_markdown(content_type, content_length)
        elif layout_name == "Two Content":
            return self._generate_two_content_markdown(content_type, content_length)
        elif layout_name == "Picture with Caption":
            return self._generate_picture_markdown(content_type, content_length)
        elif layout_name == "Agenda, 6 Textboxes":
            return self._generate_agenda_markdown(content_type, content_length)
        elif layout_name == "SWOT Analysis":
            return self._generate_swot_markdown(content_type, content_length)
        else:
            return self._generate_basic_markdown(layout_name, content_type, content_length)

    def validate_layout_coverage(self, template_json: Dict[str, Any]) -> Dict[str, bool]:
        """Ensure all layouts in template have test coverage."""
        layouts = template_json.get("layouts", {})
        coverage = {}

        for layout_name in layouts.keys():
            coverage[layout_name] = layout_name in self.supported_layouts

        return coverage

    def generate_structured_frontmatter_tests(
        self, layouts: List[str], output_dir: Path
    ) -> List[GeneratedTestFile]:
        """Generate structured frontmatter examples for each layout."""
        generated_files = []

        for layout_name in layouts:
            if layout_name in self.supported_layouts:
                md_content = self._generate_markdown_section(
                    layout_name, {}, ContentType.BUSINESS, ContentLength.MEDIUM
                )

                if md_content:
                    filename = f"{layout_name.lower().replace(' ', '_')}_example.md"
                    file_path = output_dir / filename

                    # Ensure output directory exists
                    file_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(md_content)

                    generated_files.append(
                        GeneratedTestFile(
                            file_path=file_path,
                            layout_name=layout_name,
                            file_type="markdown",
                            content_preview=md_content[:100] + "...",
                        )
                    )

        return generated_files

    # Layout-specific generators for JSON format
    def _generate_title_slide(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Title Slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "layout": layout_name,
            "title": f"**{content_lib['titles'][0]}** with *Formatting*",
            "rich_content": [{"heading": content_lib["content"][0], "level": 2}],
        }

    def _generate_title_content(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Title and Content slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "layout": layout_name,
            "title": f"{content_lib['titles'][0]} with **Bold** and *Italic*",
            "rich_content": [
                {"heading": "Overview", "level": 2},
                {"paragraph": content_lib["content"][0]},
                {
                    "bullets": [
                        f"**{content_lib['bullets'][0]}**",
                        f"*{content_lib['bullets'][1]}*",
                        f"***{content_lib['bullets'][2] if len(content_lib['bullets']) > 2 else 'Enhanced features'}***",
                    ],
                    "bullet_levels": [1, 1, 1],
                },
            ],
        }

    def _generate_four_columns_with_titles(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Four Columns With Titles slide data."""
        columns = self.content_generator.build_column_content(4, content_type, content_length)

        slide_data = {
            "type": layout_name,
            "title": f"{content_type.value.title()} **Feature** Comparison",
        }

        # Add column placeholders using convention-based naming
        for i, column in enumerate(columns, 1):
            slide_data[f"title_col{i}_1"] = self.content_generator.apply_random_formatting(
                column["title"]
            )
            slide_data[f"content_col{i}_1"] = self.content_generator.apply_random_formatting(
                column["content"]
            )

        return slide_data

    def _generate_four_columns(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Four Columns slide data."""
        columns = self.content_generator.build_column_content(4, content_type, content_length)

        slide_data = {
            "type": layout_name,
            "title": f"{content_type.value.title()} Overview",
        }

        # Add column content (no titles)
        for i, column in enumerate(columns, 1):
            slide_data[f"content_col{i}_1"] = self.content_generator.apply_random_formatting(
                column["content"]
            )

        return slide_data

    def _generate_three_columns_with_titles(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Three Columns With Titles slide data."""
        columns = self.content_generator.build_column_content(3, content_type, content_length)

        slide_data = {
            "type": layout_name,
            "title": f"Three-Column {content_type.value.title()} Analysis",
        }

        for i, column in enumerate(columns, 1):
            slide_data[f"title_col{i}_1"] = self.content_generator.apply_random_formatting(
                column["title"]
            )
            slide_data[f"content_col{i}_1"] = self.content_generator.apply_random_formatting(
                column["content"]
            )

        return slide_data

    def _generate_three_columns(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Three Columns slide data."""
        columns = self.content_generator.build_column_content(3, content_type, content_length)

        slide_data = {
            "type": layout_name,
            "title": f"Three-Column {content_type.value.title()} Summary",
        }

        for i, column in enumerate(columns, 1):
            slide_data[f"content_col{i}_1"] = self.content_generator.apply_random_formatting(
                column["content"]
            )

        return slide_data

    def _generate_comparison(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Comparison slide data."""
        comparison = self.content_generator.build_comparison_content("features", content_type)

        return {
            "type": layout_name,
            "title": f"{content_type.value.title()} **Comparison** Analysis",
            "title_left_1": comparison["left"]["title"],
            "content_left_1": self.content_generator.apply_random_formatting(
                comparison["left"]["content"]
            ),
            "title_right_1": comparison["right"]["title"],
            "content_right_1": self.content_generator.apply_random_formatting(
                comparison["right"]["content"]
            ),
        }

    def _generate_two_content(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Two Content slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "title": f"Two-Section {content_type.value.title()} Layout",
            "content_left_1": [
                f"**{content_lib['bullets'][0]}**",
                (
                    f"*{content_lib['bullets'][1]}*"
                    if len(content_lib["bullets"]) > 1
                    else "*Enhanced features*"
                ),
            ],
            "content_right_1": [
                f"***{content_lib['content'][0][:50]}***",
                "___Enhanced capabilities___",
            ],
        }

    def _generate_picture_with_caption(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Picture with Caption slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "title": f"{content_type.value.title()} **Visual** Overview",
            "text_caption_1": f"***{content_lib['titles'][0]}*** visualization",
            "content": self.content_generator.apply_random_formatting(content_lib["content"][0]),
        }

    def _generate_agenda_6_textboxes(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Agenda 6 Textboxes slide data."""
        agenda_items = self.content_generator.generate_agenda_content(6)

        slide_data = {
            "type": layout_name,
            "title": f"**{content_type.value.title()}** Meeting Agenda",
        }

        for i, item in enumerate(agenda_items, 1):
            slide_data[f"number_item{i}_1"] = item["number"]
            slide_data[f"content_item{i}_1"] = self.content_generator.apply_random_formatting(
                item["item"]
            )

        return slide_data

    def _generate_swot_analysis(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate SWOT Analysis slide data."""
        swot = self.content_generator.generate_swot_content()

        return {
            "type": layout_name,
            "title": f"**{content_type.value.title()}** SWOT Analysis",
            "content_16": self.content_generator.apply_random_formatting(swot["strengths"]),
            "content_17": self.content_generator.apply_random_formatting(swot["weaknesses"]),
            "content_18": self.content_generator.apply_random_formatting(swot["opportunities"]),
            "content_19": self.content_generator.apply_random_formatting(swot["threats"]),
        }

    # Additional layout generators...
    def _generate_section_header(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Section Header slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "layout": layout_name,
            "title": f"Section: **{content_lib['titles'][0]}**",
            "rich_content": [
                {
                    "paragraph": self.content_generator.apply_random_formatting(
                        content_lib["content"][0]
                    )
                }
            ],
        }

    def _generate_title_only(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Title Only slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "layout": layout_name,
            "title": f"**{content_lib['titles'][0]}** with ***Emphasis***",
        }

    def _generate_blank(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Blank slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "layout": layout_name,
            "rich_content": [
                {"heading": "Blank Layout Test", "level": 1},
                {
                    "paragraph": self.content_generator.apply_random_formatting(
                        content_lib["content"][0]
                    )
                },
            ],
        }

    def _generate_content_with_caption(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Content with Caption slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "layout": layout_name,
            "title": f"{content_type.value.title()} Content with Caption",
            "text_caption_1": self.content_generator.apply_random_formatting(
                content_lib["titles"][0]
            ),
            "rich_content": [{"paragraph": content_lib["content"][0]}],
        }

    def _generate_title_vertical_text(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Title and Vertical Text slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "layout": layout_name,
            "title": f"**{content_lib['titles'][0]}** Vertical Layout",
            "content_1": self.content_generator.apply_random_formatting(content_lib["content"][0]),
        }

    def _generate_vertical_title_text(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Vertical Title and Text slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return {
            "type": layout_name,
            "layout": layout_name,
            "title_top_1": content_lib["titles"][0],
            "content_1": self.content_generator.apply_random_formatting(content_lib["content"][0]),
        }

    def _generate_title_6_item_lists(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Title and 6-item Lists slide data."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        slide_data = {
            "type": layout_name,
            "title": f"**{content_type.value.title()}** Feature Lists",
        }

        # Generate 6 list items
        for i in range(1, 7):
            slide_data[f"number_item{i}_1"] = f"{i:02d}"
            title_idx = (i - 1) % len(content_lib["titles"])
            content_idx = (i - 1) % len(content_lib["bullets"])
            slide_data[f"content_{12 + i}_1"] = self.content_generator.apply_random_formatting(
                content_lib["titles"][title_idx]
            )
            slide_data[f"content_item{i}_1"] = self.content_generator.apply_random_formatting(
                content_lib["bullets"][content_idx]
            )

        return slide_data

    def _generate_big_number(
        self,
        layout_name: str,
        layout_info: Dict[str, Any],
        content_type: ContentType,
        content_length: ContentLength,
    ) -> Dict[str, Any]:
        """Generate Big Number slide data."""
        # content_lib = self.content_generator.get_content_library(content_type)[content_length]  # Future: use for content

        return {
            "type": layout_name,
            "layout": layout_name,
            "title": "**42%**",
            "content_1": f"Improvement in *{content_type.value}* with ___enhanced___ capabilities",
        }

    # Markdown generation methods
    def _generate_columns_markdown(
        self,
        layout_name: str,
        num_columns: int,
        content_type: ContentType,
        content_length: ContentLength,
    ) -> str:
        """Generate markdown for column layouts."""
        columns = self.content_generator.build_column_content(
            num_columns, content_type, content_length
        )

        frontmatter = {
            "layout": layout_name,
            "title": f"{content_type.value.title()} Feature Overview",
            "columns": [],
        }

        for column in columns:
            col_data = {"content": column["content"]}
            if "With Titles" in layout_name:
                col_data["title"] = column["title"]
                frontmatter["columns"].append(col_data)
            else:
                frontmatter["columns"].append(col_data)

        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        return f"---\n{yaml_str}---\n\nContent from {layout_name} structured frontmatter above."

    def _generate_comparison_markdown(
        self, content_type: ContentType, content_length: ContentLength
    ) -> str:
        """Generate markdown for comparison layout."""
        comparison = self.content_generator.build_comparison_content("features", content_type)

        frontmatter = {
            "layout": "Comparison",
            "title": f"{content_type.value.title()} Solution Analysis",
            "comparison": {"left": comparison["left"], "right": comparison["right"]},
        }

        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        return f"---\n{yaml_str}---\n\nContent from Comparison structured frontmatter above."

    def _generate_two_content_markdown(
        self, content_type: ContentType, content_length: ContentLength
    ) -> str:
        """Generate markdown for two content layout."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        frontmatter = {
            "layout": "Two Content",
            "title": f"{content_type.value.title()} Dual Analysis",
            "sections": [
                {
                    "title": "Primary Focus",
                    "content": [content_lib["bullets"][0], content_lib["content"][0][:50]],
                },
                {
                    "title": "Secondary Focus",
                    "content": [
                        (
                            content_lib["bullets"][1]
                            if len(content_lib["bullets"]) > 1
                            else "Enhanced features"
                        ),
                        (
                            content_lib["content"][1]
                            if len(content_lib["content"]) > 1
                            else "Additional benefits"
                        ),
                    ],
                },
            ],
        }

        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        return f"---\n{yaml_str}---\n\nContent from Two Content structured frontmatter above."

    def _generate_picture_markdown(
        self, content_type: ContentType, content_length: ContentLength
    ) -> str:
        """Generate markdown for picture layout."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        frontmatter = {
            "layout": "Picture with Caption",
            "title": f"{content_type.value.title()} Visual Analysis",
            "media": {
                "caption": f"{content_lib['titles'][0]} visualization",
                "description": content_lib["content"][0],
            },
        }

        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        return (
            f"---\n{yaml_str}---\n\nContent from Picture with Caption structured frontmatter above."
        )

    def _generate_agenda_markdown(
        self, content_type: ContentType, content_length: ContentLength
    ) -> str:
        """Generate markdown for agenda layout."""
        agenda_items = self.content_generator.generate_agenda_content(6)

        frontmatter = {
            "layout": "Agenda, 6 Textboxes",
            "title": f"{content_type.value.title()} Meeting Agenda",
            "agenda": [{"number": item["number"], "item": item["item"]} for item in agenda_items],
        }

        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        return (
            f"---\n{yaml_str}---\n\nContent from Agenda, 6 Textboxes structured frontmatter above."
        )

    def _generate_swot_markdown(
        self, content_type: ContentType, content_length: ContentLength
    ) -> str:
        """Generate markdown for SWOT layout."""
        swot = self.content_generator.generate_swot_content()

        frontmatter = {
            "layout": "SWOT Analysis",
            "title": f"{content_type.value.title()} SWOT Analysis",
            "swot": swot,
        }

        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        return f"---\n{yaml_str}---\n\nContent from SWOT Analysis structured frontmatter above."

    def _generate_basic_markdown(
        self, layout_name: str, content_type: ContentType, content_length: ContentLength
    ) -> str:
        """Generate basic markdown for simple layouts."""
        content_lib = self.content_generator.get_content_library(content_type)[content_length]

        return f"""---
layout: {layout_name}
---
# {content_lib['titles'][0]}

{content_lib['content'][0]}

Additional content for {layout_name} layout testing."""


# Convenience functions
def generate_test_files_for_template(
    template_path: Path, output_dir: Path, content_type: ContentType = ContentType.BUSINESS
) -> TestGenerationReport:
    """Convenience function to generate test files for a template."""
    generator = TemplateTestGenerator()
    return generator.generate_test_files(template_path, output_dir, content_type)


def validate_template_coverage(template_path: Path) -> Dict[str, bool]:
    """Convenience function to validate template layout coverage."""
    with open(template_path, "r") as f:
        template_data = json.load(f)

    generator = TemplateTestGenerator()
    return generator.validate_layout_coverage(template_data)
