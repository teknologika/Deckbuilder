#!/usr/bin/env python3
"""
Content-First Tools for Deckbuilder MCP Server

These tools implement the content-first design philosophy for intelligent presentation generation.
They have been moved from the main MCP server to keep the core server focused on presentation
generation while preserving the content analysis functionality for potential future use.

Content-First Workflow:
1. analyze_presentation_needs() -> overall structure and strategy
2. recommend_slide_approach() -> layout recommendations with confidence scores
3. optimize_content_for_layout() -> production-ready structured frontmatter
4. create_presentation_from_markdown() -> final PowerPoint with proper placeholder mapping
"""

import json

# Import content-first tools (will be implemented later)
try:
    from .content_analysis import analyze_presentation_needs
    from .content_optimization import optimize_content_for_layout
    from .layout_recommendations import recommend_slide_approach
except ImportError:
    # Placeholder functions for when these modules don't exist yet
    def analyze_presentation_needs(*args, **kwargs):
        return "Content analysis tool not implemented yet"

    def recommend_slide_approach(*args, **kwargs):
        return "Layout recommendation tool not implemented yet"

    def optimize_content_for_layout(*args, **kwargs):
        return "Content optimization tool not implemented yet"


async def analyze_presentation_needs_tool(
    user_input: str,
    audience: str = "general",
    constraints: str = None,
    presentation_goal: str = "inform",
) -> str:
    """
    Analyze user's presentation needs and recommend structure.

    Content-first approach: Understand communication goals before suggesting layouts.
    Acts as intelligent presentation consultant, not layout picker.

    Enhanced with structured frontmatter intelligence for optimal content-to-layout mapping.

    Args:
        user_input: Raw description of what they want to present
        audience: Target audience ("board", "team", "customers", "technical", "general")
        constraints: Time/slide constraints ("10 minutes", "5 slides max", "data-heavy")
        presentation_goal: Primary goal ("persuade", "inform", "report", "update", "train")

    Returns:
        JSON string with content analysis and structural recommendations

    Example:
        user_input: "I need to present our Q3 results to the board. We had 23% revenue
                    growth, expanded to 3 new markets, but customer churn increased to 8%.
                    I want to show we're growing but acknowledge the churn issue and present
                    our retention strategy."
        audience: "board"
        presentation_goal: "report"

        Returns analysis with:
        - Content analysis (key messages, narrative arc, complexity level)
        - Audience considerations (expertise level, attention span, preferred format)
        - Recommended structure (slide sequence with purpose and timing)
        - Presentation strategy (opening/closing approach, engagement tactics)

    This analysis feeds into the complete content-first workflow for intelligent presentations.
    """
    try:
        analysis_result = analyze_presentation_needs(user_input, audience, constraints, presentation_goal)
        return json.dumps(analysis_result, indent=2)
    except Exception as e:
        return f"Error analyzing presentation needs: {str(e)}"


async def recommend_slide_approach_tool(content_piece: str, message_intent: str, presentation_context: str = None) -> str:
    """
    Recommend optimal slide layouts based on specific content and communication intent.

    Content-first approach: Analyzes what you want to communicate with this specific
    content piece and recommends the most effective slide layouts.

    Enhanced with intelligent structured frontmatter pattern matching for precise content-to-layout optimization.

    Args:
        content_piece: Specific content to present (e.g., "We increased revenue 25%,
                       expanded to 3 markets, but churn rose to 8%")
        message_intent: What you want this content to communicate (e.g.,
                        "show growth while acknowledging challenges")
        presentation_context: Optional JSON string from analyze_presentation_needs_tool output

    Returns:
        JSON string with layout recommendations, confidence scores, and structured frontmatter previews

    Example:
        content_piece: "Our mobile app has these key features: real-time notifications,
                       offline mode, cloud sync, and advanced analytics dashboard"
        message_intent: "showcase the comprehensive feature set to potential customers"

        Returns recommendations like:
        - Four Columns layout (confidence: 0.90) for feature comparison grid
        - Title and Content layout (confidence: 0.75) for traditional feature list
        - Direct field YAML preview with content_col1, content_col2, etc.
        - Structured frontmatter intelligence for optimal placeholder mapping

    This tool bridges the gap between content analysis (Tool #1) and content optimization (Tool #3)
    by providing specific layout guidance with production-ready structured frontmatter examples.
    """
    try:
        # Parse presentation context if provided
        context_dict = None
        if presentation_context:
            try:
                context_dict = json.loads(presentation_context)
            except json.JSONDecodeError:
                # If parsing fails, continue without context
                pass

        # Get layout recommendations
        recommendations = recommend_slide_approach(content_piece, message_intent, context_dict)

        return json.dumps(recommendations, indent=2)

    except Exception as e:
        return f"Error recommending slide approach: {str(e)}"


async def optimize_content_for_layout_tool(content: str, chosen_layout: str, slide_context: str = None) -> str:
    """
    Optimize content structure and generate ready-to-use YAML for immediate presentation creation.

    Final step in content-first workflow: Takes raw content and chosen layout, then optimizes
    the content structure and generates production-ready structured frontmatter YAML.

    Enhanced with direct field format matching structured frontmatter patterns for seamless
    content-to-placeholder mapping and professional presentation output.

    Args:
        content: Raw content to optimize (e.g., "Our platform offers real-time
                 analytics, automated reporting, custom dashboards, and API integration")
        chosen_layout: Layout to optimize for (e.g., "Four Columns" from
                       recommend_slide_approach_tool)
        slide_context: Optional JSON string with context from previous tools
                       (analyze_presentation_needs, recommend_slide_approach)

    Returns:
        JSON string with optimized YAML structure, gap analysis, and presentation tips

    Example:
        content: "Traditional approach costs $50K annually with 2-week deployment
                 vs our solution at $30K with same-day setup"
        chosen_layout: "Comparison"

        Returns:
        - optimized_content.yaml_structure: Ready-to-use structured frontmatter YAML
        - gap_analysis: Content fit assessment and layout utilization analysis
        - presentation_tips: Delivery guidance and audience-specific recommendations
        - Direct field format: title_left, content_left, title_right, content_right

    Complete Content-First Workflow:
    1. analyze_presentation_needs_tool() -> overall structure and strategy
    2. recommend_slide_approach_tool() -> layout recommendations with confidence scores
    3. optimize_content_for_layout_tool() -> production-ready structured frontmatter ✅ THIS TOOL
    4. create_presentation_from_markdown() -> final PowerPoint with proper placeholder mapping
    """
    try:
        # Parse slide context if provided
        context_dict = None
        if slide_context:
            try:
                context_dict = json.loads(slide_context)
            except json.JSONDecodeError:
                # If parsing fails, continue without context
                pass

        # Optimize content for the chosen layout
        optimization_result = optimize_content_for_layout(content, chosen_layout, context_dict)

        return json.dumps(optimization_result, indent=2)

    except Exception as e:
        return f"Error optimizing content for layout: {str(e)}"
