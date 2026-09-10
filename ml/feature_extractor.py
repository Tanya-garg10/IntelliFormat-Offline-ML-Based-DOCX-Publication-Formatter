"""
Feature Extractor Module
Extracts text, formatting, positional, and structural offline features for ML classification.
Complies strictly with 100% offline requirement (no network, no LLMs).
"""

import re
import string
from typing import Dict, Any, List, Optional
import numpy as np
from parser.paragraph_parser import ParagraphInfo

FEATURE_NAMES = [
    # Text Features
    "char_count",
    "word_count",
    "sentence_count",
    "avg_word_length",
    "num_uppercase_chars",
    "is_all_caps",
    "uppercase_ratio",
    "num_digits",
    "digit_ratio",
    "num_punct",
    "has_colon",
    "has_question_mark",
    "has_citation_pattern",
    "has_reference_pattern",
    "has_chapter_keyword",
    # Formatting Features
    "font_size",
    "is_bold",
    "is_italic",
    "is_underline",
    "alignment",
    "line_spacing",
    "space_before",
    "space_after",
    "first_line_indent",
    # Positional Features
    "paragraph_index",
    "position_ratio",
    "is_first_paragraph",
    "is_near_doc_beginning",
    "is_near_doc_end",
    "prev_is_empty",
    "next_is_empty",
    # Structural Features
    "starts_with_chapter",
    "starts_with_numeric_heading",
    "starts_with_roman",
    "starts_with_figure",
    "starts_with_table",
    "starts_with_references",
    "starts_with_bullet",
    "starts_with_numbered_list",
]

# Precompiled regex patterns for speed
RE_SENTENCE_SPLIT = re.compile(r"[.!?]+(?:\s+|$)")
RE_CITATION = re.compile(r"\[\d+(?:[,\s\-–\d]+)?\]|\([A-Z][a-zA-Z\s]+,\s*(?:19|20)\d{2}\)")
RE_REFERENCE_ENTRY = re.compile(r"^(?:\[\d+\]|\d+\.|\d+\))\s+[A-Z]|doi:\s*10\.|http[s]?://|pp\.\s*\d+|(?:19|20)\d{2}[a-z]?[\.,]")
RE_CHAPTER = re.compile(r"^(?:chapter|chapitre|capitulo|part)\s+(?:\d+|[ivxlcdm]+|\b[a-z]+\b)", re.IGNORECASE)
RE_NUMERIC_HEADING = re.compile(r"^\d+(?:\.\d+)*\.?\s+[A-Z]")
RE_ROMAN_HEADING = re.compile(r"^(?:[IVXLCDM]+)\.\s+[A-Z]")
RE_FIGURE = re.compile(r"^(?:figure|fig\.|image|img\.)\s*\d+", re.IGNORECASE)
RE_TABLE = re.compile(r"^(?:table|tab\.)\s*\d+", re.IGNORECASE)
RE_REFERENCES_HEADER = re.compile(r"^(?:references|bibliography|works\s+cited|literature\s+cited)$", re.IGNORECASE)
RE_BULLET = re.compile(r"^[\u2022\u2023\u25E6\u2043\u2219\*\-\–—]\s+")
RE_NUMBERED_LIST = re.compile(r"^(?:\d+[\.\)]|[a-zA-Z][\.\)]|\([0-9a-zA-Z]+\))\s+")


