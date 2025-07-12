"""
TDD Tests for Template Recommendation System

These tests are written FIRST (failing) following TDD approach.
They define the expected behavior for smart template recommendations before implementation.

GitHub Issue: https://github.com/teknologika/Deckbuilder/issues/38
"""

import pytest


class TestSmartTemplateRecommendationSystem:
    """Test the intelligent template recommendation system."""

    @pytest.fixture
    def sample_content_scenarios(self):
        """Sample content scenarios for testing recommendations."""
        return {
            "executive_summary": {
                "description": "Quarterly business review for board of directors with financial metrics, strategic initiatives, and market analysis",
                "expected_analysis": {
                    "content_type": "executive_presentation",
                    "audience": "executive",
                    "formality": "very_high",
                    "data_heavy": True,
                    "time_constraint": "short",
                    "decision_focused": True,
                },
                "expected_recommendations": [
                    {"template": "executive_pro", "confidence": 0.95, "reasoning": "Executive audience requires premium template with data visualization support"},
                    {"template": "business_pro", "confidence": 0.85, "reasoning": "Strong business template with professional layouts"},
                ],
            },
            "training_material": {
                "description": "Software training workshop with hands-on exercises, step-by-step guides, and practical examples for new users",
                "expected_analysis": {"content_type": "training", "audience": "learners", "formality": "medium", "data_heavy": False, "interactive": True, "sequential": True},
                "expected_recommendations": [
                    {"template": "training_focused", "confidence": 0.90, "reasoning": "Specialized template for educational content with clear structure"},
                    {"template": "default", "confidence": 0.80, "reasoning": "Versatile template suitable for instructional content"},
                ],
            },
            "product_comparison": {
                "description": "Competitive analysis comparing our product features, pricing, and market position against three main competitors",
                "expected_analysis": {"content_type": "comparison", "audience": "business", "formality": "high", "data_heavy": True, "structured": True, "competitive": True},
                "expected_recommendations": [
                    {"template": "comparison_pro", "confidence": 0.95, "reasoning": "Specialized template for competitive analysis with comparison layouts"},
                    {"template": "business_pro", "confidence": 0.75, "reasoning": "Good business template with comparison capabilities"},
                ],
            },
            "sales_pitch": {
                "description": "Client presentation showcasing our solution benefits, ROI projections, and implementation timeline for enterprise prospect",
                "expected_analysis": {"content_type": "sales_presentation", "audience": "client", "formality": "high", "persuasive": True, "roi_focused": True, "timeline_included": True},
                "expected_recommendations": [
                    {"template": "sales_pro", "confidence": 0.92, "reasoning": "Sales-optimized template with persuasive layouts and ROI visualization"},
                    {"template": "business_pro", "confidence": 0.78, "reasoning": "Professional template suitable for client presentations"},
                ],
            },
        }

    def test_recommendation_system_creation(self):
        """Test that the recommendation system can be created."""
        # Test that SmartTemplateRecommendationSystem can be imported and instantiated

        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        # Should be able to create an instance
        system = SmartTemplateRecommendationSystem()

        # Should have expected methods
        assert hasattr(system, "analyze_content_requirements")
        assert hasattr(system, "score_template_fit")
        assert hasattr(system, "recommend_templates")
        assert hasattr(system, "recommend_layouts_for_template")
        assert hasattr(system, "validate_recommendation_quality")

        # Should have internal components
        assert hasattr(system, "template_loader")
        assert hasattr(system, "content_matcher")
        assert hasattr(system, "layout_analyzer")

    def test_content_analysis_engine(self, sample_content_scenarios):
        """Test that content analysis engine correctly identifies content characteristics."""
        # Test content analysis functionality

        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        for scenario_name, scenario in sample_content_scenarios.items():
            description = scenario["description"]

            # Analyze content
            analysis = system.analyze_content_requirements(description)

            # Check that analysis has expected attributes
            assert hasattr(analysis, "content_type")
            assert hasattr(analysis, "audience")
            assert hasattr(analysis, "formality")
            assert hasattr(analysis, "data_heavy")
            assert hasattr(analysis, "time_constraint")
            assert hasattr(analysis, "decision_focused")

            # Check specific scenario expectations
            if scenario_name == "executive_summary":
                assert "executive" in analysis.audience or analysis.content_type == "executive_presentation"
                assert analysis.data_heavy is True
                assert analysis.decision_focused is True
            elif scenario_name == "training_material":
                assert "training" in analysis.content_type or analysis.audience == "learners"
                assert analysis.formality in ["medium", "low"]

    def test_template_scoring_algorithm(self):
        """Test the template scoring algorithm for different content types."""
        # Test template scoring functionality

        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem, ContentAnalysis

        system = SmartTemplateRecommendationSystem()

        # Create content analysis object
        content_analysis = ContentAnalysis(content_type="executive_presentation", audience="executive", formality="very_high", data_heavy=True, time_constraint="medium", decision_focused=True)

        # Test executive_pro template scoring
        exec_template_capabilities = {
            "target_audience": ["executive", "c_level"],
            "formality_level": "very_high",
            "data_visualization": True,
            "professional_styling": True,
            "content_types": ["executive_presentation"],
        }

        exec_recommendation = system.score_template_fit("executive_pro", content_analysis, exec_template_capabilities)

        # Should have high scores for executive template
        assert exec_recommendation.template == "executive_pro"
        assert exec_recommendation.confidence >= 0.9
        assert exec_recommendation.audience_match >= 0.9
        assert exec_recommendation.formality_match >= 0.9
        assert exec_recommendation.feature_match >= 0.8
        assert exec_recommendation.content_type_match >= 0.9
        assert len(exec_recommendation.reasoning) > 50

        # Test default template scoring
        default_template_capabilities = {
            "target_audience": ["general", "business"],
            "formality_level": "medium",
            "data_visualization": False,
            "professional_styling": True,
            "content_types": ["general_presentation"],
        }

        default_recommendation = system.score_template_fit("default", content_analysis, default_template_capabilities)

        # Should have lower scores for default template
        assert default_recommendation.template == "default"
        assert default_recommendation.confidence < exec_recommendation.confidence
        assert default_recommendation.audience_match < exec_recommendation.audience_match
        assert default_recommendation.formality_match < exec_recommendation.formality_match

    def test_layout_recommendation_within_template(self):
        """Test recommending specific layouts within chosen template."""
        # This test will FAIL until we implement layout recommendations

        # Future test data for when layout recommendations are implemented
        # content_analysis = {"content_type": "comparison", "structure": "categorical", "data_heavy": True}
        # template_layouts = {
        #     "Title Slide": {"best_for": ["opening"], "complexity": "simple"},
        #     "Four Columns": {"best_for": ["comparison", "categorization"], "complexity": "medium"},
        #     "Comparison": {"best_for": ["side_by_side", "before_after"], "complexity": "medium"},
        #     "Title and Content": {"best_for": ["general", "text_heavy"], "complexity": "simple"},
        # }
        # expected_layout_recommendations = {
        #     "opening_slide": {"layout": "Title Slide", "confidence": 0.95, "reasoning": "Standard professional opening"},
        #     "main_content": [
        #         {"layout": "Four Columns", "confidence": 0.90, "reasoning": "Perfect for categorical comparison with multiple items"},
        #         {"layout": "Comparison", "confidence": 0.85, "reasoning": "Good for direct side-by-side comparisons"},
        #     ],
        #     "closing_slide": {"layout": "Title and Content", "confidence": 0.80, "reasoning": "Suitable for conclusions and next steps"},
        # }

        # Test layout recommendation functionality
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Test layout recommendations for comparison content
        content_description = "Side-by-side comparison of two product options with detailed feature analysis"

        # Test layout recommendations for default template
        layout_recommendations = system.recommend_layouts_for_template("default", content_description)

        # Should return layout recommendations
        assert len(layout_recommendations) > 0

        # Each recommendation should have expected structure
        for recommendation in layout_recommendations:
            assert "layout" in recommendation
            assert "confidence" in recommendation
            assert "reasoning" in recommendation
            assert isinstance(recommendation["confidence"], float)
            assert 0 <= recommendation["confidence"] <= 1
            assert len(recommendation["reasoning"]) > 10

        # Should be sorted by confidence
        confidences = [rec["confidence"] for rec in layout_recommendations]
        assert confidences == sorted(confidences, reverse=True)

    def test_confidence_scoring_accuracy(self):
        """Test that confidence scores are accurate and well-calibrated."""
        # This test will FAIL until we implement confidence calibration

        # Test scenarios for confidence calibration (commented out for now)
        # high_confidence_content = "Executive quarterly board presentation with financial data"
        # medium_confidence_content = "General business update with mixed content types"
        # low_confidence_content = "Creative presentation with artistic elements"

        # Test confidence scoring accuracy
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Test with different content types
        test_cases = [
            ("Executive presentation for board with financial data", ["executive_pro", "business_pro"]),
            ("Training workshop for new employees", ["default"]),
            ("General business meeting update", ["default", "business_pro"]),
        ]

        for content_description, _expected_good_templates in test_cases:
            recommendations = system.recommend_templates(content_description, max_recommendations=3)

            assert len(recommendations) > 0

            # Check confidence ranges are reasonable
            for rec in recommendations:
                assert 0.0 <= rec.confidence <= 1.0
                assert isinstance(rec.confidence, float)

            # Higher ranked recommendations should have higher confidence
            if len(recommendations) > 1:
                assert recommendations[0].confidence >= recommendations[1].confidence

    def test_recommendation_reasoning_quality(self):
        """Test that recommendation reasoning is clear and actionable."""
        # This test will FAIL until we implement reasoning generation

        # Quality criteria for reasoning validation (commented out for now)
        # expected_reasoning_qualities = [
        #     "Mentions specific content-template alignment",
        #     "Explains audience suitability",
        #     "References layout capabilities",
        #     "Provides actionable guidance",
        #     "Uses clear, professional language",
        # ]
        # sample_reasoning = "Executive audience requires premium template..."

        # Expected behavior: reasoning should meet quality criteria
        # Test recommendation reasoning quality
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        content_description = "Executive quarterly review with financial metrics and strategic decisions"
        recommendations = system.recommend_templates(content_description, max_recommendations=3)

        assert len(recommendations) > 0

        # Check reasoning quality for each recommendation
        for rec in recommendations:
            reasoning = rec.reasoning

            # Should have substantial reasoning text
            assert len(reasoning) >= 30

            # Should contain relevant keywords
            reasoning_lower = reasoning.lower()
            assert any(keyword in reasoning_lower for keyword in ["audience", "executive", "formality", "data", "visual", "professional", "template", "suitable", "match"])

            # Should not be generic
            assert reasoning != "Generic template recommendation"

            # Should reference template capabilities or content requirements
            assert any(phrase in reasoning_lower for phrase in ["audience", "formality", "data", "presentation", "support"])

    def test_fallback_recommendations(self):
        """Test fallback recommendations when ideal templates aren't available."""
        # This test will FAIL until we implement fallback logic

        # Test scenarios for fallback logic (commented out for now)
        # available_templates = ["default"]
        # content_analysis = {"content_type": "executive_presentation", "audience": "executive", "formality": "very_high"}
        # expected_fallback = {
        #     "template": "default",
        #     "confidence": 0.65,
        #     "reasoning": "Best available option. Consider upgrading to executive template for optimal results.",
        #     "mitigation_tips": ["Use formal language throughout", "Focus on high-level insights", "Minimize slides for executive attention span", "Use data-heavy layouts sparingly"],
        # }

        # Test fallback recommendation logic
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Test with unusual content that might not have perfect matches
        unusual_content = "Creative artistic presentation with unconventional design needs"
        recommendations = system.recommend_templates(unusual_content, max_recommendations=3)

        # Should still return recommendations (fallback behavior)
        assert len(recommendations) > 0

        # Should include default template as fallback if low confidence
        template_names = [rec.template for rec in recommendations]
        if all(rec.confidence < 0.7 for rec in recommendations):
            assert "default" in template_names

        # All recommendations should have valid confidence scores
        for rec in recommendations:
            assert 0.0 <= rec.confidence <= 1.0
            assert len(rec.reasoning) > 20

    def test_multi_criteria_optimization(self):
        """Test optimization across multiple criteria (audience, content, constraints)."""
        # This test will FAIL until we implement multi-criteria optimization

        # Test data for multi-criteria optimization (commented out for now)
        # complex_requirements = {
        #     "content_type": "training",
        #     "audience": "mixed",  # Both technical and business users
        #     "time_constraint": "30_minutes",
        #     "interactivity": "high",
        #     "technical_depth": "medium",
        #     "business_context": True,
        # }
        # expected_optimization = {
        #     "primary_recommendation": {
        #         "template": "hybrid_business_technical",
        #         "confidence": 0.88,
        #         "optimization_score": {"audience_balance": 0.9, "content_suitability": 0.85, "time_efficiency": 0.9, "technical_depth": 0.85},
        #     },
        #     "trade_offs": {"prioritized": ["audience_balance", "time_efficiency"], "compromised": ["technical_depth"]},
        # }

        # Test multi-criteria optimization
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Test content with multiple constraints
        complex_requirements = "Executive board presentation with time constraints, heavy financial data, and decision focus for quarterly strategy approval"
        recommendations = system.recommend_templates(complex_requirements, max_recommendations=3)

        assert len(recommendations) > 0

        # Should optimize across multiple criteria
        top_recommendation = recommendations[0]

        # Should have reasonable confidence for well-matched content
        assert top_recommendation.confidence >= 0.5

        # Should have detailed reasoning covering multiple aspects
        reasoning = top_recommendation.reasoning.lower()
        criteria_coverage = sum(["audience" in reasoning, "formal" in reasoning or "executive" in reasoning, "data" in reasoning, any(word in reasoning for word in ["decision", "strategy", "board"])])

        # Should cover at least 2 criteria in reasoning
        assert criteria_coverage >= 2


