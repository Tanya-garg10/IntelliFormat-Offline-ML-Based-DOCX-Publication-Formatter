"""
Main DocxParser module.
Extracts document structure, paragraphs, tables, images, and section layout metrics.
Designed for high performance on large (400+ pages) manuscripts.
"""

import os
from typing import List, Dict, Any, Optional
from docx import Document
from .paragraph_parser import ParagraphParser, ParagraphInfo
from .table_parser import TableParser, TableInfo
from .image_parser import ImageParser, ImageInfo


class DocxParser:
    """High-performance parser for Microsoft Word .docx manuscripts."""

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Manuscript file not found at: {file_path}")
        self.file_path = file_path
        self.doc: Optional[Document] = None
        self.paragraphs: List[ParagraphInfo] = []
        self.tables: List[TableInfo] = []
        self.images: List[ImageInfo] = []
        self.stats: Dict[str, Any] = {}

    def load(self) -> "DocxParser":
        """Loads and parses the document."""
        try:
            self.doc = Document(self.file_path)
        except Exception as e:
            raise ValueError(f"Corrupted or invalid DOCX manuscript: {str(e)}") from e

        # Extract paragraphs
        raw_paras = self.doc.paragraphs
        parsed_paras: List[ParagraphInfo] = []
        total_words = 0
        total_chars = 0

        for i, p in enumerate(raw_paras):
            info = ParagraphParser.parse_paragraph(p, index=i)
            parsed_paras.append(info)
            w_count = len(info.clean_text.split())
            total_words += w_count
            total_chars += len(info.clean_text)

        self.paragraphs = parsed_paras

        # Extract tables
        parsed_tables: List[TableInfo] = []
        for t_idx, tbl in enumerate(self.doc.tables):
            t_info = TableParser.parse_table(tbl, index=t_idx)
            parsed_tables.append(t_info)
        self.tables = parsed_tables

        # Extract images
        self.images = ImageParser.extract_images(self.doc)

        # Estimate pages: Standard academic/book formatting has ~280-320 words per page
        # plus table/figure spacing offsets
        estimated_pages = max(1, round(total_words / 280) + len(self.tables) + len(self.images))

        # Check for empty document
        has_content = bool(total_chars > 0 or self.tables or self.images)

        self.stats = {
            "filename": os.path.basename(self.file_path),
            "file_size_bytes": os.path.getsize(self.file_path),
            "paragraph_count": len(self.paragraphs),
            "non_empty_paragraphs": sum(1 for p in self.paragraphs if p.clean_text),
            "table_count": len(self.tables),
            "image_count": len(self.images),
            "total_words": total_words,
            "total_chars": total_chars,
            "estimated_pages": estimated_pages,
            "is_empty": not has_content,
        }
        return self

    def get_summary(self) -> Dict[str, Any]:
        return self.stats
