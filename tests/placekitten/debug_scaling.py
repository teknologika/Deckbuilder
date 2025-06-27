#!/usr/bin/env python3
"""Debug script to test PlaceKitten scaling behavior."""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from placekitten import PlaceKitten


def test_scaling():
    kitten = PlaceKitten("demo")

    print("🔍 Testing PlaceKitten scaling behavior...")
    print()

    # Test 1: Full size image
    print("1. Full size image (no dimensions):")
    full_size = kitten.generate(image_id=1)
    print(f"   Size: {full_size.get_size()}")
    print()

    # Test 2: Width only
    print("2. Width only (600px):")
    width_only = kitten.generate(width=600, image_id=1)
    w, h = width_only.get_size()
    print(f"   Size: {w}x{h}")

    # Calculate expected height
    orig_w, orig_h = full_size.get_size()
    expected_h = int(600 * orig_h / orig_w)
    print(f"   Expected: 600x{expected_h}")
    print(f"   Match: {'✅' if h == expected_h else '❌'}")
    print()

    # Test 3: Height only
    print("3. Height only (400px):")
    height_only = kitten.generate(height=400, image_id=1)
    w, h = height_only.get_size()
    print(f"   Size: {w}x{h}")

    # Calculate expected width
    expected_w = int(400 * orig_w / orig_h)
    print(f"   Expected: {expected_w}x400")
    print(f"   Match: {'✅' if w == expected_w else '❌'}")
    print()

    # Test 4: Both dimensions
    print("4. Both dimensions (800x600):")
    both_dims = kitten.generate(width=800, height=600, image_id=1)
    w, h = both_dims.get_size()
    print(f"   Size: {w}x{h}")
    print(f"   Expected: 800x600")
    print(f"   Match: {'✅' if (w == 800 and h == 600) else '❌'}")
    print()

    # Test aspect ratios
    orig_ratio = orig_w / orig_h
    width_ratio = width_only.get_size()[0] / width_only.get_size()[1]
    height_ratio = height_only.get_size()[0] / height_only.get_size()[1]

    print("📐 Aspect ratio analysis:")
    print(f"   Original ratio: {orig_ratio:.6f}")
    print(f"   Width-only ratio: {width_ratio:.6f} (diff: {abs(orig_ratio - width_ratio):.6f})")
    print(f"   Height-only ratio: {height_ratio:.6f} (diff: {abs(orig_ratio - height_ratio):.6f})")

    if abs(orig_ratio - width_ratio) < 0.001 and abs(orig_ratio - height_ratio) < 0.001:
        print("   ✅ Aspect ratios preserved!")
    else:
        print("   ❌ Aspect ratios NOT preserved!")


if __name__ == "__main__":
    test_scaling()
