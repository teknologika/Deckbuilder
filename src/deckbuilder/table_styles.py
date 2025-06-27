"""
Table styling definitions for PowerPoint presentations.

This module contains all the predefined table styles including header styles,
row styles, and border styles that can be applied to tables in presentations.
"""

from pptx.dml.color import RGBColor
from pptx.util import Cm

# Table header styling definitions
TABLE_HEADER_STYLES = {
    "dark_blue_white_text": {"bg": RGBColor(68, 114, 196), "text": RGBColor(255, 255, 255)},
    "light_blue_dark_text": {"bg": RGBColor(217, 237, 255), "text": RGBColor(51, 51, 51)},
    "dark_gray_white_text": {"bg": RGBColor(102, 102, 102), "text": RGBColor(255, 255, 255)},
    "light_gray_dark_text": {"bg": RGBColor(242, 242, 242), "text": RGBColor(51, 51, 51)},
    "white_dark_text": {"bg": RGBColor(255, 255, 255), "text": RGBColor(51, 51, 51)},
    "accent_color_white_text": {"bg": RGBColor(68, 114, 196), "text": RGBColor(255, 255, 255)},
}

# Table row styling definitions
TABLE_ROW_STYLES = {
    "alternating_light_gray": {"primary": RGBColor(255, 255, 255), "alt": RGBColor(248, 248, 248)},
    "alternating_light_blue": {"primary": RGBColor(255, 255, 255), "alt": RGBColor(240, 248, 255)},
    "solid_white": {"primary": RGBColor(255, 255, 255), "alt": RGBColor(255, 255, 255)},
    "solid_light_gray": {"primary": RGBColor(248, 248, 248), "alt": RGBColor(248, 248, 248)},
    "no_fill": {"primary": None, "alt": None},
}

# Table border styling definitions
TABLE_BORDER_STYLES = {
    "thin_gray": {"width": Cm(0.025), "color": RGBColor(166, 166, 166), "style": "all"},
    "thick_gray": {"width": Cm(0.05), "color": RGBColor(166, 166, 166), "style": "all"},
    "header_only": {"width": Cm(0.025), "color": RGBColor(166, 166, 166), "style": "header"},
    "outer_only": {"width": Cm(0.025), "color": RGBColor(166, 166, 166), "style": "outer"},
    "no_borders": {"width": Cm(0), "color": None, "style": "none"},
}
