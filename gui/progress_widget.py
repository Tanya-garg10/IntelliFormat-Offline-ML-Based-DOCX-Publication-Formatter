"""
Progress Widget Module (PySide6)
Displays active pipeline state, processed paragraph count, elapsed time, and ETA.
"""

try:
    from PySide6.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QProgressBar,
        QFrame,
    )
    from PySide6.QtCore import Qt, QTimer
except ImportError:
    QWidget = object

import time
from typing import Optional


class ProgressWidget(QWidget):
    """Real-time progress monitoring widget for formatting operations."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_time: float = 0.0
        self.total_paragraphs: int = 1
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        self.lbl_operation = QLabel("Status: Idle")
        self.lbl_operation.setStyleSheet("font-size: 14px; font-weight: bold; color: #1E293B;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid #CBD5E1;
                border-radius: 6px;
                text-align: center;
                height: 22px;
                background-color: #F1F5F9;
            }
            QProgressBar::chunk {
                background-color: #2563EB;
                border-radius: 5px;
            }
            """
        )

        # Telemetry labels row
        stats_row = QHBoxLayout()
        self.lbl_processed = QLabel("Processed: 0 / 0 paragraphs")
        self.lbl_elapsed = QLabel("Elapsed: 0.0s")
        self.lbl_eta = QLabel("Estimated Remaining: --")

        stats_row.addWidget(self.lbl_processed)
        stats_row.addWidget(self.lbl_elapsed)
        stats_row.addWidget(self.lbl_eta)

        layout.addWidget(self.lbl_operation)
        layout.addWidget(self.progress_bar)
        layout.addLayout(stats_row)

    def start_processing(self, total_paragraphs: int):
        self.start_time = time.time()
        self.total_paragraphs = max(1, total_paragraphs)
        self.progress_bar.setValue(0)
        self.lbl_operation.setText("Status: Starting analysis...")
        self.lbl_processed.setText(f"Processed: 0 / {self.total_paragraphs} paragraphs")

    def update_progress(self, current: int, operation_msg: str):
        elapsed = max(0.001, time.time() - self.start_time)
        pct = int(min(100, (current / self.total_paragraphs) * 100))
        self.progress_bar.setValue(pct)
        self.lbl_operation.setText(f"Status: {operation_msg}")
        self.lbl_processed.setText(f"Processed: {current} / {self.total_paragraphs} paragraphs")
        self.lbl_elapsed.setText(f"Elapsed: {elapsed:.1f}s")

        if current > 0:
            rate = current / elapsed
            remaining_paras = max(0, self.total_paragraphs - current)
            eta_sec = remaining_paras / rate if rate > 0 else 0
            self.lbl_eta.setText(f"Estimated Remaining: {eta_sec:.1f}s")
        else:
            self.lbl_eta.setText("Estimated Remaining: Calculating...")

    def finish_processing(self, summary_msg: str = "Completed successfully"):
        elapsed = time.time() - self.start_time
        self.progress_bar.setValue(100)
        self.lbl_operation.setText(f"Status: {summary_msg}")
        self.lbl_elapsed.setText(f"Elapsed: {elapsed:.1f}s")
        self.lbl_eta.setText("Estimated Remaining: 0.0s")
