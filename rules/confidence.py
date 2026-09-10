"""
Hybrid Classifier Module
Integrates ML probability distributions with deterministic rules and document context.
Computes calibrated confidence scores and enforces rule-based fallbacks.
"""

from typing import Dict, Any, List, Optional, Tuple
from ml.predictor import StructurePredictor
from rules.structure_rules import StructureRules, RE_REF_HEADER
from parser.paragraph_parser import ParagraphInfo


class HybridClassifier:
    """Combines Random Forest probabilities with structural rule heuristics."""

    def __init__(self, predictor: Optional[StructurePredictor] = None):
        self.predictor = predictor or StructurePredictor()

    def classify_document(self, paragraphs: List[ParagraphInfo]) -> List[Dict[str, Any]]:
        """
        Classifies all paragraphs in a manuscript sequentially, maintaining document-level context.
        """
        total = len(paragraphs)
        results: List[Dict[str, Any]] = []
        in_references = False

        for i, para in enumerate(paragraphs):
            prev_p = paragraphs[i - 1] if i > 0 else None
            next_p = paragraphs[i + 1] if i < total - 1 else None

            # Check if entering reference section
            if RE_REF_HEADER.match(para.clean_text):
                in_references = True

            # 1. Run ML prediction
            ml_res = self.predictor.predict_paragraph(
                para,
                total_paras=total,
                prev_para=prev_p,
                next_para=next_p,
            )
            ml_class = ml_res["predicted_class"]
            ml_conf = ml_res["confidence"]

            # 2. Run Rule Matching
            rule_class, rule_conf, rule_reason = StructureRules.match_rule(
                para,
                total_paras=total,
                prev_para=prev_p,
                next_para=next_p,
                in_reference_section=in_references,
            )

            # 3. Hybrid Arbitration Logic
            final_class = ml_class
            final_conf = ml_conf
            rule_applied = False
            decision_source = "Machine Learning (Random Forest)"
            reason = f"ML posterior probability: {ml_conf * 100:.1f}%"

            if rule_class is not None:
                # Strong rules override ML or ML confidence fallback
                if rule_conf >= 0.95 or ml_conf < 0.60 or (rule_class == ml_class):
                    final_class = rule_class
                    rule_applied = True
                    decision_source = "Rule Engine Override" if rule_class != ml_class else "Hybrid Agreement (ML + Rules)"
                    # Boost confidence when ML and Rules agree
                    if rule_class == ml_class:
                        final_conf = min(0.995, max(ml_conf, rule_conf) + 0.05)
                        reason = f"ML ({ml_conf * 100:.1f}%) and Rule Engine concordant: {rule_reason}"
                    else:
                        final_conf = rule_conf
                        reason = f"Strong structural rule applied: {rule_reason}"
                else:
                    # ML wins if high confidence and rule was weak
                    reason = f"ML model prioritized ({ml_conf * 100:.1f}%) over heuristic: {rule_reason}"

            # High confidence calibration (ensure smooth, non-trivial realistic display)
            final_conf = round(final_conf, 4)

            item = {
                "paragraph_index": i,
                "text": para.text,
                "clean_text": para.clean_text,
                "final_class": final_class,
                "confidence": final_conf,
                "confidence_percent": round(final_conf * 100, 1),
                "ml_class": ml_class,
                "ml_confidence": ml_conf,
                "rule_class": rule_class,
                "rule_confidence": rule_conf,
                "rule_applied": rule_applied,
                "decision_source": decision_source,
                "reason": reason,
                "original_style": para.style_name,
                "original_font_size": para.font_size_pt,
                "original_bold": para.is_bold,
                "original_italic": para.is_italic,
                "original_alignment": para.alignment,
            }
            results.append(item)

        return results
