# In-Memory Language/Font Formatting Implementation

## Overview

This feature implements language and font formatting during presentation creation rather than as a post-processing step. This approach is more efficient, eliminates file path resolution issues, and provides cleaner architecture.

## Core Principle

**Template Preservation**: Only apply language/font formatting when explicitly specified. If None, leave template formatting completely untouched.

## Implementation Plan

### Phase 1: Add Language/Font Parameters to Creation Pipeline

1. **Update `Deckbuilder.create_presentation()` signature:**
   ```python
   def create_presentation(
       self,
       presentation_data: Dict[str, Any],
       fileName: str = "Sample_Presentation", 
       templateName: str = "default",
       language_code: Optional[str] = None,  # NEW
       font_name: Optional[str] = None,      # NEW
   ) -> str:
   ```

2. **Pass formatting parameters through pipeline:**
   - Only if `language_code is not None` or `font_name is not None`
   - Store parameters in `PresentationBuilder` and `ContentFormatter`

### Phase 2: Integrate FormattingSupport into ContentFormatter

1. **Update `ContentFormatter` to handle optional formatting:**
   ```python
   class ContentFormatter:
       def __init__(self, language_code=None, font_name=None):
           self.language_code = language_code
           self.font_name = font_name
           # Only import FormattingSupport if formatting needed
           if language_code or font_name:
               from ..content.formatting_support import FormattingSupport
               self.formatter = FormattingSupport()
   ```

2. **Apply formatting only when specified:**
   - During text run processing, check if formatting parameters exist
   - If None, skip all formatting and preserve template defaults
   - If specified, apply language ID and/or font name

### Phase 3: Update CLI Integration

1. **Clean CLI call to engine (environment variables already resolved by Click):**
   ```python
   # In src/deckbuilder/cli/main.py create_presentation()
   # self.language and self.font already contain env var values or None
   result = db.create_presentation(
       presentation_data,
       fileName=output_name,
       templateName=template_name,
       language_code=self.language,  # None or resolved env var value
       font_name=self.font,          # None or resolved env var value  
   )
   ```

2. **Remove all post-creation formatting code:**
   - Delete file path extraction and FormattingSupport post-processing
   - Keep only the clean result message

### Phase 4: Template Theme Font Handling

1. **Update theme fonts only when font_name specified:**
   ```python
   # In Deckbuilder.create_presentation()
   if font_name is not None:
       # Update theme majorFont and minorFont before slide creation
       formatter = FormattingSupport()
       formatter.update_theme_fonts(self.prs, font_name)
   ```

## Implementation Behavior

- ✅ **Template preservation**: If no language/font specified → template formatting untouched
- ✅ **Explicit formatting**: If language/font specified → applied during creation
- ✅ **No fallbacks in engine**: Environment variables handled only in CLI layer
- ✅ **Clean separation**: CLI resolves env vars, engine applies explicit values
- ✅ **Single I/O operation**: Format during creation, save once

## Benefits

- **Performance**: Single file I/O operation instead of create → save → load → format → save
- **Architecture**: Clean separation between CLI (env var resolution) and engine (creation)
- **Reliability**: No file path resolution dependencies
- **Consistency**: Formatting applied to all content during creation process
- **Template Integrity**: Preserves original template formatting when no customization specified

## Testing Scenarios

1. **No formatting**: `deckbuilder create test.md` → Template formatting preserved
2. **Environment variables**: `DECK_PROOFING_LANGUAGE="ja-JP" DECK_DEFAULT_FONT="Comic Sans MS" deckbuilder create test.md` → Japanese + Comic Sans applied
3. **CLI override**: `DECK_FONT="Arial" deckbuilder --font "Comic Sans MS" create test.md` → Comic Sans used (CLI overrides env var)

## Files Modified

- `src/deckbuilder/core/engine.py` - Add language_code/font_name parameters
- `src/deckbuilder/core/presentation_builder.py` - Pass formatting through pipeline  
- `src/deckbuilder/content/formatter.py` - Integrate FormattingSupport for optional formatting
- `src/deckbuilder/cli/main.py` - Clean up post-processing, pass parameters to engine

## Implementation Status

- [ ] Phase 1: Update engine signature and parameter passing
- [ ] Phase 2: Integrate FormattingSupport into ContentFormatter
- [ ] Phase 3: Update CLI integration and remove post-processing
- [ ] Phase 4: Add theme font handling
- [ ] Testing: Verify Japanese + Comic Sans MS via environment variables