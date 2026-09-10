"""
Tests for DOCX Loading and Parser robustness.
"""

import os
import pytest
from parser.docx_parser import DocxParser
from docx import Document


def test_load_valid_docx():
    parser = DocxParser("samples/input.docx").load()
    summary = parser.get_summary()
    assert summary["paragraph_count"] > 0
    assert summary["estimated_pages"] >= 1
    assert not summary["is_empty"]


def test_load_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        DocxParser("samples/does_not_exist_9999.docx").load()


def test_empty_docx_handling(tmp_path):
    empty_path = str(tmp_path / "empty.docx")
    doc = Document()
    doc.save(empty_path)

    parser = DocxParser(empty_path).load()
    summary = parser.get_summary()
    assert summary["is_empty"] is True
    assert summary["paragraph_count"] == 0
