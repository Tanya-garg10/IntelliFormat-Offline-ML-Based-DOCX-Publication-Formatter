"""
Upload Widget Module (PySide6)
Provides drag-and-drop manuscript loading and summary metadata display.
"""

try:
    from PySide6.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QFileDialog,
        QFrame,
        QGridLayout,
    )
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtGui import QDragEnterEvent, QDropEvent
except ImportError:
    # Graceful fallback for non-GUI environments
    QWidget = object
    Signal = lambda *args: None

from typing import Dict, Any, Optional
import os


class UploadWidget(QWidget):
    """File upload card and metadata summary area."""

    file_selected = Signal(str) if hasattr(Signal, "__call__") else None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_file_path: Optional[str] = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Drop Zone Frame
        self.drop_frame = QFrame()
        self.drop_frame.setFrameShape(QFrame.StyledPanel)
        self.drop_frame.setStyleSheet(
            """
            QFrame {
                border: 2px dashed #3B82F6;
                border-radius: 8px;
                background-color: #F8FAFC;
                padding: 24px;
            }
            QFrame:hover {
                background-color: #EFF6FF;
            }
            """
        )
        drop_layout = QVBoxLayout(self.drop_frame)
        drop_layout.setAlignment(Qt.AlignCenter)

        self.lbl_title = QLabel("Select or Drag & Drop Word Manuscript (.docx)")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1E293B;")
        self.lbl_subtitle = QLabel("Supports voluminous 400+ page manuscripts • 100% Offline Processing")
        self.lbl_subtitle.setStyleSheet("font-size: 13px; color: #64748B;")

        self.btn_browse = QPushButton("Browse DOCX File")
        self.btn_browse.setStyleSheet(
            """
            QPushButton {
                background-color: #2563EB;
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
            """
        )
        self.btn_browse.clicked.connect(self._on_browse_clicked)

        drop_layout.addWidget(self.lbl_title, alignment=Qt.AlignCenter)
        drop_layout.addWidget(self.lbl_subtitle, alignment=Qt.AlignCenter)
        drop_layout.addWidget(self.btn_browse, alignment=Qt.AlignCenter)

        layout.addWidget(self.drop_frame)

        # Stats Card
        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet(
            "QFrame { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; }"
        )
        stats_layout = QGridLayout(self.stats_frame)

        self.lbl_filename = QLabel("File: No manuscript loaded")
        self.lbl_filename.setStyleSheet("font-weight: bold; color: #0F172A;")

        self.lbl_pages = QLabel("Pages: -")
        self.lbl_paras = QLabel("Paragraphs: -")
        self.lbl_tables = QLabel("Tables: -")
        self.lbl_figures = QLabel("Figures: -")

        stats_layout.addWidget(self.lbl_filename, 0, 0, 1, 4)
        stats_layout.addWidget(self.lbl_pages, 1, 0)
        stats_layout.addWidget(self.lbl_paras, 1, 1)
        stats_layout.addWidget(self.lbl_tables, 1, 2)
        stats_layout.addWidget(self.lbl_figures, 1, 3)

        layout.addWidget(self.stats_frame)

    def _on_browse_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Manuscript DOCX",
            "",
            "Word Documents (*.docx)",
        )
        if file_path:
            self.set_file(file_path)

    def set_file(self, file_path: str):
        self.selected_file_path = file_path
        self.lbl_filename.setText(f"File: {os.path.basename(file_path)}")
        if hasattr(self, "file_selected") and self.file_selected:
            self.file_selected.emit(file_path)

    def update_document_stats(self, stats: Dict[str, Any]):
        self.lbl_pages.setText(f"Pages: {stats.get('estimated_pages', '-')}")
        self.lbl_paras.setText(f"Paragraphs: {stats.get('paragraph_count', '-')}")
        self.lbl_tables.setText(f"Tables: {stats.get('table_count', '-')}")
        self.lbl_figures.setText(f"Figures: {stats.get('image_count', '-')}")
