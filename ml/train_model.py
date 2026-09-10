"""
ML Training Pipeline Module
Trains an offline scikit-learn RandomForestClassifier on extracted document features.
Calculates Accuracy, Precision, Recall, F1 Score, and Confusion Matrix.
Saves model to ml/model.pkl via joblib.
"""

import os
import sys
import json
import joblib

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
from ml.feature_extractor import FeatureExtractor, FEATURE_NAMES
from parser.paragraph_parser import ParagraphInfo

CLASSES = [
    "TITLE",
    "AUTHOR",
    "CHAPTER_HEADING",
    "SUBHEADING",
    "BODY",
    "CAPTION",
    "REFERENCE",
    "NUMBERED_LIST",
    "BULLET_LIST",
]


def extract_features_from_row(row: pd.Series, total_rows: int, idx: int) -> np.ndarray:
    """Reconstructs ParagraphInfo and extracts canonical 36-feature vector."""
    text = str(row.get("text", "") or "")
    f_size = float(row.get("font_size", 12.0) or 12.0)
    bold = bool(int(row.get("bold", 0) or 0))
    italic = bool(int(row.get("italic", 0) or 0))
    align = int(row.get("alignment", 0) or 0)
    pos = float(row.get("position_ratio", idx / max(total_rows, 1)) or 0.0)

    p_info = ParagraphInfo(
        index=idx,
        text=text,
        clean_text=text.strip(),
        alignment=align,
        font_size_pt=f_size,
        is_bold=bold,
        is_italic=italic,
    )

    feats_dict = FeatureExtractor.extract_features(
        p_info,
        total_paras=total_rows,
    )
    # Ensure position_ratio from dataset is preserved if provided
    if "position_ratio" in row and pd.notna(row["position_ratio"]):
        feats_dict["position_ratio"] = float(row["position_ratio"])

    return FeatureExtractor.to_vector(feats_dict)


def train_and_evaluate(
    csv_path: str = "dataset/training_data.csv",
    model_output_path: str = "ml/model.pkl",
    metrics_output_path: str = "ml/training_metrics.json",
) -> Dict[str, Any]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Training dataset not found: {csv_path}")

    df = pd.read_csv(csv_path)
    total_samples = len(df)
    if total_samples < 20:
        raise ValueError(f"Too few samples in training dataset: {total_samples}")

    X_list = []
    y_list = []

    for idx, row in df.iterrows():
        label = str(row["label"]).strip()
        if label not in CLASSES:
            continue
        vec = extract_features_from_row(row, total_samples, idx)
        X_list.append(vec)
        y_list.append(label)

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list)

    # Stratified 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Train Random Forest Classifier
    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=16,
        min_samples_split=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    # Predictions & probabilities
    y_pred = clf.predict(X_test)

    # Metrics
    acc = float(accuracy_score(y_test, y_pred))
    prec_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
    prec_weighted = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
    rec_weighted = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1_mac = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
    f1_wt = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    # Confusion Matrix
    unique_labels = sorted(list(set(y_test).union(set(y_pred))))
    cm = confusion_matrix(y_test, y_pred, labels=unique_labels).tolist()

    # Per-class metrics
    clf_report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    # Feature importances
    feat_importances = {
        name: round(float(imp), 4)
        for name, imp in zip(FEATURE_NAMES, clf.feature_importances_)
    }
    sorted_importances = sorted(feat_importances.items(), key=lambda x: x[1], reverse=True)

    metrics: Dict[str, Any] = {
        "model_type": "RandomForestClassifier",
        "total_samples": total_samples,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "num_features": len(FEATURE_NAMES),
        "accuracy": round(acc, 4),
        "precision_macro": round(prec_macro, 4),
        "precision_weighted": round(prec_weighted, 4),
        "recall_macro": round(rec_macro, 4),
        "recall_weighted": round(rec_weighted, 4),
        "f1_macro": round(f1_mac, 4),
        "f1_weighted": round(f1_wt, 4),
        "confusion_matrix": cm,
        "labels": unique_labels,
        "classification_report": clf_report,
        "top_features": sorted_importances[:10],
    }

    # Save model and artifacts
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(clf, model_output_path)

    os.makedirs(os.path.dirname(metrics_output_path), exist_ok=True)
    with open(metrics_output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Model saved to: {model_output_path}")
    print(f"Accuracy: {acc * 100:.2f}% | F1 (Macro): {f1_mac * 100:.2f}%")
    return metrics


if __name__ == "__main__":
    train_and_evaluate()
