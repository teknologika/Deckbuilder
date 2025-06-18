# Inline Formatting Test for Deck Builder MCP

Please use the `create_presentation_from_markdown` tool to test all inline formatting capabilities with this content:

---
layout: title
---
# ***Inline Formatting Test***
## Comprehensive ___PowerPoint___ **Formatting** *Validation*

---
layout: content
---
# Basic Formatting Tests

## Single Format Types
Test each formatting type individually to verify proper rendering.

- **Bold text** should appear in bold weight
- *Italic text* should appear slanted
- ___Underlined text___ should have underline decoration

## Combined Formatting Tests
Test multiple formatting applied to the same text.

- ***Bold and italic combined*** should be both bold and slanted
- ***___Bold, italic, and underlined___*** should have all three formats
- This paragraph contains *mixed* **formatting** with ___different___ ***styles*** throughout the sentence.

---
layout: content
---
# Advanced Formatting Scenarios

## Inline Formatting in Sentences
Regular text with **important highlights** and *emphasis* words, plus ___key terms___ that need attention.

- First bullet with **bold section** in the middle
- Second bullet with *italic emphasis* and ___underlined terms___
- Third bullet with ***bold italic*** and regular text combined
- Complex bullet: Start normal, then **bold start** *italic middle* ___underlined end___ back to normal

## Formatting Edge Cases
Test boundary conditions and special scenarios.

- **Bold at start** of bullet point
- Bullet point ending with *italic formatting*
- ___Entire bullet point underlined from start to finish___
- ***Entire bullet point with bold italic formatting applied***
- Mixed: **Bold** then *italic* then ___underlined___ then ***bold italic*** in sequence

---
layout: content
---
# Paragraph Formatting Tests

## Complex Paragraph Example
This paragraph demonstrates ***comprehensive formatting capabilities*** within a single block of text. We start with **bold emphasis** for important points, use *italic text* for subtle emphasis, and apply ___underlining___ to highlight ***key terminology and concepts***. 

The formatting should work seamlessly across word boundaries and maintain readability while providing visual hierarchy through **strategic use** of *different* ___formatting___ ***combinations***.

## Multiple Paragraphs with Formatting
First paragraph with **bold statements** and *italic nuances*.

Second paragraph with ___underlined key points___ and ***bold italic emphasis***.

Third paragraph mixing **bold**, *italic*, ___underlined___, and ***bold italic*** formatting throughout the text flow.

---
layout: table
style: dark_blue_white_text
row_style: alternating_light_gray
---
# Formatting Test Results
| Format Type | Syntax | Expected Result | Status |
| **Bold** | `**text**` | Bold weight text | ✓ Test |
| *Italic* | `*text*` | Slanted text | ✓ Test |
| ___Underlined___ | `___text___` | Underlined text | ✓ Test |
| ***Bold Italic*** | `***text***` | Bold and slanted | ✓ Test |
| ***___All Three___*** | `***___text___***` | Bold, italic, underlined | ✓ Test |

---
layout: content
---
# Test Completion Notes

## Validation Checklist
Review the generated presentation to verify:

- **Bold formatting** appears with increased font weight
- *Italic formatting* appears with slanted text
- ___Underlined formatting___ appears with underline decoration
- ***Combined formatting*** shows multiple effects simultaneously
- Regular text remains unformatted between formatted sections
- Formatting boundaries are clean without artifacts
- Table content preserves formatting in cells
- Headings maintain their bold property while adding inline formatting

## Expected Output File
The presentation should be saved as: `Sample_Presentation.YYYY-MM-DD_HHMM.g.pptx`

**Test completed successfully if all formatting appears as expected in PowerPoint!**