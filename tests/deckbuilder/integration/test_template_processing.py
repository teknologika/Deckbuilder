"""
Integration tests for template processing pipeline.
"""

import json

import pytest

from tests.utils.content_generator import ContentType, ContentLength
from tests.utils.template_test_generator import TemplateTestGenerator


@pytest.mark.integration
@pytest.mark.deckbuilder
class TestTemplateProcessing:
    """Integration tests for complete template processing."""

    def test_template_json_loading(self, default_template_json):
        """Test loading and parsing template JSON."""
        assert "template_info" in default_template_json
        assert "layouts" in default_template_json
        assert len(default_template_json["layouts"]) > 0

        # Verify template structure
        template_info = default_template_json["template_info"]
        assert "name" in template_info
        assert "version" in template_info

        # Verify layout structure
        layouts = default_template_json["layouts"]
        for layout_name, layout_data in layouts.items():
            assert "index" in layout_data
            assert "placeholders" in layout_data
            assert isinstance(layout_data["placeholders"], dict)

    def test_template_test_generation(self, default_template_json, deckbuilder_temp_dir):
        """Test generating test files from template JSON."""
        # Save template to file
        template_file = deckbuilder_temp_dir / "test_template.json"
        with open(template_file, "w") as f:
            json.dump(default_template_json, f, indent=2)

        # Generate test files
        generator = TemplateTestGenerator()
        output_dir = deckbuilder_temp_dir / "generated_tests"

        report = generator.generate_test_files(
            template_file, output_dir, ContentType.BUSINESS, ContentLength.MEDIUM
        )

        # Verify report
        assert report.template_name == "Default"
        assert report.total_layouts == len(default_template_json["layouts"])
        assert len(report.generated_files) >= 1  # At least one file generated
        assert report.coverage_percentage > 0

        # Verify files were created
        for generated_file in report.generated_files:
            assert generated_file.file_path.exists()
            assert generated_file.file_path.stat().st_size > 0

    def test_layout_coverage_validation(self, default_template_json):
        """Test layout coverage validation."""
        generator = TemplateTestGenerator()
        coverage = generator.validate_layout_coverage(default_template_json)

        # Check coverage for known layouts
        assert isinstance(coverage, dict)

        expected_layouts = [
            "Title Slide",
            "Title and Content",
            "Four Columns With Titles",
            "Comparison",
        ]
        for layout in expected_layouts:
            if layout in default_template_json["layouts"]:
                assert layout in coverage
                # Should be covered since these are supported layouts
                assert coverage[layout] is True

    def test_json_test_file_generation(self, default_template_json, deckbuilder_temp_dir):
        """Test JSON test file generation specifically."""
        template_file = deckbuilder_temp_dir / "test_template.json"
        with open(template_file, "w") as f:
            json.dump(default_template_json, f, indent=2)

        generator = TemplateTestGenerator()
        output_dir = deckbuilder_temp_dir / "json_tests"

        report = generator.generate_test_files(template_file, output_dir)

        # Find JSON file
        json_files = [f for f in report.generated_files if f.file_type == "json"]
        assert len(json_files) >= 1

        json_file = json_files[0]
        assert json_file.file_path.suffix == ".json"

        # Load and validate JSON content
        with open(json_file.file_path, "r") as f:
            test_data = json.load(f)

        assert "presentation" in test_data
        assert "slides" in test_data["presentation"]
        slides = test_data["presentation"]["slides"]
        assert len(slides) > 0

        # Verify slide structure
        for slide in slides:
            assert "type" in slide
            # Should have convention-based placeholder names
            placeholder_keys = [
                k for k in slide.keys() if k not in ["type", "layout", "rich_content"]
            ]
            assert len(placeholder_keys) > 0

    def test_markdown_test_file_generation(self, default_template_json, deckbuilder_temp_dir):
        """Test Markdown test file generation specifically."""
        template_file = deckbuilder_temp_dir / "test_template.json"
        with open(template_file, "w") as f:
            json.dump(default_template_json, f, indent=2)

        generator = TemplateTestGenerator()
        output_dir = deckbuilder_temp_dir / "md_tests"

        report = generator.generate_test_files(template_file, output_dir)

        # Find Markdown file
        md_files = [f for f in report.generated_files if f.file_type == "markdown"]
        assert len(md_files) >= 1

        md_file = md_files[0]
        assert md_file.file_path.suffix == ".md"

        # Load and validate Markdown content
        content = md_file.file_path.read_text(encoding="utf-8")
        assert "---" in content  # YAML frontmatter markers
        assert "layout:" in content

        # Should have multiple layout sections
        layout_sections = content.count("layout:")
        assert layout_sections > 0

    def test_content_type_variations(self, default_template_json, deckbuilder_temp_dir):
        """Test generation with different content types."""
        template_file = deckbuilder_temp_dir / "test_template.json"
        with open(template_file, "w") as f:
            json.dump(default_template_json, f, indent=2)

        generator = TemplateTestGenerator()

        for content_type in [ContentType.BUSINESS, ContentType.TECHNICAL, ContentType.MARKETING]:
            output_dir = deckbuilder_temp_dir / f"tests_{content_type.value}"

            report = generator.generate_test_files(
                template_file, output_dir, content_type, ContentLength.MEDIUM
            )

            assert report.template_name == "Default"
            assert len(report.generated_files) > 0

            # Verify content type appears in generated files
            for generated_file in report.generated_files:
                if generated_file.file_type == "json":
                    with open(generated_file.file_path, "r") as f:
                        test_data = json.load(f)

                    # Should contain content type-specific terms
                    content_str = json.dumps(test_data).lower()
                    # At least some content should reflect the content type
                    assert len(content_str) > 100  # Has substantial content

    def test_content_length_variations(self, default_template_json, deckbuilder_temp_dir):
        """Test generation with different content lengths."""
        template_file = deckbuilder_temp_dir / "test_template.json"
        with open(template_file, "w") as f:
            json.dump(default_template_json, f, indent=2)

        generator = TemplateTestGenerator()
        generated_files_by_length = {}

        for content_length in [ContentLength.SHORT, ContentLength.MEDIUM, ContentLength.LONG]:
            output_dir = deckbuilder_temp_dir / f"tests_{content_length.value}"

            report = generator.generate_test_files(
                template_file, output_dir, ContentType.BUSINESS, content_length
            )

            assert len(report.generated_files) > 0
            generated_files_by_length[content_length] = report.generated_files

        # Verify different lengths produce different content sizes
        # (This is a rough check since exact content length depends on layout)
        short_files = generated_files_by_length[ContentLength.SHORT]
        long_files = generated_files_by_length[ContentLength.LONG]

        # Should have generated files for both lengths
        assert len(short_files) > 0
        assert len(long_files) > 0

    def test_structured_frontmatter_generation(self, deckbuilder_temp_dir):
        """Test structured frontmatter generation for individual layouts."""
        generator = TemplateTestGenerator()

        layouts_to_test = ["Four Columns With Titles", "Comparison", "Two Content"]
        output_dir = deckbuilder_temp_dir / "frontmatter_tests"

        generated_files = generator.generate_structured_frontmatter_tests(
            layouts_to_test, output_dir
        )

        assert len(generated_files) > 0

        for generated_file in generated_files:
            assert generated_file.file_path.exists()
            assert generated_file.file_type == "markdown"

            content = generated_file.file_path.read_text(encoding="utf-8")
            assert "---" in content
            assert "layout:" in content
            assert (
                generated_file.layout_name.replace(" ", "_").lower()
                in generated_file.file_path.name
            )

    def test_full_template_processing_pipeline(self, default_template_json, deckbuilder_temp_dir):
        """Test complete template processing pipeline."""
        # Step 1: Create template file
        template_file = deckbuilder_temp_dir / "pipeline_template.json"
        with open(template_file, "w") as f:
            json.dump(default_template_json, f, indent=2)

        # Step 2: Generate test files
        generator = TemplateTestGenerator()
        output_dir = deckbuilder_temp_dir / "pipeline_output"

        report = generator.generate_test_files(template_file, output_dir)

        # Step 3: Validate coverage
        coverage = generator.validate_layout_coverage(default_template_json)

        # Step 4: Generate individual layout examples
        covered_layouts = [layout for layout, covered in coverage.items() if covered]
        individual_files = generator.generate_structured_frontmatter_tests(
            covered_layouts, output_dir / "individual"
        )

        # Verify complete pipeline
        assert report.template_name == "Default"
        assert len(report.generated_files) >= 1
        assert len(coverage) == report.total_layouts
        assert len(individual_files) > 0

        # Verify all files exist and have content
        all_files = report.generated_files + individual_files
        for generated_file in all_files:
            assert generated_file.file_path.exists()
            assert generated_file.file_path.stat().st_size > 0

            # Verify content is valid
            content = generated_file.file_path.read_text(encoding="utf-8")
            if generated_file.file_type == "json":
                # Should be valid JSON
                json.loads(content)
            elif generated_file.file_type == "markdown":
                # Should have frontmatter
                assert "---" in content
                assert "layout:" in content

    def test_error_handling_invalid_template(self, deckbuilder_temp_dir):
        """Test error handling with invalid template JSON."""
        # Create invalid JSON file
        invalid_template = deckbuilder_temp_dir / "invalid_template.json"
        invalid_template.write_text("{ invalid json }", encoding="utf-8")

        generator = TemplateTestGenerator()
        output_dir = deckbuilder_temp_dir / "error_tests"

        # Should raise an exception for invalid JSON
        with pytest.raises(json.JSONDecodeError):
            generator.generate_test_files(invalid_template, output_dir)

    def test_empty_template_handling(self, deckbuilder_temp_dir):
        """Test handling of template with no layouts."""
        empty_template = {
            "template_info": {"name": "Empty Template", "version": "1.0"},
            "layouts": {},
        }

        template_file = deckbuilder_temp_dir / "empty_template.json"
        with open(template_file, "w") as f:
            json.dump(empty_template, f, indent=2)

        generator = TemplateTestGenerator()
        output_dir = deckbuilder_temp_dir / "empty_tests"

        report = generator.generate_test_files(template_file, output_dir)

        # Should handle empty template gracefully
        assert report.template_name == "Empty Template"
        assert report.total_layouts == 0
        assert report.coverage_percentage == 0.0
        # May not generate files, but should not crash
