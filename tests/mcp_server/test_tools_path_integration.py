#!/usr/bin/env python3
"""
Unit tests for MCP Server PathManager integration

Tests that the MCP server tools properly use PathManager
for template analysis and path resolution.
"""

import os
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.mcp_server.tools import TemplateAnalyzer
from src.deckbuilder.path_manager import path_manager


class TestMCPToolsPathManagerIntegration:
    """Test MCP server tools use PathManager consistently"""

    def test_template_analyzer_constructor_uses_path_manager(self):
        """Test TemplateAnalyzer constructor uses PathManager"""
        with patch.object(path_manager, 'get_template_folder') as mock_template, \
             patch.object(path_manager, 'get_output_folder') as mock_output:
            
            mock_template.return_value = Path("/test/templates")
            mock_output.return_value = Path("/test/output")
            
            analyzer = TemplateAnalyzer()
            
            # Should call PathManager methods
            mock_template.assert_called_once()
            mock_output.assert_called_once()
            
            # Should set paths correctly
            assert analyzer.template_path == "/test/templates"
            assert analyzer.output_folder == "/test/output"

    def test_template_analyzer_no_direct_environment_access(self):
        """Test TemplateAnalyzer doesn't directly access environment variables"""
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(path_manager, 'get_template_folder') as mock_template, \
                 patch.object(path_manager, 'get_output_folder') as mock_output:
                
                mock_template.return_value = Path("/test/templates")
                mock_output.return_value = Path("/test/output")
                
                analyzer = TemplateAnalyzer()
                
                # Should work even with no environment variables
                assert analyzer.template_path == "/test/templates"
                assert analyzer.output_folder == "/test/output"

    def test_analyze_pptx_template_uses_path_manager_validation(self):
        """Test analyze_pptx_template uses PathManager for validation"""
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/templates")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/output")):
            
            analyzer = TemplateAnalyzer()
            
            with patch.object(path_manager, 'validate_template_folder_exists') as mock_validate, \
                 patch.object(path_manager, 'get_template_file_path') as mock_file_path:
                
                mock_validate.return_value = False
                mock_file_path.return_value = Path("/templates/test.pptx")
                
                with pytest.raises(RuntimeError, match="Template folder not found"):
                    analyzer.analyze_pptx_template("test")
                
                mock_validate.assert_called_once()

    def test_analyze_pptx_template_uses_path_manager_file_path(self):
        """Test analyze_pptx_template uses PathManager for file path resolution"""
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/templates")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/output")):
            
            analyzer = TemplateAnalyzer()
            
            with patch.object(path_manager, 'validate_template_folder_exists', return_value=True), \
                 patch.object(path_manager, 'get_template_file_path') as mock_file_path, \
                 patch('src.mcp_server.tools.os.path.exists', return_value=False):
                
                mock_file_path.return_value = Path("/templates/test.pptx")
                
                with pytest.raises(FileNotFoundError, match="Template file not found"):
                    analyzer.analyze_pptx_template("test")
                
                # Should call PathManager to get template file path
                mock_file_path.assert_called_once_with("test.pptx")

    @patch('src.mcp_server.tools.Presentation')
    def test_analyze_pptx_template_successful_analysis(self, mock_presentation):
        """Test successful template analysis uses correct paths"""
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/templates")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/output")):
            
            analyzer = TemplateAnalyzer()
            
            # Mock successful template loading
            mock_prs = MagicMock()
            mock_prs.slide_layouts = []
            mock_presentation.return_value = mock_prs
            
            with patch.object(path_manager, 'validate_template_folder_exists', return_value=True), \
                 patch.object(path_manager, 'get_template_file_path') as mock_file_path, \
                 patch('src.mcp_server.tools.os.path.exists', return_value=True):
                
                mock_file_path.return_value = Path("/templates/test.pptx")
                
                result = analyzer.analyze_pptx_template("test")
                
                # Should successfully analyze with PathManager-resolved path
                assert isinstance(result, dict)
                mock_presentation.assert_called_once_with("/templates/test.pptx")

    def test_template_name_normalization(self):
        """Test template name normalization works with PathManager"""
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/templates")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/output")):
            
            analyzer = TemplateAnalyzer()
            
            with patch.object(path_manager, 'validate_template_folder_exists', return_value=True), \
                 patch.object(path_manager, 'get_template_file_path') as mock_file_path, \
                 patch('src.mcp_server.tools.os.path.exists', return_value=False):
                
                mock_file_path.return_value = Path("/templates/test.pptx")
                
                # Test without .pptx extension
                with pytest.raises(FileNotFoundError):
                    analyzer.analyze_pptx_template("test")
                
                # Should add .pptx extension and call PathManager
                mock_file_path.assert_called_with("test.pptx")
                
                # Test with .pptx extension
                mock_file_path.reset_mock()
                with pytest.raises(FileNotFoundError):
                    analyzer.analyze_pptx_template("test.pptx")
                
                # Should pass through with extension
                mock_file_path.assert_called_with("test.pptx")