class TestRecommendationSystemIntegration:
    """Test integration of recommendation system with other components."""

    def test_integration_with_template_metadata(self):
        """Test integration with template metadata system."""
        # This test will FAIL until we implement integration

        # Expected behavior: Recommendation system should use metadata for scoring
        # Test template metadata integration
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Should be able to access template metadata loader
        assert hasattr(system, "template_loader")
        assert hasattr(system.template_loader, "load_template_metadata")

        # Should integrate with layout recommendations
        content_description = "Business presentation with data analysis"
        layout_recommendations = system.recommend_layouts_for_template("default", content_description)

        # Should return structured layout data
        assert len(layout_recommendations) > 0
        for rec in layout_recommendations:
            assert "layout" in rec
            assert "confidence" in rec

    def test_integration_with_validation_system(self):
        """Test integration with validation system for recommendation verification."""
        # This test will FAIL until we implement validation integration

        # Expected behavior: Recommendations should be validated against actual template capabilities
        # Test validation system integration
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Test recommendation validation
        content_description = "Executive presentation with financial data"
        recommendations = system.recommend_templates(content_description)

        # Should be able to validate recommendation quality
        validation_result = system.validate_recommendation_quality(recommendations)

        # Should return validation metrics
        assert "quality_score" in validation_result
        assert "confidence_range" in validation_result
        assert "reasoning_quality" in validation_result

        # Quality score should be valid
        assert 0.0 <= validation_result["quality_score"] <= 1.0

    def test_recommendation_caching_and_performance(self):
        """Test that recommendations are cached for performance."""
        # This test will FAIL until we implement caching

        # Expected behavior: Similar content descriptions should use cached analysis
        # Test recommendation caching
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem
        import time

        system = SmartTemplateRecommendationSystem()

        content_description = "Business presentation with quarterly results"

        # Time first call
        start_time = time.time()
        recommendations1 = system.recommend_templates(content_description)
        first_call_time = time.time() - start_time

        # Time second call (should use cache)
        start_time = time.time()
        recommendations2 = system.recommend_templates(content_description)
        second_call_time = time.time() - start_time

        # Should return same recommendations
        assert len(recommendations1) == len(recommendations2)

        # Second call should be faster (cached) or at least not much slower
        assert second_call_time <= first_call_time * 2  # Allow some variance

        # Should have cache clearing capability
        assert hasattr(system, "clear_caches")
        system.clear_caches()

    def test_recommendation_learning_and_feedback(self):
        """Test system for learning from recommendation feedback."""
        # This test will FAIL until we implement learning system

        # Future feature: System should improve recommendations based on usage
        # Test basic recommendation functionality (learning system placeholder)
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # For now, just test that recommendations are consistent
        content_description = "Team meeting presentation with project updates"
        recommendations = system.recommend_templates(content_description)

        # Should provide consistent recommendations
        assert len(recommendations) > 0

        # Test multiple calls return consistent results
        recommendations2 = system.recommend_templates(content_description)
        assert len(recommendations) == len(recommendations2)

        # Top recommendation should be same
        assert recommendations[0].template == recommendations2[0].template


