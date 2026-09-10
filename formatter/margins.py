"""
Margin Manager Module
Applies standardized publication page dimensions, margins, and gutter settings.
"""

from docx import Document
from docx.shared import Cm, Pt
from docx.enum.section import WD_SECTION_START, WD_ORIENT


class MarginManager:
    """Configures page geometry and margins matching strict publication specifications."""

    # Exact publication specifications:
    TOP_MARGIN_CM = 1.52
    BOTTOM_MARGIN_CM = 1.52
    LEFT_MARGIN_CM = 1.97
    RIGHT_MARGIN_CM = 1.96
    GUTTER_CM = 0.0  # Left gutter orientation

    @classmethod
    def apply_margins(
        cls,
        doc: Document,
        top_cm: float = TOP_MARGIN_CM,
        bottom_cm: float = BOTTOM_MARGIN_CM,
        left_cm: float = LEFT_MARGIN_CM,
        right_cm: float = RIGHT_MARGIN_CM,
        gutter_cm: float = GUTTER_CM,
    ) -> None:
        """Applies margins to all sections in the document."""
        for section in doc.sections:
            section.top_margin = Cm(top_cm)
            section.bottom_margin = Cm(bottom_cm)
            section.left_margin = Cm(left_cm)
            section.right_margin = Cm(right_cm)
            section.gutter = Cm(gutter_cm)
            section.orientation = WD_ORIENT.PORTRAIT
            section.different_first_page_header_footer = False

            # Ensure single-column layout
            try:
                sectPr = section._sectPr
                cols = sectPr.xpath("./w:cols")
                if cols:
                    cols[0].set(
                        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num",
                        "1",
                    )
            except Exception:
                pass
