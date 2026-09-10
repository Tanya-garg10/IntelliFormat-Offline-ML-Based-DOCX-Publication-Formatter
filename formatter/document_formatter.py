"""
Document Formatter Module
Applies publication styling specifications across paragraphs, tables, images, and page geometry.
Guarantees absolute preservation of text (zero content modification).
"""

import os
from typing import List, Dict, Any, Optional
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from .margins import MarginManager
from .styles import PublicationStyles, PUBLICATION_SPECS
from .headings import HeadingManager
from parser.docx_parser import DocxParser
from rules.confidence import HybridClassifier


class DocumentFormatter:
    """End-to-end formatter applying academic publication specifications to DOCX manuscripts."""

    def __init__(
        self,
        input_path: str,
        output_path: str = "output/formatted_book.docx",
        include_toc: bool = True,
        custom_specs: Optional[Dict[str, Any]] = None,
    ):
        self.input_path = os.path.abspath(input_path)
        self.output_path = os.path.abspath(output_path)
        self.include_toc = include_toc
        self.custom_specs = custom_specs or {}
        self.doc: Optional[Document] = None
        self.stats: Dict[str, Any] = {}

    def format(
        self,
        classifications: Optional[List[Dict[str, Any]]] = None,
        progress_callback=None,
    ) -> str:
        """
        Executes complete formatting pipeline.
        Returns path to generated output DOCX.
        """
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file not found: {self.input_path}")

        # Load fresh document copy
        self.doc = Document(self.input_path)

        # 1. Apply Margins
        top_cm = self.custom_specs.get("top_margin_cm", MarginManager.TOP_MARGIN_CM)
        bottom_cm = self.custom_specs.get("bottom_margin_cm", MarginManager.BOTTOM_MARGIN_CM)
        left_cm = self.custom_specs.get("left_margin_cm", MarginManager.LEFT_MARGIN_CM)
        right_cm = self.custom_specs.get("right_margin_cm", MarginManager.RIGHT_MARGIN_CM)

        MarginManager.apply_margins(
            self.doc,
            top_cm=top_cm,
            bottom_cm=bottom_cm,
            left_cm=left_cm,
            right_cm=right_cm,
        )

        if progress_callback:
            progress_callback(15, "Standardized page margins and single-column geometry")

        # 2. Parse & Classify if not provided
        if classifications is None:
            parser = DocxParser(self.input_path).load()
            classifier = HybridClassifier()
            classifications = classifier.classify_document(parser.paragraphs)

        total_paras = len(self.doc.paragraphs)
        headings_for_toc = []

        # 3. Format Paragraphs
        processed_count = 0
        style_distribution = {}

        for i, p in enumerate(self.doc.paragraphs):
            cls_item = classifications[i] if i < len(classifications) else {"final_class": "BODY"}
            target_cls = cls_item.get("final_class", "BODY")

            style_spec = PUBLICATION_SPECS.get(target_cls, PUBLICATION_SPECS["BODY"]).copy()

            # Override with any custom user settings if provided
            if target_cls == "BODY" and "body_line_spacing" in self.custom_specs:
                style_spec["line_spacing"] = float(self.custom_specs["body_line_spacing"])

            # Apply style without touching underlying text
            PublicationStyles.apply_style_to_paragraph(p, style_spec)

            # Collect for Table of Contents
            if target_cls in ("CHAPTER_HEADING", "SUBHEADING") and p.text.strip():
                headings_for_toc.append({
                    "text": p.text.strip(),
                    "final_class": target_cls,
                    "estimated_page": max(1, round(processed_count / 15) + 1),
                })

            style_distribution[target_cls] = style_distribution.get(target_cls, 0) + 1
            processed_count += 1

            if progress_callback and i % max(1, total_paras // 10) == 0:
                pct = 20 + int((i / total_paras) * 60)
                progress_callback(pct, f"Formatting paragraph {i+1} of {total_paras}")

        # 4. Format Tables (Preserve 100% of data, standard table styling)
        for t_idx, table in enumerate(self.doc.tables):
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            for r_idx, row in enumerate(table.rows):
                # Header row formatting
                is_header = (r_idx == 0)
                for cell in row.cells:
                    for cp in cell.paragraphs:
                        cp.paragraph_format.line_spacing = 1.15
                        cp.paragraph_format.space_before = Pt(2.0)
                        cp.paragraph_format.space_after = Pt(2.0)
                        cp.paragraph_format.first_line_indent = Cm(0.0)
                        for crun in cp.runs:
                            crun.font.name = "Times New Roman"
                            crun.font.size = Pt(10.0)
                            crun.font.bold = is_header
                            crun.font.color.rgb = RGBColor(0, 0, 0)

        if progress_callback:
            progress_callback(85, f"Formatted {len(self.doc.tables)} tables with publication grid")

        # 5. Optional Table of Contents Insertion
        if self.include_toc and len(headings_for_toc) >= 2:
            # Find insertion point (typically after Title/Author)
            insert_idx = 1
            for idx, c in enumerate(classifications[:10]):
                if c.get("final_class") in ("TITLE", "AUTHOR"):
                    insert_idx = idx + 1
            HeadingManager.generate_table_of_contents(self.doc, headings_for_toc, insert_position_index=insert_idx)

        # 6. Save formatted publication DOCX
        out_dir = os.path.dirname(self.output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        self.doc.save(self.output_path)

        if progress_callback:
            progress_callback(100, "Publication DOCX generated successfully")

        self.stats = {
            "output_path": self.output_path,
            "paragraphs_formatted": processed_count,
            "tables_formatted": len(self.doc.tables),
            "style_distribution": style_distribution,
            "toc_included": self.include_toc,
            "file_size_bytes": os.path.getsize(self.output_path),
        }
        return self.output_path
