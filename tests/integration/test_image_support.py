#!/usr/bin/env python3
"""
Integration tests for PlaceKitten-Deckbuilder image support.
Tests the end-to-end image workflow including fallback generation.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))  # noqa: E402

from deckbuilder.converter import markdown_to_canonical_json  # noqa: E402


def test_image_integration(fresh_deckbuilder):
    """Test image support in presentations."""
    print("🧪 Testing PlaceKitten-Deckbuilder image integration...")

    # Use the fresh_deckbuilder fixture which has proper environment setup
    deck = fresh_deckbuilder

    # Test slide with Picture with Caption layout using structured frontmatter
    markdown_content = """---
layout: Picture with Caption
title: System Architecture Overview
image: "non_existent_image.png"
text_caption: "System architecture with Frontend, API, and Database components"
---
"""

    # Convert markdown to canonical JSON format
    canonical_data = markdown_to_canonical_json(markdown_content)

    # Create presentation from canonical JSON
    result = deck.create_presentation(canonical_data, "image_test")
    print(f"✅ {result}")

    # Extract the actual file path from the result message
    assert result and isinstance(result, str)

    # Result format: "Successfully created presentation with 1 slides. Successfully created presentation: filename.pptx"
    if "Successfully created presentation:" in result:
        filename = result.split("Successfully created presentation:")[-1].strip()
        # Get the output folder from environment
        output_folder = os.environ.get("DECK_OUTPUT_FOLDER")
        if output_folder:
            result_path = Path(output_folder) / filename
        else:
            result_path = Path(filename)
    else:
        result_path = Path(result)

    assert result_path.exists(), f"Generated file does not exist: {result_path}"
    assert result_path.suffix == ".pptx"
    assert "image_test" in result_path.name

    print(f"📄 Generated presentation: {result_path.name}")
    print(f"📍 Location: {result_path.parent}")
    print("✅ Image integration test completed successfully!")
    return True


def test_placekitten_availability():
    """Test PlaceKitten library availability."""
    print("🐱 Testing PlaceKitten availability...")

    try:
        from placekitten import PlaceKitten

        pk = PlaceKitten()
        images = pk.list_available_images()
        print(f"✅ PlaceKitten available with {len(images)} images")
        return True
    except ImportError:
        print("⚠️ PlaceKitten library not available - fallbacks will be disabled")
        return False
    except Exception as e:
        print(f"❌ PlaceKitten error: {e}")
        return False


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v", "-s"])
