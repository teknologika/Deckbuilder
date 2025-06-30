#!/usr/bin/env python3
"""
End-to-End Golden File Validation Tests

Tests that validate the golden test files (test_presentation.md and test_presentation.json)
actually work correctly by:
1. Calling deckbuilder CLI commands directly
2. Generating actual PowerPoint files
3. Using python-pptx to validate content placement
4. Creating a feedback loop that catches broken mappings

This ensures our test data stays current and catches regressions in template mapping.
"""

import os
import subprocess
import tempfile
import pytest
from pathlib import Path
from pptx import Presentation

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class TestGoldenFileValidation:
    """End-to-end validation of golden test files"""

    @classmethod
    def setup_class(cls):
        """Setup for all tests in this class"""
        cls.project_root = Path(__file__).parent.parent.parent.parent
        cls.templates_dir = cls.project_root / "templates"
        cls.examples_dir = cls.templates_dir / "examples"
        cls.golden_md = cls.examples_dir / "test_presentation.md"
        cls.golden_json = cls.examples_dir / "test_presentation.json"

        # Ensure templates directory exists and is initialized
        if not cls.templates_dir.exists():
            subprocess.run(
                [
                    "python",
                    str(cls.project_root / "src" / "deckbuilder" / "cli.py"),
                    "init",
                    str(cls.templates_dir),
                ],
                check=True,
                cwd=cls.project_root,
            )

    def test_golden_markdown_file_exists_and_comprehensive(self):
        """Test that golden markdown file exists and covers all layouts"""
        assert self.golden_md.exists(), f"Golden markdown file not found: {self.golden_md}"

        content = self.golden_md.read_text()

        # Check for expected layouts in the markdown (both uppercase and lowercase variants)
        expected_layouts = [
            "Title Slide",
            "Title and Content",
            "Section Header",
            "Two Content",
            "Comparison",
            "Four Columns",
            "Three Columns With Titles",
            "Three Columns",
            "Picture with Caption",
            "table",  # Note: uses lowercase in frontmatter
        ]

        for layout in expected_layouts:
            assert f"layout: {layout}" in content, f"Layout '{layout}' not found in golden markdown"

        # Check for formatting examples
        assert "**" in content, "Bold formatting not found in golden markdown"
        assert "*" in content, "Italic formatting not found in golden markdown"
        assert "___" in content, "Underline formatting not found in golden markdown"

    def test_golden_json_file_exists_and_comprehensive(self):
        """Test that golden JSON file exists and covers all layouts"""
        assert self.golden_json.exists(), f"Golden JSON file not found: {self.golden_json}"

        import json

        with open(self.golden_json) as f:
            data = json.load(f)

        assert "presentation" in data, "JSON missing 'presentation' key"
        assert "slides" in data["presentation"], "JSON missing 'slides' key"

        slides = data["presentation"]["slides"]
        assert len(slides) > 5, f"Expected multiple slides, got {len(slides)}"

        # Check for layout variety
        slide_types = [slide.get("type", "") for slide in slides]
        expected_types = ["Title Slide", "Title and Content", "Section Header"]

        for expected_type in expected_types:
            assert expected_type in slide_types, f"Slide type '{expected_type}' not found in JSON"

    def test_cli_generates_presentation_from_markdown(self):
        """Test CLI can generate PowerPoint from golden markdown file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use the CLI directly with the --output-dir flag to override output location
            result = subprocess.run(
                [
                    "python",
                    str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                    "create",
                    str(self.golden_md),
                    "--output",
                    "test_output_md",
                    "--output-dir",
                    temp_dir,
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Check if CLI supports --output-dir flag or if we need to modify approach
            if result.returncode != 0 and "--output-dir" in result.stderr:
                # CLI doesn't support --output-dir, use environment variable approach
                env = os.environ.copy()
                env["DECK_TEMPLATE_FOLDER"] = str(self.templates_dir)
                env["DECK_OUTPUT_FOLDER"] = temp_dir

                result = subprocess.run(
                    [
                        "python",
                        str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                        "create",
                        str(self.golden_md),
                        "--output",
                        "test_output_md",
                    ],
                    capture_output=True,
                    text=True,
                    env=env,
                    cwd=self.project_root,
                )

            assert (
                result.returncode == 0
            ), f"CLI failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

            # Find the actual output file (CLI creates a subdirectory with the output name)
            search_dirs = [
                Path(temp_dir),
                Path(temp_dir) / "test_output_md",  # CLI creates subdirectory in temp
            ]
            pptx_files = []

            for search_dir in search_dirs:
                if search_dir.exists():
                    pptx_files.extend(search_dir.glob("test_output_md*.pptx"))
                    pptx_files.extend(search_dir.glob("*.pptx"))  # any pptx file in output dir

            assert (
                len(pptx_files) > 0
            ), (
                f"No output file found in {[str(d) for d in search_dirs]}\n"
                f"Searched files: {[list(d.glob('*.pptx')) if d.exists() else 'DIR_NOT_EXISTS' for d in search_dirs]}\n"
                f"STDOUT: {result.stdout}"
            )

            output_path = pptx_files[0]  # Use the first (and likely only) match

            # Validate the generated PowerPoint file
            self._validate_powerpoint_content(output_path, "markdown")

    def test_cli_generates_presentation_from_json(self):
        """Test CLI can generate PowerPoint from golden JSON file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Use the CLI directly with the --output-dir flag to override output location
            result = subprocess.run(
                [
                    "python",
                    str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                    "create",
                    str(self.golden_json),
                    "--output",
                    "test_output_json",
                    "--output-dir",
                    temp_dir,
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Check if CLI supports --output-dir flag or if we need to modify approach
            if result.returncode != 0 and "--output-dir" in result.stderr:
                # CLI doesn't support --output-dir, use environment variable approach
                env = os.environ.copy()
                env["DECK_TEMPLATE_FOLDER"] = str(self.templates_dir)
                env["DECK_OUTPUT_FOLDER"] = temp_dir

                result = subprocess.run(
                    [
                        "python",
                        str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                        "create",
                        str(self.golden_json),
                        "--output",
                        "test_output_json",
                    ],
                    capture_output=True,
                    text=True,
                    env=env,
                    cwd=self.project_root,
                )

            assert (
                result.returncode == 0
            ), f"CLI failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

            # Find the actual output file (CLI creates a subdirectory with the output name)
            search_dirs = [
                Path(temp_dir),
                Path(temp_dir) / "test_output_json",  # CLI creates subdirectory in temp
            ]
            pptx_files = []

            for search_dir in search_dirs:
                if search_dir.exists():
                    pptx_files.extend(search_dir.glob("test_output_json*.pptx"))
                    pptx_files.extend(search_dir.glob("*.pptx"))  # any pptx file in output dir

            assert (
                len(pptx_files) > 0
            ), (
                f"No output file found in {[str(d) for d in search_dirs]}\n"
                f"Searched files: {[list(d.glob('*.pptx')) if d.exists() else 'DIR_NOT_EXISTS' for d in search_dirs]}\n"
                f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            )

            output_path = pptx_files[0]  # Use the first (and likely only) match

            # Validate the generated PowerPoint file
            self._validate_powerpoint_content(output_path, "json")

    def test_markdown_and_json_produce_similar_content(self):
        """Test that markdown and JSON golden files produce presentations with similar content"""
        with tempfile.TemporaryDirectory() as temp_dir:
            env = os.environ.copy()
            env["DECK_TEMPLATE_FOLDER"] = str(self.templates_dir)
            env["DECK_OUTPUT_FOLDER"] = temp_dir

            # Generate both presentations
            subprocess.run(
                [
                    "python",
                    str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                    "create",
                    str(self.golden_md),
                    "--output",
                    "from_markdown",
                ],
                check=True,
                env=env,
                cwd=temp_dir,  # Run from temp directory
            )

            subprocess.run(
                [
                    "python",
                    str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                    "create",
                    str(self.golden_json),
                    "--output",
                    "from_json",
                ],
                check=True,
                env=env,
                cwd=temp_dir,  # Run from temp directory
            )

            # Find the actual output files (CLI creates subdirectories)
            search_dirs = [
                Path(temp_dir),
                Path(temp_dir) / "from_markdown",
                Path(temp_dir) / "from_json",
            ]

            md_files = []
            json_files = []

            for search_dir in search_dirs:
                if search_dir.exists():
                    md_files.extend(search_dir.glob("from_markdown*.pptx"))
                    md_files.extend(
                        search_dir.glob("*.pptx") if "from_markdown" in str(search_dir) else []
                    )
                    json_files.extend(search_dir.glob("from_json*.pptx"))
                    json_files.extend(
                        search_dir.glob("*.pptx") if "from_json" in str(search_dir) else []
                    )

            assert (
                len(md_files) > 0
            ), f"No markdown output file found in {[str(d) for d in search_dirs]}"
            assert (
                len(json_files) > 0
            ), f"No JSON output file found in {[str(d) for d in search_dirs]}"

            md_output = md_files[0]
            json_output = json_files[0]

            # Compare slide counts
            md_prs = Presentation(str(md_output))
            json_prs = Presentation(str(json_output))

            # Both should have multiple slides
            assert (
                len(md_prs.slides) > 3
            ), f"Markdown presentation has too few slides: {len(md_prs.slides)}"
            assert (
                len(json_prs.slides) > 3
            ), f"JSON presentation has too few slides: {len(json_prs.slides)}"

            # Both should have title slides
            md_first_slide = md_prs.slides[0]
            json_first_slide = json_prs.slides[0]

            md_title = self._extract_slide_title(md_first_slide)
            json_title = self._extract_slide_title(json_first_slide)

            assert (
                "Deckbuilder" in md_title
            ), f"Expected 'Deckbuilder' in markdown title, got: {md_title}"
            assert (
                "Deckbuilder" in json_title
            ), f"Expected 'Deckbuilder' in JSON title, got: {json_title}"

    def _validate_powerpoint_content(self, pptx_path: Path, source_type: str):
        """Validate that PowerPoint file contains expected content"""
        prs = Presentation(str(pptx_path))

        # Basic validation
        assert len(prs.slides) > 0, f"No slides found in {source_type} presentation"

        # Check first slide (should be title slide)
        first_slide = prs.slides[0]
        title_text = self._extract_slide_title(first_slide)

        assert title_text, f"No title found on first slide of {source_type} presentation"
        assert "Deckbuilder" in title_text, f"Expected 'Deckbuilder' in title, got: {title_text}"

        # Validate multiple slides exist with content
        slides_with_content = 0
        for slide in prs.slides:
            if self._slide_has_content(slide):
                slides_with_content += 1

        assert (
            slides_with_content >= 3
        ), f"Expected at least 3 content slides, found {slides_with_content}"

        # Check for formatting preservation (if any bold text exists)
        has_formatting = False
        for slide in prs.slides:
            if self._slide_has_formatting(slide):
                has_formatting = True
                break

        # Note: We expect some formatting in our golden files
        assert has_formatting, f"No text formatting found in {source_type} presentation"

    def _extract_slide_title(self, slide) -> str:
        """Extract title text from a slide"""
        title_text = ""

        # Try to find title placeholder
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                # First non-empty text is likely the title
                title_text = shape.text.strip()
                break

        return title_text

    def _slide_has_content(self, slide) -> bool:
        """Check if slide has meaningful content"""
        for shape in slide.shapes:
            if hasattr(shape, "text") and len(shape.text.strip()) > 10:
                return True
        return False

    def _slide_has_formatting(self, slide) -> bool:
        """Check if slide has text formatting (bold, italic, etc.)"""
        for shape in slide.shapes:
            if hasattr(shape, "text_frame"):
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.bold or run.font.italic or run.font.underline:
                            return True
        return False

    def test_cli_version_command(self):
        """Test that CLI version command works"""
        result = subprocess.run(
            ["python", str(self.project_root / "src" / "deckbuilder" / "cli.py"), "--version"],
            capture_output=True,
            text=True,
            cwd=self.project_root,  # Keep root for version command
        )

        assert result.returncode == 0, f"Version command failed: {result.stderr}"
        assert "Deckbuilder CLI" in result.stdout, f"Unexpected version output: {result.stdout}"

    def test_cli_config_show_command(self):
        """Test that CLI config show command works"""
        env = os.environ.copy()
        env["DECK_TEMPLATE_FOLDER"] = str(self.templates_dir)

        result = subprocess.run(
            ["python", str(self.project_root / "src" / "deckbuilder" / "cli.py"), "config", "show"],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.project_root,  # Keep root for config command
        )

        assert result.returncode == 0, f"Config show failed: {result.stderr}"
        assert (
            "Template Folder" in result.stdout
        ), f"Config output missing template folder: {result.stdout}"

    def test_cli_template_list_command(self):
        """Test that CLI template list command works"""
        env = os.environ.copy()
        env["DECK_TEMPLATE_FOLDER"] = str(self.templates_dir)

        result = subprocess.run(
            [
                "python",
                str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                "template",
                "list",
            ],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.project_root,  # Keep root for template list command
        )

        assert result.returncode == 0, f"Template list failed: {result.stderr}"
        assert "default" in result.stdout, f"Default template not found: {result.stdout}"

    def test_golden_files_stay_current_with_templates(self):
        """Test that ensures golden files are updated if templates change"""
        # This test validates our feedback loop concept
        # If templates change but golden files don't, this should catch it

        # Generate presentations from both golden files
        with tempfile.TemporaryDirectory() as temp_dir:
            env = os.environ.copy()
            env["DECK_TEMPLATE_FOLDER"] = str(self.templates_dir)
            env["DECK_OUTPUT_FOLDER"] = temp_dir

            # Test both files can be processed without errors
            md_result = subprocess.run(
                [
                    "python",
                    str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                    "create",
                    str(self.golden_md),
                    "--output",
                    "golden_md_test",
                ],
                capture_output=True,
                text=True,
                env=env,
                cwd=temp_dir,  # Run from temp directory
            )

            json_result = subprocess.run(
                [
                    "python",
                    str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                    "create",
                    str(self.golden_json),
                    "--output",
                    "golden_json_test",
                ],
                capture_output=True,
                text=True,
                env=env,
                cwd=temp_dir,  # Run from temp directory
            )

            # Both should succeed
            assert (
                md_result.returncode == 0
            ), f"Golden markdown processing failed: {md_result.stderr}"
            assert (
                json_result.returncode == 0
            ), f"Golden JSON processing failed: {json_result.stderr}"

            # Find and validate the actual output files (CLI creates subdirectories)
            search_dirs = [
                Path(temp_dir),
                Path(temp_dir) / "golden_md_test",
                Path(temp_dir) / "golden_json_test",
            ]

            md_files = []
            json_files = []

            for search_dir in search_dirs:
                if search_dir.exists():
                    md_files.extend(search_dir.glob("golden_md_test*.pptx"))
                    md_files.extend(
                        search_dir.glob("*.pptx") if "golden_md_test" in str(search_dir) else []
                    )
                    json_files.extend(search_dir.glob("golden_json_test*.pptx"))
                    json_files.extend(
                        search_dir.glob("*.pptx") if "golden_json_test" in str(search_dir) else []
                    )

            assert len(md_files) > 0, f"Golden MD file not found in {[str(d) for d in search_dirs]}"
            assert (
                len(json_files) > 0
            ), f"Golden JSON file not found in {[str(d) for d in search_dirs]}"

            md_output = md_files[0]
            json_output = json_files[0]

            assert (
                md_output.stat().st_size > 10000
            ), f"Golden MD produced invalid file: {md_output.stat().st_size} bytes"
            assert (
                json_output.stat().st_size > 10000
            ), f"Golden JSON produced invalid file: {json_output.stat().st_size} bytes"


class TestCLIErrorHandling:
    """Test CLI error handling scenarios"""

    @classmethod
    def setup_class(cls):
        """Setup for error handling tests"""
        cls.project_root = Path(__file__).parent.parent.parent.parent

    def test_cli_handles_missing_input_file(self):
        """Test CLI properly handles missing input files"""
        result = subprocess.run(
            [
                "python",
                str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                "create",
                "nonexistent.md",
            ],
            capture_output=True,
            text=True,
            cwd=self.project_root,
        )

        assert result.returncode != 0, "CLI should fail with missing input file"
        assert "not found" in result.stderr.lower() or "not found" in result.stdout.lower()

    def test_cli_handles_invalid_file_format(self):
        """Test CLI properly handles invalid file formats"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as temp_file:
            temp_file.write("This is not a valid format")
            temp_file.flush()

            try:
                result = subprocess.run(
                    [
                        "python",
                        str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                        "create",
                        temp_file.name,
                    ],
                    capture_output=True,
                    text=True,
                    cwd=self.project_root,
                )

                assert result.returncode != 0, "CLI should fail with unsupported format"
                assert "unsupported" in result.stderr.lower() or "format" in result.stderr.lower()

            finally:
                os.unlink(temp_file.name)

    def test_cli_handles_missing_templates_folder(self):
        """Test CLI properly handles missing templates folder"""
        env = os.environ.copy()
        env["DECK_TEMPLATE_FOLDER"] = "/nonexistent/templates"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as temp_file:
            temp_file.write("---\nlayout: Title Slide\n---\n# Test")
            temp_file.flush()

            try:
                result = subprocess.run(
                    [
                        "python",
                        str(self.project_root / "src" / "deckbuilder" / "cli.py"),
                        "create",
                        temp_file.name,
                    ],
                    capture_output=True,
                    text=True,
                    env=env,
                    cwd=self.project_root,
                )

                assert result.returncode != 0, "CLI should fail with missing templates"

            finally:
                os.unlink(temp_file.name)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
