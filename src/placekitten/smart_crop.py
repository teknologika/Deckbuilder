"""
Smart Crop - Intelligent cropping engine with computer vision.

This module implements the intelligent cropping pipeline using OpenCV
for edge detection, contour analysis, and rule-of-thirds composition.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image


class SmartCropEngine:
    """
    Intelligent cropping engine using computer vision techniques.

    Implements a multi-step pipeline:
    1. Original analysis and preprocessing
    2. Edge detection with Canny algorithm
    3. Contour identification and analysis
    4. Rule-of-thirds composition calculation
    5. Optimal crop area determination
    """

    def __init__(self):
        """Initialize the smart crop engine."""
        self.debug_steps = []
        self.crop_info = {}

    def smart_crop(
        self,
        image: Image.Image,
        target_width: int,
        target_height: int,
        save_steps: bool = False,
        output_prefix: str = "smart_crop",
        output_folder: Optional[str] = None,
        strategy: str = "haar-face",
    ) -> Tuple[Image.Image, Dict]:
        """
        Perform intelligent cropping with computer vision.

        Args:
            image: PIL Image to crop
            target_width: Target width in pixels
            target_height: Target height in pixels
            save_steps: Save intermediate processing steps
            output_prefix: Prefix for step visualization files
            output_folder: Directory to save step files (optional)

        Returns:
            Tuple of (cropped_image, crop_info)
        """
        # Clear previous debug info
        self.debug_steps = []
        self.crop_info = {}

        # Convert PIL to OpenCV format
        cv_image = self._pil_to_cv2(image)
        original_height, original_width = cv_image.shape[:2]

        # Step 1: Original analysis
        step1_image = cv_image.copy()
        self._add_debug_step("1-original", step1_image, save_steps, output_prefix, output_folder)

        # Step 2: Grayscale conversion
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        step2_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self._add_debug_step("2-grayscale", step2_image, save_steps, output_prefix, output_folder)

        # Step 3: Noise reduction with Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        step3_image = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)
        self._add_debug_step("3-blurred", step3_image, save_steps, output_prefix, output_folder)

        # Step 4: Edge detection with Canny
        edges = cv2.Canny(blurred, 50, 150)
        # Highlight edges in red for visualization
        step4_vis = cv_image.copy()
        step4_vis[edges > 0] = [0, 0, 255]  # Red edges
        self._add_debug_step("4-edges", step4_vis, save_steps, output_prefix, output_folder)

        # Strategy-based subject detection
        subject_bbox = None
        largest_area = 0

        if strategy == "haar-face":
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                subject_bbox = max(faces, key=lambda r: r[2] * r[3])  # Select largest face
                x, y, w, h = subject_bbox
                step5_image = cv_image.copy()
                cv2.rectangle(step5_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                largest_area = w * h
            else:
                step5_image = cv_image.copy()

            # Fallback to contour-based detection if face detection fails
            if subject_bbox is None:
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                largest_contour = None
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > largest_area:
                        largest_area = area
                        largest_contour = contour

                if largest_contour is not None:
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    subject_bbox = (x, y, w, h)
                    cv2.drawContours(step5_image, [largest_contour], -1, (0, 255, 0), 3)

        else:
            # Default to contour-based detection
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            largest_contour = None
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > largest_area:
                    largest_area = area
                    largest_contour = contour

            step5_image = cv_image.copy()
            if largest_contour is not None:
                cv2.drawContours(step5_image, [largest_contour], -1, (0, 255, 0), 3)
                x, y, w, h = cv2.boundingRect(largest_contour)
                subject_bbox = (x, y, w, h)
        self._add_debug_step("5-largest-contour", step5_image, save_steps, output_prefix, output_folder)

        # Step 6: Calculate bounding box of subject (visualization only)
        if subject_bbox is not None:
            x, y, w, h = subject_bbox
            step6_image = cv_image.copy()
            cv2.rectangle(step6_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Fill bounding box with semi-transparent blue
            overlay = step6_image.copy()
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 0, 0), -1)
            step6_image = cv2.addWeighted(step6_image, 0.8, overlay, 0.2, 0)
        else:
            step6_image = cv_image.copy()
        self._add_debug_step("6-bounding-box", step6_image, save_steps, output_prefix, output_folder)

        # Step 7: Rule of thirds grid and composition
        crop_box = self._calculate_optimal_crop(original_width, original_height, target_width, target_height, subject_bbox)

        # Visualize rule of thirds and crop area
        step7_image = cv_image.copy()
        self._draw_rule_of_thirds(step7_image, original_width, original_height)
        self._add_debug_step("7-rule-of-thirds", step7_image, save_steps, output_prefix, output_folder)

        # Step 8: Final crop area visualization
        step8_image = cv_image.copy()
        x1, y1, x2, y2 = crop_box
        cv2.rectangle(step8_image, (x1, y1), (x2, y2), (255, 0, 255), 3)  # Magenta border
        self._add_debug_step("8-crop-area", step8_image, save_steps, output_prefix, output_folder)

        # Step 9: Perform the actual crop
        cropped_cv = cv_image[y1:y2, x1:x2]
        cropped_resized = cv2.resize(cropped_cv, (target_width, target_height), interpolation=cv2.INTER_LANCZOS4)

        # Convert back to PIL
        final_image = self._cv2_to_pil(cropped_resized)

        # Save final result
        self._add_debug_step("9-final", cropped_resized, save_steps, output_prefix, output_folder)

        # Store crop information
        self.crop_info = {
            "original_size": (original_width, original_height),
            "target_size": (target_width, target_height),
            "crop_box": crop_box,
            "subject_bbox": subject_bbox,
            "contour_area": largest_area,
            "steps_saved": len(self.debug_steps) if save_steps else 0,
        }

        return final_image, self.crop_info

    def _calculate_optimal_crop(
        self,
        orig_width: int,
        orig_height: int,
        target_width: int,
        target_height: int,
        subject_bbox: Optional[Tuple[int, int, int, int]],
    ) -> Tuple[int, int, int, int]:
        """
        Calculate optimal crop box using rule of thirds and subject positioning.

        Args:
            orig_width: Original image width
            orig_height: Original image height
            target_width: Target crop width
            target_height: Target crop height
            subject_bbox: Bounding box of main subject (x, y, w, h)

        Returns:
            Crop box as (x1, y1, x2, y2)
        """
        target_ratio = target_width / target_height

        # Calculate crop dimensions maintaining target aspect ratio
        if orig_width / orig_height > target_ratio:
            # Original is wider - crop width
            crop_height = orig_height
            crop_width = int(crop_height * target_ratio)
        else:
            # Original is taller - crop height
            crop_width = orig_width
            crop_height = int(crop_width / target_ratio)

        # Default to center crop
        crop_x = (orig_width - crop_width) // 2
        crop_y = (orig_height - crop_height) // 2

        # Adjust based on subject position if available
        if subject_bbox is not None:
            subj_x, subj_y, subj_w, subj_h = subject_bbox
            subj_center_x = subj_x + subj_w // 2
            subj_center_y = subj_y + subj_h // 2

            # Try to position subject in lower third (rule of thirds)
            ideal_subj_x = crop_width // 2
            ideal_subj_y = int(crop_height * 2 / 3)  # Lower third

            # Calculate desired crop position
            desired_crop_x = subj_center_x - ideal_subj_x
            desired_crop_y = subj_center_y - ideal_subj_y

            # Ensure crop stays within image bounds
            crop_x = max(0, min(desired_crop_x, orig_width - crop_width))
            crop_y = max(0, min(desired_crop_y, orig_height - crop_height))

        return (crop_x, crop_y, crop_x + crop_width, crop_y + crop_height)

    def _draw_rule_of_thirds(self, image: np.ndarray, width: int, height: int) -> None:
        """Draw rule of thirds grid on image."""
        # Vertical lines
        cv2.line(image, (width // 3, 0), (width // 3, height), (255, 255, 0), 2)
        cv2.line(image, (2 * width // 3, 0), (2 * width // 3, height), (255, 255, 0), 2)

        # Horizontal lines
        cv2.line(image, (0, height // 3), (width, height // 3), (255, 255, 0), 2)
        cv2.line(image, (0, 2 * height // 3), (width, 2 * height // 3), (255, 255, 0), 2)

    def _pil_to_cv2(self, pil_image: Image.Image) -> np.ndarray:
        """Convert PIL Image to OpenCV format."""
        # Convert PIL to RGB if not already
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        # Convert to numpy array and change from RGB to BGR
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        return cv_image

    def _cv2_to_pil(self, cv_image: np.ndarray) -> Image.Image:
        """Convert OpenCV image to PIL format."""
        # Convert from BGR to RGB
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image)

    def _add_debug_step(
        self,
        step_name: str,
        image: np.ndarray,
        save_steps: bool,
        output_prefix: str,
        output_folder: Optional[str] = None,
    ) -> None:
        """Add debug step and optionally save to file."""
        if save_steps:
            step_info = {"name": step_name, "image": image.copy()}
            self.debug_steps.append(step_info)

            # Save step image with proper folder handling
            filename = f"{output_prefix}_{step_name}.jpg"
            if output_folder:
                # Ensure output folder exists
                Path(output_folder).mkdir(parents=True, exist_ok=True)
                filepath = Path(output_folder) / filename
            else:
                filepath = Path(filename)

            cv2.imwrite(str(filepath), image)

    def get_debug_steps(self) -> List[Dict]:
        """Get list of debug steps with images."""
        return self.debug_steps

    def get_crop_info(self) -> Dict:
        """Get detailed information about the last crop operation."""
        return self.crop_info


# Global instance for easy access
smart_crop_engine = SmartCropEngine()
