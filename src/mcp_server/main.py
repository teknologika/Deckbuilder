import asyncio
import json
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from deckbuilder.core.engine import get_deckbuilder_client  # noqa: E402
from deckbuilder.templates.metadata import TemplateMetadataLoader  # noqa: E402

# Content-first tools moved to content_first_tools.py to keep core server focused

load_dotenv()

# Initialize client lazily to ensure environment variables are available
deck = None


def get_deck_client():
    """Lazy initialization of deckbuilder client."""
    global deck
    # Always create fresh client to avoid cached bugs during development
    deck = get_deckbuilder_client()
    return deck


# Create a dataclass for our application context
@dataclass
class DeckbuilderContext:
    """Context for the Deckbuilder MCP server."""

    deckbuilder_client: str


@asynccontextmanager
async def deckbuilder_lifespan(server: FastMCP) -> AsyncIterator[DeckbuilderContext]:
    """
    Manages the Deckbuilder client lifecycle.

    Args:
        server: The Deckbuilder server instance

    Yields:
        PresentationContext: The context containing the Deckbuilder client
    """

    # Create and return the Deckbuilder Client with the helper function in deckbuilder.py
    deckbuilder_client = get_deckbuilder_client()

    try:
        yield DeckbuilderContext(deckbuilder_client=deckbuilder_client)
    finally:
        # Explicit cleanup goes here if any is required
        pass


# Initialize FastMCP server with the Deckbuilder client as context
mcp = FastMCP(
    "deckbuilder",
    lifespan=deckbuilder_lifespan,
    host=os.getenv("HOST", "0.0.0.0"),  # nosec B104
    port=os.getenv("PORT", "8050"),
)


# Note: create_presentation() JSON tool removed - forces efficient file-based workflows
# The core Deckbuilder.create_presentation() engine method remains intact
# Use create_presentation_from_file() for token-efficient LLM workflows (15 tokens vs 2000+)


