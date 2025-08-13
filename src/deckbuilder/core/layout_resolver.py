"""Layout resolution utilities for name-based lookups."""

from typing import List
from pptx import Presentation


class LayoutResolver:
    """Provides name-based layout resolution functionality."""

    @staticmethod
    def get_layout_by_name(prs: Presentation, layout_name: str):
        """
        Find layout by exact name match.

        Args:
            prs: PowerPoint presentation object
            layout_name: Exact layout name to find

        Returns:
            Layout object if found

        Raises:
            ValueError: If layout not found with helpful suggestions
        """
        # Direct name matching
        for layout in prs.slide_layouts:
            if layout.name == layout_name:
                return layout

        # Generate helpful error with suggestions
        available = [layout.name for layout in prs.slide_layouts]
        similar = [name for name in available if layout_name.lower() in name.lower()]

        error_msg = f"Layout '{layout_name}' not found.\n"
        if similar:
            error_msg += f"Similar layouts: {similar}\n"
        error_msg += f"Available layouts: {available}"

        raise ValueError(error_msg)

    @staticmethod
    def list_available_layouts(prs: Presentation) -> List[str]:
        """
        List all available layout names.

        Args:
            prs: PowerPoint presentation object

        Returns:
            List of layout names
        """
        return [layout.name for layout in prs.slide_layouts]

    @staticmethod
    def validate_layout_exists(prs: Presentation, layout_name: str) -> bool:
        """
        Check if layout exists without raising exception.

        Args:
            prs: PowerPoint presentation object
            layout_name: Layout name to check

        Returns:
            True if layout exists, False otherwise
        """
        try:
            LayoutResolver.get_layout_by_name(prs, layout_name)
            return True
        except ValueError:
            return False
