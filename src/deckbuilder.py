import os
import shutil
import json
import yaml
import re
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
try:
    from table_styles import TABLE_HEADER_STYLES, TABLE_ROW_STYLES, TABLE_BORDER_STYLES
    from slide_layouts import DEFAULT_LAYOUTS, DEFAULT_PPT_LAYOUTS
except ImportError:
    # Fallback values if modules don't exist
    TABLE_HEADER_STYLES = {
        "dark_blue_white_text": {"bg": RGBColor(46, 89, 132), "text": RGBColor(255, 255, 255)}
    }
    TABLE_ROW_STYLES = {
        "alternating_light_gray": {"primary": RGBColor(255, 255, 255), "alt": RGBColor(240, 240, 240)}
    }
    TABLE_BORDER_STYLES = {
        "thin_gray": {"width": Pt(1), "color": RGBColor(128, 128, 128), "style": "all"}
    }
    DEFAULT_LAYOUTS = {"content": "titleandcontent", "title": "titleslide"}
    DEFAULT_PPT_LAYOUTS = {"titleandcontent": 1, "titleslide": 0}

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Deckbuilder:

    def __init__(self):
        self.template_path = os.getenv('DECK_TEMPLATE_FOLDER')
        self.template_name = os.getenv('DECK_TEMPLATE_NAME')
        self.output_folder = os.getenv('DECK_OUTPUT_FOLDER')
        self.prs = Presentation()
        
        # Ensure default template exists in templates folder
        self._check_template_exists(self.template_name or 'default')
        
    def _check_template_exists(self, templateName: str):
        """Check if template exists in the templates folder and copy if needed."""

        # Use self.template_name if available, otherwise use default
        if not templateName or templateName == 'default':
            templateName = self.template_name or 'default'

        # Ensure templateName ends with .pptx
        if not templateName.endswith('.pptx'):
            templateName += '.pptx'
        
        if self.template_path:
            try:
                # Create templates folder if it doesn't exist
                os.makedirs(self.template_path, exist_ok=True)
                
                # Check if template exists in templates folder
                default_template = os.path.join(self.template_path, templateName)
                if not os.path.exists(default_template):
                    # Copy from src/default.pptx
                    src_template = os.path.join(os.path.dirname(__file__), 'default.pptx')
                    if os.path.exists(src_template):
                        shutil.copy2(src_template, default_template)
            except (OSError, IOError):
                # Handle file operation errors silently
                pass
    
    
    def create_presentation(self, templateName: str = "default", fileName: str = "Sample_Presentation") -> str:
        # Check template exists
        self._check_template_exists(templateName)
        
        # Create deck with template
        if not templateName.endswith('.pptx'):
            templateName += '.pptx'
        if self.template_path:
            template_path = os.path.join(self.template_path, templateName)
            self.prs = Presentation(template_path) if os.path.exists(template_path) else Presentation()
        else:
            self.prs = Presentation()
        
        self._clear_slides()

        return f"Creating presentation: {fileName}"


    def write_presentation(self, fileName: str = "Sample_Presentation") -> str:
        """Writes the presentation to disk with versioning."""
        # Get output folder from environment or use default
        output_folder = self.output_folder or '.'
        
        # Ensure output folder exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Create base filename with .latest.pptx extension
        base_name = f"{fileName}.latest.pptx"
        latest_file = os.path.join(output_folder, base_name)
        
        # Handle versioning if file exists
        if os.path.exists(latest_file):
            # Find the highest version number
            version_num = 1
            while True:
                version_file = os.path.join(output_folder, f"{fileName}.latest.pptx.v{version_num:02d}.pptx")
                if not os.path.exists(version_file):
                    break
                version_num += 1
            
            # Rename current latest to versioned file
            os.rename(latest_file, version_file)
        
        # Write the latest file
        self.prs.save(latest_file)
        
        return f"Successfully created presentation: {os.path.basename(latest_file)}"

    def add_slide_from_json(self, json_data) -> str:
        """
        Add a slide to the presentation using JSON data.
        
        Args:
            json_data: JSON string or dictionary containing slide data
            
        Returns:
            Success message
        """
        try:
            # Handle both string and dictionary inputs
            if isinstance(json_data, str):
                # Parse JSON data - handle potential double encoding
                data = json.loads(json_data)
                
                # If the result is still a string, parse it again
                if isinstance(data, str):
                    data = json.loads(data)
            else:
                # Already a dictionary
                data = json_data
            
            # Handle different JSON formats
            if "slides" in data:
                # Multiple slides format
                for slide_data in data["slides"]:
                    self._add_slide(slide_data)
            elif "presentation" in data and "slides" in data["presentation"]:
                # Presentation wrapper format
                for slide_data in data["presentation"]["slides"]:
                    self._add_slide(slide_data)
            else:
                # Single slide format
                self._add_slide(data)
                
            return "Successfully added slide(s) from JSON data"
            
        except json.JSONDecodeError as e:
            return f"Error parsing JSON: {str(e)}"
        except Exception as e:
            return f"Error adding slide: {str(e)}"

    def _clear_slides(self):
        """Clear all slides from the presentation."""
        slide_count = len(self.prs.slides)
        for i in range(slide_count - 1, -1, -1):
            rId = self.prs.slides._sldIdLst[i].rId
            self.prs.part.drop_rel(rId)
            del self.prs.slides._sldIdLst[i]

    def _add_slide(self, slide_data: dict):
        """
        Add a single slide to the presentation based on slide data.
        
        Args:
            slide_data: Dictionary containing slide information
        """
        # Get slide type and determine layout
        slide_type = slide_data.get("type", "content")
        layout_name = DEFAULT_LAYOUTS.get(slide_type, "titleandcontent")
        layout_index = DEFAULT_PPT_LAYOUTS.get(layout_name, 1)
        
        slide_layout = self.prs.slide_layouts[layout_index]
        slide = self.prs.slides.add_slide(slide_layout)
        
        # Add title if provided
        if "title" in slide_data and slide.shapes.title:
            slide.shapes.title.text = slide_data["title"]
        
        # Add subtitle for title slides
        if "subtitle" in slide_data and slide_type == "title":
            for shape in slide.placeholders:
                if shape.placeholder_format.idx == 1:  # Subtitle placeholder
                    shape.text = slide_data["subtitle"]
                    break
        
        # Handle rich content
        if "rich_content" in slide_data:
            self._add_rich_content_to_slide(slide, slide_data["rich_content"])
        elif "content" in slide_data:
            # Fallback to simple content (backwards compatibility)
            self._add_simple_content_to_slide(slide, slide_data["content"])
        
        # Add table if provided
        if "table" in slide_data:
            self._add_table_to_slide(slide, slide_data["table"])


    def _add_rich_content_to_slide(self, slide, rich_content: list):
        """Add rich content blocks to a slide with improved formatting"""
        # Find the content placeholder
        content_placeholder = None
        for shape in slide.placeholders:
            if shape.placeholder_format.idx == 1:  # Content placeholder
                content_placeholder = shape
                break
        
        if not content_placeholder:
            return
        
        # Clear existing content
        content_placeholder.text = ""
        text_frame = content_placeholder.text_frame
        text_frame.clear()
        text_frame.word_wrap = True
        
        # Set margins for better spacing
        text_frame.margin_left = Cm(0.25)
        text_frame.margin_right = Cm(0.25)
        text_frame.margin_top = Cm(0.25)
        text_frame.margin_bottom = Cm(0.25)
        
        # Add each content block with proper hierarchy
        first_content = True
        for block in rich_content:
            if "heading" in block:
                p = text_frame.add_paragraph()
                p.text = block["heading"]
                p.font.bold = True
                p.space_after = Pt(6)
                p.space_before = Pt(12) if not first_content else Pt(0)
                
            elif "paragraph" in block:
                p = text_frame.add_paragraph()
                p.text = block["paragraph"]
                p.space_after = Pt(6)
                p.space_before = Pt(3)
                
            elif "bullets" in block:
                
                # Get bullet levels if available, otherwise default to level 1
                bullet_levels = block.get("bullet_levels", [1] * len(block["bullets"]))
                
                for bullet_idx, bullet in enumerate(block["bullets"]):
                    p = text_frame.add_paragraph()
                    p.text = bullet
                    
                    # Use the parsed bullet level
                    bullet_level = bullet_levels[bullet_idx] if bullet_idx < len(bullet_levels) else 1
                    p.level = bullet_level
                    
                    # Set spacing based on level
                    if bullet_level == 1:
                        p.space_after = Pt(3)
                    else:  # Level 2+ (sub-bullets)
                        p.space_after = Pt(2)
            
            first_content = False

    def _add_simple_content_to_slide(self, slide, content):
        """Add simple content to slide (backwards compatibility)"""
        for shape in slide.placeholders:
            if shape.placeholder_format.idx == 1:  # Content placeholder
                if isinstance(content, str):
                    shape.text = content
                elif isinstance(content, list):
                    shape.text = "\n".join(content)
                break

    def _add_table_to_slide(self, slide, table_data):
        """
        Add a styled table to a slide.
        
        Args:
            slide: The slide to add the table to
            table_data: Dictionary containing table data and styling options
        """
        # Get table data - support both 'data' and 'rows' keys for backwards compatibility
        data = table_data.get("data", table_data.get("rows", []))
        if not data:
            return
        
        # Get styling options
        header_style = table_data.get("header_style", "dark_blue_white_text")
        row_style = table_data.get("row_style", "alternating_light_gray")
        border_style = table_data.get("border_style", "thin_gray")
        custom_colors = table_data.get("custom_colors", {})
        
        # Find content placeholder or create table in available space
        content_placeholder = None
        for shape in slide.placeholders:
            if shape.placeholder_format.idx == 1:  # Content placeholder
                content_placeholder = shape
                break
        
        if content_placeholder:
            # Remove placeholder and create table in its place
            left = content_placeholder.left
            top = content_placeholder.top
            width = content_placeholder.width
            height = content_placeholder.height
            
            # Remove the placeholder
            sp = content_placeholder._element
            sp.getparent().remove(sp)
        else:
            # Default positioning if no placeholder found
            left = Cm(2.5)
            top = Cm(5)
            width = Cm(20)
            height = Cm(12)
        
        # Create the table
        rows = len(data)
        cols = len(data[0]) if data else 1
        
        table = slide.shapes.add_table(rows, cols, left, top, width, height).table
        
        # Apply table data
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                cell = table.cell(row_idx, col_idx)
                cell.text = str(cell_data)
        
        # Apply styling
        self._apply_table_styling(table, header_style, row_style, border_style, custom_colors)

    def _apply_table_styling(self, table, header_style, row_style, border_style, custom_colors):
        """
        Apply styling to a table.
        
        Args:
            table: The table object to style
            header_style: Header style name
            row_style: Row style name
            border_style: Border style name
            custom_colors: Dictionary of custom color overrides
        """
        # Apply header styling
        if header_style in TABLE_HEADER_STYLES:
            header_colors = TABLE_HEADER_STYLES[header_style]
            
            # Override with custom colors if provided
            bg_color = self._parse_custom_color(custom_colors.get("header_bg")) or header_colors["bg"]
            text_color = self._parse_custom_color(custom_colors.get("header_text")) or header_colors["text"]
            
            # Style header row (first row)
            for col_idx in range(len(table.columns)):
                cell = table.cell(0, col_idx)
                # Set background color
                cell.fill.solid()
                cell.fill.fore_color.rgb = bg_color
                
                # Set text color and formatting
                for paragraph in cell.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = text_color
                        run.font.bold = True
        
        # Apply row styling
        if row_style in TABLE_ROW_STYLES and len(table.rows) > 1:
            row_colors = TABLE_ROW_STYLES[row_style]
            
            # Override with custom colors if provided
            primary_color = self._parse_custom_color(custom_colors.get("primary_row")) or row_colors["primary"]
            alt_color = self._parse_custom_color(custom_colors.get("alt_row")) or row_colors["alt"]
            
            # Style data rows (skip header row)
            for row_idx in range(1, len(table.rows)):
                is_alt_row = (row_idx - 1) % 2 == 1
                bg_color = alt_color if is_alt_row else primary_color
                
                if bg_color is not None:
                    for col_idx in range(len(table.columns)):
                        cell = table.cell(row_idx, col_idx)
                        cell.fill.solid()
                        cell.fill.fore_color.rgb = bg_color
        
        # Apply border styling
        if border_style in TABLE_BORDER_STYLES:
            self._apply_table_borders(table, TABLE_BORDER_STYLES[border_style], custom_colors)

    def _apply_table_borders(self, table, border_config, custom_colors):
        """
        Apply border styling to a table.
        
        Args:
            table: The table object
            border_config: Border configuration dictionary
            custom_colors: Custom color overrides
        """
        border_width = border_config["width"]
        border_color = self._parse_custom_color(custom_colors.get("border_color")) or border_config["color"]
        border_style = border_config["style"]
        
        if border_style == "none" or border_width.cm == 0:
            return
        
        # Apply borders based on style
        for row_idx in range(len(table.rows)):
            for col_idx in range(len(table.columns)):
                cell = table.cell(row_idx, col_idx)
                
                if border_style == "all":
                    # All borders
                    self._set_cell_borders(cell, border_width, border_color, all_sides=True)
                elif border_style == "header" and row_idx == 0:
                    # Only header bottom border
                    self._set_cell_borders(cell, border_width, border_color, bottom=True)
                elif border_style == "outer":
                    # Only outer borders
                    is_top = row_idx == 0
                    is_bottom = row_idx == len(table.rows) - 1
                    is_left = col_idx == 0
                    is_right = col_idx == len(table.columns) - 1
                    
                    self._set_cell_borders(cell, border_width, border_color, 
                                         top=is_top, bottom=is_bottom, 
                                         left=is_left, right=is_right)

    def _set_cell_borders(self, cell, width, color, all_sides=False, 
                         top=False, bottom=False, left=False, right=False):
        """
        Set borders for a table cell.
        
        Args:
            cell: The table cell
            width: Border width
            color: Border color
            all_sides: Apply to all sides
            top, bottom, left, right: Apply to specific sides
        """
        if color is None:
            return
            
        if all_sides:
            top = bottom = left = right = True
        
        # Note: python-pptx has limited border support
        # This is a simplified implementation
        try:
            if hasattr(cell, 'border'):
                if top and hasattr(cell.border, 'top'):
                    cell.border.top.color.rgb = color
                    cell.border.top.width = width
                if bottom and hasattr(cell.border, 'bottom'):
                    cell.border.bottom.color.rgb = color
                    cell.border.bottom.width = width
                if left and hasattr(cell.border, 'left'):
                    cell.border.left.color.rgb = color
                    cell.border.left.width = width
                if right and hasattr(cell.border, 'right'):
                    cell.border.right.color.rgb = color
                    cell.border.right.width = width
        except (AttributeError, Exception):
            # Borders not fully supported in python-pptx, skip silently
            pass

    def _parse_custom_color(self, color_value):
        """
        Parse a custom color value (hex string) to RGBColor.
        
        Args:
            color_value: Hex color string (e.g., "#FF0000")
            
        Returns:
            RGBColor object or None if invalid
        """
        if not color_value or not isinstance(color_value, str):
            return None
        
        try:
            # Remove # if present
            color_value = color_value.lstrip('#')
            
            # Convert hex to RGB
            if len(color_value) == 6:
                r = int(color_value[0:2], 16)
                g = int(color_value[2:4], 16)
                b = int(color_value[4:6], 16)
                return RGBColor(r, g, b)
        except (ValueError, TypeError):
            pass
        
        return None

    def parse_markdown_with_frontmatter(self, markdown_content: str) -> list:
        """
        Parse markdown content with frontmatter into slide data.
        
        Args:
            markdown_content: Markdown string with frontmatter slide definitions
            
        Returns:
            List of slide dictionaries ready for _add_slide()
        """
        slides = []
        
        # Split content by frontmatter boundaries
        slide_blocks = re.split(r'^---\s*$', markdown_content, flags=re.MULTILINE)
        
        i = 0
        while i < len(slide_blocks):
            # Skip empty blocks
            if not slide_blocks[i].strip():
                i += 1
                continue
                
            # Look for frontmatter + content pairs
            if i + 1 < len(slide_blocks):
                try:
                    frontmatter_raw = slide_blocks[i].strip()
                    content_raw = slide_blocks[i + 1].strip() if i + 1 < len(slide_blocks) else ""
                    
                    # Parse frontmatter
                    slide_config = yaml.safe_load(frontmatter_raw) or {}
                    
                    # Parse markdown content into slide data
                    slide_data = self._parse_slide_content(content_raw, slide_config)
                    slides.append(slide_data)
                    
                    i += 2  # Skip both frontmatter and content blocks
                except yaml.YAMLError:
                    # If YAML parsing fails, treat as regular content
                    content_raw = slide_blocks[i].strip()
                    slide_data = self._parse_slide_content(content_raw, {})
                    slides.append(slide_data)
                    i += 1
            else:
                # Single block without frontmatter
                content_raw = slide_blocks[i].strip()
                slide_data = self._parse_slide_content(content_raw, {})
                slides.append(slide_data)
                i += 1
        
        return slides

    def _parse_slide_content(self, content: str, config: dict) -> dict:
        """Convert markdown content + config into slide data dict with mixed content support"""
        slide_data = {
            "type": config.get("layout", "content"),
            **config  # Include all frontmatter as slide properties
        }
        
        if not content.strip():
            return slide_data
            
        lines = content.split('\n')
        
        # Extract title (first # header) 
        title_found = False
        content_lines = []
        
        for line in lines:
            if line.startswith('# ') and not title_found:
                slide_data["title"] = line[2:].strip()
                title_found = True
            elif line.startswith('## ') and slide_data["type"] == "title":
                slide_data["subtitle"] = line[3:].strip()
            else:
                content_lines.append(line)
        
        # Parse mixed content based on slide type
        if slide_data["type"] == "table":
            slide_data["table"] = self._parse_markdown_table('\n'.join(content_lines), config)
        elif slide_data["type"] != "title":  # Content slides get rich content
            rich_content = self._parse_rich_content('\n'.join(content_lines))
            if rich_content:
                slide_data["rich_content"] = rich_content
        
        return slide_data

    def _parse_rich_content(self, content: str) -> list:
        """Parse mixed markdown content into structured content blocks with better hierarchy"""
        blocks = []
        lines = content.split('\n')
        current_block = None
        
        for line in lines:
            original_line = line
            line = line.strip()
            if not line:
                continue
                
            # Handle nested bullet points by preserving indentation
            if line.startswith('- ') or line.startswith('* '):
                # Determine indentation level
                indent_level = len(original_line) - len(original_line.lstrip())
                bullet_text = line[2:].strip()
                
                if not current_block or "bullets" not in current_block:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {"bullets": [], "bullet_levels": []}
                
                current_block["bullets"].append(bullet_text)
                # Map indentation to bullet levels (0 indent = level 1, 2+ spaces = level 2, etc.)
                level = 1 if indent_level < 2 else 2
                current_block["bullet_levels"].append(level)
                
            elif line.startswith('## '):  # Subheading
                if current_block:
                    blocks.append(current_block)
                current_block = {
                    "heading": line[3:].strip(),
                    "level": 2
                }
                
            elif line.startswith('### '):  # Sub-subheading
                if current_block:
                    blocks.append(current_block)
                current_block = {
                    "heading": line[4:].strip(),
                    "level": 3
                }
                
            else:  # Regular paragraph
                if not current_block or "paragraph" not in current_block:
                    if current_block:
                        blocks.append(current_block)
                    current_block = {"paragraph": line}
                else:
                    current_block["paragraph"] += " " + line
        
        if current_block:
            blocks.append(current_block)
            
        return blocks

    def _parse_markdown_table(self, content: str, config: dict) -> dict:
        """Extract table from markdown and apply styling config"""
        table_data = {
            "data": [],
            "header_style": config.get("style", "dark_blue_white_text"),
            "row_style": config.get("row_style", "alternating_light_gray"),
            "border_style": config.get("border_style", "thin_gray"),
            "custom_colors": config.get("custom_colors", {})
        }
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for line in lines:
            if line.startswith('|') and line.endswith('|'):
                # Parse table row
                cells = [cell.strip() for cell in line[1:-1].split('|')]
                table_data["data"].append(cells)
            elif '|' in line and not line.startswith('|'):
                # Handle tables without outer pipes
                cells = [cell.strip() for cell in line.split('|')]
                table_data["data"].append(cells)
            elif line.startswith('---') or line.startswith('==='):
                # Skip separator lines
                continue
        
        return table_data

def get_deckbuilder_client():
    # Return singleton instance of Deckbuilder
    return Deckbuilder()