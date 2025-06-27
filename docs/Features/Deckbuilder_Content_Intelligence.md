# Deckbuilder Content Intelligence Guide

**For users who want AI-powered layout recommendations and content optimization.**

This is an advanced feature that analyzes your content and suggests optimal presentation layouts. Most users won't need this for basic presentation creation.

## Overview

Content Intelligence uses semantic analysis to:
- Understand what you want to communicate
- Recommend the best layouts for your content
- Suggest content improvements
- Optimize text for chosen layouts

**When to use this:**
- You're unsure which layout works best for your content
- You want data-driven layout recommendations
- You're building AI-powered presentation tools
- You need content optimization suggestions

## Quick Start

```python
from deckbuilder.layout_intelligence import LayoutIntelligence

# Initialize the intelligence system
intelligence = LayoutIntelligence()

# Analyze your content
content = """
Our new mobile app has four key features: real-time notifications
for instant updates, offline mode for uninterrupted access,
cloud sync across all devices, and an advanced analytics dashboard.
"""

# Get layout recommendations
recommendations = intelligence.recommend_layouts(content)

for rec in recommendations:
    print(f"Layout: {rec.layout_name}")
    print(f"Confidence: {rec.confidence:.2f}")
    print(f"Why: {', '.join(rec.reasoning)}")
    print()
```

## Core Functions

### `analyze_content(content)` - Content Analysis

Analyzes text to understand communication intent and structure.

```python
def analyze_content(content: str) -> ContentAnalysis
```

**Parameters:**
- `content` (str): Raw text content to analyze

**Returns:** `ContentAnalysis` object with:
- `intent` - What you're trying to communicate (comparison, overview, features, etc.)
- `content_type` - Type of content (image_content, statistics, process_steps)
- `structure_indicators` - Content structure clues (multiple_columns, bullet_list, etc.)
- `keywords_found` - Relevant semantic keywords detected
- `content_blocks` - Number of distinct content sections
- `has_images` / `has_numbers` - Content type flags

**Example:**
```python
content = """
Q4 2024 Performance vs Q3 2024:
Revenue increased from $1.8M to $2.1M (16.7% growth)
Customer satisfaction improved from 4.2 to 4.6 stars
Market share expanded from 12% to 15%
"""

analysis = intelligence.analyze_content(content)

print(f"Intent: {analysis.intent}")                    # "comparison"
print(f"Content Type: {analysis.content_type}")        # "statistics"
print(f"Structure: {analysis.structure_indicators}")   # ["multiple_items", "numeric_data"]
print(f"Keywords: {analysis.keywords_found}")          # ["vs", "increased", "improved", "performance"]
print(f"Has Numbers: {analysis.has_numbers}")          # True
```

### `recommend_layouts(content, max_recommendations)` - Layout Recommendations

Suggests optimal layouts based on content analysis.

```python
def recommend_layouts(content: str, max_recommendations: int = 3) -> List[LayoutRecommendation]
```

**Parameters:**
- `content` (str): Content to analyze
- `max_recommendations` (int): Maximum layouts to recommend (default: 3)

**Returns:** List of `LayoutRecommendation` objects with:
- `layout_name` - Recommended layout name
- `confidence` - Confidence score (0.0 to 1.0)
- `reasoning` - Human-readable explanation
- `placeholder_mapping` - Suggested content placement
- `optimization_hints` - Content improvement suggestions

**Example:**
```python
content = """
Our platform offers these core capabilities:
Performance: 99.9% uptime with sub-second response times
Security: Enterprise-grade encryption with SOC2 compliance
Scalability: Auto-scaling to handle traffic spikes
Support: 24/7 expert assistance with dedicated account management
"""

recommendations = intelligence.recommend_layouts(content, max_recommendations=2)

for rec in recommendations:
    print(f"\nLayout: {rec.layout_name}")
    print(f"Confidence: {rec.confidence:.2f}")
    print(f"Reasoning: {', '.join(rec.reasoning)}")
    print(f"Content mapping: {rec.placeholder_mapping}")
    print(f"Optimization: {', '.join(rec.optimization_hints)}")

# Output:
# Layout: Four Columns
# Confidence: 0.95
# Reasoning: Multiple distinct features, structured format, feature showcase
# Content mapping: {'title': 'Platform Capabilities', 'col1_title': 'Performance', ...}
# Optimization: Consider adding metrics, Use bullet points for clarity
```

## Data Structures

### `ContentAnalysis`

```python
@dataclass
class ContentAnalysis:
    intent: str                    # What you're trying to communicate
    content_type: str             # Type of content
    structure_indicators: List[str] # Content structure patterns
    keywords_found: List[str]      # Semantic keywords
    content_blocks: int           # Number of content sections
    has_images: bool              # Image content detected
    has_numbers: bool             # Numeric content detected
```

**Intent Types:**
- `"comparison"` - Comparing options, before/after, vs scenarios
- `"overview"` - High-level summary, executive overview
- `"features"` - Product features, capabilities, benefits
- `"metrics"` - Performance data, statistics, KPIs
- `"process"` - Step-by-step workflows, procedures
- `"timeline"` - Chronological information, roadmaps
- `"organization"` - Team structure, hierarchy, roles

**Content Types:**
- `"image_content"` - Visual-heavy content
- `"statistics"` - Numeric data and metrics
- `"process_steps"` - Sequential procedures
- `"feature_list"` - Product capabilities
- `"comparison_data"` - Comparative information
- `"text_heavy"` - Primarily textual content

### `LayoutRecommendation`

```python
@dataclass
class LayoutRecommendation:
    layout_name: str              # Layout name to use
    confidence: float             # Confidence (0.0-1.0)
    reasoning: List[str]          # Why this layout works
    placeholder_mapping: Dict[str, str]  # Content → placeholder mapping
    optimization_hints: List[str] # Content improvement suggestions
```

