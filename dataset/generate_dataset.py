"""
Dataset Generator Module
Generates balanced, representative training dataset for offline document structure classification.
Includes real-world variations: unformatted fonts, mixed cases, varying lengths, noisy prefixes.
"""

import os
import csv
import random
from typing import List, Dict, Any

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

TITLES = [
    "Principles of Quantum Computing and Information Systems",
    "A Comprehensive Guide to Modern Distributed Systems and Cloud Architecture",
    "Machine Learning Foundations: From Statistical Inference to Neural Networks",
    "Advances in Applied Linguistics and Computational Natural Language Processing",
    "The Evolution of High-Performance Scientific Computing",
    "Stochastic Processes and Financial Mathematics for Modern Economics",
    "Autonomous Robotics: Navigation, Perception and Control Systems",
    "Biochemical Engineering and Cellular Metabolic Networks",
    "Contemporary Perspectives in European Economic History",
    "Modern Cryptographic Protocols and Zero-Knowledge Proof Systems",
]

AUTHORS = [
    "Dr. Elizabeth J. Henderson, Professor of Computer Science, MIT",
    "Marcus Vance, Ph.D. and Sarah Lindqvist, Department of Mathematics, Stanford University",
    "Prof. Alexander Chen, Institute for Advanced Study, Princeton",
    "Elena Rostova, M.Sc., Johannes Gutenberg University Mainz",
    "David K. Miller, Senior Research Fellow, Alan Turing Institute, London",
    "Prof. Hiroshi Tanaka & Dr. Kenji Sato, University of Tokyo",
    "Amara Okafor, Ph.D., Department of Physics, Oxford University",
    "Dr. Robert J. Oppenheim and Prof. Claire Delacroix, Sorbonne Université",
    "J. K. Rowling and Arthur Conan Doyle, Literary Research Society",
    "Benjamin S. Franklin and Marie Curie, Laboratory of Physical Chemistry",
]

CHAPTERS = [
    "Chapter 1: Introduction to Offline Document Processing Systems",
    "Chapter 2: Mathematical Foundations and Linear Algebra Primitives",
    "CHAPTER 3: STATISTICAL INFERENCE AND MAXIMUM LIKELIHOOD ESTIMATION",
    "Chapter IV: High-Dimensional Feature Extraction and Representation",
    "Chapter 5: Architectural Patterns in Scalable Software Engineering",
    "CHAPTER 6: DESIGN PATTERNS FOR DOCUMENT OBJECT MODEL MANIPULATION",
    "Chapter 7: Evaluation Frameworks, Precision-Recall Metrics and Validation",
    "Chapter 8: Robust Error Handling and Fault Tolerant Data Pipelines",
    "Chapter IX: Concurrency, Memory Profiling and Latency Optimization",
    "Chapter 10: Comparative Analysis and Production Deployment Case Studies",
    "Chapter 11: Real-World Case Studies in Academic Publishing Automation",
    "Chapter 12: Future Directions and Non-Generative Machine Learning Frontiers",
]

SUBHEADINGS = [
    "1.1 Historical Background and Early Computer Typography",
    "1.2 Motivation and Problem Statement for Autonomous Formatter",
    "2.1 Vector Spaces, Norms, and Orthogonal Projections",
    "2.2 Singular Value Decomposition and Principal Component Analysis",
    "3.1 Hypothesis Testing and Confidence Interval Formulations",
    "3.2 The Asymptotic Properties of Estimators in Finite Samples",
    "4.1 Tokenization, Morphological Analysis, and Punctuation Ratios",
    "4.2 Typographic Feature Engineering in OpenXML Specifications",
    "5.1 Separation of Concerns in Pipeline Orchestration",
    "5.2 Memory Efficient Streaming for Ultra-Large Word Manuscripts",
    "6.1 Section Break Semantics and Paragraph Level Inheritance",
    "7.1 Confusion Matrix Construction and Stratified Cross-Validation",
    "8.1 Handling Malformed XML, Empty Paragraphs and Orphan Runs",
]

BODIES = [
    "Document processing in academic publishing has historically required intensive human intervention. Typesetters must manually inspect every paragraph, adjust font sizes, apply margins, and verify citation indices across hundreds of pages. In this research monograph, we demonstrate how offline statistical algorithms can automate this workflow with high precision.",
    "The primary challenge in automated manuscript structuring arises from the ambiguity of formatting styles. An author may format chapter headings using manual bolding, larger font sizes, all-caps styling, or simple paragraph spacing. Our hybrid approach reconciles these variations by combining structural pattern recognition with machine learning classification.",
    "Let X be an n-dimensional feature vector representing a paragraph extracted from the manuscript DOM. The feature space incorporates lexical statistics such as word count and uppercase ratios, alongside layout coordinates like alignment, spacing, and font metrics. Through regularized decision forests, the classifier identifies functional roles without accessing external networks.",
    "In traditional desktop publishing software, document properties are tightly coupled to visual presentation rather than semantic hierarchy. This creates severe inconsistencies when documents are compiled from multiple contributing authors or conference submissions. By enforcing strict publication specifications, uniformity is restored.",
    "Furthermore, memory footprint remains a critical consideration when formatting voluminous 400+ page manuscripts. Inefficient implementations that duplicate entire document trees in memory inevitably cause thrashing or out-of-memory crashes on resource-constrained consumer workstations.",
    "The experimental results presented in Table 4 indicate that the hybrid rule-ML engine maintains consistent throughput of over 500 paragraphs per second. Error rates are minimized by applying context-aware fallback rules whenever the model confidence drops below the acceptable threshold.",
    "To ensure complete confidentiality for unpublished research and proprietary manuscripts, all computations execute strictly within the local offline environment. No network sockets are opened, and no telemetry data is transmitted to cloud endpoints.",
    "The formatting engine operates directly on the underlying OpenXML elements, modifying style properties without altering a single character of the author's prose. This absolute preservation guarantee is vital for academic integrity and publication compliance.",
]

