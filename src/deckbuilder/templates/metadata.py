#!/usr/bin/env python3
"""
Template Metadata Loader

Loads and processes enhanced template metadata for intelligent template discovery and recommendations.
Bridges existing template JSON structure with semantic metadata for content-first workflows.

This module implements the foundation for TDD Template Discovery (GitHub Issue #38).
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from deckbuilder.utils.path import path_manager
from .pattern_loader import PatternLoader


@dataclass
class LayoutMetadata:
    """Metadata for a single layout within a template."""

    display_name: str
    description: str
    placeholders: List[str]
    required_placeholders: List[str]
    optional_placeholders: List[str] = field(default_factory=list)
    best_for: str = ""
    content_type: str = "general"
    complexity: str = "simple"
    supports_images: bool = False
    supports_tables: bool = False


@dataclass
class TemplateMetadata:
    """Complete metadata for a template including all layouts."""

    template_name: str
    description: str
    use_cases: List[str]
    style: str = "professional"
    target_audience: List[str] = field(default_factory=lambda: ["general"])
    layouts: Dict[str, LayoutMetadata] = field(default_factory=dict)
    total_layouts: int = 0
    complexity_breakdown: Dict[str, int] = field(default_factory=dict)


class TemplateMetadataLoader:
    """
    Enhanced template metadata loader with semantic intelligence.

    Loads existing template JSON files and enhances them with semantic metadata
    for intelligent template discovery and content-first recommendations.
    """

    def __init__(self, template_folder: Optional[Path] = None):
        """Initialize with template folder path."""
        self.template_folder = template_folder or self._get_default_template_folder()
        self.logger = logging.getLogger(__name__)
        self._metadata_cache: Dict[str, TemplateMetadata] = {}

        # Initialize PatternLoader for structured frontmatter patterns
        self.pattern_loader = PatternLoader(self.template_folder)

    def _get_default_template_folder(self) -> Path:
        """Get default template folder from package assets."""
        return path_manager.get_assets_templates_path()

    def load_template_metadata(self, template_name: str) -> TemplateMetadata:
        """
        Load enhanced metadata for a specific template.

        Args:
            template_name: Name of template (e.g., 'default', 'business_pro')

        Returns:
            TemplateMetadata object with comprehensive template information

        Raises:
            FileNotFoundError: If template JSON file doesn't exist
            ValueError: If template JSON is invalid or corrupted
        """
        if template_name in self._metadata_cache:
            return self._metadata_cache[template_name]

        # Check if PowerPoint template exists
        pptx_file = self.template_folder / f"{template_name}.pptx"
        if not pptx_file.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found at {pptx_file}")

        # Create metadata from patterns (new primary approach)
        try:
            metadata = self.create_template_metadata_from_patterns(template_name)
            self.logger.info(f"Created template metadata for '{template_name}' from patterns")
        except (ValueError, FileNotFoundError) as e:
            # JSON mapping files were removed - no fallback needed
            raise ValueError(f"Failed to create metadata for template '{template_name}': {e}. Template patterns required.")

        # Cache for performance
        self._metadata_cache[template_name] = metadata

        return metadata

    def _parse_template_data(self, template_name: str, template_data: Dict[str, Any]) -> TemplateMetadata:
        """Parse template JSON data into enhanced metadata structure."""

        # Extract basic template info (for potential future use)
        _ = template_data.get("template_info", {})

        # Check if this is an enhanced format with layout_metadata section
        if "layout_metadata" in template_data:
            return self._parse_enhanced_format(template_name, template_data)
        else:
            # Handle legacy format (current template JSON structure)
            return self._parse_legacy_format(template_name, template_data)

    def _parse_enhanced_format(self, template_name: str, template_data: Dict[str, Any]) -> TemplateMetadata:
        """Parse enhanced template format with layout_metadata section."""

        # Extract basic template info
        template_info = template_data.get("template_info", {})
        description = template_info.get("description", f"Template: {template_name}")
        use_cases = template_info.get("use_cases", ["General presentations"])
        target_audience = template_info.get("target_audience", ["general"])

        # Parse layout metadata directly from enhanced format
        layout_metadata_data = template_data.get("layout_metadata", {})
        layout_metadata = {}
        complexity_breakdown = {"simple": 0, "medium": 0, "complex": 0}

        for layout_id, layout_info in layout_metadata_data.items():
            # Create LayoutMetadata from enhanced format
            layout_meta = LayoutMetadata(
                display_name=layout_info.get("display_name", layout_id),
                description=layout_info.get("description", ""),
                placeholders=layout_info.get("placeholders", []),
                required_placeholders=layout_info.get("required_placeholders", []),
                optional_placeholders=layout_info.get("optional_placeholders", []),
                best_for=layout_info.get("best_for", ""),
                content_type=layout_info.get("content_type", "general"),
                complexity=layout_info.get("complexity", "simple"),
                supports_images=layout_info.get("supports_images", False),
                supports_tables=layout_info.get("supports_tables", False),
            )

            layout_metadata[layout_id] = layout_meta
            complexity_breakdown[layout_meta.complexity] += 1

        return TemplateMetadata(
            template_name=template_name,
            description=description,
            use_cases=use_cases,
            target_audience=target_audience,
            layouts=layout_metadata,
            total_layouts=len(layout_metadata),
            complexity_breakdown=complexity_breakdown,
        )

    def _parse_legacy_format(self, template_name: str, template_data: Dict[str, Any]) -> TemplateMetadata:
        """Parse legacy template format (current production format)."""

        # Extract basic template info
        template_info = template_data.get("template_info", {})
        _ = template_info.get("name", template_name)  # For potential future use

        # Generate semantic metadata based on template structure analysis
        layouts_data = template_data.get("layouts", {})
        layout_metadata = {}
        complexity_breakdown = {"simple": 0, "medium": 0, "complex": 0}

        for layout_name, layout_info in layouts_data.items():
            placeholders = self._extract_placeholder_names(layout_info.get("placeholders", {}))

            # Generate layout metadata with semantic analysis
            layout_meta = self._generate_layout_metadata(layout_name, placeholders)
            layout_metadata[layout_name] = layout_meta

            # Update complexity breakdown
            complexity_breakdown[layout_meta.complexity] += 1

        # Generate template-level metadata
        description = self._generate_template_description(template_name, layout_metadata)
        use_cases = self._generate_use_cases(layout_metadata)
        target_audience = self._determine_target_audience(template_name, layout_metadata)

        return TemplateMetadata(
            template_name=template_name,
            description=description,
            use_cases=use_cases,
            target_audience=target_audience,
            layouts=layout_metadata,
            total_layouts=len(layout_metadata),
            complexity_breakdown=complexity_breakdown,
        )

    def _extract_placeholder_names(self, placeholders: Dict[str, str]) -> List[str]:
        """Extract placeholder names from layout structure, excluding footers."""
        # Filter out common footer placeholders to focus on content placeholders
        footer_placeholders = {"date_footer", "footer_footer", "slide_number_footer"}
        technical_names = [name for name in placeholders.values() if name not in footer_placeholders]

        # Convert technical names to semantic names for user-friendly interface
        return [self._technical_to_semantic(name) for name in technical_names]

    def _technical_to_semantic(self, technical_name: str) -> str:
        """Convert technical placeholder names to user-friendly semantic names dynamically."""

        name_lower = technical_name.lower()

        # Handle title variations dynamically
        if "title" in name_lower:
            if "subtitle" in name_lower:
                return "subtitle"
            elif any(indicator in name_lower for indicator in ["col", "1", "2", "3", "4", "5", "6"]):
                # Extract column number or identifier
                for i in range(1, 7):
                    if str(i) in technical_name or f"col{i}" in name_lower:
                        return f"title_col{i}"
                return "title_col1"  # fallback
            else:
                return "title"

        # Handle content variations dynamically
        elif "content" in name_lower:
            # Check for positional indicators
            if any(indicator in name_lower for indicator in ["left", "right"]):
                if "left" in name_lower:
                    return "content_left"
                elif "right" in name_lower:
                    return "content_right"
            elif any(indicator in name_lower for indicator in ["top", "bottom"]):
                if "top" in name_lower and "left" in name_lower:
                    return "content_top_left"
                elif "top" in name_lower and "right" in name_lower:
                    return "content_top_right"
                elif "bottom" in name_lower and "left" in name_lower:
                    return "content_bottom_left"
                elif "bottom" in name_lower and "right" in name_lower:
                    return "content_bottom_right"
            elif any(str(i) in technical_name for i in range(1, 7)):
                # Extract column number
                for i in range(1, 7):
                    if str(i) in technical_name:
                        return f"content_col{i}"
                return "content_col1"  # fallback
            else:
                return "content"

        # Handle image placeholders
        elif "image" in name_lower or "picture" in name_lower:
            if any(str(i) in technical_name for i in range(1, 10)):
                for i in range(1, 10):
                    if str(i) in technical_name:
                        return f"image_{i}"
            return "image"

        # Handle text variations
        elif "text" in name_lower:
            if "caption" in name_lower:
                return "caption"
            else:
                return "content"

        # Handle other common patterns
        elif "subtitle" in name_lower:
            return "subtitle"
        elif "summary" in name_lower:
            return "summary"
        elif "bullet" in name_lower:
            return "bullets"

        # For unrecognized patterns, clean up the name
        semantic_name = technical_name.lower()

        # Remove common prefixes and suffixes
        for prefix in ["slide_", "layout_"]:
            if semantic_name.startswith(prefix):
                semantic_name = semantic_name[len(prefix) :]
                break

        for suffix in ["_top", "_footer", "_placeholder", "_box"]:
            if semantic_name.endswith(suffix):
                semantic_name = semantic_name[: -len(suffix)]
                break

        return semantic_name or technical_name.lower()  # fallback to original if empty

    def _generate_layout_metadata(self, layout_name: str, placeholders: List[str]) -> LayoutMetadata:
        """Generate semantic metadata for a layout based on its structure."""

        # Analyze layout structure for semantic properties
        complexity = self._determine_layout_complexity(placeholders)
        content_type = self._determine_content_type(layout_name, placeholders)
        supports_images = any("image" in p.lower() for p in placeholders)
        supports_tables = layout_name in ["Title and Content", "Section Header"]

        # Generate description and best-for based on layout characteristics
        description = self._generate_layout_description(layout_name, placeholders)
        best_for = self._generate_best_for(layout_name, placeholders)

        # Determine required vs optional placeholders
        required_placeholders = self._determine_required_placeholders(layout_name, placeholders)
        optional_placeholders = [p for p in placeholders if p not in required_placeholders]

        return LayoutMetadata(
            display_name=layout_name,
            description=description,
            placeholders=placeholders,
            required_placeholders=required_placeholders,
            optional_placeholders=optional_placeholders,
            best_for=best_for,
            content_type=content_type,
            complexity=complexity,
            supports_images=supports_images,
            supports_tables=supports_tables,
        )

    def _determine_layout_complexity(self, placeholders: List[str]) -> str:
        """Determine layout complexity based on number of placeholders."""
        placeholder_count = len(placeholders)
        if placeholder_count <= 2:
            return "simple"
        elif placeholder_count <= 6:
            return "medium"
        else:
            return "complex"

    def _determine_content_type(self, layout_name: str, placeholders: List[str]) -> str:
        """Determine content type based on layout structure."""
        name_lower = layout_name.lower()

        if "title" in name_lower and ("slide" in name_lower or len(placeholders) <= 2):
            return "title"
        elif "comparison" in name_lower or ("left" in str(placeholders) and "right" in str(placeholders)):
            return "comparison"
        elif "column" in name_lower or len([p for p in placeholders if "col" in p.lower()]) >= 3:
            return "structured"
        elif "picture" in name_lower or "image" in str(placeholders):
            return "visual"
        elif "swot" in name_lower:
            return "analysis"
        else:
            return "text"

    def _generate_layout_description(self, layout_name: str, placeholders: List[str]) -> str:
        """Generate descriptive text for layout based on its characteristics."""

        descriptions = {
            "Title Slide": "Professional title slide with title and subtitle",
            "Title and Content": "Standard slide with title and content area",
            "Two Content": "Split layout with two content sections",
            "Comparison": "Side-by-side comparison layout",
            "Three Columns": "Three-column layout for organized content",
            "Four Columns": "Four-column layout for categories or processes",
            "Picture with Caption": "Image layout with descriptive caption",
            "SWOT Analysis": "Structured SWOT analysis matrix",
        }

        return descriptions.get(layout_name, f"Layout with {len(placeholders)} content areas")

    def _generate_best_for(self, layout_name: str, placeholders: List[str]) -> str:
        """Generate usage recommendations for layout."""

        recommendations = {
            "Title Slide": "Presentation opening, section introductions",
            "Title and Content": "General content, bullet points, explanations",
            "Two Content": "Before/after comparisons, split topics",
            "Comparison": "Side-by-side analysis, option evaluation",
            "Three Columns": "Process steps, feature categories, timelines",
            "Four Columns": "Feature comparisons, process steps, categories, matrix analysis",
            "Picture with Caption": "Visual content, diagrams, examples",
            "SWOT Analysis": "Strategic analysis, business planning",
        }

        return recommendations.get(layout_name, "Structured content presentation")

    def _determine_required_placeholders(self, layout_name: str, placeholders: List[str]) -> List[str]:
        """Determine which placeholders are required vs optional."""
        # Title is almost always required
        required = []

        for placeholder in placeholders:
            p_lower = placeholder.lower()
            if "title" in p_lower and "subtitle" not in p_lower:
                required.append(placeholder)
            elif layout_name == "Title Slide" and "subtitle" in p_lower:
                required.append(placeholder)

        return required

    def _generate_template_description(self, template_name: str, layouts: Dict[str, LayoutMetadata]) -> str:
        """Generate description for entire template."""
        layout_count = len(layouts)

        if template_name.lower() == "default":
            return f"Standard business presentation template with {layout_count} versatile layouts"
        else:
            return f"Professional template with {layout_count} specialized layouts"

    def _generate_use_cases(self, layouts: Dict[str, LayoutMetadata]) -> List[str]:
        """Generate use cases based on available layouts."""
        use_cases = set()

        # Analyze layout capabilities to suggest use cases
        if any("Title Slide" in name for name in layouts.keys()):
            use_cases.add("Business presentations")

        if any("comparison" in meta.content_type for meta in layouts.values()):
            use_cases.add("Comparative analysis")

        if any("structured" in meta.content_type for meta in layouts.values()):
            use_cases.add("Process documentation")
            use_cases.add("Feature comparisons")

        if any(meta.supports_images for meta in layouts.values()):
            use_cases.add("Visual presentations")

        # Default use cases
        use_cases.update(["General presentations", "Training materials"])

        return sorted(use_cases)

    def _determine_target_audience(self, template_name: str, layouts: Dict[str, LayoutMetadata]) -> List[str]:
        """Determine target audience based on template characteristics."""
        if template_name.lower() in ["executive", "business_pro"]:
            return ["executive", "business"]
        elif template_name.lower() in ["minimal", "simple"]:
            return ["general", "academic"]
        else:
            return ["business", "general"]

    def get_all_available_templates(self) -> Dict[str, Any]:
        """
        Get metadata for all available templates in the template folder.

        Returns:
            Dictionary with 'templates' and 'total_templates' keys as defined by TDD tests
        """
        if not self.template_folder.exists():
            self.logger.warning(f"Template folder not found: {self.template_folder}")
            return {"templates": {}, "total_templates": 0}

        templates = {}

        # Find all JSON files in template folder
        for template_file in self.template_folder.glob("*.json"):
            template_name = template_file.stem

            try:
                metadata = self.load_template_metadata(template_name)
                # Convert TemplateMetadata to simple dict format as expected by test
                templates[template_name] = {
                    "name": metadata.template_name,
                    "layouts": {
                        layout_name: {
                            "display_name": layout_meta.display_name,
                            "description": layout_meta.description,
                            "placeholders": layout_meta.placeholders,
                        }
                        for layout_name, layout_meta in metadata.layouts.items()
                    },
                }
            except (FileNotFoundError, ValueError) as e:
                self.logger.error(f"Failed to load template '{template_name}': {e}")

        return {"templates": templates, "total_templates": len(templates)}

    def validate_template_exists(self, template_name: str) -> bool:
        """Check if a template exists and is valid."""
        # Handle edge cases
        if not template_name or template_name is None:
            return False

        try:
            self.load_template_metadata(template_name)
            return True
        except (FileNotFoundError, ValueError, TypeError):
            return False

    def get_template_names(self) -> List[str]:
        """Get list of all available template names."""
        all_templates_data = self.get_all_available_templates()
        return list(all_templates_data.get("templates", {}).keys())

    def clear_cache(self) -> None:
        """Clear the metadata cache (useful for testing or reloading)."""
        self._metadata_cache.clear()
        self.pattern_loader.clear_cache()

    def get_enhanced_layout_metadata(self, layout_name: str) -> Optional[LayoutMetadata]:
        """
        Get enhanced layout metadata by combining template and pattern data.

        Args:
            layout_name: Name of the layout to get metadata for

        Returns:
            Enhanced LayoutMetadata object with pattern data integrated
        """
        # Get pattern data from PatternLoader
        pattern_data = self.pattern_loader.get_pattern_for_layout(layout_name)

        if not pattern_data:
            self.logger.warning(f"No pattern data found for layout: {layout_name}")
            return None

        # Extract information from pattern data
        yaml_pattern = pattern_data.get("yaml_pattern", {})
        validation = pattern_data.get("validation", {})
        description = pattern_data.get("description", "")
        _ = pattern_data.get("example", "")  # For potential future use

        # Extract placeholder names from yaml_pattern (excluding layout)
        placeholders = [field for field in yaml_pattern.keys() if field != "layout"]

        # Get required and optional fields from validation
        required_placeholders = validation.get("required_fields", [])
        optional_placeholders = validation.get("optional_fields", [])

        # If optional_placeholders is empty, derive from placeholders
        if not optional_placeholders:
            optional_placeholders = [p for p in placeholders if p not in required_placeholders]

        # Determine layout characteristics
        supports_images = any("image" in p.lower() for p in placeholders)
        supports_tables = layout_name in ["Title and Content", "Section Header"]
        complexity = self._determine_layout_complexity(placeholders)
        content_type = self._determine_content_type(layout_name, placeholders)
        best_for = self._generate_best_for(layout_name, placeholders)

        return LayoutMetadata(
            display_name=layout_name,
            description=description,
            placeholders=placeholders,
            required_placeholders=required_placeholders,
            optional_placeholders=optional_placeholders,
            best_for=best_for,
            content_type=content_type,
            complexity=complexity,
            supports_images=supports_images,
            supports_tables=supports_tables,
        )

    def get_all_pattern_based_layouts(self) -> Dict[str, LayoutMetadata]:
        """
        Get all available layouts based on pattern data.

        Returns:
            Dictionary mapping layout names to enhanced LayoutMetadata objects
        """
        patterns = self.pattern_loader.load_patterns()
        layouts = {}

        for layout_name in patterns.keys():
            layout_meta = self.get_enhanced_layout_metadata(layout_name)
            if layout_meta:
                layouts[layout_name] = layout_meta

        return layouts

    def create_template_metadata_from_patterns(self, template_name: str) -> TemplateMetadata:
        """
        Create template metadata using pattern data as the primary source.

        Args:
            template_name: Name of the template

        Returns:
            TemplateMetadata object with pattern-based layout information
        """
        # Get all layouts from patterns
        layouts = self.get_all_pattern_based_layouts()

        if not layouts:
            raise ValueError(f"No pattern-based layouts found for template: {template_name}")

        # Generate template-level metadata
        description = self._generate_template_description(template_name, layouts)
        use_cases = self._generate_use_cases(layouts)
        target_audience = self._determine_target_audience(template_name, layouts)

        # Calculate complexity breakdown
        complexity_breakdown = {"simple": 0, "medium": 0, "complex": 0}
        for layout_meta in layouts.values():
            complexity_breakdown[layout_meta.complexity] += 1

        return TemplateMetadata(
            template_name=template_name,
            description=description,
            use_cases=use_cases,
            target_audience=target_audience,
            layouts=layouts,
            total_layouts=len(layouts),
            complexity_breakdown=complexity_breakdown,
        )

    def get_pattern_example(self, layout_name: str) -> Dict[str, Any]:
        """
        Get structured example data from pattern file.

        Args:
            layout_name: Name of the layout to get example for

        Returns:
            Dictionary with example data or empty dict if not found
        """
        pattern_data = self.pattern_loader.get_pattern_for_layout(layout_name)

        if not pattern_data:
            return {}

        example_text = pattern_data.get("example", "")
        if not example_text:
            return {}

        # Parse the frontmatter from the example
        try:
            # Split the example into frontmatter and content
            if "---" in example_text:
                parts = example_text.split("---")
                if len(parts) >= 2:
                    frontmatter_text = parts[1].strip()

                    # Parse YAML frontmatter
                    import yaml

                    example_data = yaml.safe_load(frontmatter_text)

                    # Remove the layout field as it's not needed for examples
                    if isinstance(example_data, dict) and "layout" in example_data:
                        example_data = {k: v for k, v in example_data.items() if k != "layout"}

                    return example_data or {}
        except Exception as e:
            self.logger.warning(f"Failed to parse example for layout '{layout_name}': {e}")

        return {}

    def get_layout_validation_info(self, layout_name: str) -> Dict[str, Any]:
        """
        Get validation information for a specific layout.

        Args:
            layout_name: Name of the layout to get validation info for

        Returns:
            Dictionary with validation requirements
        """
        pattern_data = self.pattern_loader.get_pattern_for_layout(layout_name)

        if not pattern_data:
            return {}

        validation = pattern_data.get("validation", {})
        yaml_pattern = pattern_data.get("yaml_pattern", {})

        return {
            "required_fields": validation.get("required_fields", []),
            "optional_fields": validation.get("optional_fields", []),
            "field_types": validation.get("field_types", {}),
            "available_fields": list(yaml_pattern.keys()),
        }
