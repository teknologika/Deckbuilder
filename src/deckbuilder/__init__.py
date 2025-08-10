"""
Deckbuilder - PowerPoint Presentation Engine

Core presentation generation engine with template support and
structured frontmatter processing.
"""

from .core.engine import Deckbuilder, get_deckbuilder_client
from .content.frontmatter import (
    StructuredFrontmatterConverter,
    StructuredFrontmatterValidator,
)

__version__ = "1.2.8"
__all__ = [
    "Deckbuilder",
    "get_deckbuilder_client",
    "StructuredFrontmatterConverter",
    "StructuredFrontmatterValidator",
]