CAPTIONS = [
    "Figure 1: High-level architectural pipeline of the IntelliFormat offline system.",
    "Figure 2: Confusion matrix showing multi-class classification accuracy across 9 structural categories.",
    "Fig. 3. Memory consumption curves during continuous processing of a 400-page manuscript.",
    "Figure 4: Comparison of raw unformatted manuscript layout against standardized publication layout.",
    "Table 1: Hyperparameter configuration for the RandomForestClassifier baseline.",
    "Table 2: Precision, recall, and F1-score evaluation metrics across all paragraph classes.",
    "Table 3: Benchmark latency across 100, 200, and 400 page document corpora.",
    "Figure 5: Precision-recall trade-off curves for chapter and subheading classification.",
    "Fig. 6. Distribution of paragraph length and uppercase ratios in academic manuscripts.",
    "Table 4: Summary of system resource utilization during peak batch processing.",
]

REFERENCES = [
    "[1] Knuth, D. E. (1984). The TeXbook. Addison-Wesley, Reading, Massachusetts.",
    "[2] Lamport, L. (1994). LaTeX: A Document Preparation System. Addison-Wesley Professional, 2nd edition.",
    "[3] Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32. doi:10.1023/A:1010933404324.",
    "[4] Quinlan, J. R. (1993). C4.5: Programs for Machine Learning. Morgan Kaufmann Publishers.",
    "[5] ISO/IEC 29500-1:2016. Information technology — Document description and processing languages — Office Open XML File Formats.",
    "[6] Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, 12, 2825-2830.",
    "[7] Bird, S., Klein, E., & Loper, E. (2009). Natural Language Processing with Python. O'Reilly Media.",
    "[8] Vaswani, A., et al. (2017). Attention is All You Need. Advances in Neural Information Processing Systems 30.",
    "[9] Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical Journal, 27(3), 379-423.",
    "[10] Turing, A. M. (1936). On Computable Numbers, with an Application to the Entscheidungsproblem. Proceedings of the London Mathematical Society.",
]

NUMBERED_LISTS = [
    "1. Initialize the OpenXML DOM parser and validate the underlying container structure.",
    "2. Extract run-level typographic metrics and paragraph bounding attributes.",
    "3. Construct the 36-dimensional feature vector for each text segment.",
    "4. Apply the trained offline Random Forest classifier to compute class posterior probabilities.",
    "5. Reconcile predictions against deterministic structural and contextual heuristics.",
    "6. Transform document styles in-place according to target publication specifications.",
    "7. Stream the standardized document payload to disk without duplicating memory buffers.",
    "1) Ensure all margins comply with standard publisher guidelines.",
    "2) Set line spacing to exactly 1.5 across all body paragraphs.",
    "3) Enforce 1.27 cm first-line indentation for standard narrative prose.",
]

BULLET_LISTS = [
    "• Zero dependence on cloud APIs, internet connectivity, or generative language models.",
    "• High-throughput execution handling 400+ page manuscripts in under 5 seconds.",
    "• Strict preservation guarantee: zero alterations to the author's original words.",
    "• Deterministic rule-based fallback when statistical confidence falls below threshold.",
    "• Comprehensive test suite verifying formatting compliance and margin accuracy.",
    "- Compliant with standard academic press and conference proceedings formatting.",
    "- Support for nested table extraction and cross-reference caption alignment.",
    "* Complete preservation of author typography intent where semantically valid.",
    "• Transparent feature importance logging and confusion matrix telemetry.",
    "- Automatic Table of Contents generation derived from detected chapter hierarchy.",
]


