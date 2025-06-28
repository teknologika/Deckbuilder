---
layout: Title Slide
---
# **Test Presentation** with *Inline* Formatting
## Testing all ___placeholders___ and **formatting** capabilities

---
layout: Title and Content
---
# Content Slide with **Bold** and *Italic*

## Overview
This section demonstrates content slides with various formatting options.

- First bullet point with **bold text**
- Second point with *italic text*
- Third point with ***bold and italic***
- Fourth point with ___underlined text___

Additional paragraph with **mixed** *formatting* and ___underlines___.

---
layout: Two Content
title: Two Content Layout Test
sections:
  - title: Left Side Content
    content:
      - "**Feature A** details"
      - "*Feature B* information"
      - "***Critical*** updates"
  - title: Right Side Content
    content:
      - "___Important___ notices"
      - "**Security** measures"
      - "*Performance* metrics"
---

Content from Two Content structured frontmatter above.

---
layout: Four Columns
title: Four Column Layout **Comprehensive** Test
columns:
  - title: Performance
    content: "**Fast processing** with optimized algorithms and *sub-millisecond* response times"
  - title: Security
    content: "***Enterprise-grade*** encryption with ___SOC2___ and GDPR compliance"
  - title: Usability
    content: "*Intuitive* interface with **minimal** learning curve and comprehensive docs"
  - title: Cost
    content: "___Transparent___ pricing with **flexible** plans and *proven* ROI"
---

Content from Four Columns structured frontmatter above.

---
layout: table
style: dark_blue_white_text
row_style: alternating_light_gray
border_style: thin_gray
---
# Table Slide with **Formatted** Content

| **Feature** | *Status* | ___Priority___ |
| Authentication | **Complete** | *High* |
| User Management | ***In Progress*** | ___Medium___ |
| Reporting | *Planned* | **Low** |
| API Integration | ___Blocked___ | ***Critical*** |

---
layout: Section Header
---
# Section Break: **Testing** *Complete*

This section demonstrates ___section header___ layout with **formatting** and serves as a divider between major topics.

---
layout: Title Only
---
# Title Only Layout: **Bold** *Italic* ___Underline___

---
layout: Picture with Caption
title: Image Support **Demonstration**
media:
  image_path: "assets/non_existent_image.png"  # Non-existent - triggers PlaceKitten fallback
  alt_text: "System architecture diagram with main components"
  caption: "Smart image fallback with ***professional*** styling"
  description: |
    This slide demonstrates PlaceKitten integration with:
    • **Automatic fallback** when images are missing
    • *Professional grayscale* styling for business presentations
    • ***Smart cropping*** with face detection and rule-of-thirds
    • ___Consistent caching___ for optimal performance
---

---
layout: Picture with Caption
title: Valid Image **Test**
media:
  image_path: "src/placekitten/images/ACuteKitten-1.png"  # Valid PlaceKitten image
  alt_text: "Adorable kitten demonstrating valid image processing"
  caption: "Direct image insertion with ***processing*** pipeline"
  description: |
    This slide shows valid image handling:
    • **Direct image** validation and processing
    • *Automatic resizing* to placeholder dimensions
    • ***High-quality*** output with caching
    • ___Accessibility support___ with alt text
---

---
layout: Comparison
title: Comparison Layout **Full** Test
comparison:
  left:
    title: Option A Benefits
    content: "**Cost effective** solution with *rapid* deployment and ***proven*** technology"
  right:
    title: Option B Benefits
    content: "___Advanced___ features with **future-proof** architecture and *scalable* design"
---

Content from Comparison structured frontmatter above.

---
layout: Content with Caption
---
# Content with Caption Test

## Main Content
This layout demonstrates content with caption functionality:

- **Primary** content area
- *Secondary* information
- ***Important*** notes

Caption area with ___formatted___ text and **emphasis**.

---
layout: Blank
---
# Blank Layout Test

This tests the blank layout with minimal structure and **formatted** content.
