from .engine import Deckbuilder
from .presentation_builder import PresentationBuilder
from .slide_builder_legacy import SlideBuilder  # Legacy import until refactor complete

# New modular architecture modules
from .table_handler import TableHandler
from .content_processor import ContentProcessor

# from .slide_coordinator import SlideCoordinator      # TODO: Create next

__all__ = [
    "Deckbuilder",
    "PresentationBuilder",
    "SlideBuilder",  # Will delegate to new architecture when complete
    "TableHandler",
    "ContentProcessor",
    # "SlideCoordinator",
]