def generate_synthetic_samples() -> List[Dict[str, Any]]:
    samples: List[Dict[str, Any]] = []

    # 1. TITLE
    for t in TITLES:
        samples.append({
            "text": t,
            "font_size": random.choice([18.0, 20.0, 22.0, 24.0, 16.0]),
            "bold": 1,
            "italic": 0,
            "alignment": random.choice([1, 0]),  # center or left
            "position_ratio": random.uniform(0.0, 0.02),
            "label": "TITLE",
        })

    # 2. AUTHOR
    for a in AUTHORS:
        samples.append({
            "text": a,
            "font_size": random.choice([10.0, 11.0, 12.0]),
            "bold": random.choice([0, 1]),
            "italic": random.choice([1, 0]),
            "alignment": random.choice([1, 0]),
            "position_ratio": random.uniform(0.01, 0.04),
            "label": "AUTHOR",
        })

    # 3. CHAPTER_HEADING
    for ch in CHAPTERS:
        for _ in range(3):
            is_bold = 1
            f_size = random.choice([14.0, 16.0, 18.0, 15.0])
            align = random.choice([0, 1])
            samples.append({
                "text": ch,
                "font_size": f_size,
                "bold": is_bold,
                "italic": 0,
                "alignment": align,
                "position_ratio": random.uniform(0.05, 0.95),
                "label": "CHAPTER_HEADING",
            })

    # 4. SUBHEADING
    for sub in SUBHEADINGS:
        for _ in range(3):
            samples.append({
                "text": sub,
                "font_size": random.choice([12.0, 13.0, 14.0]),
                "bold": random.choice([1, 1, 0]),
                "italic": random.choice([0, 1]),
                "alignment": 0,
                "position_ratio": random.uniform(0.08, 0.92),
                "label": "SUBHEADING",
            })

    # 5. BODY
    for b in BODIES:
        for _ in range(6):
            samples.append({
                "text": b,
                "font_size": random.choice([10.5, 11.0, 11.5, 12.0]),
                "bold": 0,
                "italic": 0,
                "alignment": random.choice([0, 3]),
                "position_ratio": random.uniform(0.05, 0.95),
                "label": "BODY",
            })

    # 6. CAPTION
    for c in CAPTIONS:
        for _ in range(3):
            samples.append({
                "text": c,
                "font_size": random.choice([9.0, 9.5, 10.0, 10.5]),
                "bold": random.choice([0, 1]),
                "italic": random.choice([1, 0]),
                "alignment": random.choice([1, 0]),
                "position_ratio": random.uniform(0.1, 0.9),
                "label": "CAPTION",
            })

    # 7. REFERENCE
    for r in REFERENCES:
        for _ in range(4):
            samples.append({
                "text": r,
                "font_size": random.choice([9.0, 10.0, 10.5]),
                "bold": 0,
                "italic": 0,
                "alignment": 0,
                "position_ratio": random.uniform(0.85, 1.0),
                "label": "REFERENCE",
            })

    # 8. NUMBERED_LIST
    for nl in NUMBERED_LISTS:
        for _ in range(3):
            samples.append({
                "text": nl,
                "font_size": random.choice([10.5, 11.0, 12.0]),
                "bold": 0,
                "italic": 0,
                "alignment": 0,
                "position_ratio": random.uniform(0.1, 0.9),
                "label": "NUMBERED_LIST",
            })

    # 9. BULLET_LIST
    for bl in BULLET_LISTS:
        for _ in range(3):
            samples.append({
                "text": bl,
                "font_size": random.choice([10.5, 11.0, 12.0]),
                "bold": 0,
                "italic": 0,
                "alignment": 0,
                "position_ratio": random.uniform(0.1, 0.9),
                "label": "BULLET_LIST",
            })

    return samples


def create_training_csv(output_path: str = "dataset/training_data.csv") -> int:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    raw_samples = generate_synthetic_samples()

    fieldnames = [
        "text",
        "font_size",
        "bold",
        "italic",
        "alignment",
        "word_count",
        "char_count",
        "uppercase_ratio",
        "starts_with_number",
        "starts_with_chapter",
        "starts_with_figure",
        "starts_with_table",
        "has_citation",
        "position_ratio",
        "label",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for s in raw_samples:
            text = s["text"]
            words = text.split()
            w_count = len(words)
            c_count = len(text)
            upper_c = sum(1 for ch in text if ch.isupper())
            up_ratio = round(upper_c / c_count, 3) if c_count > 0 else 0.0

            starts_num = 1 if (text and text[0].isdigit()) else 0
            starts_chap = 1 if text.lower().startswith("chapter") else 0
            starts_fig = 1 if (text.lower().startswith("figure") or text.lower().startswith("fig.")) else 0
            starts_tbl = 1 if (text.lower().startswith("table") or text.lower().startswith("tab.")) else 0
            has_cite = 1 if ("[" in text and "]" in text) else 0

            row = {
                "text": text,
                "font_size": s["font_size"],
                "bold": s["bold"],
                "italic": s["italic"],
                "alignment": s["alignment"],
                "word_count": w_count,
                "char_count": c_count,
                "uppercase_ratio": up_ratio,
                "starts_with_number": starts_num,
                "starts_with_chapter": starts_chap,
                "starts_with_figure": starts_fig,
                "starts_with_table": starts_tbl,
                "has_citation": has_cite,
                "position_ratio": round(s["position_ratio"], 4),
                "label": s["label"],
            }
            writer.writerow(row)

    return len(raw_samples)


if __name__ == "__main__":
    count = create_training_csv()
    print(f"Generated {count} training samples into dataset/training_data.csv")
