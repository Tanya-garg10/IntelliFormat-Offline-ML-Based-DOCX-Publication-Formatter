"""
Structure Predictor Module
Loads offline scikit-learn model and computes structural class predictions with confidence scores.
"""

import os
import sys
import joblib
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.feature_extractor import FeatureExtractor, FEATURE_NAMES
from parser.paragraph_parser import ParagraphInfo

DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


class StructurePredictor:
    """Offline ML Predictor for document paragraphs."""

    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.classes_: List[str] = []
        self._load_model()

    def _load_model(self) -> None:
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                if hasattr(self.model, "classes_"):
                    self.classes_ = list(self.model.classes_)
            except Exception as e:
                sys.stderr.write(f"Warning: Failed to load model from {self.model_path}: {e}\n")
                self.model = None

    def is_ready(self) -> bool:
        return self.model is not None

    def predict_paragraph(
        self,
        para: ParagraphInfo,
        total_paras: int = 1,
        prev_para: Optional[ParagraphInfo] = None,
        next_para: Optional[ParagraphInfo] = None,
    ) -> Dict[str, Any]:
        """Extracts features and predicts class + confidence score."""
        feats = FeatureExtractor.extract_features(
            para,
            total_paras=total_paras,
            prev_para=prev_para,
            next_para=next_para,
        )
        vec = FeatureExtractor.to_vector(feats).reshape(1, -1)

        if self.model is None or not self.classes_:
            # Fallback heuristic if model file not yet loaded
            return {
                "predicted_class": "BODY",
                "confidence": 0.50,
                "probabilities": {"BODY": 0.50},
                "features": feats,
            }

        try:
            probas = self.model.predict_proba(vec)[0]
            max_idx = int(np.argmax(probas))
            best_class = str(self.classes_[max_idx])
            best_confidence = float(probas[max_idx])

            prob_dict = {
                cls_name: round(float(prob), 4)
                for cls_name, prob in zip(self.classes_, probas)
            }

            return {
                "predicted_class": best_class,
                "confidence": round(best_confidence, 4),
                "probabilities": prob_dict,
                "features": feats,
            }
        except Exception as e:
            return {
                "predicted_class": "BODY",
                "confidence": 0.50,
                "probabilities": {"BODY": 0.50},
                "features": feats,
                "error": str(e),
            }
