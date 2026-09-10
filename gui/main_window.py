"""
Main Window Module (PySide6)
Implements desktop GUI with sidebar navigation: Dashboard, Analyze, Format, Results, Performance, Settings.
Complies with modern clean white/blue UI styling.
"""

try:
    from PySide6.QtWidgets import (
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QStackedWidget,
        QPushButton,
        QLabel,
        QFrame,
        QTextEdit,
        QLineEdit,
        QSpinBox,
        QDoubleSpinBox,
        QFormLayout,
        QGroupBox,
        QTableWidget,
        QTableWidgetItem,
        QHeaderView,
        QMessageBox,
    )
    from PySide6.QtCore import Qt, QThread, Signal
except ImportError:
    QMainWindow = object
    QWidget = object
    Signal = lambda *args: None

import os
import sys
from typing import Optional, Dict, Any

from .upload_widget import UploadWidget
from .progress_widget import ProgressWidget
from .results_widget import ResultsWidget
from parser.docx_parser import DocxParser
from rules.confidence import HybridClassifier
from formatter.document_formatter import DocumentFormatter


class MainWindow(QMainWindow):
    """Main desktop application window for IntelliFormat."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IntelliFormat – Intelligent Offline DOCX-to-Publication Book Formatting")
        self.resize(1100, 750)
        self.current_docx_path: Optional[str] = None
        self.parsed_data: Optional[DocxParser] = None
        self.classifications = []
        self._init_ui()

    def _init_ui(self):
        root_widget = QWidget()
        self.setCentralWidget(root_widget)
        main_layout = QHBoxLayout(root_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Left Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(
            """
            QFrame {
                background-color: #0F172A;
                color: #F8FAFC;
                border-right: 1px solid #1E293B;
            }
            QPushButton {
                background-color: transparent;
                color: #94A3B8;
                text-align: left;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 500;
                border: none;
                border-radius: 6px;
                margin: 4px 10px;
            }
            QPushButton:hover {
                background-color: #1E293B;
                color: #FFFFFF;
            }
            QPushButton[active="true"] {
                background-color: #2563EB;
                color: #FFFFFF;
                font-weight: bold;
            }
            """
        )
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 16, 0, 16)
        sb_layout.setSpacing(4)

        # App Brand Title
        brand_label = QLabel("  INTELLIFORMAT")
        brand_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; padding: 10px 14px;")
        sub_brand = QLabel("   Offline DOCX Publication System")
        sub_brand.setStyleSheet("font-size: 11px; color: #38BDF8; padding-bottom: 16px;")

        sb_layout.addWidget(brand_label)
        sb_layout.addWidget(sub_brand)

        # Navigation buttons
        self.nav_buttons = {}
        pages = ["Dashboard", "Analyze", "Format", "Results", "Performance", "Settings"]
        for idx, page_name in enumerate(pages):
            btn = QPushButton(f"  {page_name}")
            btn.clicked.connect(lambda checked=False, i=idx: self.switch_page(i))
            sb_layout.addWidget(btn)
            self.nav_buttons[page_name] = btn

        sb_layout.addStretch()

        # Offline status badge
        offline_box = QFrame()
        offline_box.setStyleSheet("background-color: #022C22; border: 1px solid #065F46; border-radius: 6px; margin: 12px;")
        off_layout = QVBoxLayout(offline_box)
        lbl_off = QLabel("● OFFLINE SECURE")
        lbl_off.setStyleSheet("color: #34D399; font-weight: bold; font-size: 11px;")
        lbl_desc = QLabel("Zero cloud APIs • 100% Local ML")
        lbl_desc.setStyleSheet("color: #A7F3D0; font-size: 10px;")
        off_layout.addWidget(lbl_off)
        off_layout.addWidget(lbl_desc)
        sb_layout.addWidget(offline_box)

        main_layout.addWidget(sidebar)

        # 2. Right Content Stack
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #F8FAFC;")

        # Instantiate Pages
        self.page_dashboard = self._build_dashboard_page()
        self.page_analyze = self._build_analyze_page()
        self.page_format = self._build_format_page()
        self.page_results = self._build_results_page()
        self.page_performance = self._build_performance_page()
        self.page_settings = self._build_settings_page()

        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_analyze)
        self.stack.addWidget(self.page_format)
        self.stack.addWidget(self.page_results)
        self.stack.addWidget(self.page_performance)
        self.stack.addWidget(self.page_settings)

        main_layout.addWidget(self.stack)
        self.switch_page(0)

    def switch_page(self, index: int):
        self.stack.setCurrentIndex(index)
        pages = ["Dashboard", "Analyze", "Format", "Results", "Performance", "Settings"]
        for i, name in enumerate(pages):
            btn = self.nav_buttons.get(name)
            if btn:
                btn.setProperty("active", "true" if i == index else "false")
                btn.style().unpolish(btn)
                btn.style().polish(btn)

    def _build_dashboard_page(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Document Formatting Dashboard")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #0F172A;")
        layout.addWidget(title)

        self.dash_upload = UploadWidget()
        self.dash_upload.file_selected.connect(self._on_file_loaded)
        layout.addWidget(self.dash_upload)

        actions_box = QHBoxLayout()
        btn_analyze = QPushButton("1. Analyze Document Structure")
        btn_analyze.setStyleSheet("background-color: #2563EB; color: white; padding: 10px 20px; font-weight: bold; border-radius: 6px;")
        btn_analyze.clicked.connect(lambda: self.switch_page(1))

        btn_format = QPushButton("2. Format to Publication Specs")
        btn_format.setStyleSheet("background-color: #059669; color: white; padding: 10px 20px; font-weight: bold; border-radius: 6px;")
        btn_format.clicked.connect(lambda: self.switch_page(2))

        actions_box.addWidget(btn_analyze)
        actions_box.addWidget(btn_format)
        layout.addLayout(actions_box)

        layout.addStretch()
        return w

    def _build_analyze_page(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        lbl = QLabel("Structure & Element Detection")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #0F172A;")
        layout.addWidget(lbl)

        self.analyze_progress = ProgressWidget()
        layout.addWidget(self.analyze_progress)

        self.table_structure = QTableWidget(0, 4)
        self.table_structure.setHorizontalHeaderLabels(["Index", "Detected Class", "Confidence", "Paragraph Snippet"])
        self.table_structure.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        layout.addWidget(self.table_structure)

        return w

    def _build_format_page(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        lbl = QLabel("Publication Formatting Engine")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #0F172A;")
        layout.addWidget(lbl)

        specs_info = QLabel(
            "• Page: Margins (1.52cm top/bottom, 1.97cm left, 1.96cm right, gutter left)\n"
            "• Body: Times New Roman 12 pt, Justified, 1.5 line spacing, 1.27 cm first-line indent\n"
            "• Heading 1: Times New Roman 16 pt Bold\n"
            "• Subheading: Times New Roman 12 pt Bold\n"
            "• Tables & Figures: 100% Content & Data Preservation"
        )
        specs_info.setStyleSheet("background-color: #F1F5F9; padding: 14px; border-radius: 8px; font-size: 13px; line-height: 1.6;")
        layout.addWidget(specs_info)

        self.format_progress = ProgressWidget()
        layout.addWidget(self.format_progress)

        btn_run_format = QPushButton("Apply Publication Formatting & Generate DOCX")
        btn_run_format.setStyleSheet("background-color: #2563EB; color: white; padding: 12px 24px; font-size: 15px; font-weight: bold; border-radius: 6px;")
        btn_run_format.clicked.connect(self._on_format_execute)
        layout.addWidget(btn_run_format)

        layout.addStretch()
        return w

    def _build_results_page(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(24, 24, 24, 24)
        lbl = QLabel("Before / After Comparison & Verification")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #0F172A;")
        layout.addWidget(lbl)

        self.results_widget = ResultsWidget()
        layout.addWidget(self.results_widget)
        layout.addStretch()
        return w

    def _build_performance_page(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(24, 24, 24, 24)
        lbl = QLabel("Performance Benchmarking (100, 200, 400+ Pages)")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #0F172A;")
        layout.addWidget(lbl)

        self.perf_log = QTextEdit()
        self.perf_log.setReadOnly(True)
        self.perf_log.setPlaceholderText("Click 'Run Benchmark Suite' to execute 100, 200, and 400+ page latency & peak memory tests...")
        layout.addWidget(self.perf_log)

        btn_run_bench = QPushButton("Run Benchmark Suite")
        btn_run_bench.setStyleSheet("background-color: #0F172A; color: white; padding: 10px 20px; font-weight: bold; border-radius: 6px;")
        btn_run_bench.clicked.connect(self._on_run_benchmark)
        layout.addWidget(btn_run_bench)

        return w

    def _build_settings_page(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(24, 24, 24, 24)
        lbl = QLabel("Publication & Engine Settings")
        lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #0F172A;")
        layout.addWidget(lbl)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px;")
        form = QFormLayout(form_frame)

        self.set_top_margin = QDoubleSpinBox()
        self.set_top_margin.setValue(1.52)
        self.set_bottom_margin = QDoubleSpinBox()
        self.set_bottom_margin.setValue(1.52)
        self.set_left_margin = QDoubleSpinBox()
        self.set_left_margin.setValue(1.97)
        self.set_right_margin = QDoubleSpinBox()
        self.set_right_margin.setValue(1.96)

        form.addRow("Top Margin (cm):", self.set_top_margin)
        form.addRow("Bottom Margin (cm):", self.set_bottom_margin)
        form.addRow("Left Margin (cm):", self.set_left_margin)
        form.addRow("Right Margin (cm):", self.set_right_margin)

        layout.addWidget(form_frame)
        layout.addStretch()
        return w

    def _on_file_loaded(self, file_path: str):
        self.current_docx_path = file_path
        try:
            self.parsed_data = DocxParser(file_path).load()
            self.dash_upload.update_document_stats(self.parsed_data.get_summary())
        except Exception as e:
            if hasattr(QMessageBox, "critical"):
                QMessageBox.critical(self, "Error", f"Failed to load document: {e}")

    def _on_format_execute(self):
        if not self.current_docx_path:
            self.switch_page(0)
            return
        self.format_progress.start_processing(len(self.parsed_data.paragraphs) if self.parsed_data else 10)
        formatter = DocumentFormatter(self.current_docx_path, "output/formatted_book.docx")
        formatter.format(progress_callback=self.format_progress.update_progress)
        self.switch_page(3)

    def _on_run_benchmark(self):
        from performance.benchmark import run_benchmark
        self.perf_log.append("Starting benchmark suite across 100, 200, and 400+ pages...")
        res = run_benchmark()
        import json
        self.perf_log.setText(json.dumps(res, indent=2))
