"""
CLI Script to append manually labeled examples to dataset/training_data.csv.
"""

import os
import csv
import sys
import argparse

VALID_LABELS = [
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


def add_example(
    text: str,
    label: str,
    font_size: float = 12.0,
    bold: int = 0,
    italic: int = 0,
    alignment: int = 0,
    position_ratio: float = 0.5,
    csv_path: str = "dataset/training_data.csv",
) -> None:
    label = label.upper().strip()
    if label not in VALID_LABELS:
        raise ValueError(f"Invalid label '{label}'. Must be one of: {', '.join(VALID_LABELS)}")

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
        "font_size": font_size,
        "bold": bold,
        "italic": italic,
        "alignment": alignment,
        "word_count": w_count,
        "char_count": c_count,
        "uppercase_ratio": up_ratio,
        "starts_with_number": starts_num,
        "starts_with_chapter": starts_chap,
        "starts_with_figure": starts_fig,
        "starts_with_table": starts_tbl,
        "has_citation": has_cite,
        "position_ratio": round(position_ratio, 4),
        "label": label,
    }

    fieldnames = list(row.keys())
    file_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"Successfully added [{label}] example to {csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add manually labeled example to dataset")
    parser.add_argument("--text", required=True, help="Paragraph text content")
    parser.add_argument("--label", required=True, choices=VALID_LABELS, help="Target structural class")
    parser.add_argument("--font-size", type=float, default=12.0, help="Font size in pt")
    parser.add_argument("--bold", type=int, default=0, choices=[0, 1], help="Is bold (0 or 1)")
    parser.add_argument("--italic", type=int, default=0, choices=[0, 1], help="Is italic (0 or 1)")
    parser.add_argument("--alignment", type=int, default=0, help="0: Left, 1: Center, 2: Right, 3: Justify")
    parser.add_argument("--pos", type=float, default=0.5, help="Relative position in document (0.0 to 1.0)")
    args = parser.parse_args()

    add_example(
        text=args.text,
        label=args.label,
        font_size=args.font_size,
        bold=args.bold,
        italic=args.italic,
        alignment=args.alignment,
        position_ratio=args.pos,
    )
