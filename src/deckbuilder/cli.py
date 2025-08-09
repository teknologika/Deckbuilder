#!/usr/bin/env python3
"""
Backward compatibility wrapper for CLI functionality.

This file maintains compatibility with existing tests and scripts that expect
cli.py in the root directory after the reorganization moved CLI to cli/main.py.
"""

import sys
from pathlib import Path

# Add the parent directory to the Python path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the main CLI functionality
from deckbuilder.cli.main import main  # noqa: E402

if __name__ == "__main__":
    main()
