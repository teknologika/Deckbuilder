#!/usr/bin/env python3
"""
Integration tests for PlaceKitten-Deckbuilder image support.
Tests the end-to-end image workflow including fallback generation.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))  # noqa: E402

from deckbuilder.engine import Deckbuilder  # noqa: E402
from deckbuilder.converter import markdown_to_canonical_json  # noqa: E402


def test_image_integration():
    """Test image support in presentations."""
    print("🧪 Testing PlaceKitten-Deckbuilder image integration...")

    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Using temp directory: {temp_dir}")

        # Set environment variables for template and output folders
        original_output = os.environ.get("DECK_OUTPUT_FOLDER")
        original_template = os.environ.get("DECK_TEMPLATE_FOLDER")
        project_root = Path(__file__).parent.parent.parent

        os.environ["DECK_OUTPUT_FOLDER"] = temp_dir
        os.environ["DECK_TEMPLATE_FOLDER"] = str(project_root / "src" / "deckbuilder" / "assets" / "templates")

        try:
            # Clear any existing Deckbuilder singleton to ensure clean state
            Deckbuilder._instance = None

            # Create deckbuilder instance
            deck = Deckbuilder()

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

            # Check if presentation was created
            output_files = list(Path(temp_dir).glob("*image_test*.g.pptx"))

            if output_files:
                print(f"📄 Generated presentation: {output_files[0].name}")
                print(f"📍 Location: {output_files[0].parent}")
                print("✅ Image integration test completed successfully!")
                return True
            else:
                print("❌ No presentation file was generated")
                print(f"🔍 Checked location: {temp_dir}")
                return False

        finally:
            # Restore original environment
            if original_output:
                os.environ["DECK_OUTPUT_FOLDER"] = original_output
            elif "DECK_OUTPUT_FOLDER" in os.environ:
                del os.environ["DECK_OUTPUT_FOLDER"]

            if original_template:
                os.environ["DECK_TEMPLATE_FOLDER"] = original_template
            elif "DECK_TEMPLATE_FOLDER" in os.environ:
                del os.environ["DECK_TEMPLATE_FOLDER"]


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
    print("🔧 PlaceKitten-Deckbuilder Integration Test Suite")
    print("=" * 60)

    # Test 1: PlaceKitten availability
    placekitten_available = test_placekitten_availability()

    # Test 2: Image integration
    image_test_passed = test_image_integration()

    print("\n📊 Test Results:")
    print(f"  PlaceKitten Available: {'✅' if placekitten_available else '⚠️'}")
    print(f"  Image Integration: {'✅' if image_test_passed else '❌'}")

    if image_test_passed:
        print("\n🎉 All tests passed! Image support is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)