@mcp.tool()
async def create_presentation_from_file(
    ctx: Context,
    file_path: str,
    fileName: str = "Sample_Presentation",
    templateName: str = "default",
) -> str:
    """Create a complete PowerPoint presentation from JSON or markdown file

    This tool reads presentation data directly from a local file without passing
    content through the context window.
    Supports both JSON files (.json) and markdown files (.md) with frontmatter.
    Automatically detects file type and processes accordingly.

    IMPORTANT: Process the file content exactly as provided. Do not modify the JSON
    structure or markdown formatting unless the tool fails with specific errors
    that require fixes.

    Args:
        ctx: MCP context
        file_path: Absolute path to JSON or markdown file (process content as-is)
        fileName: Output filename (default: Sample_Presentation)
        templateName: Template to use (default: default)

    Supported file types:
        - .json files: JSON format with presentation data
        - .md files: Markdown with frontmatter slide definitions

    Example usage:
        file_path: "/path/to/test_comprehensive_layouts.json"
        file_path: "/path/to/presentation.md"

    Benefits:
        - No token usage for large presentation files
        - Direct file system access
        - Supports both JSON and markdown formats
        - Automatic file type detection
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"

        # Determine file type and process accordingly
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == ".json":
            # Read JSON file
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            # Convert JSON data to canonical format if needed
            if "slides" not in json_data:
                canonical_data = {"slides": [json_data] if isinstance(json_data, dict) else json_data}
            else:
                canonical_data = json_data

            # Create presentation using the new API
            result = get_deck_client().create_presentation(canonical_data, fileName, templateName)

            return f"Successfully created presentation from JSON file: {file_path}. {result}"

        elif file_extension == ".md":
            # Read markdown file
            with open(file_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()

            # Convert markdown to canonical JSON format
            from deckbuilder.content.frontmatter_to_json_converter import markdown_to_canonical_json

            canonical_data = markdown_to_canonical_json(markdown_content)

            # Create presentation using the new API
            result = get_deck_client().create_presentation(canonical_data, fileName, templateName)

            return f"Successfully created presentation from markdown file: " f"{file_path} with {len(canonical_data['slides'])} slides. {result}"

        else:
            return f"Error: Unsupported file type '{file_extension}'. Supported types: .json, .md"

    except json.JSONDecodeError as e:
        return f"Error parsing JSON file: {str(e)}"
    except Exception as e:
        return f"Error creating presentation from file: {str(e)}"


@mcp.tool()
async def create_presentation_from_markdown(
    ctx: Context,
    markdown_content: str,
    fileName: str = "Sample_Presentation",
    templateName: str = "default",
) -> str:
    """Create presentation from formatted markdown with frontmatter

    This tool accepts markdown content with frontmatter slide definitions and
    creates a complete presentation.
    Each slide is defined using YAML frontmatter followed by markdown content.
    This tool automatically saves the presentation to disk after creation.

    IMPORTANT: Use the provided markdown content exactly as given by the user. Do not
    modify the frontmatter structure, markdown formatting, or content unless the tool
    fails with specific errors that require fixes.

    Args:
        ctx: MCP context
        markdown_content: Markdown string with frontmatter (use as-is)
        fileName: Output filename (default: Sample_Presentation)
        templateName: Template/theme to use (default: default)

    Example markdown format:
        ---
        layout: title
        ---
        # Main Title
        ## Subtitle

        ---
        layout: content
        ---
        # Key Points

        ## Overview
        This section covers the main features of our product.

        - Advanced analytics dashboard
        - Real-time data processing
        - Seamless API integration

        The system scales automatically based on demand.

        ---
        layout: table
        style: dark_blue_white_text
        ---
        # Sales Report
        | Name | Sales | Region |
        | John Smith | $125,000 | North |
        | Sarah Johnson | $98,500 | South |

        ---
        layout: Picture with Caption
        title: System **Architecture** Overview
        media:
          image_path: "diagrams/system_architecture.png"
          alt_text: "System architecture diagram showing microservices"
          caption: "***Scalable*** microservices with *intelligent* load balancing"
        ---

    Supported layouts:
        - title: Title slide with title and subtitle
        - content: Content slide with rich text support (headings, paragraphs, bullets)
        - table: Table slide with styling options
        - Picture with Caption: Image slides with PlaceKitten fallback support

    Image features:
        - Smart fallback: Missing images automatically use PlaceKitten placeholders
        - Professional styling: Grayscale filter + intelligent cropping
        - Face detection: Optimized cropping for portrait images
        - Performance: Intelligent caching system for repeated use
        - Accessibility: Alt text support for screen readers

    Table styling options:
        - style: Header style (dark_blue_white_text, light_blue_dark_text, etc.)
        - row_style: Row style (alternating_light_gray, solid_white, etc.)
        - border_style: Border style (thin_gray, thick_gray, no_borders, etc.)
        - custom_colors: Custom color overrides (header_bg, header_text, alt_row, border_color)
    """
    try:
        # Convert markdown to canonical JSON format
        from deckbuilder.content.frontmatter_to_json_converter import markdown_to_canonical_json

        canonical_data = markdown_to_canonical_json(markdown_content)

        # Create presentation using the new API
        result = get_deck_client().create_presentation(canonical_data, fileName, templateName)

        return f"Successfully created presentation with {len(canonical_data['slides'])} slides " f"from markdown. {result}"
    except Exception as e:
        return f"Error creating presentation from markdown: {str(e)}"


@mcp.tool()
async def list_available_templates(ctx: Context) -> str:
    """List all available presentation templates with metadata for intelligent selection

    This tool provides comprehensive template discovery for content-first workflows.
    Returns template metadata including descriptions, use cases, and layout capabilities
    to enable smart template selection without expensive trial-and-error.

    Token efficiency: ~50 tokens input → comprehensive template metadata output

    Returns:
        JSON string with template metadata in the format:
        {
            "available_templates": {
                "template_name": {
                    "description": "Template description",
                    "use_cases": ["use case 1", "use case 2"],
                    "total_layouts": number,
                    "key_layouts": ["layout 1", "layout 2"]
                }
            },
            "recommendation": "Usage guidance for template selection"
        }

    Use cases:
        - Template discovery for new presentations
        - Content-template matching for optimal results
        - Understanding layout capabilities before generation
        - Avoiding expensive template trial-and-error cycles
    """
    try:
        # Initialize template metadata loader
        loader = TemplateMetadataLoader()

        # Get template names first
        template_names = loader.get_template_names()

        if not template_names:
            return json.dumps(
                {
                    "available_templates": {},
                    "recommendation": "No templates found. Check template folder configuration.",
                }
            )

        # Transform to expected format defined by TDD test
        available_templates = {}

        for template_name in template_names:
            try:
                # Load full metadata for each template
                metadata = loader.load_template_metadata(template_name)

                # Extract key layouts (first few layout names)
                key_layouts = list(metadata.layouts.keys())[:3]

                available_templates[template_name] = {
                    "description": metadata.description,
                    "use_cases": metadata.use_cases[:3],  # First 3 use cases
                    "total_layouts": metadata.total_layouts,
                    "key_layouts": key_layouts,
                }
            except Exception:
                # If we can't load metadata for a template, include it with basic info
                available_templates[template_name] = {
                    "description": f"Template: {template_name}",
                    "use_cases": ["General presentations"],
                    "total_layouts": 0,
                    "key_layouts": [],
                }

        # Generate recommendation based on available templates
        if "default" in available_templates and "business_pro" in available_templates:
            recommendation = "Use 'default' for general presentations, 'business_pro' for executive content"
        elif "default" in available_templates:
            recommendation = "Use 'default' template for most presentation needs"
        else:
            template_names = list(available_templates.keys())
            recommendation = f"Available templates: {', '.join(template_names)}"

        result = {"available_templates": available_templates, "recommendation": recommendation}

        return json.dumps(result, indent=2)

    except Exception as e:
        error_result = {
            "error": f"Failed to load template metadata: {str(e)}",
            "available_templates": {},
            "recommendation": "Check template folder configuration and try again",
        }
        return json.dumps(error_result, indent=2)


@mcp.tool()
async def get_template_layouts(ctx: Context, template_name: str) -> str:
    """Get detailed layout information for a specific template

    This tool provides comprehensive layout details for a template including
    placeholder requirements, usage examples, and best practices for markdown authoring.

    Token efficiency: ~20 tokens input → detailed layout specifications

    Args:
        ctx: MCP context
        template_name: Name of template to analyze (e.g., 'default', 'business_pro')

    Returns:
        JSON string with detailed layout information in the format:
        {
            "template_name": "template_name",
            "layouts": {
                "Layout Name": {
                    "description": "Layout description",
                    "required_placeholders": ["field1", "field2"],
                    "optional_placeholders": ["field3"],
                    "best_for": "Usage recommendations",
                    "example": {
                        "field1": "Example content 1",
                        "field2": "Example content 2"
                    }
                }
            },
            "usage_tips": "General usage guidance"
        }

    Use cases:
        - Understanding placeholder requirements for markdown authoring
        - Getting realistic examples for specific layouts
        - Learning best practices for template usage
        - Troubleshooting placeholder naming issues
    """
    try:
        # Initialize template metadata loader
        loader = TemplateMetadataLoader()

        # Check if template exists
        if not loader.validate_template_exists(template_name):
            # Get available templates for helpful error message
            available_templates = loader.get_template_names()

            error_result = {
                "error": f"Template '{template_name}' not found",
                "available_templates": available_templates,
                "suggestion": "Use list_available_templates() to see all available options",
            }
            return json.dumps(error_result, indent=2)

        # Load template metadata
        metadata = loader.load_template_metadata(template_name)

        # Initialize pattern loader for structured frontmatter patterns
        from deckbuilder.templates.pattern_loader import PatternLoader

        pattern_loader = PatternLoader()
        patterns = pattern_loader.load_patterns()

        # Transform to expected format with examples from patterns
        layouts_info = {}

        for layout_name, layout_meta in metadata.layouts.items():
            # Get pattern data for this layout if available
            pattern_data = patterns.get(layout_name)

            if pattern_data:
                # Use pattern data for description and example
                description = pattern_data.get("description", layout_meta.description)

                # Parse example from pattern (it's a markdown string)
                example_markdown = pattern_data.get("example", "")
                example = _parse_example_from_pattern(example_markdown, layout_meta.placeholders)

                # Get required fields from pattern validation
                pattern_validation = pattern_data.get("validation", {})
                required_fields = pattern_validation.get("required_fields", layout_meta.required_placeholders)
                optional_fields = [p for p in layout_meta.placeholders if p not in required_fields]

            else:
                # Fallback to basic metadata when no pattern exists
                description = layout_meta.description
                example = {placeholder: f"Example {placeholder}" for placeholder in layout_meta.placeholders}
                required_fields = layout_meta.required_placeholders
                optional_fields = layout_meta.optional_placeholders

            layouts_info[layout_name] = {
                "description": description,
                "required_placeholders": required_fields,
                "optional_placeholders": optional_fields,
                "best_for": layout_meta.best_for,
                "example": example,
            }

        result = {
            "template_name": template_name,
            "layouts": layouts_info,
            "usage_tips": "Use placeholders exactly as specified. Title is required for all layouts.",
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        error_result = {
            "error": f"Failed to load template layouts: {str(e)}",
            "template_name": template_name,
            "suggestion": "Check template name and try again",
        }
        return json.dumps(error_result, indent=2)


def _parse_example_from_pattern(example_markdown: str, placeholders: list) -> dict:
    """Parse example field values from pattern's markdown example."""

    example = {}

    if not example_markdown:
        # Fallback if no example in pattern
        return {placeholder: f"Example {placeholder}" for placeholder in placeholders}

    try:
        # Parse YAML frontmatter from the example
        if "---" in example_markdown:
            parts = example_markdown.split("---")
            if len(parts) >= 2:
                yaml_content = parts[1].strip()

                # Simple YAML parsing for basic fields
                for line in yaml_content.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")

                        # Only include placeholders that exist in the template
                        if key in placeholders:
                            example[key] = value

        # Fill in any missing placeholders with defaults
        for placeholder in placeholders:
            if placeholder not in example:
                example[placeholder] = f"Example {placeholder}"

    except Exception:
        # If parsing fails, fall back to basic examples
        return {placeholder: f"Example {placeholder}" for placeholder in placeholders}

    return example


