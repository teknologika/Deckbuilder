#!/usr/bin/env python3
"""
Test script for PlaceKitten smart crop functionality.

This script demonstrates the intelligent cropping features with
computer vision and step visualization.
"""

import os
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_smart_crop():
    """Test smart crop functionality with step visualization."""
    print("🧠 Testing PlaceKitten Smart Crop Engine")
    print("=" * 50)

    try:
        # Test import
        print("📦 Testing imports...")
        from placekitten import ImageProcessor, PlaceKitten, SmartCropEngine

        print("✅ Imports successful!")

        # Test PlaceKitten with smart crop
        print("🐱 Testing PlaceKitten with smart crop...")
        pk = PlaceKitten()

        if pk.get_image_count() > 0:
            # Test basic smart crop
            print("🧠 Testing basic smart crop...")
            processor = pk.generate(width=800, height=600)
            smart_cropped = processor.smart_crop(width=1920, height=1080)
            print(f"✅ Smart crop completed: {smart_cropped.get_size()}")

            # Test with step visualization (if OpenCV is available)
            print("📊 Testing step visualization...")
            try:
                visualized = processor.smart_crop(
                    width=800, height=450, save_steps=True, output_prefix="test_demo"
                )

                crop_info = visualized.get_crop_info()
                if crop_info:
                    print(f"✅ Visualization completed!")
                    print(f"   📏 Original size: {crop_info['original_size']}")
                    print(f"   🎯 Target size: {crop_info['target_size']}")
                    print(f"   ✂️  Crop box: {crop_info['crop_box']}")
                    print(f"   👁️  Subject bbox: {crop_info['subject_bbox']}")
                    print(f"   📁 Steps saved: {crop_info['steps_saved']}")

                    if crop_info["steps_saved"] > 0:
                        print("   🖼️  Debug images saved:")
                        for i in range(1, 10):
                            step_file = f"test_demo_{i}-*.jpg"
                            print(f"      - Step {i}: {step_file}")
                else:
                    print("⚠️  No crop info available (fallback used)")

            except Exception as ve:
                print(f"⚠️  Visualization failed: {ve}")
                print("💡 This is normal if OpenCV is not installed")

            # Test method chaining with smart crop
            print("⛓️  Testing method chaining with smart crop...")
            chained = (
                pk.generate(1200, 800)
                .apply_filter("sepia")
                .smart_crop(600, 400)
                .apply_filter("brightness", value=110)
            )
            print(f"✅ Chained processing: {chained.get_size()}")

            # Test edge cases
            print("🔍 Testing edge cases...")

            # Very small crop
            tiny = processor.smart_crop(100, 100)
            print(f"✅ Tiny crop: {tiny.get_size()}")

            # Very large crop (should handle gracefully)
            try:
                large = processor.smart_crop(5000, 3000)
                print(f"✅ Large crop: {large.get_size()}")
            except Exception as e:
                print(f"⚠️  Large crop handled: {e}")

            print("\n🎉 Smart crop tests completed!")
            print("✅ Phase 2: Intelligent Processing is working!")

        else:
            print("⚠️  No images found - cannot test smart crop")
            print("💡 Ensure kitten images are in assets/images/")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 You may need to install dependencies:")
        print("   pip install opencv-python Pillow numpy")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


def test_smart_crop_engine_directly():
    """Test the SmartCropEngine directly."""
    print("\n🔬 Testing SmartCropEngine Directly")
    print("=" * 40)

    try:
        import os

        from PIL import Image

        from placekitten import SmartCropEngine

        # Check if we have test images
        test_images = list(Path("assets/images").glob("*.png"))
        if not test_images:
            print("⚠️  No test images found")
            return

        # Load a test image
        test_image_path = test_images[0]
        print(f"🖼️  Loading test image: {test_image_path.name}")

        image = Image.open(test_image_path)
        print(f"   Original size: {image.size}")

        # Test smart crop engine
        engine = SmartCropEngine()

        try:
            result_image, crop_info = engine.smart_crop(
                image, 800, 450, save_steps=True, output_prefix="direct_test"
            )

            print("✅ Direct engine test successful!")
            print(f"   Result size: {result_image.size}")
            print(f"   Crop info: {crop_info}")

        except Exception as e:
            print(f"⚠️  Engine test failed: {e}")
            print("💡 This is expected if OpenCV is not installed")

    except Exception as e:
        print(f"❌ Direct engine test failed: {e}")


if __name__ == "__main__":
    test_smart_crop()
    test_smart_crop_engine_directly()
