"""
Structure Rules Module
Deterministic structural heuristics and context-aware pattern matchers.
"""

import re
from typing import Optional, Dict, Any, Tuple
from parser.paragraph_parser import ParagraphInfo

RE_CHAPTER_EXPLICIT = re.compile(
    r"^(?:chapter|chapitre|capítulo|part)\s+(?:\d+|[ivxlcdm]+|\b[a-z]+\b)(?:[:\.\s\-–—]|$)",
    re.IGNORECASE,
)
RE_SUBHEADING_NUM = re.compile(
    r"^(?:\d+\.\d+(?:\.\d+)*)\s+[A-Z]",
)
RE_CAPTION = re.compile(
    r"^(?:figure|fig\.|image|img\.|table|tab\.)\s*\d+[:\.\s\-–—]",
    re.IGNORECASE,
)
RE_REF_HEADER = re.compile(
    r"^(?:references|bibliography|works\s+cited|literature\s+cited|sources)$",
    re.IGNORECASE,
)
RE_REF_ITEM = re.compile(
    r"^(?:\[\d+\]|\d+\.|\d+\))\s+[A-Z]|doi:\s*10\.|(?:19|20)\d{2}[a-z]?[\.,]",
)
RE_BULLET_ITEM = re.compile(
    r"^[\u2022\u2023\u25E6\u2043\u2219\*\-\–—]\s+",
)
RE_NUMBERED_ITEM = re.compile(
    r"^(?:\d+[\.\)]|[a-zA-Z][\.\)]|\([0-9a-zA-Z]+\))\s+",
)
RE_ACADEMIC_AFFIL = re.compile(
    r"\b(?:university|institute|department|college|laboratory|school|center|centre|faculty|dr\.|prof\.|ph\.d|m\.sc|m\.d|email:|@)\b",
    re.IGNORECASE,
)


class StructureRules:
    """Evaluates rule-based constraints on manuscript paragraphs."""

    @staticmethod
    def match_rule(
        para: ParagraphInfo,
        total_paras: int = 1,
        prev_para: Optional[ParagraphInfo] = None,
        next_para: Optional[ParagraphInfo] = None,
        in_reference_section: bool = False,
    ) -> Tuple[Optional[str], float, str]:
        """
        Returns: (candidate_class, rule_confidence, reasoning)
        """
        text = para.clean_text
        if not text:
            return ("BODY", 0.99, "Empty paragraph defaults to standard body spacing")

        words = text.split()
        w_count = len(words)
        c_count = len(text)
        denom = max(total_paras - 1, 1)
        pos_ratio = para.index / denom

        # 1. CAPTION Detection: "Figure 1", "Fig. 1", "Table 1:"
        if RE_CAPTION.match(text) and w_count <= 45:
            return ("CAPTION", 0.985, "Matches explicit Figure/Table caption pattern")

        # 2. REFERENCE Section Header: "References", "Bibliography", "Works Cited"
        if RE_REF_HEADER.match(text):
            return ("CHAPTER_HEADING", 0.990, "Identified standard Reference/Bibliography section header")

        # 3. Inside Reference Section or Explicit Citation Item
        if in_reference_section or (pos_ratio > 0.70 and RE_REF_ITEM.match(text)):
            if RE_REF_ITEM.match(text) or ("[" in text and "]" in text and w_count > 6):
                return ("REFERENCE", 0.975, "Matches academic citation bibliography entry syntax")

        # 4. Explicit CHAPTER HEADING
        if RE_CHAPTER_EXPLICIT.match(text) and w_count <= 25:
            conf = 0.980 if (para.is_bold or para.font_size_pt >= 14.0 or para.alignment == 1) else 0.920
            return ("CHAPTER_HEADING", conf, "Matches 'Chapter X' explicit syntactic structure")

        # 5. Numeric Subheading: "1.1 Introduction", "2.3.1 Experimental Results"
        if RE_SUBHEADING_NUM.match(text) and w_count <= 20:
            return ("SUBHEADING", 0.965, "Matches hierarchical numeric section numbering pattern (e.g. 1.1)")

        # 6. BULLET LIST
        if RE_BULLET_ITEM.match(text) or "bullet" in para.style_name.lower():
            return ("BULLET_LIST", 0.980, "Matches bullet list symbol syntax")

        # 7. NUMBERED LIST
        if (RE_NUMBERED_ITEM.match(text) and w_count < 60) or "number" in para.style_name.lower():
            # Check not subheading like 1.1
            if not RE_SUBHEADING_NUM.match(text):
                return ("NUMBERED_LIST", 0.960, "Matches numbered enumeration list prefix")

        # 8. TITLE Detection: at the very beginning of the document
        if pos_ratio <= 0.03 and w_count <= 25:
            if (para.font_size_pt >= 16.0 or para.is_bold) and (para.alignment in (0, 1)):
                if not RE_ACADEMIC_AFFIL.search(text) and not RE_CHAPTER_EXPLICIT.match(text):
                    return ("TITLE", 0.960, "Prominent opening header at document origin (title candidate)")

        # 9. AUTHOR Detection: right after Title with academic credentials
        if pos_ratio <= 0.06 and w_count <= 40:
            if RE_ACADEMIC_AFFIL.search(text):
                return ("AUTHOR", 0.970, "Opening segment containing academic affiliation/credentials")
            if prev_para and prev_para.clean_text and pos_ratio <= 0.04 and not para.is_bold and w_count < 15:
                return ("AUTHOR", 0.880, "Positioned immediately below document title block")

        # 10. SUBHEADING by styling: short, bold, not all-caps chapter, precedes body
        if w_count <= 15 and (para.is_bold or (para.font_size_pt > 12.0 and para.font_size_pt < 15.0)):
            if not text.endswith(".") and not text.endswith("?"):
                return ("SUBHEADING", 0.910, "Short bold paragraph without terminal period (subheading pattern)")

        # 11. Clear BODY: long, normal font, multiple sentences, not bold
        if w_count >= 30 and not para.is_bold and para.font_size_pt <= 12.5:
            return ("BODY", 0.980, "Multi-sentence narrative text paragraph matching standard body typography")

        return (None, 0.0, "No deterministic rule triggered")
