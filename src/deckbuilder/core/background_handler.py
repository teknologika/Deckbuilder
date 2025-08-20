"""
Background Image Handler

Handles setting slide background images using full-slide picture positioning.
Since python-pptx doesn't have direct background image support, this creates
a picture shape positioned to cover the entire slide and sends it to the back.
"""

from pathlib import Path
from typing import Optional, Dict, Any


class BackgroundImageHandler:
    """Handles background image application for slides."""

    def __init__(self, image_handler, placekitten_integration):
        """
        Initialize with existing image infrastructure.

        Args:
            image_handler: ImageHandler instance for image processing
            placekitten_integration: PlaceKittenIntegration for fallback backgrounds
        """
        self.image_handler = image_handler
        self.placekitten = placekitten_integration

    def apply_background_image(self, slide, image_path: str, slide_data: Dict[str, Any], slide_index: int = 0) -> bool:
        """
        Apply background image to slide using full-slide picture positioning.

        Args:
            slide: PowerPoint slide object
            image_path: Path to background image file
            slide_data: Complete slide data for context
            slide_index: Slide index for PlaceKitten variety

        Returns:
            bool: True if background was successfully applied, False otherwise
        """
        try:
            # Get exact slide dimensions from presentation
            prs = slide.part.package.presentation_part.presentation
            slide_width = prs.slide_width
            slide_height = prs.slide_height

            # Convert to pixels for image processing (approximate conversion)
            width_pixels = int(slide_width.inches * 96)  # 96 DPI
            height_pixels = int(slide_height.inches * 96)
            dimensions = (width_pixels, height_pixels)

            # Prepare context for PlaceKitten fallback
            context = {
                "layout": slide_data.get("layout", slide_data.get("type", "unknown")),
                "slide_index": slide_index,
                "field_name": "background_image",
                "background": True,  # Indicate this is for background
            }

            # Try to use provided image
            final_image_path = None
            if image_path and isinstance(image_path, str):
                if self.image_handler.validate_image(image_path):
                    # Process image to exact slide dimensions
                    final_image_path = self.image_handler.process_image(image_path, dimensions, quality="high")
                else:
                    print(f"Warning: Invalid background image '{image_path}', using fallback")

            # Generate PlaceKitten fallback if needed
            if not final_image_path:
                final_image_path = self.placekitten.generate_fallback(dimensions, context)

            # Apply background image if we have a valid path
            if final_image_path and Path(final_image_path).exists():
                return self._create_background_picture(slide, final_image_path, slide_width, slide_height)
            else:
                print("Warning: No valid background image available for slide")
                return False

        except Exception as e:
            print(f"Error applying background image: {e}")
            return False

    def _create_background_picture(self, slide, image_path: str, slide_width, slide_height) -> bool:
        """
        Create picture shape positioned as background.

        Args:
            slide: PowerPoint slide object
            image_path: Path to processed image file
            slide_width: Exact slide width from presentation
            slide_height: Exact slide height from presentation

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Position at origin (0,0) covering entire slide
            left = top = 0

            # Create picture shape with exact slide dimensions
            pic = slide.shapes.add_picture(image_path, left, top, width=slide_width, height=slide_height)

            # Send picture to back (behind all content)
            self._send_picture_to_back(pic)

            print("✅ Successfully applied background image to slide")
            return True

        except Exception as e:
            print(f"Error creating background picture: {e}")
            return False

    def _send_picture_to_back(self, picture):
        """
        Send picture shape to back so it appears behind all other content.

        Args:
            picture: Picture shape to send to back
        """
        try:
            # Get the slide's shape tree
            shape_tree = picture.element.getparent()

            # Remove picture from current position
            shape_tree.remove(picture.element)

            # Insert at position 2 (after slide background elements but before content)
            # Position 0 and 1 are typically reserved for slide background elements
            shape_tree.insert(2, picture.element)

        except Exception as e:
            print(f"Warning: Could not send background image to back: {e}")
            # Continue anyway - picture will still be created, just not in back

    def should_apply_background(self, slide_data: Dict[str, Any]) -> bool:
        """
        Check if background image should be applied based on slide data.

        Args:
            slide_data: Slide data dictionary

        Returns:
            bool: True if background_image field exists and is valid
        """
        background_image = slide_data.get("background_image")
        return background_image is not None and isinstance(background_image, str) and background_image.strip()

    def get_background_image_path(self, slide_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract background image path from slide data.

        Args:
            slide_data: Slide data dictionary

        Returns:
            str: Background image path, or None if not found
        """
        background_image = slide_data.get("background_image")
        if background_image and isinstance(background_image, str):
            return background_image.strip()
        return None
