"""
Basic test to ensure the package can be imported and meets coverage requirements.
"""


def test_package_import():
    """Test that the main package can be imported."""
    import deckbuilder

    assert deckbuilder is not None


def test_logging_config():
    """Test logging configuration module."""
    from deckbuilder.utils.logging import debug_print, error_print, success_print

    # Test that functions exist and are callable
    assert callable(debug_print)
    assert callable(error_print)
    assert callable(success_print)

    # Test basic functionality
    debug_print("test debug message")
    error_print("test error message")
    success_print("test success message")


def test_placeholder_types():
    """Test placeholder types module."""
    from deckbuilder.content.placeholder_types import (
        is_content_placeholder,
        is_media_placeholder,
        is_subtitle_placeholder,
        is_title_placeholder,
    )
    from pptx.enum.shapes import PP_PLACEHOLDER_TYPE

    # Test that functions exist and are callable
    assert callable(is_content_placeholder)
    assert callable(is_media_placeholder)
    assert callable(is_subtitle_placeholder)
    assert callable(is_title_placeholder)

    # Test valid placeholder types
    assert is_title_placeholder(PP_PLACEHOLDER_TYPE.TITLE)
    assert is_subtitle_placeholder(PP_PLACEHOLDER_TYPE.SUBTITLE)
    assert is_content_placeholder(PP_PLACEHOLDER_TYPE.BODY)
    assert is_media_placeholder(PP_PLACEHOLDER_TYPE.PICTURE)

    # Test TypeError fix - these should NOT raise TypeError and return False
    assert not is_title_placeholder(True)  # Boolean input
    assert not is_title_placeholder(False)  # Boolean input
    assert not is_title_placeholder("string")  # String input
    assert not is_title_placeholder(123)  # Integer input
    assert not is_title_placeholder(None)  # None input

    assert not is_subtitle_placeholder(True)
    assert not is_subtitle_placeholder("invalid")

    assert not is_content_placeholder(False)
    assert not is_content_placeholder(42)

    assert not is_media_placeholder(True)
    assert not is_media_placeholder([])


def test_table_styles():
    """Test table styles module."""
    from deckbuilder.templates.table_styles import TABLE_HEADER_STYLES

    # Test that styles are defined
    assert TABLE_HEADER_STYLES is not None
    assert isinstance(TABLE_HEADER_STYLES, dict)
