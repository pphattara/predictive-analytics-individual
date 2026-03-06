#!/usr/bin/env python3
"""
Create a simple text-only PDF from a markdown file without external dependencies.

This is a fallback exporter for environments where pandoc/LaTeX are unavailable.
It preserves headings and bullets as wrapped text so a marker still receives a PDF.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List


PAGE_WIDTH = 612
PAGE_HEIGHT = 792
LEFT_MARGIN = 50
TOP_MARGIN = 50
BOTTOM_MARGIN = 50
LINE_HEIGHT = 14
FONT_SIZE = 11
CHARS_PER_LINE = 95


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def normalize_markdown(md: str) -> List[str]:
    lines: List[str] = []
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("# "):
            line = line[2:].strip().upper()
        elif line.startswith("## "):
            line = line[3:].strip()
        elif line.startswith("### "):
            line = line[4:].strip()
        line = line.replace("`", "")
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        line = re.sub(r"\*(.*?)\*", r"\1", line)
        lines.append(line)
    return lines


def wrap_line(line: str, width: int = CHARS_PER_LINE) -> List[str]:
    if not line:
        return [""]
    words = line.split()
    wrapped: List[str] = []
    current = words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            wrapped.append(current)
            current = word
    wrapped.append(current)
    return wrapped


def markdown_to_pages(md_text: str) -> List[List[str]]:
    lines = normalize_markdown(md_text)
    wrapped_lines: List[str] = []
    for line in lines:
        wrapped_lines.extend(wrap_line(line))

    max_lines_per_page = (PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN) // LINE_HEIGHT
    pages: List[List[str]] = []
    for i in range(0, len(wrapped_lines), max_lines_per_page):
        pages.append(wrapped_lines[i : i + max_lines_per_page])
    return pages or [[""]]


def build_pdf_bytes(pages: List[List[str]]) -> bytes:
    objects: List[bytes] = []

    # 1: Catalog
    # 2: Pages
    # 3: Font
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")

    page_obj_indices = []
    content_obj_indices = []
    next_obj = 4
    for _ in pages:
        page_obj_indices.append(next_obj)
        content_obj_indices.append(next_obj + 1)
        next_obj += 2

    kids = " ".join(f"{idx} 0 R" for idx in page_obj_indices)
    objects.append(f"<< /Type /Pages /Count {len(pages)} /Kids [ {kids} ] >>".encode("utf-8"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    for page_idx, lines in enumerate(pages):
        content_lines = ["BT", f"/F1 {FONT_SIZE} Tf", f"{LEFT_MARGIN} {PAGE_HEIGHT - TOP_MARGIN} Td"]
        for line in lines:
            content_lines.append(f"({escape_pdf_text(line)}) Tj")
            content_lines.append(f"0 -{LINE_HEIGHT} Td")
        content_lines.append("ET")
        content_stream = "\n".join(content_lines).encode("utf-8")
        content_obj = (
            f"<< /Length {len(content_stream)} >>\nstream\n".encode("utf-8")
            + content_stream
            + b"\nendstream"
        )
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                f"/Resources << /Font << /F1 3 0 R >> >> /Contents {content_obj_indices[page_idx]} 0 R >>"
            ).encode("utf-8")
        )
        objects.append(content_obj)

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode("utf-8"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("utf-8"))
    pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode("utf-8"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode("utf-8")
    )
    return bytes(pdf)


def main() -> None:
    src = Path("outputs/adult_census_income/report_final_iteration4.md")
    dst = Path("outputs/adult_census_income/report_final_iteration4.pdf")

    md = src.read_text(encoding="utf-8")
    pages = markdown_to_pages(md)
    dst.write_bytes(build_pdf_bytes(pages))
    print(f"written {dst} ({len(pages)} pages)")


if __name__ == "__main__":
    main()
