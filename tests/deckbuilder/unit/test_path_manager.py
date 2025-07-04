#!/usr/bin/env python3
"""
Unit tests for PathManager - Centralized path management testing

Tests all path resolution logic, environment variable handling,
and validation methods in the PathManager class.
"""

import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))  # noqa: E402

from src.deckbuilder.path_manager import PathManager, path_manager  # noqa: E402


class TestPathManager:
    """Test suite for PathManager centralized path management"""

    def test_get_project_root(self):
        """Test project root detection"""
        pm = PathManager()
        root = pm.get_project_root()

        assert isinstance(root, Path)
        assert root.exists()
        # Should be the Deckbuilder project root
        assert (root / "src" / "deckbuilder").exists()

    def test_get_assets_templates_path(self):
        """Test assets templates path resolution"""
        pm = PathManager()
        assets_path = pm.get_assets_templates_path()

        assert isinstance(assets_path, Path)
        expected = pm.get_project_root() / "assets" / "templates"
        assert assets_path == expected

    @patch.dict(os.environ, {}, clear=True)
    def test_get_template_folder_default(self):
        """Test template folder default when no environment variable"""
        pm = PathManager()
        template_folder = pm.get_template_folder()

        assert isinstance(template_folder, Path)
        # Should default to package assets/templates instead of ./templates
        assert template_folder == pm.get_assets_templates_path()

    @patch.dict(os.environ, {"DECK_TEMPLATE_FOLDER": "/custom/templates"})
    def test_get_template_folder_env_var(self):
        """Test template folder from environment variable"""
        pm = PathManager()
        template_folder = pm.get_template_folder()

        assert isinstance(template_folder, Path)
        assert str(template_folder) == "/custom/templates"

    @patch.dict(os.environ, {}, clear=True)
    def test_get_output_folder_default(self):
        """Test output folder default when no environment variable"""
        pm = PathManager()
        output_folder = pm.get_output_folder()

        assert isinstance(output_folder, Path)
        assert output_folder == Path.cwd()

    @patch.dict(os.environ, {"DECK_OUTPUT_FOLDER": "/custom/output"})
    def test_get_output_folder_env_var(self):
        """Test output folder from environment variable"""
        pm = PathManager()
        output_folder = pm.get_output_folder()

        assert isinstance(output_folder, Path)
        assert str(output_folder) == "/custom/output"

    @patch.dict(os.environ, {}, clear=True)
    def test_get_template_name_default(self):
        """Test template name default when no environment variable"""
        pm = PathManager()
        template_name = pm.get_template_name()

        assert template_name == "default"

    @patch.dict(os.environ, {"DECK_TEMPLATE_NAME": "custom"})
    def test_get_template_name_env_var(self):
        """Test template name from environment variable"""
        pm = PathManager()
        template_name = pm.get_template_name()

        assert template_name == "custom"

    def test_get_template_file_path_default(self):
        """Test template file path construction with default name"""
        pm = PathManager()

        with (
            patch.object(pm, "get_template_folder") as mock_folder,
            patch.object(pm, "get_template_name") as mock_name,
        ):
            mock_folder.return_value = Path("/templates")
            mock_name.return_value = "default"

            template_path = pm.get_template_file_path()
            assert template_path == Path("/templates/default.pptx")

    def test_get_template_file_path_custom_name(self):
        """Test template file path construction with custom name"""
        pm = PathManager()

        with patch.object(pm, "get_template_folder") as mock_folder:
            mock_folder.return_value = Path("/templates")

            template_path = pm.get_template_file_path("custom")
            assert template_path == Path("/templates/custom.pptx")

    def test_get_template_file_path_removes_extension(self):
        """Test template file path removes .pptx extension if present"""
        pm = PathManager()

        with patch.object(pm, "get_template_folder") as mock_folder:
            mock_folder.return_value = Path("/templates")

            template_path = pm.get_template_file_path("custom.pptx")
            assert template_path == Path("/templates/custom.pptx")

    def test_get_template_json_path(self):
        """Test template JSON mapping path construction"""
        pm = PathManager()

        with patch.object(pm, "get_template_folder") as mock_folder:
            mock_folder.return_value = Path("/templates")

            json_path = pm.get_template_json_path("custom")
            assert json_path == Path("/templates/custom.json")

    def test_get_template_json_path_removes_extension(self):
        """Test template JSON path removes .json extension if present"""
        pm = PathManager()

        with patch.object(pm, "get_template_folder") as mock_folder:
            mock_folder.return_value = Path("/templates")

            json_path = pm.get_template_json_path("custom.json")
            assert json_path == Path("/templates/custom.json")

    def test_validate_template_exists_true(self):
        """Test template validation when file exists"""
        pm = PathManager()

        with patch.object(pm, "get_template_file_path") as mock_path:
            mock_template = MagicMock()
            mock_template.exists.return_value = True
            mock_path.return_value = mock_template

            assert pm.validate_template_exists("test") is True

    def test_validate_template_exists_false(self):
        """Test template validation when file doesn't exist"""
        pm = PathManager()

        with patch.object(pm, "get_template_file_path") as mock_path:
            mock_template = MagicMock()
            mock_template.exists.return_value = False
            mock_path.return_value = mock_template

            assert pm.validate_template_exists("test") is False

    def test_validate_template_folder_exists_true(self):
        """Test template folder validation when folder exists"""
        pm = PathManager()

        with patch.object(pm, "get_template_folder") as mock_folder:
            mock_folder_path = MagicMock()
            mock_folder_path.exists.return_value = True
            mock_folder.return_value = mock_folder_path

            assert pm.validate_template_folder_exists() is True

    def test_validate_template_folder_exists_false(self):
        """Test template folder validation when folder doesn't exist"""
        pm = PathManager()

        with patch.object(pm, "get_template_folder") as mock_folder:
            mock_folder_path = MagicMock()
            mock_folder_path.exists.return_value = False
            mock_folder.return_value = mock_folder_path

            assert pm.validate_template_folder_exists() is False

    def test_validate_assets_exist_true(self):
        """Test assets validation when assets exist"""
        pm = PathManager()

        with patch.object(pm, "get_assets_templates_path") as mock_assets:
            mock_assets_path = MagicMock()
            mock_assets_path.exists.return_value = True

            mock_pptx = MagicMock()
            mock_pptx.exists.return_value = True
            mock_json = MagicMock()
            mock_json.exists.return_value = True

            mock_assets_path.__truediv__ = lambda self, other: (
                mock_pptx if "pptx" in str(other) else mock_json
            )
            mock_assets.return_value = mock_assets_path

            assert pm.validate_assets_exist() is True

    def test_validate_assets_exist_false(self):
        """Test assets validation when assets don't exist"""
        pm = PathManager()

        with patch.object(pm, "get_assets_templates_path") as mock_assets:
            mock_assets_path = MagicMock()
            mock_assets_path.exists.return_value = False
            mock_assets.return_value = mock_assets_path

            assert pm.validate_assets_exist() is False

    def test_list_available_templates(self):
        """Test listing available templates"""
        pm = PathManager()

        with patch.object(pm, "get_template_folder") as mock_folder:
            mock_folder_path = MagicMock()
            mock_folder_path.exists.return_value = True

            # Mock glob to return some template files
            mock_files = [
                MagicMock(stem="default"),
                MagicMock(stem="custom"),
                MagicMock(stem="business"),
            ]
            mock_folder_path.glob.return_value = mock_files
            mock_folder.return_value = mock_folder_path

            templates = pm.list_available_templates()
            assert templates == ["business", "custom", "default"]  # Should be sorted

    def test_list_available_templates_no_folder(self):
        """Test listing templates when folder doesn't exist"""
        pm = PathManager()

        with patch.object(pm, "get_template_folder") as mock_folder:
            mock_folder_path = MagicMock()
            mock_folder_path.exists.return_value = False
            mock_folder.return_value = mock_folder_path

            templates = pm.list_available_templates()
            assert templates == []

    @patch("importlib.metadata.version")
    def test_get_version_from_metadata(self, mock_version):
        """Test version retrieval from package metadata"""
        mock_version.return_value = "1.0.1"

        pm = PathManager()
        version = pm.get_version()

        assert version == "1.0.1"
        mock_version.assert_called_once_with("deckbuilder")

    def test_singleton_path_manager(self):
        """Test that path_manager is a singleton instance"""
        pm1 = path_manager
        pm2 = path_manager

        assert pm1 is pm2
        assert isinstance(pm1, PathManager)

    def test_cache_usage(self):
        """Test that PathManager caches project root"""
        pm = PathManager()

        # First call should compute and cache
        root1 = pm.get_project_root()

        # Second call should use cache
        root2 = pm.get_project_root()

        assert root1 == root2
        assert "project_root" in pm._cache


class TestPathManagerIntegration:
    """Integration tests for PathManager with real filesystem"""

    def test_real_project_root_detection(self):
        """Test that PathManager correctly detects the real project root"""
        pm = PathManager()
        root = pm.get_project_root()

        # Should find the actual Deckbuilder project
        assert (root / "src" / "deckbuilder").exists()
        assert (root / "assets" / "templates").exists()

    def test_real_assets_validation(self):
        """Test assets validation with real filesystem"""
        pm = PathManager()

        # Should find real assets
        assets_exist = pm.validate_assets_exist()
        assert assets_exist is True

    def test_environment_integration(self):
        """Test environment variable integration"""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(os.environ, {"DECK_TEMPLATE_FOLDER": temp_dir}):
                pm = PathManager()
                template_folder = pm.get_template_folder()

                # Use resolve() to handle macOS /private symlinks
                assert str(template_folder.resolve()) == str(Path(temp_dir).resolve())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