class TestMCPToolsErrorHandling:
    """Test MCP tools error handling with PathManager"""

    def test_missing_template_folder_error(self):
        """Test proper error when template folder doesn't exist"""
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/nonexistent")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/output")):
            
            analyzer = TemplateAnalyzer()
            
            with patch.object(path_manager, 'validate_template_folder_exists', return_value=False):
                with pytest.raises(RuntimeError) as exc_info:
                    analyzer.analyze_pptx_template("test")
                
                # Should show the actual template folder path
                assert "/nonexistent" in str(exc_info.value)

    def test_missing_template_file_error(self):
        """Test proper error when template file doesn't exist"""
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/templates")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/output")):
            
            analyzer = TemplateAnalyzer()
            
            with patch.object(path_manager, 'validate_template_folder_exists', return_value=True), \
                 patch.object(path_manager, 'get_template_file_path', return_value=Path("/templates/missing.pptx")), \
                 patch('src.mcp_server.tools.os.path.exists', return_value=False):
                
                with pytest.raises(FileNotFoundError) as exc_info:
                    analyzer.analyze_pptx_template("missing")
                
                # Should show the resolved template file path
                assert "/templates/missing.pptx" in str(exc_info.value)


class TestMCPToolsEnvironmentIsolation:
    """Test MCP tools are isolated from environment changes"""

    def test_analyzer_paths_stable_across_env_changes(self):
        """Test analyzer paths don't change when environment changes"""
        with patch.dict(os.environ, {"DECK_TEMPLATE_FOLDER": "/initial"}):
            with patch.object(path_manager, 'get_template_folder', return_value=Path("/initial")), \
                 patch.object(path_manager, 'get_output_folder', return_value=Path("/initial")):
                
                analyzer = TemplateAnalyzer()
                initial_path = analyzer.template_path
        
        # Change environment
        with patch.dict(os.environ, {"DECK_TEMPLATE_FOLDER": "/changed"}):
            # Analyzer should still have original path
            assert analyzer.template_path == initial_path

    def test_fresh_analyzer_uses_current_path_manager_state(self):
        """Test fresh analyzer instance uses current PathManager state"""
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/first")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/first")):
            
            analyzer1 = TemplateAnalyzer()
            path1 = analyzer1.template_path
            
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/second")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/second")):
            
            analyzer2 = TemplateAnalyzer()
            path2 = analyzer2.template_path
            
        # Should reflect different PathManager states
        assert path1 == "/first"
        assert path2 == "/second"


class TestMCPToolsRealWorldScenarios:
    """Test MCP tools with realistic scenarios"""

    def test_analyzer_with_realistic_paths(self):
        """Test analyzer with realistic file system paths"""
        with tempfile.TemporaryDirectory() as temp_dir:
            templates_dir = Path(temp_dir) / "templates"
            templates_dir.mkdir()
            
            with patch.object(path_manager, 'get_template_folder', return_value=templates_dir), \
                 patch.object(path_manager, 'get_output_folder', return_value=Path(temp_dir)), \
                 patch.object(path_manager, 'validate_template_folder_exists', return_value=True), \
                 patch.object(path_manager, 'get_template_file_path') as mock_file_path:
                
                mock_file_path.return_value = templates_dir / "test.pptx"
                
                analyzer = TemplateAnalyzer()
                
                # Should use the realistic paths
                assert str(templates_dir) in analyzer.template_path
                assert temp_dir in analyzer.output_folder

    def test_analyzer_integration_with_path_manager_validation(self):
        """Test full integration between analyzer and PathManager validation"""
        with patch.object(path_manager, 'get_template_folder', return_value=Path("/templates")), \
             patch.object(path_manager, 'get_output_folder', return_value=Path("/output")):
            
            analyzer = TemplateAnalyzer()
            
            # Test the full path resolution and validation flow
            with patch.object(path_manager, 'validate_template_folder_exists') as mock_validate, \
                 patch.object(path_manager, 'get_template_file_path') as mock_file_path:
                
                mock_validate.return_value = True
                mock_file_path.return_value = Path("/templates/test.pptx")
                
                with patch('src.mcp_server.tools.os.path.exists', return_value=True), \
                     patch('src.mcp_server.tools.Presentation') as mock_prs:
                    
                    mock_prs.return_value.slide_layouts = []
                    
                    result = analyzer.analyze_pptx_template("test")
                    
                    # Should complete the full validation and analysis flow
                    mock_validate.assert_called_once()
                    mock_file_path.assert_called_once_with("test.pptx")
                    assert isinstance(result, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])