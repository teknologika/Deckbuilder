"""
Content Analysis Module for Deck Builder MCP

This module implements content-first presentation intelligence, analyzing user input
to understand communication goals and recommend presentation structure.

Design Philosophy: Start with "what does the user want to communicate?"
not "what layouts exist?"
"""

import re
from typing import Any, Dict, List


class ContentAnalyzer:
    """
    Analyzes user presentation needs using content-first approach.
    Acts as intelligent presentation consultant, not layout picker.
    """

    def __init__(self):
        """Initialize the content analyzer with audience profiles."""
        self.audience_profiles = {
            "board": {
                "expertise_level": "expert",
                "attention_span": "short",
                "decision_authority": "decision-maker",
                "preferred_format": "high-level",
            },
            "team": {
                "expertise_level": "intermediate",
                "attention_span": "medium",
                "decision_authority": "implementer",
                "preferred_format": "detailed",
            },
            "customers": {
                "expertise_level": "general",
                "attention_span": "medium",
                "decision_authority": "decision-maker",
                "preferred_format": "visual-heavy",
            },
            "technical": {
                "expertise_level": "expert",
                "attention_span": "extended",
                "decision_authority": "influencer",
                "preferred_format": "detailed",
            },
            "general": {
                "expertise_level": "intermediate",
                "attention_span": "medium",
                "decision_authority": "influencer",
                "preferred_format": "balanced",
            },
        }

    def analyze_presentation_needs(
        self,
        user_input: str,
        audience: str = "general",
        constraints: str = None,
        presentation_goal: str = "inform",
    ) -> Dict[str, Any]:
        """
        Analyze user's presentation needs and recommend structure.

        Args:
            user_input: Raw description of what they want to present
            audience: Target audience type
            constraints: Time/slide constraints
            presentation_goal: Primary goal of presentation

        Returns:
            Dictionary with content analysis and structural recommendations
        """
        # Content Analysis
        key_messages = self._extract_key_messages(user_input)
        narrative_arc = self._determine_narrative_arc(user_input, key_messages)
        complexity_level = self._assess_complexity_level(user_input, audience)
        data_density = self._analyze_data_density(user_input)
        emotional_tone = self._detect_emotional_tone(user_input, key_messages)

        # Audience Considerations
        audience_analysis = self._analyze_audience(audience, constraints)

        # Recommended Structure
        recommended_structure = self._build_recommended_structure(key_messages, narrative_arc, audience_analysis, presentation_goal)

        # Presentation Strategy
        presentation_strategy = self._develop_presentation_strategy(narrative_arc, audience_analysis, presentation_goal)

        return {
            "content_analysis": {
                "key_messages": key_messages,
                "narrative_arc": narrative_arc,
                "complexity_level": complexity_level,
                "data_density": data_density,
                "emotional_tone": emotional_tone,
            },
            "audience_considerations": audience_analysis,
            "recommended_structure": recommended_structure,
            "presentation_strategy": presentation_strategy,
        }

    def _extract_key_messages(self, user_input: str) -> List[str]:
        """Extract key messages from user input using pattern matching."""
        # Look for metrics, percentages, numbers
        metrics = re.findall(
            r"\d+%\s*\w*|\$[\d,]+|\d+[\w\s]*(?:growth|increase|decrease|revenue|users|customers)",
            user_input.lower(),
        )

        # Look for key topics/concepts
        topics = []
        if re.search(r"growth|expand|increase|up", user_input.lower()):
            topics.append("growth/expansion")
        if re.search(r"churn|loss|decrease|down|problem|issue|challenge", user_input.lower()):
            topics.append("challenges/concerns")
        if re.search(r"strategy|plan|solution|fix|improve", user_input.lower()):
            topics.append("solutions/strategy")
        if re.search(r"new|launch|feature|product", user_input.lower()):
            topics.append("new initiatives")
        if re.search(r"market|competitor|industry", user_input.lower()):
            topics.append("market/competitive")

        # Combine metrics and topics
        key_messages = []
        if metrics:
            key_messages.extend([f"metric: {m}" for m in metrics[:3]])  # Limit to top 3
        key_messages.extend(topics)

        return key_messages[:5]  # Limit to 5 key messages

    def _determine_narrative_arc(self, user_input: str, _key_messages: List[str]) -> str:
        """Determine the narrative structure from content."""
        import re

        input_lower = user_input.lower()

        # Use word boundary matching to avoid false positives
        def has_word_pattern(patterns, text):
            """Check if any pattern exists as whole words in text."""
            for pattern in patterns:
                if re.search(r"\b" + re.escape(pattern) + r"\b", text):
                    return True
            return False

        # Check for success-challenge-solution pattern with word boundaries
        success_patterns = [
            "growth",
            "success",
            "increase",
            "expand",
            "win",
            "achievement",
            "improvement",
            "grew",
            "expanded",
            "gains",
            "positive",
        ]
        challenge_patterns = [
            "but",
            "however",
            "problem",
            "issue",
            "churn",
            "decrease",
            "challenge",
            "concern",
            "difficulty",
            "bottleneck",
            "drops",
            "causing",
        ]
        solution_patterns = [
            "strategy",
            "plan",
            "solution",
            "address",
            "fix",
            "propose",
            "recommend",
            "implement",
            "adding",
            "need",
        ]

        has_success = has_word_pattern(success_patterns, input_lower) or re.search(r"\d+%", input_lower)
        has_challenge = has_word_pattern(challenge_patterns, input_lower)
        has_solution = has_word_pattern(solution_patterns, input_lower)

        if has_success and has_challenge and has_solution:
            return "success-challenge-solution"
        elif has_challenge and has_solution:
            return "problem-solution"
        elif has_word_pattern(["compare", "vs", "versus", "option", "alternative"], input_lower):
            return "compare-contrast"
        elif has_word_pattern(["convince", "persuade", "recommend", "should"], input_lower):
            return "persuasive"
        else:
            return "informational"

    def _assess_complexity_level(self, user_input: str, audience: str) -> str:
        """Assess the complexity level needed."""
        if audience in ["board", "executive"]:
            return "executive"
        elif audience == "technical":
            return "technical"
        elif len(user_input.split()) > 50 or "detail" in user_input.lower():
            return "detailed"
        else:
            return "overview"

    def _analyze_data_density(self, user_input: str) -> str:
        """Analyze how data-heavy the presentation should be."""
        # Count numeric mentions
        numeric_mentions = len(re.findall(r"\d+", user_input))

        if numeric_mentions >= 5 or any(word in user_input.lower() for word in ["data", "metrics", "numbers", "statistics"]):
            return "metrics-heavy"
        elif any(word in user_input.lower() for word in ["story", "example", "case", "experience"]):
            return "story-driven"
        else:
            return "balanced"

    def _detect_emotional_tone(self, user_input: str, _key_messages: List[str]) -> str:
        """Detect the emotional tone of the content."""
        input_lower = user_input.lower()

        if any(word in input_lower for word in ["urgent", "critical", "immediate", "crisis"]):
            return "urgent"
        elif any(word in input_lower for word in ["concern", "worry", "issue", "problem", "challenge"]):
            return "cautious"
        elif any(word in input_lower for word in ["success", "growth", "achievement", "win"]):
            return "positive"
        else:
            return "neutral"

    def _analyze_audience(self, audience: str, constraints: str) -> Dict[str, str]:
        """Analyze audience characteristics and constraints."""
        profile = self.audience_profiles.get(audience, self.audience_profiles["general"]).copy()

        # Adjust based on constraints
        if constraints:
            if "minutes" in constraints.lower() and any(time in constraints for time in ["5", "10"]):
                profile["attention_span"] = "short"
            elif "slides" in constraints.lower():
                profile["preferred_format"] = "high-level"

        return profile

    def _build_recommended_structure(
        self,
        _key_messages: List[str],
        narrative_arc: str,
        _audience_analysis: Dict[str, str],
        _presentation_goal: str,
    ) -> List[Dict[str, str]]:
        """Build recommended slide structure."""
        structure = []

        if narrative_arc == "success-challenge-solution":
            structure = [
                {
                    "position": 1,
                    "purpose": "lead with strength",
                    "content_focus": "positive metrics/achievements",
                    "slide_intent": "establish credibility",
                    "estimated_time": "1-2 minutes",
                },
                {
                    "position": 2,
                    "purpose": "show momentum",
                    "content_focus": "expansion/progress",
                    "slide_intent": "build on success",
                    "estimated_time": "1-2 minutes",
                },
                {
                    "position": 3,
                    "purpose": "acknowledge challenge",
                    "content_focus": "problem/concern",
                    "slide_intent": "transparent communication",
                    "estimated_time": "2-3 minutes",
                },
                {
                    "position": 4,
                    "purpose": "present solution",
                    "content_focus": "strategy/plan",
                    "slide_intent": "show path forward",
                    "estimated_time": "2-3 minutes",
                },
            ]
        elif narrative_arc == "problem-solution":
            structure = [
                {
                    "position": 1,
                    "purpose": "set context",
                    "content_focus": "background/situation",
                    "slide_intent": "establish understanding",
                    "estimated_time": "1-2 minutes",
                },
                {
                    "position": 2,
                    "purpose": "define problem",
                    "content_focus": "challenges/issues",
                    "slide_intent": "create urgency",
                    "estimated_time": "2-3 minutes",
                },
                {
                    "position": 3,
                    "purpose": "present solution",
                    "content_focus": "strategy/approach",
                    "slide_intent": "provide resolution",
                    "estimated_time": "3-4 minutes",
                },
            ]
        elif narrative_arc == "compare-contrast":
            structure = [
                {
                    "position": 1,
                    "purpose": "establish criteria",
                    "content_focus": "comparison framework",
                    "slide_intent": "set evaluation context",
                    "estimated_time": "1-2 minutes",
                },
                {
                    "position": 2,
                    "purpose": "present options",
                    "content_focus": "alternatives/choices",
                    "slide_intent": "show possibilities",
                    "estimated_time": "3-4 minutes",
                },
                {
                    "position": 3,
                    "purpose": "recommend choice",
                    "content_focus": "preferred option",
                    "slide_intent": "guide decision",
                    "estimated_time": "2-3 minutes",
                },
            ]
        else:  # informational/other
            structure = [
                {
                    "position": 1,
                    "purpose": "overview",
                    "content_focus": "main topics",
                    "slide_intent": "set expectations",
                    "estimated_time": "1-2 minutes",
                },
                {
                    "position": 2,
                    "purpose": "key information",
                    "content_focus": "primary content",
                    "slide_intent": "deliver core message",
                    "estimated_time": "3-4 minutes",
                },
                {
                    "position": 3,
                    "purpose": "summary",
                    "content_focus": "takeaways",
                    "slide_intent": "reinforce learning",
                    "estimated_time": "1-2 minutes",
                },
            ]

        return structure

    def _develop_presentation_strategy(self, narrative_arc: str, audience_analysis: Dict[str, str], _presentation_goal: str) -> Dict[str, Any]:
        """Develop presentation strategy."""
        strategy = {
            "opening_approach": "data-driven",
            "closing_approach": "summary",
            "flow_pattern": "chronological",
            "engagement_tactics": ["visual"],
        }

        # Adjust based on narrative arc
        if narrative_arc == "success-challenge-solution":
            strategy["opening_approach"] = "data-driven"
            strategy["flow_pattern"] = "problem-solution"
            strategy["closing_approach"] = "call-to-action"
        elif narrative_arc == "problem-solution":
            strategy["opening_approach"] = "problem-focused"
            strategy["flow_pattern"] = "problem-solution"
            strategy["closing_approach"] = "next-steps"
        elif narrative_arc == "persuasive":
            strategy["opening_approach"] = "story-based"
            strategy["closing_approach"] = "call-to-action"
            strategy["engagement_tactics"].append("storytelling")
        elif narrative_arc == "compare-contrast":
            strategy["opening_approach"] = "framework-based"
            strategy["flow_pattern"] = "compare-contrast"
            strategy["closing_approach"] = "recommendation"

        # Adjust based on audience
        if audience_analysis["attention_span"] == "short":
            strategy["engagement_tactics"].append("interactive")
        if audience_analysis["preferred_format"] == "visual-heavy":
            strategy["engagement_tactics"] = ["visual", "interactive"]

        return strategy


# Helper function for easy import
def analyze_presentation_needs(
    user_input: str,
    audience: str = "general",
    constraints: str = None,
    presentation_goal: str = "inform",
) -> Dict[str, Any]:
    """
    Convenience function for analyzing presentation needs.

    Args:
        user_input: Raw description of what they want to present
        audience: Target audience type
        constraints: Time/slide constraints
        presentation_goal: Primary goal of presentation

    Returns:
        Dictionary with content analysis and structural recommendations
    """
    analyzer = ContentAnalyzer()
    return analyzer.analyze_presentation_needs(user_input, audience, constraints, presentation_goal)