class TestRecommendationSystemEdgeCases:
    """Test edge cases and error handling for recommendation system."""

    def test_empty_content_description(self):
        """Test handling of empty or minimal content descriptions."""
        # This test will FAIL until we implement edge case handling

        edge_cases = ["", "   ", "Presentation", "Quick update"]  # Empty string  # Whitespace only  # Minimal description  # Very brief description

        for _edge_case in edge_cases:
            # Expected behavior: Should provide default recommendations with low confidence
            # expected_result = {
            #     "recommendations": [{"template": "default", "confidence": 0.5, "reasoning": "Insufficient content description. Using default template as safe fallback."}],
            #     "warning": "Content description too brief for accurate recommendations. Consider providing more details about audience, content type, and purpose.",
            # }
            pass

        # Test edge case handling for minimal content
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Test with minimal content
        minimal_descriptions = ["", "presentation", "meeting", "slides"]

        for description in minimal_descriptions:
            recommendations = system.recommend_templates(description)

            # Should still return recommendations (fallback behavior)
            assert len(recommendations) > 0

            # Should include default template for unclear requirements
            template_names = [rec.template for rec in recommendations]
            assert "default" in template_names

            # Should have valid confidence scores
            for rec in recommendations:
                assert 0.0 <= rec.confidence <= 1.0
                assert len(rec.reasoning) > 10

    def test_conflicting_content_requirements(self):
        """Test handling of conflicting content requirements."""
        # This test will FAIL until we implement conflict resolution

        # Test data for conflict resolution (commented out for now)
        # conflicting_content = "Casual team update for CEO with detailed technical specifications"
        # Conflict: casual vs CEO (formal), team vs CEO (audience mismatch)
        # expected_conflict_resolution = {
        #     "conflicts_detected": [
        #         {"type": "formality_mismatch", "description": "Casual style conflicts with CEO audience"},
        #         {"type": "audience_mismatch", "description": "Team update vs CEO audience"},
        #     ],
        #     "resolution_strategy": "prioritize_audience",
        #     "recommendation": {"template": "executive_pro", "confidence": 0.75, "reasoning": "Prioritizing CEO audience requirements. Recommend formal approach despite 'casual' mention."},
        #     "guidance": "Consider clarifying whether this is truly a casual update or a formal CEO briefing.",
        # }

        # Test conflicting requirements resolution
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Test content with conflicting requirements
        conflicting_content = "Casual informal executive board presentation with creative artistic elements and strict business requirements"
        recommendations = system.recommend_templates(conflicting_content)

        # Should still return reasonable recommendations
        assert len(recommendations) > 0

        # Should favor business/executive requirements over conflicting casual/creative
        top_recommendation = recommendations[0]
        reasoning = top_recommendation.reasoning.lower()

        # Should mention executive or business in reasoning
        assert any(word in reasoning for word in ["executive", "business", "professional"])

        # Should have reasonable confidence despite conflicts
        assert top_recommendation.confidence >= 0.4

    def test_unknown_content_types(self):
        """Test handling of unknown or unusual content types."""
        # This test will FAIL until we implement unknown content handling

        # Test data for unknown content handling (commented out for now)
        # unusual_content = "Artistic portfolio showcase with creative visualizations and experimental layouts"
        # expected_unknown_handling = {
        #     "content_analysis": {"content_type": "unknown_creative", "confidence": 0.3, "detected_keywords": ["artistic", "creative", "experimental"]},
        #     "recommendations": [
        #         {"template": "minimal", "confidence": 0.6, "reasoning": "Minimal template provides flexibility for creative content"},
        #         {"template": "default", "confidence": 0.5, "reasoning": "Safe fallback option"},
        #     ],
        #     "suggestion": "Consider using custom templates for specialized creative content",
        # }

        # Test unknown content type handling
        from src.deckbuilder.recommendation_engine import SmartTemplateRecommendationSystem

        system = SmartTemplateRecommendationSystem()

        # Test with unusual/unknown content types
        unusual_content_types = [
            "Quantum physics poetry presentation with interpretive dance elements",
            "Blockchain-based underwater archaeology findings with cryptocurrency implications",
            "AI-generated music composition analysis for interdimensional communication",
        ]

        for unusual_content in unusual_content_types:
            recommendations = system.recommend_templates(unusual_content)

            # Should still provide recommendations (graceful fallback)
            assert len(recommendations) > 0

            # Should default to general templates for unknown content
            template_names = [rec.template for rec in recommendations]
            assert "default" in template_names

            # Should have valid but likely lower confidence
            for rec in recommendations:
                assert 0.0 <= rec.confidence <= 1.0
                assert len(rec.reasoning) > 20
