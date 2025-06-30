#!/usr/bin/env python3
"""
Integration tests for CLI path management

Tests that all CLI commands properly use PathManager for consistent
path resolution and environment variable handling.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))  # noqa: E402

from src.deckbuilder.cli import DeckbuilderCLI  # noqa: E402
from src.deckbuilder.path_manager import path_manager  # noqa: E402


class TestCLIPathManagement:
    """Test CLI commands use PathManager consistently"""

    def test_cli_environment_setup_template_folder(self):
        """Test CLI properly sets up template folder environment"""
        DeckbuilderCLI(templates_path="/custom/templates")

        assert os.getenv("DECK_TEMPLATE_FOLDER") == "/custom/templates"

    def test_cli_environment_setup_output_folder(self):
        """Test CLI properly sets up output folder environment"""
        with tempfile.TemporaryDirectory() as temp_dir:
            DeckbuilderCLI(output_path=temp_dir)

            assert os.getenv("DECK_OUTPUT_FOLDER") == temp_dir

    def test_cli_environment_setup_defaults(self):
        """Test CLI sets up proper defaults when no args provided"""
        with patch.dict(os.environ, {}, clear=True):
            DeckbuilderCLI()

            # Should set defaults
            assert os.getenv("DECK_TEMPLATE_FOLDER") == str(Path.cwd() / "templates")
            assert os.getenv("DECK_OUTPUT_FOLDER") == str(Path.cwd())
            assert os.getenv("DECK_TEMPLATE_NAME") == "default"
            assert os.getenv("DECK_PROOFING_LANGUAGE") == "en-AU"

    def test_validate_templates_folder_uses_path_manager(self):
        """Test _validate_templates_folder uses PathManager"""
        cli = DeckbuilderCLI()

        with (
            patch.object(path_manager, "validate_template_folder_exists") as mock_validate,
            patch.object(path_manager, "get_template_folder") as mock_get_folder,
        ):

            mock_validate.return_value = False
            mock_get_folder.return_value = Path("/test/templates")

            with patch("builtins.print") as mock_print:
                result = cli._validate_templates_folder()

                assert result is False
                mock_validate.assert_called_once()
                mock_get_folder.assert_called_once()
                mock_print.assert_called()

    def test_config_show_uses_path_manager(self):
        """Test config show command uses PathManager for display"""
        cli = DeckbuilderCLI()

        with (
            patch.object(path_manager, "get_template_folder") as mock_template,
            patch.object(path_manager, "get_output_folder") as mock_output,
            patch.object(path_manager, "get_template_name") as mock_name,
        ):

            mock_template.return_value = Path("/test/templates")
            mock_output.return_value = Path("/test/output")
            mock_name.return_value = "test"

            with patch("builtins.print") as mock_print:
                cli.get_config()

                # Should call PathManager methods
                mock_template.assert_called()
                mock_output.assert_called()
                mock_name.assert_called()

                # Should print configuration
                assert mock_print.call_count > 0

    def test_list_templates_uses_path_manager(self):
        """Test list_templates uses PathManager"""
        cli = DeckbuilderCLI()

        with (
            patch.object(path_manager, "validate_template_folder_exists") as mock_validate,
            patch.object(path_manager, "list_available_templates") as mock_list,
            patch.object(path_manager, "get_template_folder") as mock_folder,
        ):

            mock_validate.return_value = True
            mock_list.return_value = ["default", "custom"]
            mock_folder.return_value = Path("/test/templates")

            with patch("builtins.print") as mock_print:
                cli.list_templates()

                mock_validate.assert_called_once()
                mock_list.assert_called_once()
                mock_folder.assert_called()
                mock_print.assert_called()

    def test_init_templates_uses_path_manager(self):
        """Test init_templates uses PathManager for asset location"""
        cli = DeckbuilderCLI()

        with tempfile.TemporaryDirectory() as temp_dir:
            with (
                patch.object(path_manager, "validate_assets_exist") as mock_validate,
                patch.object(path_manager, "get_assets_templates_path") as mock_assets,
            ):

                mock_validate.return_value = False
                mock_assets.return_value = Path("/test/assets/templates")

                with patch("builtins.print") as mock_print:
                    cli.init_templates(temp_dir)

                    mock_validate.assert_called_once()
                    mock_assets.assert_called_once()
                    # Should print error about missing assets
                    assert any(
                        "Could not locate template assets" in str(call)
                        for call in mock_print.call_args_list
                    )

    @patch("src.deckbuilder.cli.Deckbuilder")
    def test_create_presentation_markdown(self, mock_deckbuilder):
        """Test create_presentation works with markdown files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = DeckbuilderCLI(output_path=temp_dir)  # Force output to temp directory

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False, dir=temp_dir
            ) as temp_md:
                temp_md.write("# Test Presentation\n---\nlayout: Title Slide\ntitle: Test\n---")
                temp_md.flush()

                mock_db_instance = MagicMock()
                mock_db_instance.create_presentation_from_markdown.return_value = "success"
                mock_deckbuilder.return_value = mock_db_instance

                with patch.object(cli, "_validate_templates_folder", return_value=True):
                    try:
                        cli.create_presentation(temp_md.name)
                        mock_db_instance.create_presentation_from_markdown.assert_called_once()
                    finally:
                        os.unlink(temp_md.name)

    @patch("src.deckbuilder.cli.Deckbuilder")
    def test_create_presentation_json(self, mock_deckbuilder):
        """Test create_presentation works with JSON files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = DeckbuilderCLI(output_path=temp_dir)  # Force output to temp directory

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False, dir=temp_dir
            ) as temp_json:
                temp_json.write(
                    '{"presentation": {"slides": [{"type": "Title Slide", "title": "Test"}]}}'
                )
                temp_json.flush()

                mock_db_instance = MagicMock()
                mock_db_instance.create_presentation_from_markdown.return_value = "success"
                mock_deckbuilder.return_value = mock_db_instance

                with patch.object(cli, "_validate_templates_folder", return_value=True):
                    try:
                        cli.create_presentation(temp_json.name)
                        # Should convert JSON to markdown and call markdown method
                        mock_db_instance.create_presentation_from_markdown.assert_called_once()
                    finally:
                        os.unlink(temp_json.name)

    def test_json_to_markdown_conversion(self):
        """Test JSON to markdown conversion for complex data"""
        cli = DeckbuilderCLI()

        json_data = {
            "presentation": {
                "slides": [
                    {
                        "type": "Title Slide",
                        "title": "Test Presentation",
                        "subtitle": "Test Subtitle",
                    },
                    {
                        "type": "Title and Content",
                        "title": "Content Slide",
                        "content": ["Item 1", "Item 2", "Item 3"],
                    },
                ]
            }
        }

        markdown = cli._convert_json_to_markdown(json_data)

        # Should contain proper frontmatter
        assert "layout: Title Slide" in markdown
        assert "title: Test Presentation" in markdown
        assert "subtitle: Test Subtitle" in markdown
        assert "layout: Title and Content" in markdown
        assert "• Item 1" in markdown


class TestCLIVersionHandling:
    """Test CLI version flag uses PathManager"""

    def test_version_flag_uses_path_manager(self):
        """Test --version flag uses PathManager.get_version()"""
        with patch.object(path_manager, "get_version") as mock_version:
            mock_version.return_value = "1.0.1-test"

            with (
                patch("builtins.print") as mock_print,
                patch("sys.argv", ["deckbuilder", "--version"]),
            ):

                from src.deckbuilder.cli import main

                try:
                    main()
                except SystemExit:
                    pass  # Expected for version command

                mock_version.assert_called_once()
                # Should print version
                printed_text = " ".join(str(call) for call in mock_print.call_args_list)
                assert "1.0.1-test" in printed_text


class TestCLIErrorHandling:
    """Test CLI error handling with PathManager"""

    def test_missing_input_file_error(self):
        """Test error handling for missing input files"""
        cli = DeckbuilderCLI()

        with pytest.raises(FileNotFoundError):
            cli.create_presentation("nonexistent.md")

    def test_unsupported_file_format_error(self):
        """Test error handling for unsupported file formats"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = DeckbuilderCLI(output_path=temp_dir)  # Force output to temp directory

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, dir=temp_dir
            ) as temp_file:
                temp_file.write("test content")
                temp_file.flush()

                with patch.object(cli, "_validate_templates_folder", return_value=True):
                    try:
                        with pytest.raises(ValueError, match="Unsupported file format"):
                            cli.create_presentation(temp_file.name)
                    finally:
                        os.unlink(temp_file.name)

    def test_template_folder_validation_error(self):
        """Test error handling when template folder doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = DeckbuilderCLI(output_path=temp_dir)  # Force output to temp directory

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False, dir=temp_dir
            ) as temp_file:
                temp_file.write("# Test")
                temp_file.flush()

                with patch.object(cli, "_validate_templates_folder", return_value=False):
                    try:
                        result = cli.create_presentation(temp_file.name)
                        assert result is None  # Should return None on validation failure
                    finally:
                        os.unlink(temp_file.name)


class TestEnvironmentIntegration:
    """Test environment variable integration"""

    def test_environment_variable_precedence(self):
        """Test that environment variables take precedence over defaults"""
        with patch.dict(
            os.environ,
            {
                "DECK_TEMPLATE_FOLDER": "/env/templates",
                "DECK_OUTPUT_FOLDER": "/env/output",
                "DECK_TEMPLATE_NAME": "env_template",
                "DECK_PROOFING_LANGUAGE": "en-US",
            },
        ):
            DeckbuilderCLI()

            # Environment variables should be preserved
            assert os.getenv("DECK_TEMPLATE_FOLDER") == "/env/templates"
            assert os.getenv("DECK_OUTPUT_FOLDER") == "/env/output"
            assert os.getenv("DECK_TEMPLATE_NAME") == "env_template"
            assert os.getenv("DECK_PROOFING_LANGUAGE") == "en-US"

    def test_cli_args_override_environment(self):
        """Test that CLI arguments override environment variables"""
        with patch.dict(
            os.environ,
            {"DECK_TEMPLATE_FOLDER": "/env/templates", "DECK_OUTPUT_FOLDER": "/env/output"},
        ):
            DeckbuilderCLI(templates_path="/cli/templates", output_path="/cli/output")

            # CLI args should override environment
            assert os.getenv("DECK_TEMPLATE_FOLDER") == "/cli/templates"
            assert os.getenv("DECK_OUTPUT_FOLDER") == "/cli/output"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
