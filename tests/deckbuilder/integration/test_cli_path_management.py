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


class TestCLIPathManagement:
    """Test CLI commands use PathManager consistently"""

    def test_cli_context_aware_template_folder(self):
        """Test CLI uses context-aware path management for template folder"""
        cli = DeckbuilderCLI(template_folder="/custom/templates")

        # CLI should use provided template folder via path manager
        assert str(cli.path_manager.get_template_folder()) == "/custom/templates"
        # CLI should NOT set environment variables (anti-pattern fixed)
        assert os.getenv("DECK_TEMPLATE_FOLDER") is None

    def test_cli_context_aware_output_behavior(self):
        """Test CLI always outputs to current directory (context-aware behavior)"""
        cli = DeckbuilderCLI()

        # CLI context always uses current directory for output
        assert str(cli.path_manager.get_output_folder()) == str(Path.cwd())
        # CLI should NOT set environment variables (anti-pattern fixed)
        assert os.getenv("DECK_OUTPUT_FOLDER") is None

    def test_cli_context_defaults(self):
        """Test CLI uses proper context-aware defaults"""
        with patch.dict(os.environ, {}, clear=True):
            cli = DeckbuilderCLI()

            # CLI context defaults
            assert str(cli.path_manager.get_template_folder()) == str(Path.cwd() / "templates")
            assert str(cli.path_manager.get_output_folder()) == str(Path.cwd())
            assert cli.path_manager.get_template_name() == "default"

            # Environment variables should NOT be set (anti-pattern fixed)
            assert os.getenv("DECK_TEMPLATE_FOLDER") is None
            assert os.getenv("DECK_OUTPUT_FOLDER") is None

    def test_validate_templates_folder_uses_path_manager(self):
        """Test _validate_templates_folder uses CLI's PathManager instance"""
        cli = DeckbuilderCLI()

        with (
            patch.object(cli.path_manager, "validate_template_folder_exists") as mock_validate,
            patch.object(cli.path_manager, "get_template_folder") as mock_get_folder,
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
        """Test config show command uses CLI's PathManager instance"""
        cli = DeckbuilderCLI()

        with (
            patch.object(cli.path_manager, "get_template_folder") as mock_template,
            patch.object(cli.path_manager, "get_output_folder") as mock_output,
            patch.object(cli.path_manager, "get_template_name") as mock_name,
        ):

            mock_template.return_value = Path("/test/templates")
            mock_output.return_value = Path("/test/output")
            mock_name.return_value = "test"

            with patch("builtins.print") as mock_print:
                cli.get_config()

                # Should call CLI's PathManager methods
                mock_template.assert_called()
                mock_output.assert_called()
                mock_name.assert_called()

                # Should print configuration
                assert mock_print.call_count > 0

    def test_list_templates_handles_missing_folder(self):
        """Test list_templates handles missing template folder gracefully"""
        cli = DeckbuilderCLI()

        # Should handle missing template folder without crashing
        cli.list_templates()  # This will likely print an error message, which is correct behavior

    def test_init_templates_creates_directory(self):
        """Test init_templates creates template directory and handles missing assets gracefully"""
        cli = DeckbuilderCLI()

        with tempfile.TemporaryDirectory() as temp_dir:
            target_dir = Path(temp_dir) / "test_templates"

            # Should create directory even if assets are missing
            cli.init_templates(str(target_dir))

            # Directory should be created
            assert target_dir.exists()
            assert target_dir.is_dir()

    @patch("src.deckbuilder.cli.Deckbuilder")
    def test_create_presentation_markdown(self, mock_deckbuilder):
        """Test create_presentation works with markdown files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = DeckbuilderCLI()  # CLI always outputs to current directory

            with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, dir=temp_dir) as temp_md:
                temp_md.write("---\nlayout: Title Slide\ntitle: Test\n---")
                temp_md.flush()

                mock_db_instance = MagicMock()
                mock_db_instance.create_presentation.return_value = "success"
                mock_deckbuilder.return_value = mock_db_instance

                with (
                    patch.object(cli, "_validate_templates_folder", return_value=True),
                    patch("pathlib.Path.exists", return_value=True),
                    patch("deckbuilder.converter.markdown_to_canonical_json") as mock_converter,
                    patch("deckbuilder.validation.PresentationValidator") as mock_validator,
                ):
                    # Mock converter to return canonical JSON format
                    mock_converter.return_value = {
                        "slides": [
                            {
                                "layout": "Title Slide",
                                "placeholders": {"title": "Test"},
                                "content": [],
                            }
                        ]
                    }

                    # Mock validator to avoid file I/O
                    mock_val_instance = mock_validator.return_value
                    mock_val_instance.validate_pre_generation.return_value = None
                    mock_val_instance.validate_post_generation.return_value = None

                    try:
                        cli.create_presentation(temp_md.name)
                        mock_converter.assert_called_once()
                        mock_db_instance.create_presentation.assert_called_once()
                    finally:
                        os.unlink(temp_md.name)

    @patch("src.deckbuilder.cli.Deckbuilder")
    def test_create_presentation_json(self, mock_deckbuilder):
        """Test create_presentation works with JSON files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = DeckbuilderCLI()  # CLI always outputs to current directory

            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, dir=temp_dir) as temp_json:
                # Write canonical JSON format
                temp_json.write('{"slides": [{"layout": "Title Slide", "placeholders": {"title": "Test"}, "content": []}]}')
                temp_json.flush()

                mock_db_instance = MagicMock()
                mock_db_instance.create_presentation.return_value = "success"
                mock_deckbuilder.return_value = mock_db_instance

                with (
                    patch.object(cli, "_validate_templates_folder", return_value=True),
                    patch("pathlib.Path.exists", return_value=True),
                ):
                    try:
                        cli.create_presentation(temp_json.name)
                        # Should use canonical JSON processing method
                        mock_db_instance.create_presentation.assert_called_once()
                    finally:
                        os.unlink(temp_json.name)