## Practical Examples

### Example 1: Feature Showcase

```python
content = """
Our cloud platform delivers unmatched performance with 99.9% uptime,
enterprise security with SOC2 compliance, infinite scalability
with auto-scaling, and 24/7 expert support.
"""

analysis = intelligence.analyze_content(content)
recommendations = intelligence.recommend_layouts(content)

# Likely results:
# Intent: "features"
# Recommended: "Four Columns" (high confidence)
# Reasoning: Multiple distinct features, structured presentation
```

### Example 2: Performance Comparison

```python
content = """
Traditional solution: $50K annual cost, 2-week deployment,
limited scalability, basic support.
Our solution: $30K annual cost, same-day deployment,
unlimited scalability, 24/7 premium support.
"""

analysis = intelligence.analyze_content(content)
recommendations = intelligence.recommend_layouts(content)

# Likely results:
# Intent: "comparison"
# Recommended: "Comparison" (high confidence)
# Reasoning: Clear before/after structure, comparative language
```

### Example 3: Process Flow

```python
content = """
Implementation follows these steps:
1. Discovery phase with stakeholder interviews
2. Design phase with wireframes and prototypes
3. Development phase with agile methodology
4. Testing phase with comprehensive QA
5. Deployment phase with phased rollout
"""

analysis = intelligence.analyze_content(content)
recommendations = intelligence.recommend_layouts(content)

# Likely results:
# Intent: "process"
# Recommended: "Title and Content" or "Five Steps" layout
# Reasoning: Sequential steps, numbered process
```

## Integration with Presentation Creation

Use content intelligence to optimize your presentation workflow:

```python
from deckbuilder import get_deckbuilder_client
from deckbuilder.layout_intelligence import LayoutIntelligence

def create_intelligent_presentation(content_pieces, filename):
    """Create presentation with AI-recommended layouts."""

    deck = get_deckbuilder_client()
    intelligence = LayoutIntelligence()

    deck.create_presentation("default", filename)

    slides = []
    for content in content_pieces:
        # Get AI recommendation
        recommendations = intelligence.recommend_layouts(content)
        best_layout = recommendations[0]  # Highest confidence

        # Create slide with recommended layout
        slide = {
            "type": best_layout.layout_name,
            "title": "Auto-Generated Title",  # Could be optimized too
        }

        # Apply recommended content mapping
        for placeholder, text in best_layout.placeholder_mapping.items():
            slide[placeholder] = text

        slides.append(slide)

    # Add all slides
    presentation_data = {"presentation": {"slides": slides}}
    deck.add_slide_from_json(presentation_data)

    return deck.write_presentation(filename)

# Usage
content_list = [
    "Our platform offers four key benefits: performance, security, scalability, support",
    "Q4 revenue: $2.1M vs Q3: $1.8M (16.7% growth)",
    "Implementation: discovery, design, development, testing, deployment"
]

result = create_intelligent_presentation(content_list, "AI_Optimized_Presentation")
```

## Customizing Intelligence

### Custom Intelligence File

You can provide your own semantic patterns:

```python
# Load custom intelligence rules
intelligence = LayoutIntelligence(intelligence_file="/path/to/custom_rules.json")
```

**Custom rules format** (`custom_rules.json`):
```json
{
    "content_patterns": {
        "intent_keywords": {
            "comparison": ["vs", "versus", "compared to", "before/after"],
            "features": ["offers", "includes", "provides", "capabilities"]
        },
        "structure_patterns": {
            "multiple_columns": ["four key", "three main", "core benefits"],
            "comparison_format": ["vs", "compared to", "traditional vs new"]
        }
    },
    "layout_compatibility": {
        "Four Columns": {
            "optimal_for": ["features", "benefits", "capabilities"],
            "confidence_factors": {
                "multiple_items": 0.8,
                "structured_list": 0.9
            }
        }
    }
}
```

## Advanced Usage

### Confidence Tuning

Filter recommendations by confidence threshold:

```python
content = "Some ambiguous content that could work with multiple layouts"
recommendations = intelligence.recommend_layouts(content)

# Only use high-confidence recommendations
high_confidence = [r for r in recommendations if r.confidence > 0.7]

if high_confidence:
    chosen_layout = high_confidence[0].layout_name
else:
    chosen_layout = "Title and Content"  # Safe fallback
```

### Content Optimization

Use optimization hints to improve content:

```python
recommendations = intelligence.recommend_layouts(content)
best_rec = recommendations[0]

print("Optimization suggestions:")
for hint in best_rec.optimization_hints:
    print(f"• {hint}")

# Example output:
# • Consider adding specific metrics for stronger impact
# • Break long sentences into bullet points for clarity
# • Add quantitative data to support claims
# • Use parallel structure for better readability
```

## Limitations

**Current limitations:**
- Works best with English content
- Optimized for business presentation content
- Limited to predefined layout types
- Confidence scores are estimates, not guarantees

**Best practices:**
- Use as a starting point, not final decision
- Combine with human judgment
- Test recommendations with your specific content
- Provide feedback to improve accuracy over time

This content intelligence system is designed to augment human creativity, not replace it. Use it as a smart assistant to guide your presentation design decisions.

## Related Documentation

- **[Template Discovery](Template_Discovery.md)** - Content-first design evolution and MCP tools design
- **[Supported Templates](Supported_Templates.md)** - Available layouts for recommendations
- **[Placeholder Matching](Placeholder_Matching.md)** - How content gets mapped to template placeholders
- **[Testing Framework](Testing_Framework.md)** - Testing content intelligence with real scenarios
