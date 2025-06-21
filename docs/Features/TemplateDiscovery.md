# Template Discovery & Self-Documentation System

## 📋 TODO / Implementation Status

### ✅ COMPLETED
- **Option C (Structured Frontmatter)**: ✅ FULLY IMPLEMENTED & OPTIMIZED
  - ✅ `StructuredFrontmatterRegistry` class created
  - ✅ Support for Four Columns, Two Content, Comparison, Picture with Caption layouts
  - ✅ One-way conversion from structured YAML to placeholder mappings
  - ✅ Integration with markdown parser (`parse_markdown_with_frontmatter`)
  - ✅ Template mapping system loading (`_ensure_layout_mapping`)
  - ✅ Validation system for structured frontmatter
  - ✅ **Option C Simplification**: Render-time formatting processing
  - ✅ **64% complexity reduction** in test files and JSON output
  - ✅ Working end-to-end with test presentations

### ✅ OPTIMIZATIONS COMPLETED
- **Formatting Pipeline Simplification**: ✅ COMPLETED
  - ✅ Removed complex formatting preprocessing explosion
  - ✅ Moved formatting processing to render time where it belongs
  - ✅ Simplified JSON output (strings with `**bold**` markers instead of complex objects)
  - ✅ Template loading fixes for environment-less operation
  - ✅ All structured frontmatter slides populate correctly with clean data

### 🔄 DESIGN EVOLUTION
- **Option B (MCP Discovery Tools)**: 🔄 REDESIGNED
  - ❌ Original 6-tool academic approach abandoned
  - ✅ **Content-First Design Strategy**: New approach based on actual user workflow
  - ✅ **3-Tool Practical Set**: Focused on presentation consulting, not layout discovery
  - ✅ **End-to-End Scenario Mapping**: Complete user journey from content to presentation

### 🚧 PENDING IMPLEMENTATION
- **Part B (Content-First MCP Tools)**: ❌ NOT STARTED
  - ❌ `analyze_presentation_needs()` MCP tool
  - ❌ `recommend_slide_approach()` MCP tool  
  - ❌ `optimize_content_for_layout()` MCP tool

- **Part B.1 (Direct Integration Support)**: ❌ NOT STARTED
  - ❌ **One-Shot Tool Integration**: Support for external tools to directly call existing MCP tools
  - ❌ **JSON/Markdown Input Support**: Accept presentation requests in structured formats
  - ❌ **Bypass Content-First Flow**: Allow direct creation when content is pre-structured
  - ❌ **Backwards Compatibility**: Ensure existing `create_presentation()` workflow unchanged

- **Part C (Auto-Documentation)**: ❌ NOT STARTED
  - ❌ Enhanced template analyzer with semantic analysis
  - ❌ Smart example generation
  - ❌ Auto-generated template guides
  - ❌ Usage pattern inference

---

## Overview

This specification defines an enhanced template analysis and discovery system that makes PowerPoint templates self-documenting for both human users and LLMs. The system combines semantic analysis of template structure with intelligent example generation to provide automatic documentation, structured frontmatter support, and programmatic discovery capabilities.

## Goals

1. **Zero Learning Curve**: Templates automatically document themselves with complete working examples
2. **LLM-Friendly Discovery**: Programmatic tools for AI systems to understand and use templates
3. **Human-Friendly Authoring**: Clean, structured frontmatter syntax for complex layouts
4. **Future-Proof**: New templates automatically gain documentation and discovery capabilities
5. **Maintain Compatibility**: Preserve existing JSON API while adding new capabilities

## Architecture Overview

### Three-Pronged Approach

**Option B: Content-First Presentation Intelligence** (MCP Tools)
- Analyze user content and communication goals first
- Recommend presentation structure based on message intent
- Content-aware layout suggestions with audience consideration

**Option C: Structured Frontmatter System** ✅ FULLY IMPLEMENTED & OPTIMIZED
- Clean YAML syntax for complex layouts
- Automatic conversion to PowerPoint placeholder mappings
- Human-readable authoring experience
- **Simplified formatting**: Render-time processing instead of preprocessing explosion