class FeatureExtractor:
    """Extracts high-dimensional offline feature vectors for document paragraph classification."""

    @staticmethod
    def extract_features(
        para: ParagraphInfo,
        total_paras: int = 1,
        prev_para: Optional[ParagraphInfo] = None,
        next_para: Optional[ParagraphInfo] = None,
    ) -> Dict[str, Any]:
        text = para.clean_text
        char_count = len(text)
        words = text.split()
        word_count = len(words)

        # Sentence count
        sentences = [s for s in RE_SENTENCE_SPLIT.split(text) if s.strip()]
        sentence_count = max(len(sentences), 1 if word_count > 0 else 0)

        # Word lengths
        avg_word_len = (
            sum(len(w) for w in words) / word_count if word_count > 0 else 0.0
        )

        # Uppercase & digits
        upper_chars = sum(1 for c in text if c.isupper())
        upper_ratio = upper_chars / char_count if char_count > 0 else 0.0
        is_all_caps = int(text.isupper() and char_count > 3)

        num_digits = sum(1 for c in text if c.isdigit())
        digit_ratio = num_digits / char_count if char_count > 0 else 0.0

        # Punctuation
        num_punct = sum(1 for c in text if c in string.punctuation)
        has_colon = int(":" in text)
        has_qm = int("?" in text)

        # Text patterns
        has_citation = int(bool(RE_CITATION.search(text)))
        has_ref = int(bool(RE_REFERENCE_ENTRY.search(text)))
        has_chap_kw = int("chapter" in text.lower() or "ch." in text.lower())

        # Formatting features
        f_size = para.font_size_pt if para.font_size_pt else 12.0
        is_bold = int(para.is_bold)
        is_italic = int(para.is_italic)
        is_underline = int(para.is_underline)
        alignment = para.alignment
        line_spacing = para.line_spacing if para.line_spacing else 1.0
        space_before = para.space_before_pt
        space_after = para.space_after_pt
        indent = para.first_line_indent_pt

        # Positional features
        denom = max(total_paras - 1, 1)
        pos_ratio = para.index / denom
        is_first = int(para.index == 0)
        is_near_start = int(pos_ratio < 0.05)
        is_near_end = int(pos_ratio > 0.85)

        prev_empty = int(prev_para is None or not prev_para.clean_text)
        next_empty = int(next_para is None or not next_para.clean_text)

        # Structural regex matching
        starts_chap = int(bool(RE_CHAPTER.match(text)))
        starts_num_head = int(bool(RE_NUMERIC_HEADING.match(text)))
        starts_roman = int(bool(RE_ROMAN_HEADING.match(text)))
        starts_fig = int(bool(RE_FIGURE.match(text)))
        starts_tbl = int(bool(RE_TABLE.match(text)))
        starts_refs = int(bool(RE_REFERENCES_HEADER.match(text)))
        starts_bullet = int(bool(RE_BULLET.match(text)) or "bullet" in para.style_name.lower())
        starts_num_list = int(bool(RE_NUMBERED_LIST.match(text)) or "number" in para.style_name.lower())

        feats: Dict[str, Any] = {
            "char_count": char_count,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_word_length": round(avg_word_len, 2),
            "num_uppercase_chars": upper_chars,
            "is_all_caps": is_all_caps,
            "uppercase_ratio": round(upper_ratio, 3),
            "num_digits": num_digits,
            "digit_ratio": round(digit_ratio, 3),
            "num_punct": num_punct,
            "has_colon": has_colon,
            "has_question_mark": has_qm,
            "has_citation_pattern": has_citation,
            "has_reference_pattern": has_ref,
            "has_chapter_keyword": has_chap_kw,
            "font_size": f_size,
            "is_bold": is_bold,
            "is_italic": is_italic,
            "is_underline": is_underline,
            "alignment": alignment,
            "line_spacing": line_spacing,
            "space_before": space_before,
            "space_after": space_after,
            "first_line_indent": indent,
            "paragraph_index": para.index,
            "position_ratio": round(pos_ratio, 4),
            "is_first_paragraph": is_first,
            "is_near_doc_beginning": is_near_start,
            "is_near_doc_end": is_near_end,
            "prev_is_empty": prev_empty,
            "next_is_empty": next_empty,
            "starts_with_chapter": starts_chap,
            "starts_with_numeric_heading": starts_num_head,
            "starts_with_roman": starts_roman,
            "starts_with_figure": starts_fig,
            "starts_with_table": starts_tbl,
            "starts_with_references": starts_refs,
            "starts_with_bullet": starts_bullet,
            "starts_with_numbered_list": starts_num_list,
        }
        return feats

    @classmethod
    def to_vector(cls, feats_dict: Dict[str, Any]) -> np.ndarray:
        """Converts feature dictionary into ordered numpy vector matching FEATURE_NAMES."""
        vec = [float(feats_dict.get(name, 0.0)) for name in FEATURE_NAMES]
        return np.array(vec, dtype=np.float32)
