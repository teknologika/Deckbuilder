#!/usr/bin/env python3
"""
Test script for PlaceKitten core functionality.

This script tests the basic PlaceKitten functionality without requiring
all dependencies to be installed.
"""

import os
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_basic_functionality():
    """Test basic PlaceKitten functionality."""
    print("🧪 Testing PlaceKitten Core Functionality")
    print("=" * 50)

    try:
        # Test import
        print("📦 Testing imports...")
        from placekitten import ImageProcessor, PlaceKitten, list_available_filters

        print("✅ Imports successful!")

        # Test filter list
        print("🎨 Testing filter registry...")
        filters = list_available_filters()
        print(f"✅ Found {len(filters)} filters: {', '.join(filters)}")

        # Test PlaceKitten initialization
        print("🐱 Testing PlaceKitten initialization...")
        pk = PlaceKitten()
        print("✅ PlaceKitten initialized!")

        # Test image discovery
        print("🔍 Testing image discovery...")
        images = pk.list_available_images()
        count = pk.get_image_count()
        print(f"✅ Found {count} images: {', '.join(images)}")

        if count > 0:
            # Test basic image generation
            print("🖼️  Testing image generation...")
            processor = pk.generate(width=400, height=300)
            print(f"✅ Generated image: {processor.get_size()}")

            # Test filter application
            print("🎨 Testing filter application...")
            filtered = processor.apply_filter("sepia")
            print(f"✅ Applied sepia filter: {filtered.get_size()}")

            # Test method chaining
            print("⛓️  Testing method chaining...")
            chained = pk.generate(800).apply_filter("grayscale").resize(200, 200)
            print(f"✅ Method chaining works: {chained.get_size()}")

            print("\n🎉 All basic tests passed!")
            print("✅ Core PlaceKitten functionality is working!")

        else:
            print("⚠️  No images found - cannot test generation")
            print("💡 Ensure kitten images are in assets/images/")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 You may need to install dependencies:")
        print("   pip install Pillow numpy")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_basic_functionality()
