"""
Classification Metrics Module
Provides calculation routines for multi-class classification and structural parsing verification.
"""

from typing import List, Dict, Any, Optional
import numpy as np


class ClassificationMetrics:
    """Calculates granular category-specific accuracies and confusion statistics."""

    @staticmethod
    def calculate_category_accuracy(
        y_true: List[str],
        y_pred: List[str],
        target_category: str,
    ) -> Optional[float]:
        """Calculates recall/accuracy for a specific category."""
        indices = [i for i, label in enumerate(y_true) if label == target_category]
        if not indices:
            return None
        correct = sum(1 for i in indices if y_pred[i] == target_category)
        return round(correct / len(indices), 4)

    @staticmethod
    def calculate_heading_accuracy(
        y_true: List[str],
        y_pred: List[str],
    ) -> Optional[float]:
        heading_classes = {"CHAPTER_HEADING", "SUBHEADING"}
        indices = [i for i, label in enumerate(y_true) if label in heading_classes]
        if not indices:
            return None
        correct = sum(1 for i in indices if y_pred[i] in heading_classes)
        return round(correct / len(indices), 4)
