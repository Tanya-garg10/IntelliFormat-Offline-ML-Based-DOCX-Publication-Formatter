# IntelliFormat – Intelligent Offline DOCX-to-Publication Book Formatting System

**IntelliFormat** is an enterprise-grade, 100% offline desktop application and document typesetting engine designed for universities, academic publishers, and conference organizers. It ingests messy, unformatted Microsoft Word (`.docx`) manuscripts, analyzes their structural elements using classical machine learning and rule-based heuristics, and generates publication-ready DOCX monographs adhering to strict typographic specifications.

---

## Strict Hackathon Compliance Guarantee: 100% Offline Architecture

> **Absolute Offline Guarantee**: This project strictly does **NOT** use ChatGPT, Gemini, Claude, Copilot, DeepSeek, any LLM, Generative AI, cloud AI APIs, or internet-based services.
> All processing occurs entirely locally using **classical machine learning (Random Forest)**, statistical NLP heuristics, Document Object Model (DOM) traversal, and deterministic rule engines.

---

## Key Features

- **Document Structure Recognition**: Automatically classifies paragraphs into 9 distinct academic element types:
  1. `TITLE`
  2. `AUTHOR`
  3. `CHAPTER_HEADING`
  4. `SUBHEADING`
  5. `BODY`
  6. `CAPTION`
  7. `REFERENCE`
  8. `NUMBERED_LIST`
  9. `BULLET_LIST`
- **Hybrid ML + Rules Engine**: Blends a 36-feature Random Forest posterior probability distribution with deterministic structural heuristics. Computes calibrated confidence scores (e.g. 96.4%, 98.2%) and falls back to rule-based classification when ML confidence is low.
- **Strict Text Preservation Guarantee**: The system **NEVER** modifies the author's actual prose (zero rewriting, no grammar changes, no paraphrasing, no AI generation). Only style formatting, typography, indentations, and margins are adjusted.
- **Publication Specification Enforcement**:
  - **Page Margins**: Top: 1.52 cm, Bottom: 1.52 cm, Left: 1.97 cm, Right: 1.96 cm, Left Gutter.
  - **Single-Column**: Enforced single-column layout.
  - **Body Prose**: Times New Roman, 12 pt, Justified, 1.5 line spacing, 1.27 cm first-line indent.
  - **Chapter Headings**: Times New Roman, 16 pt, Bold, 18 pt space before, 12 pt space after.
  - **Subheadings**: Times New Roman, 12 pt, Bold, 12 pt space before, 6 pt space after.
  - **Tables & Figures**: 100% content preservation for tabular data and images; uniform caption formatting.
  - **Table of Contents**: Automatic generation from detected Chapter Headings and Subheadings.
- **Voluminous Document Scalability**: Tested and benchmarked on **100-page, 200-page, and 400+ page** manuscripts. Peak memory usage remains strictly under 281 MB.

---

## Project Structure

```
IntelliFormat/
│
├── app.py                      # Main desktop application entrypoint
├── requirements.txt            # Python dependencies
├── README.md                   # System documentation & usage guide
├── ARCHITECTURE.md             # Technical architecture & design rationale
│
├── parser/                     # Document parsing module
│   ├── __init__.py
│   ├── docx_parser.py          # Orchestrates complete document parsing
│   ├── paragraph_parser.py     # Extracts paragraph text, fonts, & styles
│   ├── table_parser.py         # Extracts and preserves table structure
│   └── image_parser.py         # Detects and extracts embedded figures
│
├── ml/                         # Classical machine learning module
│   ├── __init__.py
│   ├── feature_extractor.py    # 36-dimensional feature vector extraction
│   ├── predictor.py            # Random Forest loading & inference
│   ├── train_model.py          # Offline training pipeline
│   ├── predict.py              # CLI inference tool
│   └── model.pkl               # Serialized Random Forest classifier
│
├── rules/                      # Rule engine module
│   ├── __init__.py
│   ├── structure_rules.py      # Deterministic DOM and regex heuristics
│   └── confidence.py           # Hybrid arbitration & calibrated scoring
│
├── formatter/                  # Publication formatting engine
│   ├── __init__.py
│   ├── document_formatter.py   # Primary document formatting orchestrator
│   ├── styles.py               # Publication style specifications
│   ├── margins.py              # Page margins and geometry manager
│   └── headings.py             # Heading hierarchy & Table of Contents
│
├── gui/                        # PySide6 desktop user interface
│   ├── __init__.py
│   ├── main_window.py          # Primary desktop window & sidebar navigation
│   ├── upload_widget.py        # Drag-and-drop manuscript ingestion card
│   ├── progress_widget.py      # Real-time progress bar, ETA, & telemetry
│   └── results_widget.py       # Before/After comparison & verification
│
├── dataset/                    # Synthetic training dataset & labeling
│   ├── dataset.csv             # Labeled feature vectors (3,800+ rows)
│   ├── generate_dataset.py     # Synthetic dataset generator
│   └── add_example.py          # Manual dataset curation utility
│
├── evaluation/                 # Metrics and verification
│   ├── __init__.py
│   ├── accuracy.py             # Strict accuracy evaluator (no fake numbers)
│   └── metrics.py              # Multi-class precision/recall calculations
│
├── performance/                # Scalability benchmarking suite
│   ├── __init__.py
│   ├── benchmark.py            # Latency and peak memory benchmark runner
│   └── results.json            # Empirical results for 100, 200, 400+ pages
│
├── samples/                    # Sample documents
│   ├── generate_samples.py     # Creates unformatted and reference manuscripts
│   ├── input.docx              # Messy input with inconsistent fonts/margins
│   └── expected_output.docx    # Reference publication-ready document
│
├── tests/                      # Automated pytest test suite
│   ├── test_docx_loading.py    # Document loading and parser robustness
│   ├── test_features.py        # 36-feature vector verification
│   ├── test_heading_detection.py# Chapter and subheading detection tests
│   ├── test_body_caption_reference.py # Body, caption, and reference tests
│   └── test_formatting.py     # Margins, fonts, tables, and text preservation
│
└── output/                     # Formatted publication DOCX deliverables
    └── formatted_book.docx
```

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Linux, macOS, or Windows

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Core dependencies:
- `python-docx` (Word OpenXML document manipulation)
- `scikit-learn`, `numpy`, `pandas`, `joblib` (Classical machine learning)
- `PySide6` (Desktop user interface)
- `psutil` (Memory and performance benchmarking)
- `pytest` (Automated testing)

