"""
Sample Manuscript Generator Module
Generates unformatted input manuscripts with messy fonts, inconsistent alignments,
and produces the corresponding expected publication-ready reference.
Also generates 100, 200, and 400+ page benchmark manuscripts.
"""

import os
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from formatter.document_formatter import DocumentFormatter


def create_unformatted_manuscript(
    output_path: str = "samples/input.docx",
    target_pages: int = 15,
) -> str:
    """Creates a realistic messy/unformatted docx manuscript."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = Document()

    # 1. Unformatted Title (Calibri, 18pt, left aligned, inconsistent color)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_t = p_title.add_run("Principles of Autonomous Document Processing and Machine Learning")
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(18.0)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(30, 60, 120)

    # 2. Author info (Arial, 10pt, no italic)
    p_author = doc.add_paragraph()
    run_a = p_author.add_run("Dr. Marcus Vance, Ph.D. - Stanford Institute of Computational Intelligence")
    run_a.font.name = "Arial"
    run_a.font.size = Pt(10.0)

    # Chapters and contents
    chapters_data = [
        (
            "Chapter 1: Foundations of Offline Machine Learning",
            [
                "1.1 Historical Perspective and Motivations",
                "Academic and technical publishing has long grappled with the labor-intensive burden of manual document preparation. Authors write in diverse software with arbitrary fonts, resulting in chaotic visual presentation across submissions.",
                "To resolve these discrepancies, early typesetting systems like TeX introduced programmatic macros. However, modern corporate and university workflows overwhelmingly rely on WYSIWYG word processors such as Microsoft Word, compounding the problem of unstandardized styling.",
                "Figure 1: Evolution of document styling paradigms from mechanical typesetting to machine learning.",
                "1.2 Non-Generative Document Analysis",
                "Modern machine learning provides robust tools for feature extraction without requiring internet connectivity or opaque large language models. Deterministic decision trees and Random Forests evaluate layout heuristics with high throughput.",
                "• Complete offline autonomy guarantees that sensitive manuscripts remain secure.\n• High throughput enables batch analysis of 400+ page books in seconds.\n• Mathematical explainability ensures that formatting decisions can be audited.",
            ],
        ),
        (
            "Chapter 2: Structural Feature Engineering",
            [
                "2.1 Lexical and Morphological Descriptors",
                "Every paragraph in an OpenXML document possesses both content characteristics and presentation attributes. We extract character counts, uppercase ratios, digit distributions, and punctuation densities to distinguish headings from prose.",
                "Table 1: Key typographic features extracted for Random Forest training.",
                "2.2 Positional Heuristics and Relational Context",
                "Paragraphs do not exist in isolation. A short bold phrase following a chapter break is almost certainly a subheading, whereas a similar phrase at the end of a document may indicate a reference header.",
                "1. Compute run-level font metrics across each paragraph node.\n2. Calculate relative document position ratios.\n3. Identify explicit pattern triggers such as numeric lists or figure labels.",
            ],
        ),
        (
            "Chapter 3: Publication Standards and Typography Enforcement",
            [
                "3.1 Standard Page Dimensions and Margins",
                "Academic monograph publication enforces stringent page boundaries: top margin of 1.52 cm, bottom margin of 1.52 cm, left margin of 1.97 cm, and right margin of 1.96 cm. Body text must adhere to 12 pt Times New Roman with 1.5 line spacing and 1.27 cm first-line indentation.",
                "3.2 Table and Figure Caption Integrity",
                "Captions must remain visually tied to their corresponding graphics or tabular data. Our engine preserves all underlying table cells and images without alteration, applying uniform 10 pt styling.",
                "Figure 2: Layout comparison before and after intelligent formatting pipeline execution.",
            ],
        ),
        (
            "References",
            [
                "[1] Knuth, D. E. (1984). The TeXbook. Addison-Wesley, Reading, Massachusetts.",
                "[2] Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.",
                "[3] ISO/IEC 29500-1:2016. Information technology — Document description and processing languages.",
                "[4] Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR 12.",
                "[5] Lamport, L. (1994). LaTeX: A Document Preparation System. Addison-Wesley.",
            ],
        ),
    ]

    # Populate paragraphs with intentional messy formatting
    font_pool = ["Calibri", "Arial", "Georgia", "Verdana", "Tahoma"]
    size_pool = [10.5, 11.0, 13.0, 11.5]

    for ch_title, sections in chapters_data:
        # Chapter heading with inconsistent styling
        p_ch = doc.add_paragraph()
        r_ch = p_ch.add_run(ch_title)
        r_ch.font.name = "Arial"
        r_ch.font.size = Pt(15.0)
        r_ch.font.bold = True

        for sec in sections:
            p_sec = doc.add_paragraph()
            r_sec = p_sec.add_run(sec)
            r_sec.font.name = font_pool[len(doc.paragraphs) % len(font_pool)]
            r_sec.font.size = Pt(size_pool[len(doc.paragraphs) % len(size_pool)])

            # Insert sample table after Table 1 mention
            if "Table 1:" in sec:
                tbl = doc.add_table(rows=4, cols=3)
                tbl_data = [
                    ["Feature Name", "Data Type", "Relevance"],
                    ["font_size", "float", "Heading separation"],
                    ["uppercase_ratio", "float", "Title / acronyms"],
                    ["word_count", "integer", "Body vs heading"],
                ]
                for row_idx, row in enumerate(tbl.rows):
                    for col_idx, cell in enumerate(row.cells):
                        cell.text = tbl_data[row_idx][col_idx]

    # Pad if target_pages > 15
    multiplier = max(1, target_pages // 5)
    if multiplier > 1:
        for m in range(2, multiplier + 1):
            p_m = doc.add_paragraph()
            p_m.add_run(f"Chapter {m + 3}: Extended Topic and Technical Evaluation Monograph").font.bold = True
            for _ in range(15):
                p_body = doc.add_paragraph()
                p_body.add_run(
                    "Standardized computational processing demands reproducible algorithms. When formatting academic documents, automated heuristics must avoid altering original sentence structure while enforcing uniform margins, consistent indentations, and balanced heading scales."
                )

    doc.save(output_path)
    return output_path


def generate_all_samples():
    print("Generating samples/input.docx...")
    in_path = create_unformatted_manuscript("samples/input.docx", target_pages=5)

    print("Generating samples/expected_output.docx...")
    formatter = DocumentFormatter(in_path, "samples/expected_output.docx", include_toc=True)
    formatter.format()

    print("Sample generation complete!")


if __name__ == "__main__":
    generate_all_samples()
