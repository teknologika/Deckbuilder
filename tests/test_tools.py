#!/usr/bin/env python3
"""
Test script for tools.py template analyzer.
"""

import os
import sys
import shutil
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools import analyze_pptx_template


def setup_test_environment():
    """Set up test environment with folders and template."""
    test_dir = os.path.dirname(__file__)
    src_dir = os.path.join(test_dir, '..', 'src')
    
    # Create test folders
    templates_folder = os.path.join(test_dir, 'templates')
    output_folder = os.path.join(test_dir, 'output')
    
    os.makedirs(templates_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    # Always copy default.pptx from src folder to output folder
    source_template = os.path.join(src_dir, 'default.pptx')
    target_template = os.path.join(output_folder, 'default.pptx')
    
    if os.path.exists(source_template):
        shutil.copy2(source_template, target_template)
        print(f"Copied template from src to: {target_template}")
    else:
        raise FileNotFoundError(f"Source template not found: {source_template}")
    
    # Set environment variables
    os.environ['DECK_TEMPLATE_FOLDER'] = output_folder
    os.environ['DECK_OUTPUT_FOLDER'] = output_folder
    
    print(f"Template folder: {templates_folder}")
    print(f"Output folder: {output_folder}")
    
    return templates_folder, output_folder


def test_analyze_template():
    """Test the template analyzer."""
    try:
        templates_folder, output_folder = setup_test_environment()
        
        # Test analyzing the default template
        print("\nAnalyzing default.pptx template...")
        result = analyze_pptx_template("default")
        
        print("\nRaw Template Structure:")
        print(json.dumps(result, indent=2))
        
        # Check if output file was created
        output_file = os.path.join(output_folder, "default.g.json")
        if os.path.exists(output_file):
            print(f"\n✓ Generated mapping file: {output_file}")
            print("  Rename to 'default.json' when ready to use with deckbuilder")
        else:
            print("✗ Output file was not created")
        
        return result
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return None


if __name__ == "__main__":
    test_analyze_template()