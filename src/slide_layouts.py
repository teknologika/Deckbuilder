"""
Slide layout definitions for PowerPoint presentations.

This module contains the default layout mappings and PowerPoint layout
indices used for creating different types of slides.
"""

# Default layout mappings if not specified in settings
DEFAULT_LAYOUTS = {
    "title": "title",                # Title slide with subtitle
    "table": "titleandcontent",      # Slide with title and table
    "content": "titleandcontent",    # Slide with title and bullet points
    "section": "sectionHeader",      # Section divider slide
    "blank": "blank"                 # Blank slide
}   

# Standard PowerPoint layout names and their indices
DEFAULT_PPT_LAYOUTS = {
    "title": 0,                    # Title Slide
    "titleandcontent": 1,          # Title and Content
    "sectionHeader": 2,            # Section Header
    "twoContent": 3,              # Two Content
    "comparison": 4,              # Comparison
    "titleOnly": 5,               # Title Only
    "blank": 6,                   # Blank
    "contentWithCaption": 7,      # Content with Caption
    "pictureWithCaption": 8,      # Picture with Caption
    "titleAndVerticalText": 9,    # Title and Vertical Text
    "verticalTitleAndText": 10    # Vertical Title and Text
}