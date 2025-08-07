"""
Deckbuilder - PowerPoint Presentation Engine

Core presentation generation engine with template support and
structured frontmatter processing.
"""

from .engine import Deckbuilder, get_deckbuilder_client
from .structured_frontmatter import (
    StructuredFrontmatterConverter,
    StructuredFrontmatterRegistry,
    StructuredFrontmatterValidator,
)

__version__ = "1.2.8"
__all__ = [
    "Deckbuilder",
    "get_deckbuilder_client",
    "StructuredFrontmatterRegistry",
    "StructuredFrontmatterConverter",
    "StructuredFrontmatterValidator",
]
