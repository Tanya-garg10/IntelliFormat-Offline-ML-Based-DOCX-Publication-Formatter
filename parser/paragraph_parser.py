"""
Paragraph parser module.
Extracts raw text, formatting metrics, runs, and layout properties from docx Paragraph elements.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_ALIGN_PARAGRAPH


@dataclass
class RunInfo:
    text: str
    font_name: Optional[str] = None
    font_size: Optional[float] = None  # in points
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color_rgb: Optional[str] = None


@dataclass
class ParagraphInfo:
    index: int
    text: str
    clean_text: str
    runs: List[RunInfo] = field(default_factory=list)
    style_name: str = "Normal"
    alignment: int = 0  # 0: Left, 1: Center, 2: Right, 3: Justify
    line_spacing: Optional[float] = 1.0
    space_before_pt: float = 0.0
    space_after_pt: float = 0.0
    first_line_indent_pt: float = 0.0
    font_family: str = "Times New Roman"
    font_size_pt: float = 12.0
    is_bold: bool = False
    is_italic: bool = False
    is_underline: bool = False
    is_all_caps: bool = False
    has_image: bool = False
    raw_docx_paragraph: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "text": self.text,
            "style_name": self.style_name,
            "alignment": self.alignment,
            "line_spacing": self.line_spacing,
            "space_before_pt": self.space_before_pt,
            "space_after_pt": self.space_after_pt,
            "first_line_indent_pt": self.first_line_indent_pt,
            "font_family": self.font_family,
            "font_size_pt": self.font_size_pt,
            "is_bold": self.is_bold,
            "is_italic": self.is_italic,
            "is_underline": self.is_underline,
            "is_all_caps": self.is_all_caps,
            "has_image": self.has_image,
        }


class ParagraphParser:
    """Extracts granular formatting and content info from docx.text.paragraph.Paragraph."""

    @staticmethod
    def parse_paragraph(paragraph: Paragraph, index: int) -> ParagraphInfo:
        text = paragraph.text or ""
        clean_text = text.strip()

        # Alignment mapping
        align_code = 0
        if paragraph.alignment is not None:
            val = paragraph.alignment
            if val == WD_ALIGN_PARAGRAPH.CENTER:
                align_code = 1
            elif val == WD_ALIGN_PARAGRAPH.RIGHT:
                align_code = 2
            elif val == WD_ALIGN_PARAGRAPH.JUSTIFY:
                align_code = 3
            else:
                align_code = 0

        # Spacing
        fmt = paragraph.paragraph_format
        line_spacing = 1.0
        if fmt.line_spacing is not None:
            try:
                line_spacing = float(fmt.line_spacing)
            except (ValueError, TypeError):
                line_spacing = 1.0

        space_before = 0.0
        if fmt.space_before is not None:
            try:
                space_before = float(fmt.space_before.pt)
            except Exception:
                space_before = 0.0

        space_after = 0.0
        if fmt.space_after is not None:
            try:
                space_after = float(fmt.space_after.pt)
            except Exception:
                space_after = 0.0

        first_line_indent = 0.0
        if fmt.first_line_indent is not None:
            try:
                first_line_indent = float(fmt.first_line_indent.pt)
            except Exception:
                first_line_indent = 0.0

        # Parse runs
        runs_info: List[RunInfo] = []
        total_chars = 0
        bold_chars = 0
        italic_chars = 0
        underline_chars = 0
        font_sizes: List[float] = []
        font_families: List[str] = []
        has_image = False

        for run in paragraph.runs:
            run_text = run.text or ""
            r_len = len(run_text)
            total_chars += r_len

            # Check for embedded drawing/image in run element
            try:
                xml_str = run._r.xml
                if "w:drawing" in xml_str or "w:pict" in xml_str:
                    has_image = True
            except Exception:
                pass

            f_name = run.font.name if run.font.name else None
            f_size = None
            if run.font.size is not None:
                try:
                    f_size = float(run.font.size.pt)
                except Exception:
                    f_size = None

            is_b = bool(run.bold)
            is_i = bool(run.italic)
            is_u = bool(run.underline)

            if is_b:
                bold_chars += r_len
            if is_i:
                italic_chars += r_len
            if is_u:
                underline_chars += r_len

            if f_size is not None and r_len > 0:
                font_sizes.extend([f_size] * r_len)
            if f_name and r_len > 0:
                font_families.extend([f_name] * r_len)

            color_hex = None
            if run.font.color and run.font.color.rgb:
                color_hex = str(run.font.color.rgb)

            runs_info.append(
                RunInfo(
                    text=run_text,
                    font_name=f_name,
                    font_size=f_size,
                    bold=is_b,
                    italic=is_i,
                    underline=is_u,
                    color_rgb=color_hex,
                )
            )

        # Aggregate metrics
        char_denominator = max(total_chars, 1)
        is_bold_majority = (bold_chars / char_denominator) >= 0.5
        is_italic_majority = (italic_chars / char_denominator) >= 0.5
        is_underline_majority = (underline_chars / char_denominator) >= 0.5

        # Check paragraph style defaults if runs don't specify
        style_name = paragraph.style.name if paragraph.style else "Normal"
        default_font_size = 12.0
        default_font_family = "Times New Roman"

        if paragraph.style and paragraph.style.font:
            if paragraph.style.font.size:
                try:
                    default_font_size = float(paragraph.style.font.size.pt)
                except Exception:
                    pass
            if paragraph.style.font.name:
                default_font_family = paragraph.style.font.name
            if paragraph.style.font.bold and not is_bold_majority:
                is_bold_majority = True

        effective_font_size = (
            sum(font_sizes) / len(font_sizes) if font_sizes else default_font_size
        )
        effective_font_family = (
            max(set(font_families), key=font_families.count)
            if font_families
            else default_font_family
        )

        is_all_caps = clean_text.isupper() if clean_text else False

        # Check paragraph xml for drawing if runs didn't trigger
        if not has_image:
            try:
                p_xml = paragraph._p.xml
                if "w:drawing" in p_xml or "w:pict" in p_xml:
                    has_image = True
            except Exception:
                pass

        return ParagraphInfo(
            index=index,
            text=text,
            clean_text=clean_text,
            runs=runs_info,
            style_name=style_name,
            alignment=align_code,
            line_spacing=line_spacing,
            space_before_pt=space_before,
            space_after_pt=space_after,
            first_line_indent_pt=first_line_indent,
            font_family=effective_font_family,
            font_size_pt=round(effective_font_size, 1),
            is_bold=is_bold_majority,
            is_italic=is_italic_majority,
            is_underline=is_underline_majority,
            is_all_caps=is_all_caps,
            has_image=has_image,
            raw_docx_paragraph=paragraph,
        )
