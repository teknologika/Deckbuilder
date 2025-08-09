from pathlib import Path


class ImagePlaceholderHandler:
    """Handles image insertion into PowerPoint picture placeholders."""

    def __init__(self, image_handler, placekitten):
        """
        Initialize the image placeholder handler.

        Args:
            image_handler: ImageHandler instance for image processing
            placekitten: PlaceKittenIntegration instance for fallback images
        """
        self.image_handler = image_handler
        self.placekitten = placekitten

    def handle_image_placeholder(self, placeholder, field_name, field_value, slide_data):
        """
        Handle image insertion into PICTURE placeholders with smart fallback.

        Args:
            placeholder: PowerPoint picture placeholder
            field_name: Name of the field (e.g., 'image_path', 'media.image_path')
            field_value: Image path or URL
            slide_data: Complete slide data for context
        """
        try:
            # Get placeholder dimensions for proper image sizing
            width = placeholder.width
            height = placeholder.height
            dimensions = (int(width.inches * 96), int(height.inches * 96))  # Convert to pixels

            # Prepare context for consistent PlaceKitten generation
            context = {
                "layout": slide_data.get("layout", slide_data.get("type", "unknown")),
                "slide_index": getattr(self, "_current_slide_index", 0),
            }

            # Try to use provided image path
            final_image_path = None
            if field_value and isinstance(field_value, str):
                # Validate and process the provided image
                if self.image_handler.validate_image(field_value):
                    final_image_path = self.image_handler.process_image(field_value, dimensions, quality="high")
                else:
                    print(f"Warning: Invalid image path '{field_value}', using fallback")

            # Generate PlaceKitten fallback if needed
            if not final_image_path:
                final_image_path = self.placekitten.generate_fallback(dimensions, context)

            # Insert image into placeholder if we have a valid path
            if final_image_path and Path(final_image_path).exists():
                try:
                    # Check if placeholder can accept images (not already filled)
                    if hasattr(placeholder, "insert_picture"):
                        # Insert image into the picture placeholder
                        picture = placeholder.insert_picture(final_image_path)

                        # Preserve alt text if provided
                        alt_text = slide_data.get("alt_text") or slide_data.get("media", {}).get("alt_text")
                        if alt_text and hasattr(picture, "element"):
                            # Set accessibility description
                            picture.element.nvPicPr.cNvPr.descr = str(alt_text)

                        print(f"✅ Successfully inserted image into placeholder: {field_name}")
                    else:
                        msg = f"Warning: Placeholder {field_name} cannot accept images"
                        print(msg)
                        # Try to replace existing content if it's a picture shape
                        if hasattr(placeholder, "element") and hasattr(placeholder.element, "nvPicPr"):
                            print("   Placeholder already contains an image, skipping...")
                        elif hasattr(placeholder, "text_frame") and placeholder.text_frame:
                            placeholder.text_frame.text = f"Image: {Path(final_image_path).name}"

                except Exception as e:
                    print(f"Warning: Failed to insert image into placeholder: {e}")
                    # Fallback: add image path as text if insertion fails
                    if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                        placeholder.text_frame.text = f"Image: {Path(final_image_path).name}"

            else:
                print(f"Warning: No valid image available for placeholder {field_name}")
                # Fallback: show placeholder text
                if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                    placeholder.text_frame.text = "Image placeholder"

        except Exception as e:
            print(f"Error handling image placeholder {field_name}: {e}")
            # Fallback: show error message in placeholder
            if hasattr(placeholder, "text_frame") and placeholder.text_frame:
                placeholder.text_frame.text = f"Image error: {field_name}"