**Option D: Auto-Documentation System**
- Semantic analysis of PowerPoint templates
- Intelligent example generation
- Self-documenting template guides

## Option C: Structured Frontmatter System ✅ IMPLEMENTED

### Current Implementation (Optimized)

The structured frontmatter system provides clean, human-readable YAML structures that abstract away PowerPoint placeholder names while maintaining full functionality. **Optimized with Option C simplification for minimal complexity and maximum performance.**

#### Key Components

1. **`StructuredFrontmatterRegistry`** (`src/structured_frontmatter.py`)
   - Defines supported layouts and their YAML structures
   - Contains mapping rules between YAML fields and PowerPoint placeholders
   - Currently supports: Four Columns, Two Content, Comparison, Picture with Caption

2. **`StructuredFrontmatterConverter`** (`src/structured_frontmatter.py`)
   - Converts structured YAML to placeholder mappings
   - Template-aware using actual PPTX placeholder names
   - Handles dynamic mapping generation

3. **`StructuredFrontmatterValidator`** (`src/structured_frontmatter.py`)
   - Validates structured frontmatter syntax and content
   - Provides warnings and error messages
   - Ensures data integrity before conversion

#### Working Examples

**Four Columns Layout:**
```yaml
---
layout: Four Columns
title: Feature Comparison Matrix
columns:
  - title: Performance
    content: "Fast processing with optimized algorithms"
  - title: Security
    content: "Enterprise-grade encryption with SOC2 compliance"
  - title: Usability
    content: "Intuitive interface with minimal learning curve"
  - title: Cost
    content: "Transparent pricing with flexible plans"
---
```

**Comparison Layout:**
```yaml
---
layout: Comparison
title: Traditional vs Modern Approach
comparison:
  left:
    title: Traditional Method
    content: "Proven track record with established processes"
  right:
    title: Modern Solution
    content: "Cloud-native architecture with automated workflows"
---
```

**Two Content Layout:**
```yaml
---
layout: Two Content
title: Two Content Layout Test
sections:
  - title: Left Side Content
    content:
      - "**Feature A** details"
      - "*Feature B* information"
  - title: Right Side Content
    content:
      - "***Important*** updates"
      - "**Security** measures"
---
```

#### Integration Points

- ✅ Integrated with `parse_markdown_with_frontmatter()` in `deckbuilder.py`
- ✅ Template mapping automatically loaded via `_ensure_layout_mapping()`
- ✅ Works with existing semantic detection system
- ✅ Supports inline formatting (bold, italic, underline)
- ✅ Backwards compatible with regular frontmatter

#### Option C Optimization (Completed)

**Problem Solved**: Initial implementation created complex preprocessing that exploded simple content into multiple formatting representations, making test files and JSON output unnecessarily complex.

**Solution Implemented**: 
- **Input**: Clean YAML structured frontmatter (preserved)
- **Processing**: Simple string storage with `**bold**` markers (simplified)
- **Output**: Formatting applied at PowerPoint render time (optimized)

**Results**:
- ✅ **64% reduction** in test file complexity (530 → 190 lines)
- ✅ **Simple JSON**: `"**bold** text"` instead of complex formatting objects
- ✅ **Better performance**: Single-pass formatting at render time
- ✅ **Easier debugging**: Clean, readable intermediate data
- ✅ **Full functionality preserved**: All formatting still works perfectly

**Before Option C**:
```json
"Content Placeholder 2": ["**Feature A** details"],
"Content Placeholder 2_rich_content": [{"paragraph": "**Feature A** details"}],
"Content Placeholder 2_formatted": [{"text": "Feature A", "format": {"bold": true}}]
```

**After Option C**:
```json
"Content Placeholder 2": ["**Feature A** details"]
```

## Option B: Content-First Presentation Intelligence ❌ PENDING