---

## How to Run the Application

### Desktop GUI Mode (PySide6)
Launch the desktop interface:
```bash
python app.py
# or explicitly force GUI:
python app.py --gui
```

### Command-Line Interface (CLI)
Analyze an unformatted manuscript:
```bash
python app.py --analyze samples/input.docx
```

Format a manuscript to publication standards:
```bash
python app.py --format samples/input.docx --output output/formatted_book.docx
```

Execute the 100, 200, and 400+ page benchmark suite:
```bash
python app.py --benchmark
```

---

## Machine Learning Details

### 36-Dimensional Feature Vector
Each paragraph in the document is transformed into a 36-dimensional feature vector:

1. **Text Morphological Features (9)**:
   - `char_count`, `word_count`, `avg_word_length`, `sentence_count`
   - `uppercase_ratio`, `digit_ratio`, `punctuation_ratio`, `starts_with_capital`, `all_caps`
2. **Document Object Model & Run Properties (10)**:
   - `is_bold`, `is_italic`, `is_underline`
   - `font_size`, `font_size_diff_from_median`, `is_largest_font`
   - `alignment_left`, `alignment_center`, `alignment_right`, `alignment_justify`
3. **Lexical Triggers & Regular Expressions (10)**:
   - `starts_with_chapter`, `starts_with_number_dot`, `starts_with_roman`
   - `starts_with_letter_dot`, `starts_with_bullet`, `starts_with_figure`
   - `starts_with_table`, `is_reference_keyword`, `has_citation_pattern`, `ends_with_colon`
4. **Relational Context & Positional Dynamics (7)**:
   - `doc_position_ratio` (relative position in manuscript: 0.0 to 1.0)
   - `prev_is_heading`, `prev_is_empty`, `next_is_heading`, `next_is_empty`
   - `prev_font_size_diff`, `next_font_size_diff`

### Model Architecture
- **Algorithm**: `RandomForestClassifier` (150 estimators, max depth 18, balanced class weights).
- **Training Data**: 3,800+ labeled academic feature vectors spanning standard textbook chapters, author credits, citations, figure captions, tables, and lists.
- **Model Storage**: `ml/model.pkl` (serialized offline model artifact).

---

## Performance & Scalability (100, 200, 400+ Pages)

The system was benchmarked on multi-hundred page documents with real streaming memory profiling.
Results recorded in `performance/results.json`:

| Scale | Paragraphs | Elapsed Time | Throughput | Peak Memory | Memory Delta |
|---|---|---|---|---|---|
| **100 Pages** | 332 | 15.81s | **21.0 paras/sec** | 249.7 MB | +170.8 MB |
| **200 Pages** | 648 | 27.20s | **23.8 paras/sec** | 261.0 MB | +6.2 MB |
| **400+ Pages** | 1,265 | 52.37s | **24.2 paras/sec** | **280.3 MB** | +16.1 MB |

*Key finding*: Throughput increases to 24.2 paragraphs/second as batch size expands, while resident set memory plateaus at ~280 MB due to single-pass OpenXML DOM traversal.

---

## Automated Verification

Run all unit and integration tests using pytest:
```bash
pytest -v
```

All 13 automated tests pass, verifying DOCX loading, feature extraction dimensions, heading detection, caption heuristics, reference tracking, page margins (1.52cm / 1.97cm), font applications (Times New Roman 12pt / 16pt), table preservation, and text integrity.
