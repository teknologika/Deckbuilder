#!/usr/bin/env python3
"""
Logging configuration for Deckbuilder to reduce noise.
"""

import os
import sys


# Global debug flag - set to False to reduce logging
DEBUG_MODE = os.getenv("DECKBUILDER_DEBUG", "false").lower() == "true"


def debug_print(*args, **kwargs):
    """Print only if debug mode is enabled."""
    if DEBUG_MODE:
        print(*args, **kwargs)


def quiet_print(*args, **kwargs):
    """Print that can be silenced by setting DECKBUILDER_QUIET=true."""
    if not os.getenv("DECKBUILDER_QUIET", "false").lower() == "true":
        print(*args, **kwargs)


def validation_print(*args, **kwargs):
    """Print validation info only if validation debug is enabled."""
    if os.getenv("DECKBUILDER_VALIDATION_DEBUG", "false").lower() == "true":
        print(*args, **kwargs)


def slide_builder_print(*args, **kwargs):
    """Print slide builder info only if slide builder debug is enabled."""
    if os.getenv("DECKBUILDER_SLIDE_DEBUG", "false").lower() == "true":
        print(*args, **kwargs)


def content_processor_print(*args, **kwargs):
    """Print content processor info only if content processor debug is enabled."""
    if os.getenv("DECKBUILDER_CONTENT_DEBUG", "false").lower() == "true":
        print(*args, **kwargs)


def error_print(*args, **kwargs):
    """Always print errors, regardless of debug settings."""
    print(*args, **kwargs, file=sys.stderr)


def success_print(*args, **kwargs):
    """Always print success messages, regardless of debug settings."""
    print(*args, **kwargs)


def progress_print(*args, **kwargs):
    """Print progress messages for user feedback (can be silenced with DECKBUILDER_QUIET)."""
    if not os.getenv("DECKBUILDER_QUIET", "false").lower() == "true":
        print(*args, **kwargs)
