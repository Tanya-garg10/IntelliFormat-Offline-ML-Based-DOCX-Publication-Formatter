"""
Standalone predict script / interface for CLI and testing.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.predictor import StructurePredictor
from parser.paragraph_parser import ParagraphInfo

__all__ = ["StructurePredictor"]

if __name__ == "__main__":
    predictor = StructurePredictor()
    sample_text = sys.argv[1] if len(sys.argv) > 1 else "Chapter 1: Introduction to Intelligence"
    para = ParagraphInfo(index=0, text=sample_text, clean_text=sample_text.strip(), is_bold=True, font_size_pt=16.0)
    result = predictor.predict_paragraph(para, total_paras=10)
    print(f"Text: '{sample_text}'")
    print(f"Predicted Class: {result['predicted_class']}")
    print(f"Confidence: {result['confidence'] * 100:.1f}%")
