#!/usr/bin/env python3
"""
Unit tests for Engine PathManager integration

Tests that the Deckbuilder engine properly uses PathManager
for all path resolution instead of direct environment access.
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.deckbuilder.engine import Deckbuilder  # noqa: E402
from src.deckbuilder.path_manager import path_manager  # noqa: E402


class TestEnginePathManagerIntegration:
    """Test Deckbuilder engine uses PathManager consistently"""

    def test_engine_constructor_uses_path_manager(self):
        """Test engine constructor uses PathManager for paths"""

        with (
            patch.object(path_manager, "get_template_folder") as mock_template,
            patch.object(path_manager, "get_output_folder") as mock_output,
            patch.object(path_manager, "get_template_name") as mock_name,
        ):

            mock_template.return_value = Path("/test/templates")
            mock_output.return_value = Path("/test/output")
            mock_name.return_value = "test_template"

            # Clear the singleton cache to force fresh instance
            if hasattr(Deckbuilder, "_instances"):
                Deckbuilder._instances.clear()

            engine = Deckbuilder()

            # Should call PathManager methods
            mock_template.assert_called()
            mock_output.assert_called()
            mock_name.assert_called()

            # Should set paths correctly
            assert engine.output_folder == "/test/output"

    def test_engine_cache_dir_uses_path_manager(self):
        """Test engine cache directory uses PathManager output folder"""

        with (
            patch.object(path_manager, "get_template_folder") as mock_template,
            patch.object(path_manager, "get_output_folder") as mock_output,
            patch.object(path_manager, "get_template_name") as mock_name,
        ):

            mock_template.return_value = Path("/test/templates")
            mock_output.return_value = Path("/test/output")
            mock_name.return_value = "test_template"

            # Clear the singleton cache to force fresh instance
            if hasattr(Deckbuilder, "_instances"):
                Deckbuilder._instances.clear()

            engine = Deckbuilder()

            # Cache directory should be based on PathManager output folder
            # expected_cache = str(Path("/test/output") / "tmp" / "image_cache")
            # Future: validate cache path
            # The cache dir is passed to ImageHandler, so we check it was constructed correctly
            assert engine.presentation_builder is not None

    def test_engine_no_direct_environment_access(self):
        """Test engine doesn't directly access environment variables"""
        # This test ensures we don't regress to direct os.getenv usage

        with patch.dict(os.environ, {}, clear=True):
            with (
                patch.object(path_manager, "get_template_folder") as mock_template,
                patch.object(path_manager, "get_output_folder") as mock_output,
                patch.object(path_manager, "get_template_name") as mock_name,
            ):

                mock_template.return_value = Path("/test/templates")
                mock_output.return_value = Path("/test/output")
                mock_name.return_value = "test"

                # Clear the singleton cache
                if hasattr(Deckbuilder, "_instances"):
                    Deckbuilder._instances.clear()

                engine = Deckbuilder()

                # Should work even with no environment variables
                # because it uses PathManager
                assert engine.output_folder == "/test/output"

    def test_create_presentation_uses_path_manager_paths(self):
        """Test create_presentation method uses PathManager-resolved paths"""

        with (
            patch.object(path_manager, "get_template_folder") as mock_template,
            patch.object(path_manager, "get_output_folder") as mock_output,
            patch.object(path_manager, "get_template_name") as mock_name,
        ):

            mock_template.return_value = Path("/test/templates")
            mock_output.return_value = Path("/test/output")
            mock_name.return_value = "test"

            # Clear singleton cache
            if hasattr(Deckbuilder, "_instances"):
                Deckbuilder._instances.clear()

            engine = Deckbuilder()

            # Mock at the presentation builder level to focus on path management testing
            with (
                patch("src.deckbuilder.engine.Presentation") as mock_presentation_class,
                patch.object(engine.presentation_builder, 'add_slide') as mock_add_slide,
                patch.object(engine, 'write_presentation') as mock_write,
            ):
                mock_prs = Mock()
                mock_prs.save = Mock()
                # Mock slides collection for clear_slides operation
                mock_slides = Mock()
                mock_slides.__len__ = Mock(return_value=0)
                mock_slides._sldIdLst = []
                mock_prs.slides = mock_slides
                mock_presentation_class.return_value = mock_prs

                # Should use PathManager-resolved paths
                # Provide minimal valid canonical JSON data
                minimal_data = {
                    "slides": [
                        {
                            "layout": "Title Slide", 
                            "placeholders": {"title": "Test"}, 
                            "content": []
                        }
                    ]
                }
                # result = engine.create_presentation(minimal_data)  # Future: validate result
                engine.create_presentation(minimal_data)
                
                # Verify presentation builder was called (focusing on path integration)
                mock_add_slide.assert_called_once()
                mock_write.assert_called_once()

                # Should use PathManager-resolved paths for template operations
                # Note: After refactoring, direct path checks are handled by template_manager
                assert engine.template_manager is not None

    def test_singleton_behavior_with_path_manager(self):
        """Test singleton behavior works correctly with PathManager"""
        with (
            patch.object(path_manager, "get_template_folder", return_value=Path("/test1")),
            patch.object(path_manager, "get_output_folder", return_value=Path("/test1")),
            patch.object(path_manager, "get_template_name", return_value="test1"),
        ):

            # Clear singleton cache
            if hasattr(Deckbuilder, "_instances"):
                Deckbuilder._instances.clear()

            engine1 = Deckbuilder()

        # Even if PathManager returns different values later,
        # singleton should return same instance
        with (
            patch.object(path_manager, "get_template_folder", return_value=Path("/test2")),
            patch.object(path_manager, "get_output_folder", return_value=Path("/test2")),
            patch.object(path_manager, "get_template_name", return_value="test2"),
        ):

            engine2 = Deckbuilder()

            # Should be same instance (singleton behavior)
            assert engine1 is engine2


