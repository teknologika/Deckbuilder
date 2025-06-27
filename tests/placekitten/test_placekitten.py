#!/usr/bin/env python3
"""
Test script for PlaceKitten library - Phase 2 functionality testing.
Tests computer vision pipeline, smart cropping, and step visualization.
"""

import os
import sys
from pathlib import Path

# Add the src directory to Python path
project_root = Path(__file__).parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from placekitten import PlaceKitten

    print("✅ PlaceKitten import successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)


def test_basic_functionality():
    """Test basic PlaceKitten functionality."""
    print("\n🧪 Testing basic functionality...")

    try:
        # Initialize PlaceKitten
        kitten = PlaceKitten("demo")
        print("✅ PlaceKitten initialization successful")

        # Show available images
        images = kitten.list_available_images()
        print(f"✅ Found {len(images)} available images:")
        for i, img in enumerate(images[:3], 1):  # Show first 3 with 1-based indexing
            print(f"   {i}: {img}")

        return kitten
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return None


def test_smart_cropping():
    """Test smart cropping functionality with step visualization."""
    from placekitten import PlaceKitten

    kitten = PlaceKitten("demo")

    # Create test output directory
    test_output_dir = Path(__file__).parent / "test_output"
    test_output_dir.mkdir(exist_ok=True)

    # Generate image with smart cropping and step visualization
    processor = kitten.generate(
        width=800, height=450, image_id=1  # 16:9 aspect ratio, 1-based indexing
    )

    # Test smart cropping with step visualization
    smart_processor = processor.smart_crop(
        width=800,
        height=450,
        save_steps=True,
        output_prefix="test_demo",
        output_folder=str(test_output_dir),
    )

    # Save the final result
    output_file = smart_processor.save(str(test_output_dir / "test_final_result.jpg"))
    assert output_file.endswith("test_final_result.jpg")

    # Check if debug steps were saved
    step_files = [f for f in test_output_dir.iterdir() if f.name.startswith("test_demo_")]
    assert len(step_files) == 9  # Should have 9 processing steps


def test_filter_pipeline():
    """Test filter pipeline functionality."""
    from placekitten import PlaceKitten

    kitten = PlaceKitten("demo")

    # Create test output directory
    test_output_dir = Path(__file__).parent / "test_output"
    test_output_dir.mkdir(exist_ok=True)

    # Test different filters
    filters_to_test = ["grayscale", "sepia", "blur"]

    for filter_name in filters_to_test:
        processor = kitten.generate(
            width=400, height=225, filter_type=filter_name, image_id=1  # 1-based indexing
        )
        output_file = processor.save(str(test_output_dir / f"test_filter_{filter_name}.jpg"))
        assert output_file.endswith(f"test_filter_{filter_name}.jpg")


def main():
    """Run comprehensive PlaceKitten tests."""
    print("🐱 PlaceKitten Phase 2 Testing Suite")
    print("=" * 50)

    # Clean up any existing test files in root directory
    root_test_files = [f for f in os.listdir(".") if f.startswith("test_")]
    if root_test_files:
        print(f"🧹 Cleaning up {len(root_test_files)} old test files from root directory...")
        for f in root_test_files:
            try:
                os.remove(f)
                print(f"   🗑️  Removed {f}")
            except Exception as e:
                print(f"   ❌ Could not remove {f}: {e}")

    # Test 1: Basic functionality
    kitten = test_basic_functionality()
    if not kitten:
        return

    # Test 2: Smart cropping with computer vision
    test_smart_cropping()

    # Test 3: Filter pipeline
    test_filter_pipeline()

    print("\n🎉 All tests completed successfully!")
    print("Phase 2 implementation is working correctly.")

    # Show generated files in proper test output directory
    test_output_dir = Path(__file__).parent / "test_output"
    if test_output_dir.exists():
        generated_files = list(test_output_dir.iterdir())
        print(f"\n📁 Generated {len(generated_files)} test files in {test_output_dir}:")
        for f in sorted(generated_files):
            print(f"   📄 {f.name}")


if __name__ == "__main__":
    main()
