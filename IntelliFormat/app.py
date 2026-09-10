"""
IntelliFormat – Intelligent Offline DOCX-to-Publication Book Formatting System
Main Application Entrypoint
Supports desktop GUI (PySide6) as well as CLI and automated execution modes.
Strictly 100% Offline (No cloud APIs, no LLMs, no network dependencies).
"""

import os
import sys
import argparse
import time

# Ensure current directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from parser.docx_parser import DocxParser
from rules.confidence import HybridClassifier
from formatter.document_formatter import DocumentFormatter
from evaluation.accuracy import AccuracyEvaluator
from performance.benchmark import run_benchmark


def run_gui():
    """Attempts to launch PySide6 Desktop GUI."""
    try:
        from PySide6.QtWidgets import QApplication
        from gui.main_window import MainWindow

        # Check for headless environment
        if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
            print("Notice: Headless Linux environment detected (no DISPLAY server).")
            print("Launching interactive CLI / API mode. Run with --help for options.")
            run_cli_interactive()
            return

        app = QApplication(sys.argv)
        app.setApplicationName("IntelliFormat")
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except ImportError:
        print("PySide6 is not installed or GUI libraries are unavailable in this environment.")
        print("Defaulting to IntelliFormat CLI Engine.")
        run_cli_interactive()
    except Exception as e:
        print(f"GUI Initialization encountered error: {e}")
        print("Falling back to CLI engine.")
        run_cli_interactive()


def run_cli_interactive():
    print("=" * 68)
    print("INTELLIFORMAT: Offline Intelligent DOCX-to-Publication System")
    print("Zero Cloud APIs • No LLMs • 100% Local Classical ML + Rules Engine")
    print("=" * 68)
    sample_input = "samples/input.docx"
    output_path = "output/formatted_book.docx"

    if os.path.exists(sample_input):
        print(f"\n[1] Parsing sample manuscript: '{sample_input}'...")
        parser = DocxParser(sample_input).load()
        stats = parser.get_summary()
        print(f"    Total Paragraphs: {stats['paragraph_count']}")
        print(f"    Estimated Pages:  {stats['estimated_pages']}")
        print(f"    Tables:           {stats['table_count']}")
        print(f"    Embedded Figures: {stats['image_count']}")

        print("\n[2] Executing Hybrid Structure Classification (Random Forest + Rules)...")
        classifier = HybridClassifier()
        classifications = classifier.classify_document(parser.paragraphs)

        class_counts = {}
        for c in classifications:
            cls_name = c["final_class"]
            class_counts[cls_name] = class_counts.get(cls_name, 0) + 1

        print("    Detected Structures:")
        for cls_name, count in sorted(class_counts.items()):
            print(f"      • {cls_name:16}: {count}")

        print(f"\n[3] Applying Publication Specifications to '{output_path}'...")
        formatter = DocumentFormatter(sample_input, output_path, include_toc=True)
        t0 = time.time()
        formatter.format(classifications=classifications)
        t1 = time.time()
        print(f"    Formatted publication DOCX generated in {t1 - t0:.2f}s!")
        print(f"    Saved to: {os.path.abspath(output_path)}")
        print("=" * 68)


def main():
    parser = argparse.ArgumentParser(description="IntelliFormat Offline DOCX Formatter")
    parser.add_argument("--gui", action="store_true", help="Force desktop GUI mode")
    parser.add_argument("--analyze", type=str, help="Path to input DOCX for structure analysis")
    parser.add_argument("--format", type=str, help="Path to input DOCX for full publication formatting")
    parser.add_argument("--output", type=str, default="output/formatted_book.docx", help="Output file path")
    parser.add_argument("--benchmark", action="store_true", help="Run 100, 200, 400+ page benchmark suite")
    parser.add_argument("--no-toc", action="store_true", help="Disable Table of Contents generation")
    args = parser.parse_args()

    if args.benchmark:
        run_benchmark()
        return

    if args.analyze:
        print(f"Analyzing manuscript: {args.analyze}")
        p = DocxParser(args.analyze).load()
        clf = HybridClassifier()
        results = clf.classify_document(p.paragraphs)
        for r in results[:20]:
            print(f"[{r['final_class']}] (Confidence: {r['confidence_percent']}%) - {r['clean_text'][:60]}")
        return

    if args.format:
        print(f"Formatting manuscript: {args.format} -> {args.output}")
        fmt = DocumentFormatter(args.format, args.output, include_toc=not args.no_toc)
        fmt.format()
        print(f"Successfully generated formatted publication document: {args.output}")
        return

    if args.gui:
        run_gui()
    else:
        # Default behavior: try GUI if available, otherwise CLI
        run_gui()


if __name__ == "__main__":
    main()
