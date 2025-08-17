from .engine import Deckbuilder
from .presentation_builder import PresentationBuilder
from .slide_builder import SlideBuilder  # Enhanced modular architecture

# New modular architecture modules
from .table_handler import TableHandler
from .content_processor import ContentProcessor
from .slide_coordinator import SlideCoordinator

__all__ = [
    "Deckbuilder",
    "PresentationBuilder",
    "SlideBuilder",  # Enhanced modular architecture
    "TableHandler",
    "ContentProcessor",
    "SlideCoordinator",
]
