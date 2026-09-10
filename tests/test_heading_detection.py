"""
Tests for Heading and Subheading detection.
"""

from rules.confidence import HybridClassifier
from parser.paragraph_parser import ParagraphInfo


def test_chapter_heading_detection():
    classifier = HybridClassifier()
    p = ParagraphInfo(
        index=2,
        text="Chapter 4: Statistical Pattern Recognition",
        clean_text="Chapter 4: Statistical Pattern Recognition",
        is_bold=True,
        font_size_pt=16.0,
    )
    res = classifier.classify_document([p])[0]
    assert res["final_class"] == "CHAPTER_HEADING"
    assert res["confidence"] >= 0.90


def test_subheading_detection():
    classifier = HybridClassifier()
    p = ParagraphInfo(
        index=4,
        text="4.1 Linear Classifiers and Kernel Tricks",
        clean_text="4.1 Linear Classifiers and Kernel Tricks",
        is_bold=True,
        font_size_pt=12.0,
    )
    res = classifier.classify_document([p])[0]
    assert res["final_class"] == "SUBHEADING"
    assert res["confidence"] >= 0.85