### Design Philosophy: Content-First Approach

**Problem with Original Design**: The initial 6-tool approach was layout-centric, asking "what layouts exist?" instead of "what does the user want to communicate?"

**New Strategy**: Start with user content and communication goals, then recommend optimal presentation structure.

### Content-First MCP Tools

#### Tool 1: Presentation Needs Analysis
```python
@server.tool()
def analyze_presentation_needs(
    user_input: str,                 # Raw description of what they want to present
    audience: str = None,            # "board", "team", "customers", "technical"
    constraints: str = None,         # "10 minutes", "5 slides max", "data-heavy"
    presentation_goal: str = None    # "persuade", "inform", "report", "train"
) -> dict:
    """Analyze user needs and recommend presentation structure"""
```

**Returns**: Content analysis + narrative arc + structural recommendations

#### Tool 2: Content-Aware Layout Recommendations
```python
@server.tool()
def recommend_slide_approach(
    content_piece: str,              # Specific content to present
    message_intent: str,             # What they want this content to communicate
    presentation_context: dict = None # From analyze_presentation_needs()
) -> dict:
    """Get specific layout and content organization recommendations"""
```

**Returns**: Layout suggestions + content structuring + examples

#### Tool 3: Content Optimization & Validation
```python
@server.tool() 
def optimize_content_for_layout(
    content: str,
    chosen_layout: str,
    slide_context: dict = None
) -> dict:
    """Optimize content structure and validate fit with layout"""
```

**Returns**: Formatted content + gap analysis + ready-to-use YAML

### End-to-End Content-First Workflow

#### Real User Scenario:
*"I need to present our Q3 results to the board. We had 23% revenue growth, expanded to 3 new markets, but customer churn increased to 8%. I want to show we're growing but acknowledge the churn issue and present our retention strategy."*

#### Step 1: Content & Goals Analysis
```python
analyze_presentation_needs(
    user_input="Q3 results: 23% growth, 3 new markets, 8% churn, retention strategy",
    audience="board", 
    presentation_goal="balanced report"
)

Returns: {
    "content_analysis": {
        "key_messages": ["strong growth", "expansion success", "churn challenge", "solution"],
        "narrative_arc": "success-challenge-solution",
        "complexity_level": "executive summary"
    },
    "recommended_structure": [
        {"position": 1, "purpose": "lead with strength", "content_focus": "revenue growth"},
        {"position": 2, "purpose": "show momentum", "content_focus": "market expansion"},  
        {"position": 3, "purpose": "acknowledge challenge", "content_focus": "churn increase"},
        {"position": 4, "purpose": "present solution", "content_focus": "retention strategy"}
    ]
}
```

#### Step 2: Slide-Specific Recommendations
```python
# For the growth metric
recommend_slide_approach(
    content_piece="23% revenue growth in Q3",
    message_intent="lead with strength"
)

Returns: {
    "recommended_layouts": [
        {"layout": "Big Number", "reason": "metrics deserve prominence", "confidence": 0.9}
    ],
    "content_suggestions": {
        "primary_message": "Q3 Revenue Growth",
        "supporting_data": ["vs Q2", "key drivers"],
        "visual_approach": "large number with context"
    }
}

# For the churn challenge
recommend_slide_approach(
    content_piece="customer churn increased to 8%",
    message_intent="acknowledge challenge transparently"
)

Returns: {
    "recommended_layouts": [
        {"layout": "Problem-Solution", "reason": "pairs challenge with solution", "confidence": 0.95}
    ],
    "content_suggestions": {
        "framing": "acknowledge but contextualize",
        "supporting_data": ["industry benchmark", "root cause"],
        "transition": "leads to solution discussion"
    }
}
```

#### Step 3: Content Optimization
```python
optimize_content_for_layout(
    content="customer churn 8%, industry average 12%, onboarding friction",
    chosen_layout="Problem-Solution"
)

Returns: {
    "optimized_content": {
        "yaml_structure": """
layout: Problem Solution
title: Addressing Customer Churn Challenge
problem:
  title: Q3 Churn Rate
  content: 
    - "**8% churn rate** (vs 12% industry average)"
    - "Primary cause: **onboarding friction**"
solution:
  title: Retention Strategy
  content:
    - "**Redesigned onboarding** (30% faster)"
    - "**Expected impact**: 5% churn by Q4"
"""
    },
    "presentation_tips": {
        "delivery": "acknowledge quickly, focus on solution"
    }
}
```

### Key Benefits of Content-First Approach

1. **User-Centric**: Starts with what user wants to communicate, not system capabilities
2. **Audience-Aware**: Board vs team presentation = different approaches
3. **Message-Driven**: Focuses on communication effectiveness
4. **Context-Sensitive**: Each slide considers the whole presentation narrative
5. **Practical**: Provides ready-to-use optimized content
6. **Intelligent**: Acts as presentation consultant, not just layout picker

### Real-World Example: Content-First Analysis in Action

#### Scenario: Mobile App Redesign Executive Presentation

**User Input:**
```
"I need to present our mobile app redesign project to the executive team. 
We completed user research with 500 customers, redesigned the checkout flow, 
and saw a 35% increase in conversion rates during beta testing. However, 
development took 3 months longer than planned and cost 40% more than budgeted. 
I want to show the business impact while being transparent about the overruns 
and propose how to prevent this in future projects."

Audience: "board"
Constraints: "15 minutes" 
Goal: "report"
```

**Content-First Analysis Output:**

```json
{
  "content_analysis": {
    "key_messages": ["metric: 500 customers", "metric: 35%", "metric: 40%", 
                     "growth/expansion", "solutions/strategy"],
    "narrative_arc": "success-challenge-solution",
    "complexity_level": "executive", 
    "data_density": "balanced",
    "emotional_tone": "neutral"
  },
  "audience_considerations": {
    "expertise_level": "expert",
    "attention_span": "short",
    "preferred_format": "high-level"
  },
  "recommended_structure": [
    {
      "position": 1, "purpose": "lead with strength",
      "content_focus": "35% conversion increase", 
      "slide_intent": "establish credibility", "estimated_time": "1-2 minutes"
    },
    {
      "position": 2, "purpose": "show momentum", 
      "content_focus": "user research and improvements",
      "slide_intent": "build on success", "estimated_time": "1-2 minutes"
    },
    {
      "position": 3, "purpose": "acknowledge challenge",
      "content_focus": "budget and timeline overruns", 
      "slide_intent": "transparent communication", "estimated_time": "2-3 minutes"
    },
    {
      "position": 4, "purpose": "present solution",
      "content_focus": "prevention strategy for future projects",
      "slide_intent": "show path forward", "estimated_time": "2-3 minutes"
    }
  ],
  "presentation_strategy": {
    "opening_approach": "data-driven",
    "closing_approach": "call-to-action", 
    "flow_pattern": "problem-solution",
    "engagement_tactics": ["visual", "interactive"]
  }
}
```

**Key Insights:**
- **Narrative Arc**: Success-challenge-solution pattern detected automatically
- **Board Optimization**: High-level content, short attention span considerations
- **Strategic Flow**: Lead with wins → acknowledge issues → present solutions
- **Timing**: Optimized 4-slide structure for 15-minute constraint

**Value Delivered:**
Instead of asking "What PowerPoint layouts exist?", the system understands "What story are you trying to tell?" and provides strategic guidance on content sequencing, audience adaptation, and communication effectiveness.

### Integration with Structured Frontmatter

The content-first tools will:
1. **Analyze** → Understand user's communication goals
2. **Recommend** → Suggest structured frontmatter layouts based on content
3. **Optimize** → Generate ready-to-use YAML with proper content structure
4. **Validate** → Ensure content fits layout and communication goals

## Option D: Auto-Documentation System ❌ PENDING

### Planned Features

#### Enhanced Template Analysis
- Semantic analysis of PowerPoint layouts
- Purpose inference (comparison, content, media, etc.)
- Complexity assessment and usage recommendations
- Spatial layout analysis

#### Smart Example Generation
- Context-aware content generation
- Realistic scenario creation
- Multiple format examples (JSON, frontmatter, structured)
- Best practice demonstrations

#### Auto-Generated Documentation
- Template-specific usage guides
- Layout comparison matrices
- Integration examples
- Troubleshooting guides

## Current File Structure

```
src/
├── deckbuilder.py (✅ enhanced with structured frontmatter)
├── structured_frontmatter.py (✅ complete implementation)
├── placeholder_types.py (✅ existing semantic detection)
├── tools.py (✅ existing template analyzer)
└── main.py (✅ MCP server entry point)

docs/Features/
├── PlaceholderMatching.md (✅ existing)
├── TemplateDiscovery.md (✅ this file)
└── generated/ (❌ planned for auto-docs)

tests/
├── test_presentation.md (✅ uses structured frontmatter)
├── test_structured_frontmatter.md (✅ additional examples)
└── test_presentation.json (✅ expected output)
```

## Implementation Roadmap

### Phase 1: Option B - Content-First MCP Tools (1-2 weeks)
1. Implement `analyze_presentation_needs()` with content analysis
2. Build `recommend_slide_approach()` with layout intelligence  
3. Create `optimize_content_for_layout()` with YAML generation
4. Test complete content-first workflow with real scenarios

### Phase 2: Option D - Auto-Documentation (1-2 weeks)
1. Enhance template analyzer with semantic analysis
2. Implement smart example generation
3. Create auto-documentation generators
4. Generate template-specific guides

### Phase 3: Integration & Polish (1 week)
1. Connect all three systems (B+C+D)
2. Comprehensive error handling and fallbacks
3. End-to-end testing with real presentations
4. Performance optimization and documentation

## Success Criteria

1. ✅ **Structured Frontmatter Working**: Clean YAML syntax converts correctly to PowerPoint content
2. ✅ **Optimized Performance**: 64% complexity reduction with render-time formatting
3. ❌ **Content-First Intelligence**: LLM analyzes user content before suggesting layouts
4. ❌ **Presentation Consulting**: LLM acts as intelligent presentation advisor
5. ✅ **Backward Compatibility**: Existing JSON API continues to work unchanged
6. ❌ **End-to-End Workflow**: Complete user journey from content to presentation

## Technical Notes

### Current Implementation Strengths
- ✅ **Optimized performance**: Render-time formatting processing
- ✅ **Minimal complexity**: 64% reduction in intermediate data complexity
- ✅ Robust template mapping system with fallbacks
- ✅ Clean separation of concerns (registry, converter, validator)
- ✅ Template-aware mapping using actual PowerPoint placeholder names
- ✅ Comprehensive error handling and validation
- ✅ Seamless integration with existing semantic detection
- ✅ **Clean data flow**: Simple strings with formatting markers

### Known Limitations
- ❌ Only supports four layout types currently (can be extended easily)
- ❌ No bidirectional conversion (structured → YAML) - not needed for current use case
- ❌ Limited to predefined structure patterns (by design for safety)
- ❌ No content-first intelligence tools yet (Option B redesigned and pending)
- ❌ Missing audience-aware recommendations
- ❌ No narrative arc analysis capabilities

### Extension Points
- **New Layout Support**: Add entries to `StructuredFrontmatterRegistry.STRUCTURE_DEFINITIONS`
- **Custom Structures**: Extend registry with new `structure_type` patterns
- **Advanced Validation**: Enhance `StructuredFrontmatterValidator` with layout-specific rules
- **Content Intelligence**: Implement content analysis and narrative understanding
- **Audience Analysis**: Add audience-specific presentation recommendations
- **Template Integration**: Connect with auto-documentation system when implemented

This specification serves as both documentation and implementation guide for the complete template discovery system, with clear status tracking and next steps.