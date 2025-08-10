#!/usr/bin/env python3
"""
Smart Template Recommendation System

This module implements intelligent template recommendations based on content analysis,
audience detection, and presentation requirements. It provides template-level
recommendations rather than just layout recommendations.

Key Features:
- Content analysis engine for automatic content type detection
- Template scoring algorithms with confidence metrics
- Multi-criteria optimization for audience and presentation requirements
- Integration with existing template metadata and validation systems
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from .metadata import TemplateMetadataLoader
from ..content.matcher import ContentTemplateMatcher
from .layout_analyzer import LayoutCapabilityAnalyzer


@dataclass
class TemplateRecommendation:
    """Single template recommendation with confidence scoring and reasoning."""

    template: str
    confidence: float
    reasoning: str
    fit_score: float
    audience_match: float
    formality_match: float
    feature_match: float
    content_type_match: float


@dataclass
class ContentAnalysis:
    """Content analysis results for recommendation generation."""

    content_type: str
    audience: str
    formality: str
    data_heavy: bool
    time_constraint: str
    decision_focused: bool


class SmartTemplateRecommendationSystem:
    """
    Intelligent template recommendation system with advanced content analysis.

    Provides template-level recommendations based on comprehensive content analysis,
    audience detection, and presentation requirements matching.
    """

    def __init__(self):
        """Initialize the recommendation system with required components."""
        self.logger = logging.getLogger(__name__)
        self.template_loader = TemplateMetadataLoader()
        self.content_matcher = ContentTemplateMatcher()
        self.layout_analyzer = LayoutCapabilityAnalyzer()

        # Template capability cache for performance
        self._template_capabilities_cache: Dict[str, Dict[str, Any]] = {}

        # Recommendation cache for performance
        self._recommendation_cache: Dict[str, List[TemplateRecommendation]] = {}

        self.logger.debug("SmartTemplateRecommendationSystem initialized")

    def analyze_content_requirements(self, content_description: str) -> ContentAnalysis:
        """
        Analyze content description to determine presentation requirements.

        Args:
            content_description: Description of presentation content and goals

        Returns:
            ContentAnalysis object with detected characteristics
        """
        description_lower = content_description.lower()

        # Detect content type
        content_type = self._detect_content_type(description_lower)

        # Detect audience
        audience = self._detect_audience(description_lower)

        # Detect formality level
        formality = self._detect_formality(description_lower)

        # Detect if data-heavy
        data_heavy = self._detect_data_heavy(description_lower)

        # Detect time constraints
        time_constraint = self._detect_time_constraint(description_lower)

        # Detect if decision-focused
        decision_focused = self._detect_decision_focused(description_lower)

        return ContentAnalysis(
            content_type=content_type,
            audience=audience,
            formality=formality,
            data_heavy=data_heavy,
            time_constraint=time_constraint,
            decision_focused=decision_focused,
        )

    def score_template_fit(
        self,
        template_name: str,
        content_analysis: ContentAnalysis,
        template_capabilities: Optional[Dict[str, Any]] = None,
    ) -> TemplateRecommendation:
        """
        Score how well a template fits the content requirements.

        Args:
            template_name: Name of template to score
            content_analysis: Analyzed content requirements
            template_capabilities: Optional template capability override

        Returns:
            TemplateRecommendation with detailed scoring breakdown
        """
        if template_capabilities is None:
            template_capabilities = self._get_template_capabilities(template_name)

        # Calculate individual scoring components
        audience_match = self._score_audience_match(content_analysis.audience, template_capabilities)
        formality_match = self._score_formality_match(content_analysis.formality, template_capabilities)
        feature_match = self._score_feature_match(content_analysis, template_capabilities)
        content_type_match = self._score_content_type_match(content_analysis.content_type, template_capabilities)

        # Calculate weighted total score
        total_score = audience_match * 0.3 + formality_match * 0.25 + feature_match * 0.25 + content_type_match * 0.2

        # Generate reasoning
        reasoning = self._generate_fit_reasoning(
            template_name,
            content_analysis,
            template_capabilities,
            audience_match,
            formality_match,
            feature_match,
            content_type_match,
        )

        return TemplateRecommendation(
            template=template_name,
            confidence=total_score,
            reasoning=reasoning,
            fit_score=total_score,
            audience_match=audience_match,
            formality_match=formality_match,
            feature_match=feature_match,
            content_type_match=content_type_match,
        )

    def recommend_templates(self, content_description: str, max_recommendations: int = 3) -> List[TemplateRecommendation]:
        """
        Generate ranked template recommendations for content.

        Args:
            content_description: Description of presentation content and goals
            max_recommendations: Maximum number of recommendations to return

        Returns:
            List of TemplateRecommendation objects ranked by confidence
        """
        # Check cache first
        cache_key = f"{content_description}_{max_recommendations}"
        if cache_key in self._recommendation_cache:
            return self._recommendation_cache[cache_key]

        # Analyze content requirements
        content_analysis = self.analyze_content_requirements(content_description)

        # Get available templates
        available_templates = self._get_available_templates()

        # Score all templates
        recommendations = []
        for template_name in available_templates:
            try:
                recommendation = self.score_template_fit(template_name, content_analysis)
                recommendations.append(recommendation)
            except Exception as e:
                self.logger.warning(f"Error scoring template {template_name}: {e}")
                continue

        # Sort by confidence and limit results
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        final_recommendations = recommendations[:max_recommendations]

        # Add fallback if no good recommendations
        if not final_recommendations or final_recommendations[0].confidence < 0.5:
            final_recommendations = self._add_fallback_recommendations(content_analysis, final_recommendations, max_recommendations)

        # Cache the results
        self._recommendation_cache[cache_key] = final_recommendations

        return final_recommendations

    def recommend_layouts_for_template(self, template_name: str, content_description: str, max_recommendations: int = 3) -> List[Dict[str, Any]]:
        """
        Recommend specific layouts within a template for given content.

        Args:
            template_name: Template to recommend layouts for
            content_description: Content description for layout matching
            max_recommendations: Maximum layouts to recommend

        Returns:
            List of layout recommendations with confidence and reasoning
        """
        try:
            # Get template metadata
            template_metadata = self.template_loader.load_template_metadata(template_name)

            # Analyze content requirements
            content_analysis = self.analyze_content_requirements(content_description)

            # Score layouts within template
            layout_recommendations = []
            for layout_name, layout_info in template_metadata.layouts.items():
                # Use layout analyzer to get capabilities
                layout_capabilities = self.layout_analyzer.analyze_layout_capabilities(layout_info.__dict__)

                # Generate confidence score based on content match
                confidence = self._score_layout_content_match(content_analysis, layout_capabilities)

                # Generate reasoning
                reasoning = self._generate_layout_reasoning(layout_name, content_analysis, layout_capabilities)

                layout_recommendations.append(
                    {
                        "layout": layout_name,
                        "confidence": confidence,
                        "reasoning": reasoning,
                        "capabilities": layout_capabilities,
                    }
                )

            # Sort and limit results
            layout_recommendations.sort(key=lambda x: x["confidence"], reverse=True)
            return layout_recommendations[:max_recommendations]

        except Exception as e:
            self.logger.error(f"Error recommending layouts for template {template_name}: {e}")
            return []

    def validate_recommendation_quality(self, recommendations: List[TemplateRecommendation]) -> Dict[str, Any]:
        """
        Validate the quality of generated recommendations.

        Args:
            recommendations: List of template recommendations to validate

        Returns:
            Dictionary with quality metrics and validation results
        """
        if not recommendations:
            return {
                "quality_score": 0.0,
                "issues": ["No recommendations generated"],
                "confidence_range": (0.0, 0.0),
                "reasoning_quality": "poor",
            }

        # Calculate quality metrics
        confidences = [rec.confidence for rec in recommendations]
        max_confidence = max(confidences)
        min_confidence = min(confidences)
        avg_confidence = sum(confidences) / len(confidences)

        # Check for quality issues
        issues = []
        if max_confidence < 0.6:
            issues.append("Low maximum confidence score")
        if max_confidence - min_confidence < 0.1:
            issues.append("Poor recommendation differentiation")
        if len({rec.template for rec in recommendations}) != len(recommendations):
            issues.append("Duplicate template recommendations")

        # Assess reasoning quality
        reasoning_lengths = [len(rec.reasoning) for rec in recommendations]
        avg_reasoning_length = sum(reasoning_lengths) / len(reasoning_lengths)

        if avg_reasoning_length < 50:
            reasoning_quality = "poor"
        elif avg_reasoning_length < 100:
            reasoning_quality = "adequate"
        else:
            reasoning_quality = "good"

        # Calculate overall quality score
        quality_score = min(1.0, (avg_confidence + (max_confidence - min_confidence)) / 2)

        return {
            "quality_score": quality_score,
            "issues": issues,
            "confidence_range": (min_confidence, max_confidence),
            "reasoning_quality": reasoning_quality,
            "recommendation_count": len(recommendations),
            "avg_confidence": avg_confidence,
        }

    def clear_caches(self) -> None:
        """Clear all internal caches."""
        self._template_capabilities_cache.clear()
        self._recommendation_cache.clear()
        self.logger.debug("Recommendation system caches cleared")

    def _detect_content_type(self, description_lower: str) -> str:
        """Detect the type of content from description."""
        if any(word in description_lower for word in ["executive", "board", "c-level", "leadership"]):
            return "executive_presentation"
        elif any(word in description_lower for word in ["training", "workshop", "tutorial", "learn"]):
            return "training"
        elif any(word in description_lower for word in ["sales", "pitch", "proposal", "demo"]):
            return "sales_presentation"
        elif any(word in description_lower for word in ["research", "analysis", "findings", "study"]):
            return "research_presentation"
        elif any(word in description_lower for word in ["project", "status", "update", "progress"]):
            return "project_update"
        else:
            return "general_presentation"

    def _detect_audience(self, description_lower: str) -> str:
        """Detect target audience from description."""
        if any(word in description_lower for word in ["executive", "board", "director", "c-level", "leadership"]):
            return "executive"
        elif any(word in description_lower for word in ["technical", "engineer", "developer", "implementation"]):
            return "technical"
        elif any(word in description_lower for word in ["client", "customer", "external", "stakeholder"]):
            return "external"
        elif any(word in description_lower for word in ["team", "internal", "employee", "staff"]):
            return "internal"
        elif any(word in description_lower for word in ["student", "trainee", "learner", "new"]):
            return "learners"
        else:
            return "general"

    def _detect_formality(self, description_lower: str) -> str:
        """Detect formality level from description."""
        if any(word in description_lower for word in ["board", "formal", "official", "corporate"]):
            return "very_high"
        elif any(word in description_lower for word in ["business", "professional", "presentation"]):
            return "high"
        elif any(word in description_lower for word in ["team", "meeting", "update", "review"]):
            return "medium"
        else:
            return "low"

    def _detect_data_heavy(self, description_lower: str) -> bool:
        """Detect if presentation is data-heavy."""
        data_indicators = [
            "metrics",
            "data",
            "analytics",
            "numbers",
            "statistics",
            "performance",
            "kpi",
            "dashboard",
            "financial",
            "revenue",
            "quarterly",
            "analysis",
            "report",
            "findings",
        ]
        return any(word in description_lower for word in data_indicators)

    def _detect_time_constraint(self, description_lower: str) -> str:
        """Detect time constraints from description."""
        if any(word in description_lower for word in ["quick", "brief", "short", "summary"]):
            return "short"
        elif any(word in description_lower for word in ["detailed", "comprehensive", "thorough", "complete"]):
            return "long"
        else:
            return "medium"

    def _detect_decision_focused(self, description_lower: str) -> bool:
        """Detect if presentation is decision-focused."""
        decision_indicators = [
            "decision",
            "choose",
            "recommend",
            "approval",
            "vote",
            "select",
            "approve",
            "strategy",
            "direction",
            "plan",
            "strategic",
            "initiative",
            "board",
            "review",
            "proposal",
        ]
        return any(word in description_lower for word in decision_indicators)

    def _get_template_capabilities(self, template_name: str) -> Dict[str, Any]:
        """Get template capabilities with caching."""
        if template_name in self._template_capabilities_cache:
            return self._template_capabilities_cache[template_name]

        # Define template capabilities (this would typically come from metadata)
        capabilities = self._build_template_capabilities(template_name)
        self._template_capabilities_cache[template_name] = capabilities
        return capabilities

    def _build_template_capabilities(self, template_name: str) -> Dict[str, Any]:
        """Build template capabilities definition."""
        # Default capabilities
        capabilities = {
            "target_audience": ["general"],
            "formality_level": "medium",
            "data_visualization": False,
            "professional_styling": True,
            "content_types": ["general_presentation"],
        }

        # Template-specific capabilities
        if template_name == "executive_pro":
            capabilities.update(
                {
                    "target_audience": ["executive", "c_level"],
                    "formality_level": "very_high",
                    "data_visualization": True,
                    "professional_styling": True,
                    "content_types": ["executive_presentation", "business_review"],
                }
            )
        elif template_name == "business_pro":
            capabilities.update(
                {
                    "target_audience": ["business", "professional"],
                    "formality_level": "high",
                    "data_visualization": True,
                    "professional_styling": True,
                    "content_types": ["business_presentation", "sales_presentation"],
                }
            )
        elif template_name == "default":
            capabilities.update(
                {
                    "target_audience": ["general", "business"],
                    "formality_level": "medium",
                    "data_visualization": False,
                    "professional_styling": True,
                    "content_types": ["general_presentation", "training"],
                }
            )

        return capabilities

    def _score_audience_match(self, detected_audience: str, template_capabilities: Dict[str, Any]) -> float:
        """Score audience match between content and template."""
        target_audiences = template_capabilities.get("target_audience", ["general"])

        if detected_audience in target_audiences:
            return 1.0
        elif detected_audience == "executive" and "business" in target_audiences:
            return 0.8
        elif detected_audience == "business" and "general" in target_audiences:
            return 0.7
        elif "general" in target_audiences:
            return 0.6
        else:
            return 0.3

    def _score_formality_match(self, detected_formality: str, template_capabilities: Dict[str, Any]) -> float:
        """Score formality match between content and template."""
        template_formality = template_capabilities.get("formality_level", "medium")

        formality_scores = {
            ("very_high", "very_high"): 1.0,
            ("very_high", "high"): 0.8,
            ("high", "very_high"): 0.9,
            ("high", "high"): 1.0,
            ("high", "medium"): 0.7,
            ("medium", "high"): 0.8,
            ("medium", "medium"): 1.0,
            ("medium", "low"): 0.6,
            ("low", "medium"): 0.7,
            ("low", "low"): 1.0,
        }

        return formality_scores.get((detected_formality, template_formality), 0.5)

    def _score_feature_match(self, content_analysis: ContentAnalysis, template_capabilities: Dict[str, Any]) -> float:
        """Score feature match between content requirements and template capabilities."""
        score = 0.0

        # Data visualization capability
        if content_analysis.data_heavy:
            if template_capabilities.get("data_visualization", False):
                score += 0.4
            else:
                score += 0.1  # Penalty for missing required feature
        else:
            score += 0.3  # No special requirements

        # Professional styling (always beneficial)
        if template_capabilities.get("professional_styling", False):
            score += 0.3

        # Decision focus support
        if content_analysis.decision_focused:
            if template_capabilities.get("decision_support", False):
                score += 0.3
            else:
                score += 0.2
        else:
            score += 0.3

        return min(1.0, score)

    def _score_content_type_match(self, detected_content_type: str, template_capabilities: Dict[str, Any]) -> float:
        """Score content type match between detected type and template support."""
        supported_types = template_capabilities.get("content_types", ["general_presentation"])

        if detected_content_type in supported_types:
            return 1.0
        elif "general_presentation" in supported_types:
            return 0.7
        else:
            return 0.4

    def _generate_fit_reasoning(
        self,
        template_name: str,
        content_analysis: ContentAnalysis,
        template_capabilities: Dict[str, Any],
        audience_match: float,
        formality_match: float,
        feature_match: float,
        content_type_match: float,
    ) -> str:
        """Generate human-readable reasoning for template fit score."""
        reasons = []

        # Audience reasoning
        if audience_match >= 0.9:
            reasons.append(f"Perfect audience match for {content_analysis.audience} presentations")
        elif audience_match >= 0.7:
            reasons.append(f"Good audience compatibility for {content_analysis.audience} content")
        else:
            reasons.append(f"Limited audience match for {content_analysis.audience} requirements")

        # Formality reasoning
        template_formality = template_capabilities.get("formality_level", "medium")
        if formality_match >= 0.9:
            reasons.append(f"Formality level ({template_formality}) matches content requirements")
        elif formality_match >= 0.7:
            reasons.append(f"Acceptable formality level for {content_analysis.formality} content")

        # Feature reasoning
        if content_analysis.data_heavy and template_capabilities.get("data_visualization", False):
            reasons.append("Excellent data visualization support for metrics-heavy content")
        elif content_analysis.data_heavy:
            reasons.append("Limited data visualization capabilities for data-heavy content")

        # Content type reasoning
        if content_type_match >= 0.9:
            reasons.append(f"Specialized support for {content_analysis.content_type}")

        return ". ".join(reasons)

    def _score_layout_content_match(self, content_analysis: ContentAnalysis, layout_capabilities: Dict[str, Any]) -> float:
        """Score how well a layout matches content requirements."""
        score = 0.0

        # Content type matching
        if content_analysis.content_type == "comparison" and "comparison" in layout_capabilities.get("best_for", []):
            score += 0.4
        elif content_analysis.data_heavy and "metrics" in layout_capabilities.get("best_for", []):
            score += 0.4
        else:
            score += 0.2

        # Complexity matching
        layout_complexity = layout_capabilities.get("complexity", "medium")
        if content_analysis.time_constraint == "short" and layout_complexity == "simple":
            score += 0.3
        elif content_analysis.time_constraint == "long" and layout_complexity == "complex":
            score += 0.3
        else:
            score += 0.2

        # Visual support
        if content_analysis.data_heavy and layout_capabilities.get("supports_tables", False):
            score += 0.3
        else:
            score += 0.2

        return min(1.0, score)

    def _generate_layout_reasoning(
        self,
        layout_name: str,
        content_analysis: ContentAnalysis,
        layout_capabilities: Dict[str, Any],
    ) -> str:
        """Generate reasoning for layout recommendation."""
        reasons = []

        best_for = layout_capabilities.get("best_for", [])
        if best_for:
            reasons.append(f"Optimized for {', '.join(best_for[:2])}")

        if content_analysis.data_heavy and layout_capabilities.get("supports_tables", False):
            reasons.append("Excellent table and data visualization support")

        complexity = layout_capabilities.get("complexity", "medium")
        if content_analysis.time_constraint == "short" and complexity == "simple":
            reasons.append("Simple layout suitable for time-constrained presentations")

        return ". ".join(reasons) if reasons else f"Standard {layout_name} layout"

    def _get_available_templates(self) -> List[str]:
        """Get list of available templates."""
        try:
            template_data = self.template_loader.get_all_available_templates()
            if isinstance(template_data, dict) and "templates" in template_data:
                return list(template_data["templates"].keys())
            elif isinstance(template_data, list):
                return template_data
            else:
                return ["default", "business_pro", "executive_pro"]
        except Exception:
            # Fallback to common templates
            return ["default", "business_pro", "executive_pro"]

    def _add_fallback_recommendations(
        self,
        content_analysis: ContentAnalysis,
        existing_recommendations: List[TemplateRecommendation],
        max_recommendations: int,
    ) -> List[TemplateRecommendation]:
        """Add fallback recommendations if primary recommendations are insufficient."""
        fallback_recommendations = existing_recommendations.copy()

        # Always include default template as fallback
        if not any(rec.template == "default" for rec in fallback_recommendations):
            default_rec = TemplateRecommendation(
                template="default",
                confidence=0.6,
                reasoning="Default template suitable for most content types with general audience",
                fit_score=0.6,
                audience_match=0.7,
                formality_match=0.6,
                feature_match=0.5,
                content_type_match=0.7,
            )
            fallback_recommendations.append(default_rec)

        # Sort again and limit
        fallback_recommendations.sort(key=lambda x: x.confidence, reverse=True)
        return fallback_recommendations[:max_recommendations]
