# Speaker Notes Feature - Implementation Plan

## Current State Analysis
- **No existing speaker notes functionality** in the codebase
- Python-pptx >=1.0.0 provides robust notes slide API
- Current architecture: `engine.py` → `presentation_builder.py` → `slide_builder.py`

## Implementation Plan

### Phase 1: Core Infrastructure
1. **Extend canonical JSON format** to support `speaker_notes` field
2. **Enhance SlideBuilder** (`slide_builder.py`) to process speaker notes after main content
3. **Add notes processing method** using python-pptx `slide.notes_slide` API

### Phase 2: Content Integration  
4. **Leverage existing ContentFormatter** for rich text formatting in notes
5. **Support markdown frontmatter** notes syntax in structured frontmatter
6. **Ensure inline formatting** (bold, italic, underline) works in notes

### Phase 3: MCP Tools Enhancement
7. **Update MCP tools** to accept and process speaker notes in markdown
8. **Enhance validation** to include notes slide validation
9. **Add comprehensive testing** for notes functionality

### Technical Approach
- Use python-pptx `slide.notes_slide` and `notes_text_frame` APIs
- Create notes slides on-demand when content provided
- Maintain backward compatibility with existing presentations
- Follow existing architecture patterns for consistency

This will add professional speaker notes support while preserving Deckbuilder's content-first philosophy and robust template system.