#!/usr/bin/env python3
"""
Content Template Matcher

This module provides intelligent content-to-template matching for optimal template selection.
Created to satisfy TDD test requirements, ready for Phase 2 enhancement.
"""

from typing import Dict, List, Any
import logging


class ContentTemplateMatcher:
    """Matches analyzed content to optimal templates with confidence scoring.

    This is a basic implementation to satisfy TDD test requirements.
    Ready for enhancement with advanced ML-style matching in Phase 2.
    """

    def __init__(self):
        """Initialize the content template matcher."""
        self.logger = logging.getLogger(__name__)

    def analyze_content_description(self, content_description: str) -> Dict[str, Any]:
        """Analyze content description to determine type and requirements.

        Args:
            content_description: Text description of presentation content

        Returns:
            Dictionary with content analysis results
        """
        # Enhanced implementation for TDD test compatibility
        content_lower = content_description.lower()

        # Enhanced content type detection
        content_type = "general_presentation"
        if any(word in content_lower for word in ["executive", "board", "quarterly", "strategic", "ceo"]):
            content_type = "executive_presentation"
        elif any(word in content_lower for word in ["training", "workshop", "tutorial", "instruction", "step-by-step"]):
            content_type = "training"
        elif any(word in content_lower for word in ["comparison", "versus", "vs", "compare", "features", "pricing"]):
            content_type = "comparison"
        elif any(word in content_lower for word in ["timeline", "schedule", "project", "milestone", "deliverable"]):
            content_type = "timeline"

        # Enhanced audience detection
        audience = "general"
        if any(word in content_lower for word in ["executive", "board", "ceo", "c-level"]):
            audience = "executive"
        elif any(word in content_lower for word in ["team", "internal", "staff", "responsibilities"]):
            audience = "team"
        elif any(
            word in content_lower
            for word in [
                "client",
                "customer",
                "business",
                "target",
                "sales",
                "regional",
                "performance",
            ]
        ):
            audience = "business"

        # Enhanced formality detection
        formality = "medium"
        if any(word in content_lower for word in ["formal", "professional", "executive", "strategic", "quarterly"]):
            formality = "high"
        elif any(word in content_lower for word in ["casual", "informal", "friendly"]):
            formality = "low"

        # Enhanced data detection
        data_heavy = any(
            word in content_lower
            for word in [
                "data",
                "metrics",
                "analysis",
                "financial",
                "numbers",
                "statistics",
                "performance",
                "pricing",
                "features",
            ]
        )

        # Enhanced structure detection
        structure = "general"
        if any(word in content_lower for word in ["comparison", "versus", "vs"]):
            structure = "comparative"
        elif any(word in content_lower for word in ["summary", "overview", "executive"]):
            structure = "summary_focused"
        elif any(word in content_lower for word in ["step", "sequence", "process", "instruction"]):
            structure = "sequential"
        elif any(word in content_lower for word in ["timeline", "chronological", "milestone"]):
            structure = "chronological"

        return {
            "content_type": content_type,
            "audience": audience,
            "formality": formality,
            "data_heavy": data_heavy,
            "structure": structure,
        }

    def match_content_to_templates(self, content_analysis: Dict[str, Any], available_templates: List[str]) -> List[Dict[str, Any]]:
        """Match analyzed content to optimal templates.

        Args:
            content_analysis: Results from analyze_content_description
            available_templates: List of available template names

        Returns:
            List of template matches with confidence scores and reasoning
        """
        # Basic implementation - ready for Phase 2 enhancement
        matches = []

        content_type = content_analysis.get("content_type", "general_presentation")
        audience = content_analysis.get("audience", "general")
        formality = content_analysis.get("formality", "medium")
        data_heavy = content_analysis.get("data_heavy", False)

        for template in available_templates:
            confidence = 0.6  # Base confidence
            reasoning = f"Template available for {content_type}"

            # Template-specific scoring
            if template == "default":
                confidence = 0.7
                reasoning = "Versatile template suitable for most presentation needs"

                if content_type in ["general_presentation", "training"]:
                    confidence = 0.8
                    reasoning = "Good match for general content with standard layouts"

            elif "business" in template.lower() or "pro" in template.lower():
                confidence = 0.65
                reasoning = "Professional template with advanced layouts"

                if content_type == "executive_presentation":
                    confidence = 0.95
                    reasoning = "Executive audience requires professional template with data support"
                elif audience == "executive":
                    confidence = 0.9
                    reasoning = "Executive-level template with professional layouts"
                elif formality == "high":
                    confidence = 0.85
                    reasoning = "Professional template matching formal presentation style"
                elif data_heavy:
                    confidence = 0.8
                    reasoning = "Advanced template with strong data visualization support"

            # Calculate fit score breakdown
            fit_score = {
                "audience_match": (1.0 if audience == "executive" and "business" in template else 0.8),
                "formality_match": 1.0 if formality == "high" and "pro" in template else 0.7,
                "feature_match": 0.9 if data_heavy and "pro" in template else 0.6,
            }

            matches.append(
                {
                    "template": template,
                    "confidence": confidence,
                    "reasoning": reasoning,
                    "fit_score": fit_score,
                }
            )

        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches
