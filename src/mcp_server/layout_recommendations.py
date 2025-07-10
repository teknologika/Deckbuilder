"""
Layout Recommendation Engine for Content-First Presentation Intelligence

This module implements Tool #2: recommend_slide_approach() which analyzes specific
content pieces and recommends optimal PowerPoint layouts based on communication intent.

Design Philosophy: Match content structure and message intent to most effective layout,
not just "what layouts exist?"
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LayoutRecommendation:
    """Single layout recommendation with confidence scoring"""

    layout: str
    confidence: float
    reason: str
    best_for: str


class LayoutRecommendationEngine:
    """
    Analyzes content pieces and recommends optimal slide layouts.

    Focuses on content structure, message intent, and communication effectiveness
    rather than just available template options.
    """

    def __init__(self):
        """Initialize with layout intelligence mapping"""
        self.layout_intelligence = self._build_layout_intelligence()
        self.available_layouts = self._get_available_layouts()

    def recommend_slide_approach(self, content_piece: str, message_intent: str, presentation_context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze content and recommend optimal slide layouts.

        Args:
            content_piece: Specific content to present
            message_intent: What they want this content to communicate
            presentation_context: Optional context from analyze_presentation_needs()

        Returns:
            Dictionary with layout recommendations, content analysis, and suggestions
        """
        # Analyze the content structure and type
        content_analysis = self._analyze_content_structure(content_piece)

        # Determine communication intent
        intent_analysis = self._analyze_message_intent(message_intent, content_piece)

        # Generate layout recommendations with confidence scoring
        layout_recommendations = self._generate_layout_recommendations(content_analysis, intent_analysis, presentation_context)

        # Provide content structuring suggestions
        content_suggestions = self._generate_content_suggestions(content_analysis, intent_analysis, layout_recommendations)

        # Generate structured frontmatter preview
        structured_frontmatter = self._generate_structured_frontmatter_preview(layout_recommendations, content_piece, message_intent)

        return {
            "recommended_layouts": [
                {
                    "layout": rec.layout,
                    "confidence": rec.confidence,
                    "reason": rec.reason,
                    "best_for": rec.best_for,
                }
                for rec in layout_recommendations
            ],
            "content_analysis": content_analysis,
            "content_suggestions": content_suggestions,
            "structured_frontmatter": structured_frontmatter,
        }

    def _analyze_content_structure(self, content_piece: str) -> Dict[str, Any]:
        """Analyze the structure and characteristics of the content."""
        content_lower = content_piece.lower()

        # Count various content elements
        numbers_count = len(re.findall(r"\d+%|\$[\d,]+|\d+", content_piece))
        bullet_indicators = len(re.findall(r"[-*•]|\d+\.|\w\)", content_piece))

        # Detect content patterns
        has_comparison = any(word in content_lower for word in ["vs", "versus", "compared to", "versus", "against"])
        has_list_structure = bullet_indicators > 2 or content_piece.count("\n") > 2 or content_piece.count(",") >= 3 or content_piece.count(":") >= 2
        has_metrics = numbers_count >= 2
        has_process = any(word in content_lower for word in ["first", "then", "next", "finally", "step"])

        # Determine content type
        if has_comparison:
            content_type = "comparison"
        elif has_metrics:
            content_type = "metrics_data"
        elif has_process:
            content_type = "process_timeline"
        elif has_list_structure:
            content_type = "structured_list"
        else:
            content_type = "narrative_text"

        # Count distinct elements for layout sizing
        distinct_elements = self._count_distinct_elements(content_piece)

        return {
            "content_type": content_type,
            "data_elements": numbers_count,
            "distinct_elements": distinct_elements,
            "has_comparison": has_comparison,
            "has_metrics": has_metrics,
            "has_list_structure": has_list_structure,
            "has_process": has_process,
            "structure_pattern": self._determine_structure_pattern(content_piece),
            "visual_emphasis": self._determine_visual_emphasis(content_piece, content_type),
        }

    def _analyze_message_intent(self, message_intent: str, content_piece: str) -> Dict[str, Any]:
        """Analyze what the user wants to communicate with this content."""
        intent_lower = message_intent.lower()

        # Categorize communication intent
        if any(word in intent_lower for word in ["compare", "contrast", "versus", "vs"]):
            intent_category = "comparison"
        elif any(word in intent_lower for word in ["highlight", "emphasize", "showcase", "feature"]):
            intent_category = "emphasis"
        elif any(word in intent_lower for word in ["explain", "show process", "demonstrate", "walk through"]):
            intent_category = "explanation"
        elif any(word in intent_lower for word in ["data", "metrics", "numbers", "performance"]):
            intent_category = "data_presentation"
        elif any(word in intent_lower for word in ["overview", "summary", "introduction"]):
            intent_category = "overview"
        else:
            intent_category = "general_information"

        return {
            "intent_category": intent_category,
            "emphasis_level": self._determine_emphasis_level(message_intent),
            "audience_focus": self._determine_audience_focus(message_intent),
            "communication_goal": self._determine_communication_goal(message_intent),
        }

    def _generate_layout_recommendations(
        self,
        content_analysis: Dict[str, Any],
        intent_analysis: Dict[str, Any],
        presentation_context: Optional[Dict] = None,
    ) -> List[LayoutRecommendation]:
        """Generate ranked layout recommendations based on content and intent analysis."""
        recommendations = []

        content_type = content_analysis["content_type"]
        intent_category = intent_analysis["intent_category"]
        distinct_elements = content_analysis["distinct_elements"]

        # Apply layout intelligence rules
        if content_type == "comparison" or intent_category == "comparison":
            if distinct_elements == 2:
                recommendations.append(
                    LayoutRecommendation(
                        "Comparison",
                        0.95,
                        "Two distinct elements perfect for side-by-side comparison",
                        "head-to-head comparisons and before/after scenarios",
                    )
                )
                recommendations.append(
                    LayoutRecommendation(
                        "Two Content",
                        0.80,
                        "Alternative two-column layout for comparison content",
                        "detailed side-by-side content with more text",
                    )
                )
            elif 3 <= distinct_elements <= 4:
                recommendations.append(
                    LayoutRecommendation(
                        "Four Columns",
                        0.90,
                        f"{distinct_elements} elements ideal for structured comparison grid",
                        "feature matrices and multi-factor comparisons",
                    )
                )
                recommendations.append(
                    LayoutRecommendation(
                        "Comparison",
                        0.70,
                        "Simplified two-way comparison focusing on main contrasts",
                        "high-level comparison without detailed breakdown",
                    )
                )

        elif content_type == "metrics_data" or intent_category == "data_presentation":
            if content_analysis["data_elements"] >= 3:
                recommendations.append(
                    LayoutRecommendation(
                        "Four Columns",
                        0.85,
                        "Multiple metrics benefit from structured grid presentation",
                        "KPI dashboards and performance metrics",
                    )
                )
            recommendations.append(
                LayoutRecommendation(
                    "Title and Content",
                    0.75,
                    "Traditional layout works well for data with explanatory text",
                    "metrics with context and analysis",
                )
            )

        elif content_type == "structured_list":
            if 3 <= distinct_elements <= 4:
                recommendations.append(
                    LayoutRecommendation(
                        "Four Columns",
                        0.88,
                        "List structure maps well to column-based presentation",
                        "feature lists and categorized information",
                    )
                )
            recommendations.append(
                LayoutRecommendation(
                    "Title and Content",
                    0.85,
                    "Classic bulleted list presentation",
                    "traditional content delivery with clear hierarchy",
                )
            )
            if distinct_elements == 2:
                recommendations.append(
                    LayoutRecommendation(
                        "Two Content",
                        0.80,
                        "Two main topics work well in side-by-side layout",
                        "dual-topic presentations",
                    )
                )

        elif content_type == "process_timeline":
            recommendations.append(
                LayoutRecommendation(
                    "Four Columns",
                    0.80,
                    "Process steps map well to sequential columns",
                    "step-by-step processes and timelines",
                )
            )
            recommendations.append(
                LayoutRecommendation(
                    "Title and Content",
                    0.75,
                    "Sequential list format for process explanation",
                    "detailed process documentation",
                )
            )

        else:  # narrative_text or general
            recommendations.append(
                LayoutRecommendation(
                    "Title and Content",
                    0.85,
                    "Standard layout ideal for narrative and explanatory content",
                    "general information and detailed explanations",
                )
            )
            if intent_category == "overview":
                recommendations.append(
                    LayoutRecommendation(
                        "Section Header",
                        0.70,
                        "High-level overview content works as section divider",
                        "topic introductions and agenda items",
                    )
                )

        # Add fallback recommendations if none were generated
        if not recommendations:
            recommendations.append(
                LayoutRecommendation(
                    "Title and Content",
                    0.70,
                    "Default layout suitable for most content types",
                    "general content presentation and information delivery",
                )
            )
            if content_analysis["has_comparison"]:
                recommendations.append(
                    LayoutRecommendation(
                        "Comparison",
                        0.65,
                        "Content contains comparison elements",
                        "side-by-side comparisons and contrasts",
                    )
                )

        # Sort by confidence score
        recommendations.sort(key=lambda x: x.confidence, reverse=True)

        # Return top 3 recommendations
        return recommendations[:3]

    def _generate_content_suggestions(
        self,
        content_analysis: Dict[str, Any],
        intent_analysis: Dict[str, Any],
        layout_recommendations: List[LayoutRecommendation],
    ) -> Dict[str, Any]:
        """Generate content structuring and presentation suggestions."""
        primary_layout = layout_recommendations[0] if layout_recommendations else None

        if not primary_layout:
            return {}

        # Generate suggestions based on recommended layout
        if primary_layout.layout == "Four Columns":
            return {
                "primary_message": "Structured comparison or categorized information",
                "supporting_details": [
                    "distinct categories",
                    "balanced content distribution",
                    "clear labels",
                ],
                "recommended_structure": "title + categorized columns with headers",
                "visual_approach": "balanced grid with consistent formatting",
            }
        elif primary_layout.layout == "Comparison":
            return {
                "primary_message": "Side-by-side comparison highlighting key differences",
                "supporting_details": [
                    "contrasting elements",
                    "clear distinctions",
                    "decision factors",
                ],
                "recommended_structure": "title + left vs right comparison",
                "visual_approach": "clear visual separation with balanced content",
            }
        elif primary_layout.layout == "Two Content":
            return {
                "primary_message": "Dual-topic presentation with equal emphasis",
                "supporting_details": [
                    "complementary topics",
                    "balanced detail level",
                    "related themes",
                ],
                "recommended_structure": "title + two main content areas",
                "visual_approach": "side-by-side layout with clear separation",
            }
        else:  # Title and Content or others
            return {
                "primary_message": "Structured information with clear hierarchy",
                "supporting_details": ["main points", "supporting details", "logical flow"],
                "recommended_structure": "title + bulleted or paragraph content",
                "visual_approach": "traditional layout with clear visual hierarchy",
            }

    def _generate_structured_frontmatter_preview(
        self,
        layout_recommendations: List[LayoutRecommendation],
        content_piece: str,
        message_intent: str,
    ) -> Dict[str, Any]:
        """Generate structured frontmatter preview using new direct field format."""
        if not layout_recommendations:
            return {}

        primary_layout = layout_recommendations[0].layout

        # Generate title from content or intent
        title = self._extract_title_from_content(content_piece, message_intent)

        # Use new direct field format for structured frontmatter
        if primary_layout == "Four Columns":
            return {
                "preferred_format": "Four Columns",
                "yaml_preview": f"""layout: Four Columns
title: {title}
content_col1: "Key information for first category"
content_col2: "Key information for second category"
content_col3: "Key information for third category"
content_col4: "Key information for fourth category" """,
                "structured_format": "direct_fields",
                "content_intelligence": "Enhanced with bullets, tables, and formatting support",
            }
        elif primary_layout == "Four Columns With Titles":
            return {
                "preferred_format": "Four Columns With Titles",
                "yaml_preview": f"""layout: Four Columns With Titles
title: {title}
title_col1: "Category 1"
content_col1: "Key information for first category"
title_col2: "Category 2"
content_col2: "Key information for second category"
title_col3: "Category 3"
content_col3: "Key information for third category"
title_col4: "Category 4"
content_col4: "Key information for fourth category" """,
                "structured_format": "direct_fields",
                "content_intelligence": "Enhanced with bullets, tables, and formatting support",
            }
        elif primary_layout == "Comparison":
            return {
                "preferred_format": "Comparison",
                "yaml_preview": f"""layout: Comparison
title: {title}
title_left: "Option A"
content_left: "Benefits and characteristics of first option"
title_right: "Option B"
content_right: "Benefits and characteristics of second option" """,
                "structured_format": "direct_fields",
                "content_intelligence": "Enhanced with bullets, tables, and formatting support",
            }
        elif primary_layout == "Two Content":
            return {
                "preferred_format": "Two Content",
                "yaml_preview": f"""layout: Two Content
title: {title}
content_left: |
  - Key points for left side
  - Supporting information
content_right: |
  - Key points for right side
  - Additional details """,
                "structured_format": "direct_fields",
                "content_intelligence": "Enhanced with bullets, tables, and formatting support",
            }
        elif primary_layout == "Three Columns":
            return {
                "preferred_format": "Three Columns",
                "yaml_preview": f"""layout: Three Columns
title: {title}
content_col1: "Content for first column"
content_col2: "Content for second column"
content_col3: "Content for third column" """,
                "structured_format": "direct_fields",
                "content_intelligence": "Enhanced with bullets, tables, and formatting support",
            }
        elif primary_layout == "Three Columns With Titles":
            return {
                "preferred_format": "Three Columns With Titles",
                "yaml_preview": f"""layout: Three Columns With Titles
title: {title}
title_col1: "Category 1"
content_col1: "Content for first column"
title_col2: "Category 2"
content_col2: "Content for second column"
title_col3: "Category 3"
content_col3: "Content for third column" """,
                "structured_format": "direct_fields",
                "content_intelligence": "Enhanced with bullets, tables, and formatting support",
            }
        elif primary_layout == "SWOT Analysis":
            return {
                "preferred_format": "SWOT Analysis",
                "yaml_preview": f"""layout: SWOT Analysis
title: {title}
content_top_left: "**Strengths**: Market position and capabilities"
content_top_right: "**Weaknesses**: Areas for improvement"
content_bottom_left: "**Opportunities**: Market and growth potential"
content_bottom_right: "**Threats**: External challenges and risks" """,
                "structured_format": "direct_fields",
                "content_intelligence": "Enhanced with bullets, tables, and formatting support",
            }
        else:
            return {
                "preferred_format": primary_layout,
                "yaml_preview": f"""layout: {primary_layout}
title: {title}
content: |
  - Key point from your content
  - Supporting information
  - Additional details""",
                "structured_format": "direct_fields",
                "content_intelligence": "Enhanced with bullets, tables, and formatting support",
            }

    def _count_distinct_elements(self, content: str) -> int:
        """Count distinct content elements that could map to separate layout areas."""
        # Look for bullet points, numbered lists, or natural separators
        bullet_count = len(re.findall(r"[-*•]\s+", content))
        number_list_count = len(re.findall(r"\d+\.\s+", content))
        paragraph_count = len([p for p in content.split("\n\n") if p.strip()])

        # Special handling for comparison content
        if any(word in content.lower() for word in ["vs", "versus", "compared to", "against"]):
            # For comparisons, assume at least 2 elements being compared
            return max(2, bullet_count, number_list_count, min(paragraph_count, 4))

        # For lists, count actual items
        if bullet_count > 0:
            return bullet_count
        elif number_list_count > 0:
            return number_list_count

        # Check for comma-separated lists (like "feature1, feature2, feature3, and feature4")
        comma_separated = [item.strip() for item in content.split(",") if item.strip()]
        if len(comma_separated) >= 3:
            return min(len(comma_separated), 4)

        # Check for colon-separated lists (like "feature1: description, feature2: description")
        colon_separated = len(re.findall(r"[^:]+:", content))
        if colon_separated >= 2:
            return min(colon_separated, 4)

        # For paragraph content, minimum of 1, maximum of 4
        return max(1, min(paragraph_count, 4))

    def _determine_structure_pattern(self, content: str) -> str:
        """Determine the structural pattern of the content."""
        if re.search(r"[-*•]\s+.*[-*•]\s+", content):
            return "bulleted_list"
        elif re.search(r"\d+\.\s+.*\d+\.\s+", content):
            return "numbered_list"
        elif content.count("\n\n") >= 2:
            return "paragraph_blocks"
        else:
            return "continuous_text"

    def _determine_visual_emphasis(self, content: str, content_type: str) -> str:
        """Determine what visual emphasis would work best."""
        if content_type == "comparison":
            return "balanced_comparison"
        elif content_type == "metrics_data":
            return "data_focused"
        elif content_type == "process_timeline":
            return "sequential_flow"
        else:
            return "content_hierarchy"

    def _determine_emphasis_level(self, message_intent: str) -> str:
        """Determine how much visual emphasis is needed."""
        intent_lower = message_intent.lower()
        if any(word in intent_lower for word in ["critical", "important", "key", "highlight"]):
            return "high"
        elif any(word in intent_lower for word in ["show", "present", "explain"]):
            return "medium"
        else:
            return "standard"

    def _determine_audience_focus(self, message_intent: str) -> str:
        """Determine audience consideration from intent."""
        intent_lower = message_intent.lower()
        if any(word in intent_lower for word in ["executive", "board", "leadership"]):
            return "executive"
        elif any(word in intent_lower for word in ["technical", "detail", "implementation"]):
            return "technical"
        else:
            return "general"

    def _determine_communication_goal(self, message_intent: str) -> str:
        """Determine the primary communication goal."""
        intent_lower = message_intent.lower()
        if any(word in intent_lower for word in ["decide", "choose", "recommend"]):
            return "decision_support"
        elif any(word in intent_lower for word in ["understand", "explain", "clarify"]):
            return "comprehension"
        elif any(word in intent_lower for word in ["convince", "persuade", "sell"]):
            return "persuasion"
        else:
            return "information_sharing"

    def _extract_title_from_content(self, content_piece: str, message_intent: str) -> str:
        """Extract or generate an appropriate title from content and intent."""
        # Try to extract from first line if it looks like a title
        first_line = content_piece.split("\n")[0].strip()
        if len(first_line) < 60 and not first_line.endswith("."):
            return first_line

        # Generate from message intent
        intent_words = message_intent.split()[:3]
        if intent_words:
            return " ".join(word.capitalize() for word in intent_words)

        # Fallback
        return "Content Overview"

    def _build_layout_intelligence(self) -> Dict[str, Any]:
        """Build the layout intelligence mapping for content-to-layout recommendations."""
        return {
            "comparison_layouts": ["Comparison", "Two Content", "Four Columns"],
            "data_layouts": ["Four Columns", "Title and Content"],
            "list_layouts": ["Title and Content", "Four Columns", "Two Content"],
            "process_layouts": ["Four Columns", "Title and Content", "Two Content"],
            "narrative_layouts": ["Title and Content", "Section Header"],
        }

    def _get_available_layouts(self) -> List[str]:
        """Get list of currently available PowerPoint layouts with enhanced structured frontmatter support."""
        return [
            "Title Slide",
            "Title and Content",
            "Section Header",
            "Two Content",
            "Comparison",
            "Title Only",
            "Blank",
            "Content with Caption",
            "Picture with Caption",
            "Title and Vertical Text",
            "Vertical Title and Text",
            "Three Columns With Titles",
            "Three Columns",
            "Four Columns With Titles",
            "Four Columns",
            "Agenda, 6 Textboxes",
            "Title and 6-item Lists",
            "Big Number",
            "SWOT Analysis",
        ]


# Helper function for easy import
def recommend_slide_approach(content_piece: str, message_intent: str, presentation_context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Convenience function for getting slide layout recommendations.

    Args:
        content_piece: Specific content to present
        message_intent: What they want this content to communicate
        presentation_context: Optional context from analyze_presentation_needs()

    Returns:
        Dictionary with layout recommendations and content suggestions
    """
    engine = LayoutRecommendationEngine()
    return engine.recommend_slide_approach(content_piece, message_intent, presentation_context)