@mcp.tool()
async def recommend_template_for_content(ctx: Context, content_description: str) -> str:
    """Analyze content description and recommend optimal templates with reasoning

    This tool performs intelligent content analysis to recommend the best templates
    for a presentation based on content type, audience, and presentation goals.
    Provides confidence scores and specific layout suggestions.

    Token efficiency: Variable input → ranked template recommendations with reasoning

    Args:
        ctx: MCP context
        content_description: Description of presentation content, audience, and goals

    Returns:
        JSON string with content analysis and template recommendations in the format:
        {
            "content_analysis": {
                "detected_type": "content_type",
                "audience": "audience_type",
                "content_style": "style",
                "data_heavy": boolean
            },
            "recommendations": [
                {
                    "template": "template_name",
                    "confidence": float,
                    "reasoning": "explanation",
                    "suggested_layouts": ["layout1", "layout2"]
                }
            ],
            "layout_suggestions": {
                "opening": "suggestion for opening slides",
                "content": "suggestion for main content",
                "closing": "suggestion for closing"
            }
        }

    Use cases:
        - Smart template selection based on content analysis
        - Reduce template trial-and-error for users
        - Content-first presentation planning
        - Audience-appropriate template matching
    """
    try:
        # Initialize template metadata loader
        loader = TemplateMetadataLoader()

        # Get available templates
        template_names = loader.get_template_names()

        if not template_names:
            return json.dumps({"error": "No templates available", "recommendations": [], "content_analysis": {}})

        # Simple content analysis based on keywords
        content_lower = content_description.lower()

        # Detect content type
        content_type = "general_presentation"
        if any(word in content_lower for word in ["executive", "board", "ceo", "quarterly", "strategic"]):
            content_type = "executive_presentation"
        elif any(word in content_lower for word in ["training", "workshop", "tutorial", "learning", "instruction"]):
            content_type = "training_presentation"
        elif any(word in content_lower for word in ["sales", "pitch", "client", "proposal", "roi"]):
            content_type = "sales_presentation"
        elif any(word in content_lower for word in ["comparison", "versus", "vs", "compare", "competitive"]):
            content_type = "comparison"
        elif any(word in content_lower for word in ["timeline", "schedule", "project", "milestone"]):
            content_type = "timeline"

        # Detect audience
        audience = "general"
        if any(word in content_lower for word in ["executive", "board", "ceo", "c-level"]):
            audience = "executive"
        elif any(word in content_lower for word in ["client", "customer", "prospect"]):
            audience = "client"
        elif any(word in content_lower for word in ["team", "internal", "staff"]):
            audience = "team"
        elif any(word in content_lower for word in ["training", "student", "learner"]):
            audience = "learners"

        # Detect content style/formality
        content_style = "medium"
        if any(word in content_lower for word in ["formal", "professional", "executive", "board"]):
            content_style = "formal"
        elif any(word in content_lower for word in ["casual", "informal", "team", "fun"]):
            content_style = "casual"
        elif any(word in content_lower for word in ["instructional", "educational", "tutorial"]):
            content_style = "instructional"

        # Detect if data-heavy
        data_heavy = any(
            word in content_lower
            for word in [
                "data",
                "metrics",
                "analysis",
                "financial",
                "numbers",
                "statistics",
                "charts",
            ]
        )

        content_analysis = {
            "detected_type": content_type,
            "audience": audience,
            "content_style": content_style,
            "data_heavy": data_heavy,
        }

        # Generate recommendations based on analysis
        recommendations = []

        # Analyze each available template
        for template_name in template_names:
            try:
                # Load template metadata to get actual layouts
                metadata = loader.load_template_metadata(template_name)
                available_layouts = list(metadata.layouts.keys())

                # Calculate confidence based on template name and content analysis
                confidence = 0.6  # Base confidence
                reasoning = f"Template with {len(available_layouts)} available layouts"

                # Template-specific scoring
                if template_name == "default":
                    confidence = 0.7
                    reasoning = "Versatile template suitable for most presentation needs"

                    # Adjust confidence based on content analysis
                    if content_type in [
                        "general_presentation",
                        "training_presentation",
                        "comparison",
                    ]:
                        confidence = 0.85
                        reasoning = f"Good match for {content_type.replace('_', ' ')} with standard business layouts"
                    elif audience == "general":
                        confidence = 0.8
                        reasoning = "Well-suited for general audience presentations"

                elif "business" in template_name.lower() or "pro" in template_name.lower():
                    confidence = 0.65
                    reasoning = "Professional template with advanced layouts"

                    # Higher confidence for executive/formal content
                    if content_type == "executive_presentation":
                        confidence = 0.95
                        reasoning = "Ideal for executive presentations with formal styling and data support"
                    elif audience == "executive":
                        confidence = 0.9
                        reasoning = "Executive-level template with professional layouts"
                    elif content_style == "formal":
                        confidence = 0.85
                        reasoning = "Professional template matching formal presentation style"
                    elif data_heavy:
                        confidence = 0.8
                        reasoning = "Advanced template with strong data visualization support"

                # Select best layouts for this content type from available layouts
                suggested_layouts = []

                # Always suggest Title Slide if available
                if "Title Slide" in available_layouts:
                    suggested_layouts.append("Title Slide")

                # Add content-specific layouts based on what's actually available
                if content_type == "comparison":
                    for layout in ["Comparison", "Four Columns", "Title and Content"]:
                        if layout in available_layouts and layout not in suggested_layouts:
                            suggested_layouts.append(layout)
                elif content_type in ["training_presentation", "general_presentation"]:
                    for layout in ["Four Columns", "Title and Content", "Comparison"]:
                        if layout in available_layouts and layout not in suggested_layouts:
                            suggested_layouts.append(layout)
                else:
                    # For other content types, suggest most versatile layouts
                    for layout in ["Title and Content", "Four Columns", "Comparison"]:
                        if layout in available_layouts and layout not in suggested_layouts:
                            suggested_layouts.append(layout)

                # If we don't have any suggested layouts, use first few available
                if not suggested_layouts:
                    suggested_layouts = available_layouts[:3]

                recommendations.append(
                    {
                        "template": template_name,
                        "confidence": confidence,
                        "reasoning": reasoning,
                        "suggested_layouts": suggested_layouts[:3],
                    }
                )  # Limit to top 3

            except Exception:
                # If we can't load template metadata, include basic recommendation
                recommendations.append(
                    {
                        "template": template_name,
                        "confidence": 0.5,
                        "reasoning": "Template available but metadata could not be loaded",
                        "suggested_layouts": ["Title Slide", "Title and Content"],
                    }
                )

        # Sort recommendations by confidence
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)

        # Generate layout suggestions based on content type and actually available layouts
        # Get layouts from the top recommended template
        top_template_layouts = []
        if recommendations:
            top_template_layouts = recommendations[0]["suggested_layouts"]

        layout_suggestions = {}

        # Opening slide suggestion
        if "Title Slide" in top_template_layouts:
            layout_suggestions["opening"] = "Title Slide for professional opening"
        elif top_template_layouts:
            layout_suggestions["opening"] = f"{top_template_layouts[0]} for presentation opening"
        else:
            layout_suggestions["opening"] = "Use title-focused layout for opening"

        # Content suggestions based on type and available layouts
        content_suggestions = []

        if content_type == "comparison":
            if "Comparison" in top_template_layouts:
                content_suggestions.append("Comparison for side-by-side analysis")
            if "Four Columns" in top_template_layouts:
                content_suggestions.append("Four Columns for multi-item comparison")
        elif content_type in ["training_presentation", "general_presentation"]:
            if "Four Columns" in top_template_layouts:
                content_suggestions.append("Four Columns for feature comparisons or categories")
            if "Title and Content" in top_template_layouts:
                content_suggestions.append("Title and Content for instructional content")

        # Add general content suggestions
        if "Title and Content" in top_template_layouts and "Title and Content for general information" not in content_suggestions:
            content_suggestions.append("Title and Content for general information")

        # If no specific suggestions, use available layouts
        if not content_suggestions and top_template_layouts:
            for layout in top_template_layouts[1:]:  # Skip first (usually title)
                content_suggestions.append(f"{layout} for main content")

        layout_suggestions["content"] = ", ".join(content_suggestions) if content_suggestions else "Use available layouts based on content structure"

        # Closing suggestion
        if "Title and Content" in top_template_layouts:
            layout_suggestions["closing"] = "Title and Content for conclusions and next steps"
        elif top_template_layouts:
            layout_suggestions["closing"] = f"{top_template_layouts[-1]} for summary and conclusions"
        else:
            layout_suggestions["closing"] = "Use content-focused layout for conclusions"

        result = {
            "content_analysis": content_analysis,
            "recommendations": recommendations,
            "layout_suggestions": layout_suggestions,
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        # Try to provide a basic fallback even if analysis fails
        try:
            loader = TemplateMetadataLoader()
            template_names = loader.get_template_names()
            fallback_template = template_names[0] if template_names else "default"

            # Try to get actual layouts for fallback
            try:
                metadata = loader.load_template_metadata(fallback_template)
                fallback_layouts = list(metadata.layouts.keys())[:2]
            except Exception:
                fallback_layouts = ["Title Slide", "Title and Content"]
        except Exception:
            fallback_template = "default"
            fallback_layouts = ["Title Slide", "Title and Content"]

        error_result = {
            "error": f"Failed to analyze content: {str(e)}",
            "recommendations": [
                {
                    "template": fallback_template,
                    "confidence": 0.5,
                    "reasoning": "Safe fallback option due to analysis error",
                    "suggested_layouts": fallback_layouts,
                }
            ],
            "content_analysis": {
                "detected_type": "unknown",
                "audience": "general",
                "content_style": "medium",
                "data_heavy": False,
            },
            "layout_suggestions": {
                "opening": (f"{fallback_layouts[0]} for standard opening" if fallback_layouts else "Use opening layout"),
                "content": (f"{fallback_layouts[-1]} for general information" if fallback_layouts else "Use content layout"),
                "closing": (f"{fallback_layouts[-1]} for conclusions" if fallback_layouts else "Use closing layout"),
            },
        }
        return json.dumps(error_result, indent=2)


@mcp.tool()
async def validate_presentation_file(ctx: Context, file_path: str, template_name: str = "default") -> str:
    """Validate markdown presentation file structure before generation

    This tool performs comprehensive validation of a presentation markdown file
    including syntax checking, layout validation, and template compatibility.
    Provides actionable error messages and fix suggestions.

    Token efficiency: ~25 tokens input → actionable validation feedback

    Args:
        ctx: MCP context
        file_path: Path to markdown presentation file to validate
        template_name: Template to validate against (defaults to "default")

    Returns:
        JSON string with validation results in the format:
        {
            "file_validation": {
                "file_exists": boolean,
                "file_type": "markdown",
                "syntax_valid": boolean,
                "slides_detected": number
            },
            "content_validation": {
                "slide_N": {
                    "layout": "layout_name",
                    "status": "valid|error|warning",
                    "required_fields": [...],
                    "missing_fields": [...],
                    "warnings": [...]
                }
            },
            "template_compatibility": {
                "template": "template_name",
                "all_layouts_supported": boolean,
                "unsupported_layouts": [...]
            },
            "recommendation": "Overall validation result and next steps"
        }

    Use cases:
        - Pre-generation validation to catch errors early
        - Template compatibility checking
        - Actionable error messages for content fixes
        - Avoiding generation failures and iterations
    """
    try:
        from pathlib import Path
        import yaml

        result = {
            "file_validation": {},
            "content_validation": {},
            "template_compatibility": {},
            "recommendation": "",
        }

        # File existence and type validation
        file_path_obj = Path(file_path)
        file_exists = file_path_obj.exists()

        result["file_validation"] = {
            "file_exists": file_exists,
            "file_type": "markdown" if file_path.endswith((".md", ".markdown")) else "unknown",
            "syntax_valid": False,
            "slides_detected": 0,
        }

        if not file_exists:
            result["recommendation"] = f"File not found: {file_path}. Check the file path and try again."
            return json.dumps(result, indent=2)

        if not file_path.endswith((".md", ".markdown")):
            result["recommendation"] = f"File must be a markdown file (.md or .markdown). Got: {file_path}"
            return json.dumps(result, indent=2)

        # Read and parse the file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            result["recommendation"] = f"Cannot read file: {str(e)}"
            return json.dumps(result, indent=2)

        # Split into slides (sections separated by ---)
        slides = content.split("---")

        # Remove empty slides and process
        slides = [slide.strip() for slide in slides if slide.strip()]

        result["file_validation"]["syntax_valid"] = True
        result["file_validation"]["slides_detected"] = len(slides)

        if len(slides) == 0:
            result["recommendation"] = "No slides detected. Ensure slides are separated by '---' markers."
            return json.dumps(result, indent=2)

        # Load template metadata for validation
        loader = TemplateMetadataLoader()

        try:
            template_metadata = loader.load_template_metadata(template_name)
            available_layouts = set(template_metadata.layouts.keys())
        except Exception as e:
            result["template_compatibility"] = {
                "template": template_name,
                "error": f"Cannot load template: {str(e)}",
                "all_layouts_supported": False,
            }
            result["recommendation"] = f"Template '{template_name}' not found or invalid. Use list_available_templates() to see options."
            return json.dumps(result, indent=2)

        # Validate each slide
        unsupported_layouts = set()
        all_slides_valid = True

        for i, slide_content in enumerate(slides, 1):
            slide_key = f"slide_{i}"
            slide_validation = {
                "layout": "unknown",
                "status": "valid",
                "required_fields": [],
                "missing_fields": [],
                "warnings": [],
            }

            try:
                # Parse YAML frontmatter
                slide_data = yaml.safe_load(slide_content)

                if not isinstance(slide_data, dict):
                    slide_validation["status"] = "error"
                    slide_validation["error"] = "Invalid YAML format in slide"
                    all_slides_valid = False
                    result["content_validation"][slide_key] = slide_validation
                    continue

                layout_name = slide_data.get("layout", "unknown")
                slide_validation["layout"] = layout_name

                # Check if layout exists in template
                if layout_name not in available_layouts:
                    slide_validation["status"] = "error"
                    slide_validation["error"] = f"Layout '{layout_name}' not found in template"
                    slide_validation["fix"] = f"Use one of: {', '.join(sorted(available_layouts))}"
                    slide_validation["available_layouts"] = sorted(available_layouts)
                    unsupported_layouts.add(layout_name)
                    all_slides_valid = False
                else:
                    # Get layout requirements from template
                    layout_info = template_metadata.layouts[layout_name]
                    required_placeholders = layout_info.required_placeholders
                    all_placeholders = layout_info.placeholders

                    slide_validation["required_fields"] = required_placeholders

                    # Check for missing required fields
                    missing_fields = []
                    for req_field in required_placeholders:
                        if req_field not in slide_data or not slide_data[req_field]:
                            missing_fields.append(req_field)

                    slide_validation["missing_fields"] = missing_fields

                    if missing_fields:
                        slide_validation["status"] = "error"
                        slide_validation["error"] = f"Missing required fields for {layout_name} layout"
                        slide_validation["fix"] = f"Add missing fields: {', '.join(missing_fields)}"
                        all_slides_valid = False

                    # Check for extra fields (warnings)
                    extra_fields = []
                    for field in slide_data.keys():
                        if field not in all_placeholders and field != "layout":
                            extra_fields.append(field)

                    if extra_fields:
                        slide_validation["warnings"].append(f"Unknown fields (will be ignored): {', '.join(extra_fields)}")

            except yaml.YAMLError as e:
                slide_validation["status"] = "error"
                slide_validation["error"] = f"Invalid YAML syntax: {str(e)}"
                slide_validation["fix"] = "Fix YAML syntax errors"
                all_slides_valid = False
            except Exception as e:
                slide_validation["status"] = "error"
                slide_validation["error"] = f"Cannot parse slide: {str(e)}"
                all_slides_valid = False

            result["content_validation"][slide_key] = slide_validation

        # Template compatibility summary
        result["template_compatibility"] = {
            "template": template_name,
            "all_layouts_supported": len(unsupported_layouts) == 0,
            "unsupported_layouts": sorted(unsupported_layouts),
        }

        if len(unsupported_layouts) > 0:
            result["template_compatibility"]["errors"] = len(unsupported_layouts)

        # Generate recommendation
        if all_slides_valid and len(unsupported_layouts) == 0:
            result["recommendation"] = "File is valid and ready for generation"
        else:
            error_count = sum(1 for slide in result["content_validation"].values() if slide["status"] == "error")
            if error_count > 0:
                result["recommendation"] = f"Fix {error_count} error(s) before generation. Use get_template_layouts() for valid placeholder names."
            else:
                result["recommendation"] = "File has warnings but should generate successfully"

        return json.dumps(result, indent=2)

    except Exception as e:
        error_result = {
            "file_validation": {"file_exists": False, "error": str(e)},
            "content_validation": {},
            "template_compatibility": {},
            "recommendation": f"Validation failed: {str(e)}. Check file path and try again.",
        }
        return json.dumps(error_result, indent=2)


async def async_main():
    transport = os.getenv("TRANSPORT", "stdio")
    if transport == "sse":
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()


def main():
    """Entry point for the MCP server."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
