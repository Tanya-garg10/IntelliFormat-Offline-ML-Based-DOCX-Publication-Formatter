"""
Tests for Body, Caption, and Reference detection.
"""

from rules.confidence import HybridClassifier
from parser.paragraph_parser import ParagraphInfo


def test_caption_detection():
    classifier = HybridClassifier()
    p = ParagraphInfo(
        index=8,
        text="Figure 2: Empirical accuracy comparison across models.",
        clean_text="Figure 2: Empirical accuracy comparison across models.",
        is_italic=True,
        font_size_pt=10.0,
    )
    res = classifier.classify_document([p])[0]
    assert res["final_class"] == "CAPTION"
    assert res["confidence"] >= 0.95


def test_reference_detection():
    classifier = HybridClassifier()
    p_header = ParagraphInfo(
        index=15,
        text="References",
        clean_text="References",
        is_bold=True,
    )
    p_item = ParagraphInfo(
        index=16,
        text="[1] Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal.",
        clean_text="[1] Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal.",
    )
    res = classifier.classify_document([p_header, p_item])
    assert res[0]["final_class"] == "CHAPTER_HEADING"
    assert res[1]["final_class"] == "REFERENCE"
    assert res[1]["confidence"] >= 0.90


def test_body_detection():
    classifier = HybridClassifier()
    long_text = (
        "Modern academic publishing places stringent requirements on document formatting. "
        "Every chapter must present consistent typography, balanced paragraph margins, and uniform indentations. "
        "Automated tools must execute these formatting tasks without altering the author's prose or rewriting sentences."
    )
    p = ParagraphInfo(
        index=6,
        text=long_text,
        clean_text=long_text,
        font_size_pt=12.0,
    )
    res = classifier.classify_document([p])[0]
    assert res["final_class"] == "BODY"
