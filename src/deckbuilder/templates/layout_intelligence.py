#!/usr/bin/env python3
"""
Layout Intelligence Engine for Content-First Presentation Generation

Provides intelligent layout recommendations based on content analysis using
semantic metadata and convention-based placeholder names.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class LayoutRecommendation:
    """Layout recommendation with confidence score and reasoning"""

    layout_name: str
    confidence: float
    reasoning: List[str]
    placeholder_mapping: Dict[str, str]
    optimization_hints: List[str]


@dataclass
class ContentAnalysis:
    """Content analysis results"""

    intent: str
    content_type: str
    structure_indicators: List[str]
    keywords_found: List[str]
    content_blocks: int
    has_images: bool
    has_numbers: bool


class LayoutIntelligence:
    """
    Content-first layout intelligence engine that analyzes content and
    recommends optimal layouts with confidence scoring.
    """

    def __init__(self, intelligence_file: Optional[str] = None):
        """
        Initialize layout intelligence engine.

        Args:
            intelligence_file: Path to layout_intelligence.json file
        """
        if intelligence_file is None:
            # Default to src/layout_intelligence.json relative to this file
            current_dir = Path(__file__).parent.parent
            intelligence_file = str(current_dir / "layout_intelligence.json")

        self.intelligence_file = intelligence_file
        self.intelligence_data = self._load_intelligence_data()

    def _load_intelligence_data(self) -> Dict:
        """Load layout intelligence metadata"""
        try:
            with open(self.intelligence_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Layout intelligence file not found: {self.intelligence_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in intelligence file: {e}")

    def analyze_content(self, content: str) -> ContentAnalysis:
        """
        Analyze content to extract semantic information for layout recommendations.

        Args:
            content: Raw markdown content to analyze

        Returns:
            ContentAnalysis with detected patterns and characteristics
        """
        content_lower = content.lower()

        # Detect intent patterns
        intent = self._detect_intent(content_lower)

        # Detect content type
        content_type = self._detect_content_type(content_lower)

        # Analyze structure
        structure_indicators = self._analyze_structure(content)

        # Find relevant keywords
        keywords_found = self._find_keywords(content_lower)

        # Count content characteristics
        content_blocks = self._count_content_blocks(content)
        has_images = self._has_image_content(content_lower)
        has_numbers = self._has_numeric_content(content_lower)

        return ContentAnalysis(
            intent=intent,
            content_type=content_type,
            structure_indicators=structure_indicators,
            keywords_found=keywords_found,
            content_blocks=content_blocks,
            has_images=has_images,
            has_numbers=has_numbers,
        )

    def recommend_layouts(self, content: str, max_recommendations: int = 3) -> List[LayoutRecommendation]:
        """
        Recommend optimal layouts based on content analysis.

        Args:
            content: Content to analyze
            max_recommendations: Maximum number of recommendations to return

        Returns:
            List of LayoutRecommendation objects sorted by confidence
        """
        analysis = self.analyze_content(content)
        recommendations = []

        # Get layout compatibility data
        layout_compatibility = self.intelligence_data.get("layout_compatibility", {})
        content_patterns = self.intelligence_data.get("content_patterns", {})
        scoring_weights = self.intelligence_data.get("recommendation_engine", {}).get("scoring_weights", {})

        # Score each layout
        for layout_name, layout_info in layout_compatibility.items():
            confidence, reasoning = self._score_layout(analysis, layout_name, layout_info, content_patterns, scoring_weights)

            if confidence >= self.intelligence_data.get("recommendation_engine", {}).get("minimum_confidence", 0.6):
                placeholder_mapping = self._generate_placeholder_mapping(analysis, layout_info)
                optimization_hints = self._get_optimization_hints(layout_name, analysis)

                recommendations.append(
                    LayoutRecommendation(
                        layout_name=layout_name,
                        confidence=confidence,
                        reasoning=reasoning,
                        placeholder_mapping=placeholder_mapping,
                        optimization_hints=optimization_hints,
                    )
                )

        # Sort by confidence and return top recommendations
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        return recommendations[:max_recommendations]

    def _detect_intent(self, content_lower: str) -> str:
        """Detect primary intent from content"""
        intent_patterns = self.intelligence_data.get("content_patterns", {}).get("intent_recognition", {})

        best_intent = "overview"
        best_score = 0

        for intent, pattern_info in intent_patterns.items():
            score = 0
            keywords = pattern_info.get("keywords", [])

            for keyword in keywords:
                if keyword in content_lower:
                    score += 1

            # Normalize score by number of keywords
            if keywords:
                score = score / len(keywords)

            if score > best_score:
                best_score = score
                best_intent = intent

        return best_intent

    def _detect_content_type(self, content_lower: str) -> str:
        """Detect primary content type"""
        # Simple heuristics for content type detection
        if any(word in content_lower for word in ["image", "picture", "photo", "diagram"]):
            return "image_content"
        elif any(word in content_lower for word in ["vs", "versus", "compare", "option"]):
            return "comparison_content"
        elif re.search(r"\d+[%]|\d+\.\d+", content_lower):
            return "statistics"
        elif any(word in content_lower for word in ["step", "agenda", "process"]):
            return "agenda_content"
        elif len(re.findall(r"^#{1,3}\s", content_lower, re.MULTILINE)) >= 3:
            return "column_content"
        else:
            return "body_content"

    def _analyze_structure(self, content: str) -> List[str]:
        """Analyze content structure indicators"""
        indicators = []

        # Count headings
        heading_count = len(re.findall(r"^#{1,6}\s", content, re.MULTILINE))
        if heading_count >= 4:
            indicators.append("multiple_columns")
        elif heading_count == 2:
            indicators.append("paired_content")

        # Check for lists
        if re.search(r"^\s*[-*+]\s", content, re.MULTILINE):
            indicators.append("bullet_list")
        if re.search(r"^\s*\d+\.\s", content, re.MULTILINE):
            indicators.append("numbered_list")

        # Check for structured frontmatter
        if content.strip().startswith("---"):
            indicators.append("structured_frontmatter")

        # Check for tables
        if "|" in content and re.search(r"\|.*\|.*\|", content):
            indicators.append("table_content")

        return indicators

    def _find_keywords(self, content_lower: str) -> List[str]:
        """Find relevant keywords in content"""
        found_keywords = []
        intent_patterns = self.intelligence_data.get("content_patterns", {}).get("intent_recognition", {})

        for _intent, pattern_info in intent_patterns.items():
            keywords = pattern_info.get("keywords", [])
            for keyword in keywords:
                if keyword in content_lower:
                    found_keywords.append(keyword)

        return list(set(found_keywords))  # Remove duplicates

    def _count_content_blocks(self, content: str) -> int:
        """Count distinct content blocks"""
        # Count major sections (headings + paragraphs)
        headings = len(re.findall(r"^#{1,6}\s", content, re.MULTILINE))
        paragraphs = len([p for p in content.split("\n\n") if p.strip() and not p.strip().startswith("#")])
        return max(headings, paragraphs // 2)  # Estimate content blocks

    def _has_image_content(self, content_lower: str) -> bool:
        """Check if content references images"""
        image_indicators = ["image", "picture", "photo", "diagram", "visual", "media"]
        return any(indicator in content_lower for indicator in image_indicators)

    def _has_numeric_content(self, content_lower: str) -> bool:
        """Check if content has significant numeric data"""
        return bool(re.search(r"\d+[%]|\$\d+|\d+\.\d+|^\d+$", content_lower, re.MULTILINE))

    def _score_layout(
        self,
        analysis: ContentAnalysis,
        layout_name: str,
        layout_info: Dict,
        content_patterns: Dict,
        scoring_weights: Dict,
    ) -> Tuple[float, List[str]]:
        """Score a layout's compatibility with analyzed content"""
        score = 0.0
        reasoning = []

        # Content structure scoring
        optimal_for = layout_info.get("optimal_for", [])
        structure_match = any(indicator in analysis.structure_indicators for indicator in optimal_for)
        if structure_match:
            score += scoring_weights.get("content_structure", 0.4)
            reasoning.append(f"Content structure matches {layout_name} purpose")

        # Keyword matching scoring
        confidence_factors = layout_info.get("confidence_factors", {})
        for factor, weight in confidence_factors.items():
            if factor in analysis.keywords_found or factor in analysis.structure_indicators:
                score += scoring_weights.get("keyword_matching", 0.3) * weight
                reasoning.append(f"Found {factor} indicator")

        # Intent recognition scoring
        intent_patterns = content_patterns.get("intent_recognition", {})
        if analysis.intent in intent_patterns:
            intent_layouts = intent_patterns[analysis.intent].get("layouts", [])
            if layout_name in intent_layouts:
                score += scoring_weights.get("intent_recognition", 0.2)
                reasoning.append(f"Layout matches {analysis.intent} intent")

        # Layout compatibility scoring
        if analysis.content_blocks == 4 and "Four Columns" in layout_name:
            score += scoring_weights.get("layout_compatibility", 0.1)
            reasoning.append("Content blocks match four-column structure")
        elif analysis.content_blocks == 3 and "Three Columns" in layout_name:
            score += scoring_weights.get("layout_compatibility", 0.1)
            reasoning.append("Content blocks match three-column structure")
        elif analysis.has_images and "Picture" in layout_name:
            score += scoring_weights.get("layout_compatibility", 0.1)
            reasoning.append("Image content matches picture layout")

        return min(score, 1.0), reasoning

    def _generate_placeholder_mapping(self, analysis: ContentAnalysis, layout_info: Dict) -> Dict[str, str]:
        """Generate placeholder mapping suggestions"""
        mapping = {}
        placeholders = layout_info.get("placeholders", {})
        content_hints = layout_info.get("content_hints", {})

        for placeholder_type in ["required", "optional"]:
            if placeholder_type in placeholders:
                for placeholder in placeholders[placeholder_type]:
                    if placeholder in content_hints:
                        mapping[placeholder] = content_hints[placeholder]
                    else:
                        mapping[placeholder] = f"Content for {placeholder}"

        return mapping

    def _get_optimization_hints(self, layout_name: str, analysis: ContentAnalysis) -> List[str]:
        """Get optimization hints for the layout"""
        hints = []
        optimization_data = self.intelligence_data.get("optimization_hints", {})

        # General content length hints
        content_length = optimization_data.get("content_length", {})
        for _placeholder, hint in content_length.items():
            hints.append(hint)

        # Layout-specific hints
        layout_specific = optimization_data.get("layout_specific", {})
        if layout_name in layout_specific:
            hints.append(layout_specific[layout_name])

        # Analysis-based hints
        if analysis.has_images:
            hints.append("Consider using high-quality images with proper aspect ratios")

        if analysis.has_numbers:
            hints.append("Use consistent number formatting and consider highlighting key metrics")

        return hints[:3]  # Limit to top 3 hints


