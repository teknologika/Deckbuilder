"""
Content Processing Package

Unified content processing for PowerPoint presentation generation.
Handles content transformation from markdown to canonical JSON to PowerPoint.

Modules:
- processor: Markdown → Canonical JSON conversion
- formatter: Canonical JSON → PowerPoint content formatting
- frontmatter: Structured frontmatter handling
"""

from .processor import ContentProcessor
from .formatter import ContentFormatter
from .frontmatter import FrontmatterConverter

__all__ = [
    "ContentProcessor",
    "ContentFormatter",
    "FrontmatterConverter",
]
