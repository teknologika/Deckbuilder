"""
Content Segmenter Module

DEPRECATED: This module previously handled mixed content analysis and intelligent splitting
for dynamic shape creation. With the new template-based table layouts, this functionality
is no longer needed.

Table handling is now done through dedicated PowerPoint layouts:
- Table Only
- Table with Content Above
- Table with Content Above and Below
- Table with Content Left
- Content Table Content Table Content

Use the appropriate layout in your frontmatter instead of mixed content splitting.
"""

# Maintain backward compatibility for any remaining imports


def split_mixed_content_intelligently(content: str, base_table_styling: dict) -> dict:
    """
    DEPRECATED: Use dedicated table layouts instead.

    Returns empty segments to disable dynamic shape creation.
    """
    return {"segments": [], "has_mixed_content": False}


def extract_all_tables_from_content(content: str) -> dict:
    """
    DEPRECATED: Use dedicated table layouts instead.

    Returns content unchanged to disable table extraction.
    """
    return {"content": content, "tables": [], "table_count": 0}
