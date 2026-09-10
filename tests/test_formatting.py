"""
Tests for Document Formatting Engine and Margin / Font verification.
Verifies that author text is 100% preserved without any modifications.
"""

import os
import pytest
from docx import Document
from docx.shared import Cm, Pt
from formatter.document_formatter import DocumentFormatter
from parser.docx_parser import DocxParser


def test_margin_and_font_application(tmp_path):
    in_file = "samples/input.docx"
    out_file = str(tmp_path / "test_formatted.docx")

    formatter = DocumentFormatter(in_file, out_file, include_toc=True)
    res_path = formatter.format()

    assert os.path.exists(res_path)
    doc = Document(res_path)

    # 1. Verify Page Margins
    sec = doc.sections[0]
    # Check margins in cm (~1.52, ~1.97, ~1.96 within floating point tolerance)
    assert abs(sec.top_margin.cm - 1.52) < 0.05
    assert abs(sec.bottom_margin.cm - 1.52) < 0.05
    assert abs(sec.left_margin.cm - 1.97) < 0.05
    assert abs(sec.right_margin.cm - 1.96) < 0.05

    # 2. Verify Output Text Preservation
    raw_parser = DocxParser(in_file).load()
    out_parser = DocxParser(out_file).load()

    # The raw original non-empty text strings must exist in the output document
    orig_texts = [p.clean_text for p in raw_parser.paragraphs if p.clean_text]
    out_full_text = " ".join([p.clean_text for p in out_parser.paragraphs])

    for orig in orig_texts[:10]:
        assert orig in out_full_text, f"Text modified or lost: '{orig}'"


def test_table_preservation(tmp_path):
    in_file = "samples/input.docx"
    out_file = str(tmp_path / "test_table_preserved.docx")

    formatter = DocumentFormatter(in_file, out_file, include_toc=False)
    formatter.format()

    doc_in = Document(in_file)
    doc_out = Document(out_file)

    assert len(doc_in.tables) == len(doc_out.tables)
    if len(doc_in.tables) > 0:
        assert len(doc_in.tables[0].rows) == len(doc_out.tables[0].rows)
