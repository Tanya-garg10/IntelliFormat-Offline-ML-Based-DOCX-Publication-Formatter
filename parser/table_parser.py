"""
Table parser module.
Extracts table structure, row counts, column counts, and content preservation metadata.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from docx.table import Table


@dataclass
class TableInfo:
    index: int
    num_rows: int
    num_cols: int
    headers: List[str] = field(default_factory=list)
    cell_data: List[List[str]] = field(default_factory=list)
    total_cells: int = 0
    raw_docx_table: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "num_rows": self.num_rows,
            "num_cols": self.num_cols,
            "headers": self.headers,
            "total_cells": self.total_cells,
            "sample_data": self.cell_data[:3] if self.cell_data else [],
        }


class TableParser:
    """Parses and analyzes python-docx Table objects."""

    @staticmethod
    def parse_table(table: Table, index: int) -> TableInfo:
        rows = table.rows
        num_rows = len(rows)
        num_cols = len(table.columns) if num_rows > 0 else 0

        cell_data: List[List[str]] = []
        headers: List[str] = []

        for r_idx, row in enumerate(rows):
            row_vals = []
            for cell in row.cells:
                text = cell.text.strip() if cell.text else ""
                row_vals.append(text)
            cell_data.append(row_vals)
            if r_idx == 0:
                headers = row_vals

        return TableInfo(
            index=index,
            num_rows=num_rows,
            num_cols=num_cols,
            headers=headers,
            cell_data=cell_data,
            total_cells=num_rows * num_cols,
            raw_docx_table=table,
        )
