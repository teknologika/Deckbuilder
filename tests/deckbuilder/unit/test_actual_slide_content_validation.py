#!/usr/bin/env python3
"""
Actual Slide Content Validation Tests

These tests validate that content is ACTUALLY placed in PowerPoint slides
by examining the generated .pptx files with python-pptx.

This addresses the critical issue where tests pass but slides are blank.
"""

import json
import secrets
import shutil
import sys
import tempfile
from pathlib import Path

import pytest
from pptx import Presentation

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from deckbuilder.engine import Deckbuilder  # noqa: E402


class TestActualSlideContentValidation:
    """Test that content actually appears in PowerPoint slides"""

    def setup_method(self):
        """Setup for each test"""
        self.temp_dir = tempfile.mkdtemp()

    def _create_unique_test_dir(self) -> Path:
        """Create unique test directory with random 6-character hex string."""
        hex_id = secrets.token_hex(3)  # 3 bytes = 6 hex characters
        test_dir = Path(self.temp_dir) / f"test_{hex_id}"
        test_dir.mkdir(parents=True, exist_ok=True)
        return test_dir

    def teardown_method(self):
        """Cleanup after each test"""
        if Path(self.temp_dir).exists():
            import shutil

            shutil.rmtree(self.temp_dir)

    def _validate_slide_content(self, pptx_path: Path, expected_content: dict) -> dict:
        """
        Validate that specific content appears in slides.

        Args:
            pptx_path: Path to generated PowerPoint file
            expected_content: Dict mapping slide_index -> expected_text_list

        Returns:
            Dict with validation results
        """
        if not pptx_path.exists():
            return {"error": f"PPTX file not found: {pptx_path}"}

        prs = Presentation(str(pptx_path))
        results = {"total_slides": len(prs.slides), "slides": {}, "errors": []}

        for slide_idx, slide in enumerate(prs.slides):
            slide_text = []
            has_content = False

            # Extract all text from slide
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text.strip())
                    has_content = True
                elif hasattr(shape, "text_frame") and shape.text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        if paragraph.text.strip():
                            slide_text.append(paragraph.text.strip())
                            has_content = True

            # Check expected content
            found_expected = []
            missing_expected = []

            if slide_idx in expected_content:
                for expected_text in expected_content[slide_idx]:
                    found = any(expected_text.lower() in text.lower() for text in slide_text)
                    if found:
                        found_expected.append(expected_text)
                    else:
                        missing_expected.append(expected_text)

            results["slides"][slide_idx] = {
                "has_content": has_content,
                "text": slide_text,
                "found_expected": found_expected,
                "missing_expected": missing_expected,
            }

            # Add errors for missing content
            if slide_idx in expected_content and missing_expected:
                results["errors"].append(f"Slide {slide_idx + 1}: Missing {missing_expected}")

        return results

    def test_simple_json_content_appears_in_slides(self):
        """Test that simple JSON content actually appears in PowerPoint slides"""

        json_data = {
            "presentation": {
                "slides": [
                    {
                        "type": "Title Slide",
                        "title": "TEST_TITLE_UNIQUE_123",
                        "subtitle": "TEST_SUBTITLE_UNIQUE_456",
                    },
                    {
                        "type": "Title and Content",
                        "title": "CONTENT_TITLE_UNIQUE_789",
                        "content": "TEST_CONTENT_UNIQUE_ABC",
                    },
                ]
            }
        }

        # Create JSON file
        json_file = Path(self.temp_dir) / "simple_test.json"
        with open(json_file, "w") as f:
            json.dump(json_data, f)

        # Generate presentation using engine directly in unique directory
        test_dir = self._create_unique_test_dir()
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(test_dir)
            db = Deckbuilder()
            result = db.create_presentation_from_json(
                json_data=json_data, fileName="simple_test", templateName="default"
            )

            # Find generated file - look for .g.pptx first (what engine creates)
            output_files = list(Path(".").glob("*.g.pptx"))
            if not output_files:
                output_files = list(Path(".").glob("*.pptx"))
            assert len(output_files) > 0, f"No output file generated. Result: {result}. Files in dir: {list(Path('.').iterdir())}"

            pptx_path = output_files[0].absolute()
        finally:
            os.chdir(original_cwd)

        # Define expected content
        expected_content = {
            0: ["TEST_TITLE_UNIQUE_123", "TEST_SUBTITLE_UNIQUE_456"],  # Title slide
            1: ["CONTENT_TITLE_UNIQUE_789", "TEST_CONTENT_UNIQUE_ABC"],  # Content slide
        }

        # Validate content
        validation = self._validate_slide_content(pptx_path, expected_content)

        # Print detailed results
        print("\n📊 SLIDE CONTENT VALIDATION RESULTS:")
        print(f"Total slides: {validation['total_slides']}")

        for slide_idx, slide_data in validation["slides"].items():
            print(f"\n🖼️ SLIDE {slide_idx + 1}:")
            print(f"  Has content: {'✅' if slide_data['has_content'] else '❌'}")
            print(f"  Text found: {slide_data['text']}")
            print(f"  Expected found: {slide_data['found_expected']}")
            if slide_data["missing_expected"]:
                print(f"  ❌ Missing: {slide_data['missing_expected']}")

        if validation["errors"]:
            print("\n❌ VALIDATION ERRORS:")
            for error in validation["errors"]:
                print(f"  - {error}")

        # File will be cleaned up with temp directory

        # Assertions
        assert (
            validation["total_slides"] == 2
        ), f"Expected 2 slides, got {validation['total_slides']}"
        assert len(validation["errors"]) == 0, f"Content validation failed: {validation['errors']}"

        # Verify each slide has content
        for slide_idx in [0, 1]:
            assert validation["slides"][slide_idx][
                "has_content"
            ], f"Slide {slide_idx + 1} has no content"
            assert (
                len(validation["slides"][slide_idx]["missing_expected"]) == 0
            ), f"Slide {slide_idx + 1} missing expected content: {validation['slides'][slide_idx]['missing_expected']}"

    def test_semantic_field_names_content_appears(self):
        """Test that semantic field names actually place content in slides"""

        json_data = {
            "presentation": {
                "slides": [
                    {
                        "type": "Two Content",
                        "title": "TWO_CONTENT_TITLE_UNIQUE_999",
                        "content_left": "LEFT_CONTENT_UNIQUE_111",
                        "content_right": "RIGHT_CONTENT_UNIQUE_222",
                    }
                ]
            }
        }

        # Generate presentation in unique directory
        test_dir = self._create_unique_test_dir()
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(test_dir)
            db = Deckbuilder()
            result = db.create_presentation_from_json(
                json_data=json_data, fileName="semantic_test", templateName="default"
            )

            # Find generated file - look for timestamped version
            output_files = list(Path(".").glob("semantic_test*.pptx"))
            if not output_files:
                output_files = list(Path(".").glob("semantic_test*.g.pptx"))
            assert len(output_files) > 0, f"No output file generated. Result: {result}"

            pptx_path = output_files[0].absolute()
        finally:
            os.chdir(original_cwd)

        # Define expected content
        expected_content = {
            0: [
                "TWO_CONTENT_TITLE_UNIQUE_999",
                "LEFT_CONTENT_UNIQUE_111",
                "RIGHT_CONTENT_UNIQUE_222",
            ]
        }

        # Validate content
        validation = self._validate_slide_content(pptx_path, expected_content)

        # Print results
        print("\n📊 SEMANTIC FIELD VALIDATION:")
        for slide_idx, slide_data in validation["slides"].items():
            print(f"Slide {slide_idx + 1}: {slide_data['text']}")
            if slide_data["missing_expected"]:
                print(f"❌ Missing: {slide_data['missing_expected']}")

        # File will be cleaned up with temp directory

        # Assertions
        assert (
            validation["total_slides"] == 1
        ), f"Expected 1 slide, got {validation['total_slides']}"
        assert (
            len(validation["errors"]) == 0
        ), f"Semantic field validation failed: {validation['errors']}"
        assert validation["slides"][0]["has_content"], "Slide has no content"

    def test_rich_content_blocks_appear_in_slides(self):
        """Test that rich content blocks actually appear in PowerPoint slides"""

        json_data = {
            "presentation": {
                "slides": [
                    {
                        "type": "Title and Content",
                        "title": "RICH_CONTENT_TITLE_UNIQUE_888",
                        "rich_content": [
                            {"heading": "HEADING_UNIQUE_777", "level": 2},
                            {"paragraph": "PARAGRAPH_UNIQUE_666"},
                            {"bullets": ["BULLET_UNIQUE_555", "BULLET_UNIQUE_444"]},
                        ],
                    }
                ]
            }
        }

        # Generate presentation in unique directory
        test_dir = self._create_unique_test_dir()
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(test_dir)
            db = Deckbuilder()
            result = db.create_presentation_from_json(
                json_data=json_data, fileName="rich_content_test", templateName="default"
            )

            # Find generated file - look for timestamped version
            output_files = list(Path(".").glob("rich_content_test*.pptx"))
            if not output_files:
                output_files = list(Path(".").glob("rich_content_test*.g.pptx"))
            assert len(output_files) > 0, f"No output file generated. Result: {result}"

            pptx_path = output_files[0].absolute()
        finally:
            os.chdir(original_cwd)

        # Define expected content
        expected_content = {
            0: [
                "RICH_CONTENT_TITLE_UNIQUE_888",
                "HEADING_UNIQUE_777",
                "PARAGRAPH_UNIQUE_666",
                "BULLET_UNIQUE_555",
                "BULLET_UNIQUE_444",
            ]
        }

        # Validate content
        validation = self._validate_slide_content(pptx_path, expected_content)

        # Print results
        print("\n📊 RICH CONTENT VALIDATION:")
        for slide_idx, slide_data in validation["slides"].items():
            print(f"Slide {slide_idx + 1}: {slide_data['text']}")
            if slide_data["missing_expected"]:
                print(f"❌ Missing: {slide_data['missing_expected']}")

        # File will be cleaned up with temp directory

        # Assertions
        assert (
            validation["total_slides"] == 1
        ), f"Expected 1 slide, got {validation['total_slides']}"
        assert (
            len(validation["errors"]) == 0
        ), f"Rich content validation failed: {validation['errors']}"
        assert validation["slides"][0]["has_content"], "Slide has no content"

    def test_comprehensive_layouts_file_content_appears(self):
        """Test that the comprehensive layouts golden file actually produces content"""

        # Load the actual comprehensive layouts file
        golden_json_path = Path(__file__).parent.parent / "test_comprehensive_layouts.json"

        with open(golden_json_path, "r") as f:
            json_data = json.load(f)

        # Generate presentation in unique directory
        test_dir = self._create_unique_test_dir()
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(test_dir)
            db = Deckbuilder()
            result = db.create_presentation_from_json(
                json_data=json_data, fileName="comprehensive_test", templateName="default"
            )

            # Find generated file - look for timestamped version
            output_files = list(Path(".").glob("comprehensive_test*.pptx"))
            if not output_files:
                output_files = list(Path(".").glob("comprehensive_test*.g.pptx"))
            assert len(output_files) > 0, f"No output file generated. Result: {result}"

            pptx_path = output_files[0].absolute()
        finally:
            os.chdir(original_cwd)
        prs = Presentation(str(pptx_path))

        print("\n📊 COMPREHENSIVE LAYOUTS VALIDATION:")
        print(f"Total slides: {len(prs.slides)}")

        content_slides = 0
        blank_slides = 0

        # Check first 5 slides for content
        for i in range(min(5, len(prs.slides))):
            slide = prs.slides[i]
            slide_text = []
            has_content = False

            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    slide_text.append(shape.text.strip())
                    has_content = True
                elif hasattr(shape, "text_frame") and shape.text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        if paragraph.text.strip():
                            slide_text.append(paragraph.text.strip())
                            has_content = True

            if has_content:
                content_slides += 1
                print(f"✅ Slide {i + 1}: {slide_text[:2]}...")  # Show first 2 text items
            else:
                blank_slides += 1
                print(f"❌ Slide {i + 1}: NO CONTENT")

        # File will be cleaned up with temp directory

        # The comprehensive layouts should have content on most slides
        assert (
            content_slides > blank_slides
        ), f"Too many blank slides: {blank_slides} blank vs {content_slides} with content"
        assert content_slides >= 3, f"Expected at least 3 slides with content, got {content_slides}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
