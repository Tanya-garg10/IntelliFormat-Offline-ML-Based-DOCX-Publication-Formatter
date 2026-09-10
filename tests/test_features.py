"""
Tests for Feature Extraction module.
"""

from ml.feature_extractor import FeatureExtractor, FEATURE_NAMES
from parser.paragraph_parser import ParagraphInfo


def test_feature_vector_dimension():
    p = ParagraphInfo(
        index=0,
        text="Chapter 1: Mathematical Foundations",
        clean_text="Chapter 1: Mathematical Foundations",
        is_bold=True,
        font_size_pt=16.0,
    )
    feats = FeatureExtractor.extract_features(p, total_paras=10)
    vec = FeatureExtractor.to_vector(feats)
    assert len(vec) == len(FEATURE_NAMES)
    assert feats["starts_with_chapter"] == 1
    assert feats["is_bold"] == 1
    assert feats["word_count"] == 4


def test_citation_detection_feature():
    p = ParagraphInfo(
        index=5,
        text="As established in prior literature [14], high dimensional trees perform well.",
        clean_text="As established in prior literature [14], high dimensional trees perform well.",
    )
    feats = FeatureExtractor.extract_features(p, total_paras=20)
    assert feats["has_citation_pattern"] == 1


def test_caption_feature():
    p = ParagraphInfo(
        index=3,
        text="Figure 3: System layout and data flow diagram.",
        clean_text="Figure 3: System layout and data flow diagram.",
    )
    feats = FeatureExtractor.extract_features(p, total_paras=20)
    assert feats["starts_with_figure"] == 1
