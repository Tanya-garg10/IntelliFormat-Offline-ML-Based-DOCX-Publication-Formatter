"""
Publication Styles Module
Defines style dictionaries and helper methods to apply font and paragraph styles.
"""

from typing import Dict, Any
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

FONT_NAME_DEFAULT = "Times New Roman"
COLOR_BLACK = RGBColor(0, 0, 0)

PUBLICATION_SPECS: Dict[str, Dict[str, Any]] = {
    "TITLE": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 20.0,
        "bold": True,
        "italic": False,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "line_spacing": 1.15,
        "space_before_pt": 24.0,
        "space_after_pt": 12.0,
        "first_line_indent_cm": 0.0,
        "left_indent_cm": 0.0,
    },
    "AUTHOR": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 11.0,
        "bold": False,
        "italic": True,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "line_spacing": 1.15,
        "space_before_pt": 0.0,
        "space_after_pt": 18.0,
        "first_line_indent_cm": 0.0,
        "left_indent_cm": 0.0,
    },
    "CHAPTER_HEADING": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 16.0,
        "bold": True,
        "italic": False,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.LEFT,
        "line_spacing": 1.15,
        "space_before_pt": 18.0,
        "space_after_pt": 12.0,
        "first_line_indent_cm": 0.0,
        "left_indent_cm": 0.0,
    },
    "SUBHEADING": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 12.0,
        "bold": True,
        "italic": False,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.LEFT,
        "line_spacing": 1.15,
        "space_before_pt": 12.0,
        "space_after_pt": 6.0,
        "first_line_indent_cm": 0.0,
        "left_indent_cm": 0.0,
    },
    "BODY": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 12.0,
        "bold": False,
        "italic": False,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "line_spacing": 1.5,
        "space_before_pt": 0.0,
        "space_after_pt": 6.0,
        "first_line_indent_cm": 1.27,
        "left_indent_cm": 0.0,
    },
    "CAPTION": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 10.0,
        "bold": False,
        "italic": True,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "line_spacing": 1.15,
        "space_before_pt": 6.0,
        "space_after_pt": 12.0,
        "first_line_indent_cm": 0.0,
        "left_indent_cm": 0.0,
    },
    "REFERENCE": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 10.0,
        "bold": False,
        "italic": False,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "line_spacing": 1.15,
        "space_before_pt": 0.0,
        "space_after_pt": 4.0,
        "first_line_indent_cm": -1.27,  # Hanging indent
        "left_indent_cm": 1.27,
    },
    "NUMBERED_LIST": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 11.0,
        "bold": False,
        "italic": False,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.LEFT,
        "line_spacing": 1.15,
        "space_before_pt": 0.0,
        "space_after_pt": 3.0,
        "first_line_indent_cm": -0.63,
        "left_indent_cm": 1.27,
    },
    "BULLET_LIST": {
        "font_name": FONT_NAME_DEFAULT,
        "font_size_pt": 11.0,
        "bold": False,
        "italic": False,
        "color": COLOR_BLACK,
        "alignment": WD_ALIGN_PARAGRAPH.LEFT,
        "line_spacing": 1.15,
        "space_before_pt": 0.0,
        "space_after_pt": 3.0,
        "first_line_indent_cm": -0.63,
        "left_indent_cm": 1.27,
    },
}


class PublicationStyles:
    """Applies styles to individual python-docx Paragraph objects without altering text."""

    @staticmethod
    def apply_style_to_paragraph(paragraph, style_spec: Dict[str, Any]) -> None:
        p_fmt = paragraph.paragraph_format

        # Alignment
        if "alignment" in style_spec:
            paragraph.alignment = style_spec["alignment"]

        # Line spacing
        if "line_spacing" in style_spec:
            p_fmt.line_spacing = style_spec["line_spacing"]

        # Paragraph Spacing
        if "space_before_pt" in style_spec:
            p_fmt.space_before = Pt(style_spec["space_before_pt"])
        if "space_after_pt" in style_spec:
            p_fmt.space_after = Pt(style_spec["space_after_pt"])

        # Indentations
        if "first_line_indent_cm" in style_spec:
            p_fmt.first_line_indent = Cm(style_spec["first_line_indent_cm"])
        if "left_indent_cm" in style_spec:
            p_fmt.left_indent = Cm(style_spec["left_indent_cm"])

        # Apply run-level font properties to all existing runs
        font_name = style_spec.get("font_name", FONT_NAME_DEFAULT)
        font_size = style_spec.get("font_size_pt", 12.0)
        bold = style_spec.get("bold", False)
        italic = style_spec.get("italic", False)
        color = style_spec.get("color", COLOR_BLACK)

        # If paragraph has no runs but has text, add a run
        if not paragraph.runs and paragraph.text:
            text = paragraph.text
            paragraph.text = ""
            run = paragraph.add_run(text)
            runs = [run]
        else:
            runs = paragraph.runs

        for run in runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.font.color.rgb = color
            # Only set bold/italic if spec explicitly mandates or keep run-level emphasis for body
            if style_spec.get("override_run_emphasis", True):
                run.bold = bold
                run.italic = italic
