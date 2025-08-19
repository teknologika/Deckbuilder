"""
Deckbuilder - PowerPoint Presentation Engine

Core presentation generation engine with template support and
structured frontmatter processing.
"""

from .core.engine import Deckbuilder, get_deckbuilder_client

__version__ = "1.4.0"
__all__ = [
    "Deckbuilder",
    "get_deckbuilder_client",
]
