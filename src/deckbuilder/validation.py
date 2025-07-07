#!/usr/bin/env python3
"""
Built-in End-to-End Validation System for Deckbuilder

Provides automatic validation that runs on every presentation generation to prevent
layout regressions and ensure JSON ↔ Template ↔ PPTX alignment.

GitHub Issue: https://github.com/teknologika/Deckbuilder/issues/36
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from pptx import Presentation


class ValidationError(Exception):
    """Validation error with detailed fix instructions."""

    def __init__(
        self, message: str, slide_num: Optional[int] = None, field_name: Optional[str] = None
    ):
        self.slide_num = slide_num
        self.field_name = field_name
        super().__init__(message)


class PresentationValidator:
    """
    Built-in validation system that runs automatically on every presentation generation.

    Prevents layout regressions by validating:
    1. Pre-generation: JSON ↔ Template mapping alignment
    2. Post-generation: PPTX output ↔ JSON input verification
    """

    def __init__(self, presentation_data: Dict[str, Any], template_name: str, template_folder: str):
        self.presentation_data = presentation_data
        self.template_name = template_name
        self.template_folder = Path(template_folder)
        self.template_mapping = self._load_template_mapping()

    def _load_template_mapping(self) -> Dict[str, Any]:
        """Load template mapping JSON file."""
        mapping_file = self.template_folder / f"{self.template_name}.json"
        if not mapping_file.exists():
            raise ValidationError(
                f"Template mapping file not found: {mapping_file}\n"
                f"Fix: Create {self.template_name}.json in {self.template_folder}"
            )

        with open(mapping_file, "r") as f:
            return json.load(f)

    def validate_markdown_to_json(self, markdown_content: str, converted_json: Dict[str, Any]):
        """
        Validate Markdown → JSON conversion before template validation.

        Ensures structured frontmatter is properly converted and no data is lost.
        """
        print("🔍 Markdown → JSON validation: Frontmatter processing...")

        # Parse markdown sections manually to validate conversion
        markdown_sections = self._parse_markdown_sections(markdown_content)
        json_slides = converted_json.get("slides", [])

        # Validate slide count matches
        if len(markdown_sections) != len(json_slides):
            raise ValidationError(
                f"Markdown → JSON conversion error: {len(markdown_sections)} markdown sections "
                f"converted to {len(json_slides)} JSON slides\n"
                f"Fix: Check markdown section parsing and frontmatter conversion"
            )

        # Validate each section conversion
        for section_idx, (md_section, json_slide) in enumerate(zip(markdown_sections, json_slides)):
            self._validate_section_conversion(section_idx + 1, md_section, json_slide)

        print("✅ Markdown → JSON validation passed")

    def validate_pre_generation(self):
        """
        Validate JSON ↔ Template mapping alignment before generation.

        Raises ValidationError immediately on any mapping issues.
        """
        print("🔍 JSON → Template validation: Mapping alignment...")

        # Debug: Show template mapping structure
        print(f"[Validation] Template mapping loaded: {self.template_name}.json")
        layouts = self.template_mapping.get("layouts", {})
        print(f"[Validation] Available layouts: {list(layouts.keys())}")
        print(f"[Validation] Validating {len(self.presentation_data.get('slides', []))} slides")

        # Validate each slide's placeholders can be mapped
        for slide_idx, slide_data in enumerate(self.presentation_data.get("slides", [])):
            slide_num = slide_idx + 1
            layout_name = slide_data.get("layout")

            print(f"[Validation] Slide {slide_num}: Checking layout '{layout_name}'")

            if not layout_name:
                raise ValidationError(
                    f"Slide {slide_num}: Missing 'layout' field\n"
                    f"Fix: Add 'layout' field with valid layout name"
                )

            # Check layout exists in template mapping
            layouts = self.template_mapping.get("layouts", {})
            if layout_name not in layouts:
                available_layouts = list(layouts.keys())
                print(f"[Validation] ERROR: Layout '{layout_name}' not found in template mapping")
                raise ValidationError(
                    f"Slide {slide_num}: Unknown layout '{layout_name}'\n"
                    f"Available layouts: {', '.join(available_layouts)}\n"
                    f"Fix: Use one of the available layouts or update template mapping"
                )

            # Show slide content fields for debugging
            placeholders = slide_data.get("placeholders", {})
            content_blocks = slide_data.get("content", [])
            print(f"[Validation]   Placeholder fields: {list(placeholders.keys())}")
            print(f"[Validation]   Content blocks: {len(content_blocks)}")

            # Validate placeholder mappings
            self._validate_slide_placeholders(slide_num, slide_data, layout_name)

        print("✅ Pre-generation validation passed")

    def _validate_slide_placeholders(
        self, slide_num: int, slide_data: Dict[str, Any], layout_name: str
    ):
        """Validate that all placeholders in slide can be mapped to template."""
        layout_info = self.template_mapping["layouts"][layout_name]
        placeholder_mappings = layout_info.get("placeholders", {})

        print(f"[Validation]   Template placeholders for '{layout_name}': {placeholder_mappings}")

        # Create reverse mapping: field_name -> placeholder_index
        field_to_index = {}
        for placeholder_idx, field_name in placeholder_mappings.items():
            field_to_index[field_name] = int(placeholder_idx)

        print(f"[Validation]   Field-to-index mapping: {field_to_index}")

        # Check all placeholder fields in slide data
        placeholders = slide_data.get("placeholders", {})
        unmapped_fields = []
        mapped_fields = []

        for field_name in placeholders.keys():
            if field_name in ["style"]:  # Skip non-content fields
                continue

            # Check if field can be resolved
            if self._can_resolve_field_name(field_name, field_to_index):
                mapped_fields.append(field_name)
                print(f"[Validation]     ✓ '{field_name}' can be mapped")
            else:
                unmapped_fields.append(field_name)
                print(f"[Validation]     ✗ '{field_name}' cannot be mapped")

        if unmapped_fields:
            available_fields = list(field_to_index.keys())
            print(f"[Validation] ERROR: Unmapped fields found for slide {slide_num}")
            raise ValidationError(
                f"Slide {slide_num} ({layout_name}): Cannot map placeholder fields: {', '.join(unmapped_fields)}\n"
                f"Available template fields: {', '.join(available_fields)}\n"
                f"Fix: Update template mapping to include these fields or correct field names in JSON"
            )

    def _can_resolve_field_name(self, field_name: str, field_to_index: Dict[str, int]) -> bool:
        """
        STRICT validation - check if field name can be resolved.

        Validation must be strict and fail if there's no exact match.
        The engine will handle flexible resolution, but validation catches mismatches.
        """
        # Direct match only
        if field_name in field_to_index:
            return True

        # Only allow semantic fields that are always handled
        if field_name in ["title", "subtitle"]:
            return True  # Always handled by semantic detection

        # STRICT: No flexible matching in validation
        return False

    def validate_post_generation(self, pptx_file_path: str):
        """
        Validate PPTX output ↔ JSON input after generation.

        Raises ValidationError if generated content doesn't match specification.
        """
        print("🔍 Post-generation validation: PPTX ↔ JSON verification...")
        print(f"[Validation] Loading generated PPTX: {pptx_file_path}")

        if not Path(pptx_file_path).exists():
            raise ValidationError(f"Generated PPTX file not found: {pptx_file_path}")

        # Load generated presentation
        prs = Presentation(pptx_file_path)

        # Validate slide count
        expected_slides = len(self.presentation_data.get("slides", []))
        actual_slides = len(prs.slides)

        print(f"[Validation] Slide count check: expected={expected_slides}, actual={actual_slides}")

        if actual_slides != expected_slides:
            raise ValidationError(
                f"Slide count mismatch: expected {expected_slides}, got {actual_slides}\n"
                f"Fix: Check slide generation logic for dropped or duplicated slides"
            )

        # Validate each slide content
        validation_errors = []
        print(f"[Validation] Validating content for {actual_slides} slides...")

        for slide_idx, (slide, slide_spec) in enumerate(
            zip(prs.slides, self.presentation_data["slides"])
        ):
            slide_num = slide_idx + 1
            layout_name = slide_spec.get("layout", "unknown")
            print(f"[Validation] Slide {slide_num} ({layout_name}): Starting content validation")

            try:
                self._validate_slide_content(slide_num, slide, slide_spec)
                print(f"[Validation] Slide {slide_num}: ✓ Content validation passed")
            except ValidationError as e:
                print(f"[Validation] Slide {slide_num}: ✗ Content validation failed")
                validation_errors.append(str(e))

        if validation_errors:
            error_summary = "\n".join(validation_errors)
            raise ValidationError(
                f"Post-generation validation failed:\n{error_summary}\n"
                f"Fix: Check placeholder mapping logic in slide_builder.py"
            )

        print("✅ Post-generation validation passed")

    def _validate_slide_content(self, slide_num: int, slide, slide_spec: Dict[str, Any]):
        """Validate individual slide content against specification."""
        layout_name = slide_spec["layout"]
        actual_layout = slide.slide_layout.name

        # Validate layout
        if actual_layout != layout_name:
            raise ValidationError(
                f"Slide {slide_num}: Layout mismatch - expected '{layout_name}', got '{actual_layout}'"
            )

        # Validate critical placeholders are not empty
        self._validate_critical_placeholders(slide_num, slide, slide_spec)

        # Validate content blocks are processed
        self._validate_content_blocks(slide_num, slide, slide_spec)

    def _validate_critical_placeholders(self, slide_num: int, slide, slide_spec: Dict[str, Any]):
        """Validate that critical placeholders have content."""
        placeholders_spec = slide_spec.get("placeholders", {})
        layout_name = slide_spec["layout"]

        print(f"[Validation]   Expected placeholders: {list(placeholders_spec.keys())}")

        # Get actual placeholder content
        actual_content = {}
        all_placeholders = {}  # Track all placeholders for debugging

        for shape in slide.shapes:
            try:
                if hasattr(shape, "placeholder_format") and shape.placeholder_format:
                    ph_type = shape.placeholder_format.type
                    ph_idx = shape.placeholder_format.idx
                    try:
                        ph_name = getattr(shape.element.nvSpPr.cNvPr, "name", "unnamed")
                    except AttributeError:
                        ph_name = "unnamed"

                    content = self._extract_shape_text(shape)
                    semantic_type = self._get_semantic_type(ph_type)

                    # Track all placeholders
                    all_placeholders[f"{semantic_type}_{ph_idx}"] = {
                        "content": content,
                        "name": ph_name,
                        "has_content": bool(content.strip()),
                    }

                    if content.strip():  # Only count non-empty content
                        actual_content[f"{semantic_type}_{ph_idx}"] = content
            except ValueError:
                continue

        print("[Validation]   Found placeholders in slide:")
        for ph_key, ph_info in all_placeholders.items():
            status = "✓ HAS CONTENT" if ph_info["has_content"] else "✗ EMPTY"
            print(f"[Validation]     {ph_key} ('{ph_info['name']}'): {status}")
            if ph_info["has_content"]:
                print(
                    f"[Validation]       Content: '{ph_info['content'][:50]}{'...' if len(ph_info['content']) > 50 else ''}'"
                )

        print(f"[Validation]   Non-empty placeholders: {list(actual_content.keys())}")

        # Check critical fields that should have content
        critical_missing = []
        print("[Validation]   Checking critical field mappings:")

        for field_name, expected_content in placeholders_spec.items():
            if field_name in ["style"]:  # Skip non-content fields
                continue

            if not expected_content or str(expected_content).strip() == "":
                print(f"[Validation]     '{field_name}': SKIPPED (empty expected content)")
                continue  # Skip empty expected content

            # Check if this field has corresponding content in PPTX
            found_content = False
            expected_clean = self._strip_formatting_markers(str(expected_content))
            print(
                f"[Validation]     '{field_name}': Looking for '{expected_clean[:30]}{'...' if len(expected_clean) > 30 else ''}'"
            )

            for ph_key, actual_text in actual_content.items():
                if expected_clean.lower() in actual_text.lower():
                    found_content = True
                    print(f"[Validation]       ✓ FOUND in {ph_key}")
                    break

            if not found_content:
                print("[Validation]       ✗ NOT FOUND in any placeholder")
                critical_missing.append(f"{field_name} (expected: '{expected_clean[:30]}...')")

        # Special validation for vertical layouts
        if "vertical" in layout_name.lower():
            content_found = any(
                "content" in key.lower() or "body" in key.lower() for key in actual_content.keys()
            )
            if not content_found and placeholders_spec.get("content"):
                critical_missing.append("content (vertical layout missing main content)")

        if critical_missing:
            raise ValidationError(
                f"Slide {slide_num} ({layout_name}): Missing critical content: {', '.join(critical_missing)}"
            )

    def _validate_content_blocks(self, slide_num: int, slide, slide_spec: Dict[str, Any]):
        """Validate that content blocks are properly processed."""
        expected_content_blocks = slide_spec.get("content", [])

        print(
            f"[Validation]   Content blocks validation: {len(expected_content_blocks)} blocks expected"
        )

        if not expected_content_blocks:
            print("[Validation]     No content blocks to validate")
            return  # No content blocks expected

        # Check for tables
        expected_tables = sum(
            1 for block in expected_content_blocks if block.get("type") == "table"
        )
        actual_tables = sum(1 for shape in slide.shapes if hasattr(shape, "table"))

        print(
            f"[Validation]     Table validation: expected={expected_tables}, actual={actual_tables}"
        )

        if expected_tables > 0 and actual_tables == 0:
            print("[Validation]     ✗ Table content missing")
            raise ValidationError(
                f"Slide {slide_num}: Expected {expected_tables} table(s), found 0"
            )

        # Check for content blocks in placeholders
        content_blocks_text = [
            block.get("text", "")
            for block in expected_content_blocks
            if block.get("type") != "table" and block.get("text")
        ]

        print(f"[Validation]     Text content blocks to validate: {len(content_blocks_text)}")

        if content_blocks_text:
            found_content_text = []
            for shape in slide.shapes:
                text = self._extract_shape_text(shape)
                if text:
                    found_content_text.append(text)

            print(f"[Validation]     Actual text content found in {len(found_content_text)} shapes")

            # Check if key content from blocks appears somewhere in slide
            missing_content = []
            for i, expected_text in enumerate(content_blocks_text):
                expected_clean = self._strip_formatting_markers(expected_text)
                print(
                    f"[Validation]       Block {i + 1}: Looking for '{expected_clean[:30]}{'...' if len(expected_clean) > 30 else ''}'"
                )

                found = any(
                    expected_clean.lower() in actual_text.lower()
                    for actual_text in found_content_text
                )

                if found:
                    print("[Validation]         ✓ FOUND in slide content")
                else:
                    print("[Validation]         ✗ NOT FOUND in slide content")
                    missing_content.append(expected_clean[:30] + "...")

            if missing_content:
                print("[Validation]     ✗ Missing content blocks detected")
                raise ValidationError(
                    f"Slide {slide_num}: Missing content blocks: {', '.join(missing_content)}"
                )
            else:
                print("[Validation]     ✓ All content blocks found")

    def _extract_shape_text(self, shape) -> str:
        """Extract all text from a shape."""
        text_parts = []

        if hasattr(shape, "text") and shape.text.strip():
            text_parts.append(shape.text.strip())
        elif hasattr(shape, "text_frame") and shape.text_frame:
            for paragraph in shape.text_frame.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text.strip())

        return "\n".join(text_parts)

    def _get_semantic_type(self, ph_type) -> str:
        """Get semantic type name for a placeholder."""
        return ph_type.name if hasattr(ph_type, "name") else str(ph_type)

    def _strip_formatting_markers(self, text: str) -> str:
        """Remove formatting markers from text for comparison."""
        # Remove formatting markers
        text = re.sub(r"\*\*\*(.*?)\*\*\*", r"\1", text)  # ***bold italic***
        text = re.sub(r"___(.*?)___", r"\1", text)  # ___underline___
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # **bold**
        text = re.sub(r"\*(.*?)\*", r"\1", text)  # *italic*
        return text.strip()

    def _parse_markdown_sections(self, markdown_content: str) -> List[Dict[str, Any]]:
        """Parse markdown into sections with frontmatter and content."""
        import yaml

        # Split by frontmatter delimiters
        sections = []
        blocks = re.split(r"^---\s*$", markdown_content, flags=re.MULTILINE)

        i = 0
        while i < len(blocks):
            # Skip empty blocks
            if not blocks[i].strip():
                i += 1
                continue

            # Look for frontmatter + content pairs
            if i + 1 < len(blocks):
                try:
                    frontmatter_raw = blocks[i].strip()
                    content_raw = blocks[i + 1].strip() if i + 1 < len(blocks) else ""

                    # Parse frontmatter
                    frontmatter = yaml.safe_load(frontmatter_raw) or {}

                    sections.append(
                        {
                            "frontmatter": frontmatter,
                            "content": content_raw,
                            "raw_frontmatter": frontmatter_raw,
                        }
                    )

                    i += 2
                except yaml.YAMLError as e:
                    raise ValidationError(
                        f"YAML parsing error in markdown frontmatter: {e}\n"
                        f"Fix: Check YAML syntax in frontmatter section"
                    )
            else:
                i += 1

        return sections

    def _validate_section_conversion(
        self, section_num: int, md_section: Dict[str, Any], json_slide: Dict[str, Any]
    ):
        """Validate individual section conversion from markdown to JSON."""
        frontmatter = md_section["frontmatter"]

        # Validate layout field conversion
        expected_layout = frontmatter.get("layout")
        actual_layout = json_slide.get("layout")

        if expected_layout != actual_layout:
            raise ValidationError(
                f"Section {section_num}: Layout conversion failed\n"
                f"Markdown layout: '{expected_layout}'\n"
                f"JSON layout: '{actual_layout}'\n"
                f"Fix: Check frontmatter to JSON conversion logic"
            )

        # Validate critical frontmatter fields are preserved
        critical_fields = ["title", "layout"]
        for field in critical_fields:
            if field in frontmatter:
                # Check if field appears in JSON placeholders
                json_placeholders = json_slide.get("placeholders", {})
                if field not in json_placeholders and field != "layout":
                    raise ValidationError(
                        f"Section {section_num}: Frontmatter field '{field}' not found in JSON placeholders\n"
                        f"Markdown value: '{frontmatter[field]}'\n"
                        f"Fix: Check structured frontmatter conversion logic"
                    )