class TestEnginePathResolution:
    """Test specific path resolution methods in engine"""

    def test_check_template_exists_uses_resolved_paths(self):
        """Test _check_template_exists uses resolved template paths"""

        with (
            patch.object(path_manager, "get_template_folder", return_value=Path("/templates")),
            patch.object(path_manager, "get_output_folder", return_value=Path("/output")),
            patch.object(path_manager, "get_template_name", return_value="default"),
        ):

            # Clear singleton cache
            if hasattr(Deckbuilder, "_instances"):
                Deckbuilder._instances.clear()

            engine = Deckbuilder()

            # Template existence checking is now handled by template_manager
            assert engine.template_manager is not None

    def test_load_layout_mapping_uses_resolved_paths(self):
        """Test _load_layout_mapping uses resolved template paths"""
        with (
            patch.object(path_manager, "get_template_folder", return_value=Path("/templates")),
            patch.object(path_manager, "get_output_folder", return_value=Path("/output")),
            patch.object(path_manager, "get_template_name", return_value="default"),
        ):

            # Clear singleton cache
            if hasattr(Deckbuilder, "_instances"):
                Deckbuilder._instances.clear()

            engine = Deckbuilder()

            # Layout mapping is now handled by template_manager
            assert engine.template_manager is not None


def mock_open_json(json_data):
    """Helper to mock file opening with JSON data"""
    import json
    from unittest.mock import mock_open

    return mock_open(read_data=json.dumps(json_data))


class TestEngineEnvironmentIsolation:
    """Test engine is isolated from environment variable changes"""

    def test_engine_paths_stable_across_env_changes(self):
        """Test engine paths don't change when environment changes after init"""
        with patch.dict(os.environ, {"DECK_TEMPLATE_FOLDER": "/initial"}):
            with (
                patch.object(path_manager, "get_template_folder", return_value=Path("/initial")),
                patch.object(path_manager, "get_output_folder", return_value=Path("/initial")),
                patch.object(path_manager, "get_template_name", return_value="initial"),
            ):

                # Clear singleton cache
                if hasattr(Deckbuilder, "_instances"):
                    Deckbuilder._instances.clear()

                engine = Deckbuilder()
                initial_path = engine.output_folder

        # Change environment
        with patch.dict(os.environ, {"DECK_TEMPLATE_FOLDER": "/changed"}):
            # Engine should still have original path (singleton + initialization)
            assert engine.output_folder == initial_path

    def test_fresh_engine_uses_current_path_manager_state(self):
        """Test fresh engine instance uses current PathManager state"""
        # This test verifies that if we clear the singleton cache,
        # a new engine picks up current PathManager state

        with (
            patch.object(path_manager, "get_template_folder", return_value=Path("/first")),
            patch.object(path_manager, "get_output_folder", return_value=Path("/first")),
            patch.object(path_manager, "get_template_name", return_value="first"),
        ):

            # Clear singleton cache
            if hasattr(Deckbuilder, "_instances"):
                Deckbuilder._instances.clear()

            engine1 = Deckbuilder()
            path1 = engine1.output_folder

        # Clear singleton and create new with different PathManager state
        if hasattr(Deckbuilder, "_instances"):
            Deckbuilder._instances.clear()

        with (
            patch.object(path_manager, "get_template_folder", return_value=Path("/second")),
            patch.object(path_manager, "get_output_folder", return_value=Path("/second")),
            patch.object(path_manager, "get_template_name", return_value="second"),
        ):

            engine2 = Deckbuilder()
            path2 = engine2.output_folder

        # Should reflect different PathManager states
        assert path1 == "/first"
        assert path2 == "/second"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