class TestCLIVersionHandling:
    """Test CLI version flag uses PathManager"""

    def test_version_flag_uses_path_manager(self):
        """Test --version flag displays version information"""
        with (
            patch("builtins.print") as mock_print,
            patch("sys.argv", ["deckbuilder", "--version"]),
        ):

            from src.deckbuilder.cli import main

            try:
                main()
            except SystemExit:
                pass  # Expected for version command

            # Should print version information
            printed_text = " ".join(str(call) for call in mock_print.call_args_list)
            assert "Deckbuilder CLI" in printed_text


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
            cli = DeckbuilderCLI()  # CLI always outputs to current directory

            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, dir=temp_dir) as temp_file:
                temp_file.write("test content")
                temp_file.flush()

                with (
                    patch.object(cli, "_validate_templates_folder", return_value=True),
                    patch("pathlib.Path.exists", return_value=True),
                ):
                    try:
                        with pytest.raises(ValueError, match="Unsupported file format"):
                            cli.create_presentation(temp_file.name)
                    finally:
                        os.unlink(temp_file.name)

    def test_template_folder_validation_error(self):
        """Test error handling when template folder doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            cli = DeckbuilderCLI()  # CLI always outputs to current directory

            with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, dir=temp_dir) as temp_file:
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
        """Test that CLI respects environment variables when available"""
        with patch.dict(
            os.environ,
            {
                "DECK_TEMPLATE_FOLDER": "/env/templates",
                "DECK_TEMPLATE_NAME": "env_template",
                "DECK_PROOFING_LANGUAGE": "en-US",
            },
        ):
            cli = DeckbuilderCLI()

            # CLI should use environment variables for template settings
            assert str(cli.path_manager.get_template_folder()) == "/env/templates"
            assert cli.path_manager.get_template_name() == "env_template"
            # CLI always outputs to current directory (context-aware behavior)
            assert str(cli.path_manager.get_output_folder()) == str(Path.cwd())
            assert os.getenv("DECK_PROOFING_LANGUAGE") == "en-US"

    def test_cli_args_override_environment(self):
        """Test that CLI arguments override environment variables"""
        with patch.dict(
            os.environ,
            {"DECK_TEMPLATE_FOLDER": "/env/templates"},
        ):
            cli = DeckbuilderCLI(template_folder="/cli/templates")

            # CLI args should override environment for template folder
            assert str(cli.path_manager.get_template_folder()) == "/cli/templates"
            # CLI always outputs to current directory (can't be overridden in CLI context)
            assert str(cli.path_manager.get_output_folder()) == str(Path.cwd())
            # Environment variables should remain unchanged (anti-pattern fixed)
            assert os.getenv("DECK_TEMPLATE_FOLDER") == "/env/templates"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
