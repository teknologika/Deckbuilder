#!/usr/bin/env python3
"""
Test script for enhanced image support in Deckbuilder presentations.
Demonstrates both valid images and PlaceKitten fallback functionality.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))  # noqa: E402

from deckbuilder.engine import Deckbuilder  # noqa: E402


def run_image_presentation_test():
    """Run the enhanced presentation test with image support."""
    print("🎨 Testing Enhanced Deckbuilder with Image Support")
    print("=" * 60)

    # Set output to tests directory
    test_output_dir = Path(__file__).parent / "output"
    test_output_dir.mkdir(exist_ok=True)

    # Set environment variable for output
    original_output = os.environ.get("DECK_OUTPUT_FOLDER")
    os.environ["DECK_OUTPUT_FOLDER"] = str(test_output_dir)

    try:
        # Initialize Deckbuilder
        deck = Deckbuilder()
        print("✅ Deckbuilder initialized successfully")

        # Check PlaceKitten availability
        if deck.placekitten.is_available():
            print("✅ PlaceKitten integration available")
            fallback_info = deck.placekitten.get_fallback_info((800, 600))
            print(f"   Available images: {fallback_info.get('image_id', 'N/A')}")
            styling = fallback_info.get("styling", {}).get("base_filter", "N/A")
            print(f"   Professional styling: {styling}")
        else:
            print("⚠️ PlaceKitten not available - fallbacks disabled")

        # Read test markdown file
        test_file = Path(__file__).parent / "test_presentation.md"
        print(f"📖 Reading test file: {test_file.name}")

        with open(test_file, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        # Create presentation from enhanced markdown
        print("\n🏗️ Creating presentation with image support...")
        result = deck.create_presentation_from_markdown(
            markdown_content, fileName="enhanced_image_test", templateName="default"
        )

        print(f"✅ {result}")

        # List generated files
        output_files = list(test_output_dir.glob("*enhanced_image_test*.g.pptx"))
        if output_files:
            for file in output_files:
                file_size = file.stat().st_size / 1024  # KB
                print(f"📄 Generated: {file.name} ({file_size:.1f} KB)")

        # Display cache statistics
        cache_stats = deck.image_handler.get_cache_stats()
        print("\n📊 Image Cache Statistics:")
        print(f"   Files cached: {cache_stats['file_count']}")
        print(f"   Cache size: {cache_stats['total_size_mb']} MB")
        print(f"   Cache location: {Path(cache_stats['cache_dir']).name}")

        print("\n🎉 Image presentation test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        # Restore environment
        if original_output:
            os.environ["DECK_OUTPUT_FOLDER"] = original_output
        elif "DECK_OUTPUT_FOLDER" in os.environ:
            del os.environ["DECK_OUTPUT_FOLDER"]


def demonstrate_image_features():
    """Demonstrate specific image handling features."""
    print("\n🔧 Image Feature Demonstration")
    print("-" * 40)

    try:
        deck = Deckbuilder()

        # Test ImageHandler
        print("🖼️ ImageHandler Features:")
        valid_image = "src/placekitten/images/ACuteKitten-1.png"
        invalid_image = "assets/non_existent.png"

        print(f"   Valid image check: {deck.image_handler.validate_image(valid_image)}")
        print(f"   Invalid image check: {deck.image_handler.validate_image(invalid_image)}")

        if Path(valid_image).exists():
            dimensions = deck.image_handler.get_image_dimensions(valid_image)
            print(f"   Image dimensions: {dimensions}")

        # Test PlaceKitten fallback info
        print("\n🐱 PlaceKitten Features:")
        if deck.placekitten.is_available():
            fallback_info = deck.placekitten.get_fallback_info(
                (800, 600), context={"layout": "Picture with Caption", "slide_index": 1}
            )
            print(f"   Fallback available: {fallback_info['available']}")
            print(f"   Selected image ID: {fallback_info['image_id']}")
            print(f"   Professional config: {fallback_info['styling']['base_filter']}")
            print(f"   Cached: {fallback_info['cached']}")

        return True

    except Exception as e:
        print(f"❌ Feature demonstration failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Enhanced Deckbuilder Image Support Test Suite")
    print("=" * 60)

    # Run main presentation test
    presentation_success = run_image_presentation_test()

    # Demonstrate features
    features_success = demonstrate_image_features()

    print("\n📊 Test Results:")
    print(f"  Presentation Test: {'✅' if presentation_success else '❌'}")
    print(f"  Feature Demo: {'✅' if features_success else '❌'}")

    if presentation_success and features_success:
        print("\n🎉 All tests passed! Enhanced image support is working perfectly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check output above for details.")
        sys.exit(1)