def test_layout_intelligence():
    """Test the layout intelligence system"""
    engine = LayoutIntelligence()

    test_content = """
    # Feature Comparison: Our Platform vs Competition

    ## Performance
    Our platform delivers **fast processing** with optimized algorithms

    ## Security
    ***Enterprise-grade*** encryption with SOC2 compliance

    ## Usability
    *Intuitive* interface with minimal learning curve
    ## Cost
    Transparent pricing with flexible plans
    """

    print("Testing Layout Intelligence Engine")
    print("=" * 50)

    # Analyze content
    analysis = engine.analyze_content(test_content)
    print("Content Analysis:")
    print(f"  Intent: {analysis.intent}")
    print(f"  Content Type: {analysis.content_type}")
    print(f"  Structure: {analysis.structure_indicators}")
    print(f"  Keywords: {analysis.keywords_found}")
    print(f"  Content Blocks: {analysis.content_blocks}")

    # Get recommendations
    recommendations = engine.recommend_layouts(test_content)
    print("\nLayout Recommendations:")

    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.layout_name} (Confidence: {rec.confidence:.2f})")
        print(f"   Reasoning: {'; '.join(rec.reasoning)}")
        print(f"   Key Placeholders: {list(rec.placeholder_mapping.keys())[:3]}")
        if rec.optimization_hints:
            print(f"   Hint: {rec.optimization_hints[0]}")


if __name__ == "__main__":
    test_layout_intelligence()
