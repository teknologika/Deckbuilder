from .engine import Deckbuilder
from .presentation_builder import PresentationBuilder
from .slide_builder import SlideBuilder  # New backward compatibility wrapper
from .slide_builder_legacy import SlideBuilder as SlideBuilderLegacy  # Legacy implementation

# New modular architecture modules
from .table_handler import TableHandler
from .content_processor import ContentProcessor
from .slide_coordinator import SlideCoordinator

__all__ = [
    "Deckbuilder",
    "PresentationBuilder",
    "SlideBuilder",  # Now uses enhanced architecture with backward compatibility
    "SlideBuilderLegacy",  # Available for fallback if needed
    "TableHandler",
    "ContentProcessor",
    "SlideCoordinator",
]
