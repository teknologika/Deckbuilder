"""
Global pytest configuration and fixtures for deck-builder MCP tests.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

import pytest

# Add src to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def project_root():
    """Path to project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def temp_dir():
    """Temporary directory for test files."""
    temp_dir = tempfile.mkdtemp(prefix="deckbuilder_test_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_deckbuilder_env():
    """Mock environment variables for deckbuilder with proper cleanup."""
    # Clear any existing singleton instances for atomic testing
    try:
        from deckbuilder.engine import Deckbuilder

        if hasattr(Deckbuilder, "_instances"):
            Deckbuilder._instances.clear()
    except ImportError:
        pass

    # Create temporary directories
    import tempfile

    temp_base = tempfile.mkdtemp(prefix="deckbuilder_test_")
    templates_dir = Path(temp_base) / "templates"
    output_dir = Path(temp_base) / "output"

    templates_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Store original environment
    original_env = os.environ.copy()

    # Set test environment variables
    test_env = {
        "DECK_TEMPLATE_FOLDER": str(templates_dir),
        "DECK_OUTPUT_FOLDER": str(output_dir),
        "DECK_TEMPLATE_NAME": "default",
    }

    for key, value in test_env.items():
        os.environ[key] = value

    yield {"templates_dir": templates_dir, "output_dir": output_dir}

    # Clean up: restore environment and clear singletons
    os.environ.clear()
    os.environ.update(original_env)

    # Clear singleton instances again for next test
    try:
        if hasattr(Deckbuilder, "_instances"):
            Deckbuilder._instances.clear()
    except ImportError:
        pass

    # Clean up temp directory
    import shutil

    shutil.rmtree(temp_base, ignore_errors=True)


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    original_env = os.environ.copy()

    # Set test environment variables
    test_env = {
        "DECK_TEMPLATE_FOLDER": str(Path(__file__).parent / "fixtures" / "sample_templates"),
        "DECK_OUTPUT_FOLDER": str(Path(__file__).parent / "fixtures" / "test_outputs"),
        "DECK_TEMPLATE_NAME": "default",
    }

    for key, value in test_env.items():
        os.environ[key] = value

    yield test_env

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_template_json():
    """Basic template JSON structure for testing."""
    return {
        "template_info": {"name": "Test Template", "version": "1.0"},
        "layouts": {
            "Title Slide": {
                "index": 0,
                "placeholders": {
                    "0": "title_top_1",
                    "1": "subtitle_1",
                    "10": "date_footer_1",
                    "11": "footer_footer_1",
                    "12": "slide_number_footer_1",
                },
            },
            "Four Columns With Titles": {
                "index": 1,
                "placeholders": {
                    "0": "title_top_1",
                    "1": "title_col1_1",
                    "2": "content_col1_1",
                    "3": "title_col2_1",
                    "4": "content_col2_1",
                    "5": "title_col3_1",
                    "6": "content_col3_1",
                    "7": "title_col4_1",
                    "8": "content_col4_1",
                    "10": "date_footer_1",
                    "11": "footer_footer_1",
                    "12": "slide_number_footer_1",
                },
            },
            "Comparison": {
                "index": 2,
                "placeholders": {
                    "0": "title_top_1",
                    "1": "title_left_1",
                    "2": "content_left_1",
                    "3": "title_right_1",
                    "4": "content_right_1",
                    "10": "date_footer_1",
                    "11": "footer_footer_1",
                    "12": "slide_number_footer_1",
                },
            },
        },
    }


@pytest.fixture
def sample_presentation_data():
    """Sample presentation data structure."""
    return {
        "presentation": {
            "slides": [
                {
                    "type": "Title Slide",
                    "layout": "Title Slide",
                    "title": "Test Presentation",
                    "rich_content": [{"heading": "Testing Framework Implementation", "level": 2}],
                },
                {
                    "type": "Four Columns With Titles",
                    "title": "Four Column Test",
                    "title_col1_1": "Performance",
                    "content_col1_1": "Fast processing with optimized algorithms",
                    "title_col2_1": "Security",
                    "content_col2_1": "Enterprise-grade encryption",
                    "title_col3_1": "Usability",
                    "content_col3_1": "Intuitive interface",
                    "title_col4_1": "Cost",
                    "content_col4_1": "Competitive pricing",
                },
            ]
        }
    }


@pytest.fixture
def sample_structured_frontmatter():
    """Sample structured frontmatter for testing."""
    return """---
layout: Four Columns With Titles
title: Feature Comparison
columns:
  - title: Performance
    content: Fast processing with optimized algorithms
  - title: Security
    content: Enterprise-grade encryption and compliance
  - title: Usability
    content: Intuitive interface with minimal learning curve
  - title: Cost
    content: Competitive pricing with flexible plans
---

Content from Four Columns With Titles structured frontmatter above."""


@pytest.fixture
def formatted_content_samples():
    """Sample content with various formatting."""
    return {
        "bold": "**Bold text** for emphasis",
        "italic": "*Italic text* for subtle emphasis",
        "underline": "___Underlined text___ for highlighting",
        "combined": "***Bold and italic*** with ___underline___ combinations",
        "mixed": "Regular text with **bold**, *italic*, and ___underlined___ parts",
    }


@pytest.fixture
def table_data_sample():
    """Sample table data for testing."""
    return {
        "data": [
            ["**Feature**", "*Status*", "___Priority___"],
            ["Authentication", "**Complete**", "*High*"],
            ["User Management", "***In Progress***", "___Medium___"],
            ["Reporting", "*Planned*", "**Low**"],
            ["API Integration", "___Blocked___", "***Critical***"],
        ],
        "header_style": "dark_blue_white_text",
        "row_style": "alternating_light_gray",
        "border_style": "thin_gray",
    }


# Test helper functions
def create_test_file(path: Path, content: str) -> Path:
    """Create a test file with given content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def load_json_file(path: Path) -> Dict[str, Any]:
    """Load JSON file safely."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(path: Path, data: Dict[str, Any]) -> None:
    """Save data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
