"""
Generate report_final_iteration4.pdf from report_final_iteration4.md
Uses reportlab Platypus for proper academic PDF layout.
"""
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib import colors

BASE = Path("/Users/princephattara/Coding Project/predictive-analytics/individual")
MD_PATH  = BASE / "outputs/adult_census_income/report_final_iteration4.md"
PDF_PATH = BASE / "outputs/adult_census_income/report_final_iteration4.pdf"

# ---------- styles ----------
def build_styles():
    base = getSampleStyleSheet()
    s = {}
    s['title'] = ParagraphStyle(
        'ReportTitle', parent=base['Title'],
        fontSize=16, leading=20, spaceAfter=4,
        alignment=TA_CENTER, textColor=colors.HexColor('#1a1a2e')
    )
    s['subtitle'] = ParagraphStyle(
        'Subtitle', parent=base['Normal'],
        fontSize=11, leading=14, spaceAfter=14,
        alignment=TA_CENTER, textColor=colors.HexColor('#444444')
    )
    s['h2'] = ParagraphStyle(
        'H2', parent=base['Heading2'],
        fontSize=13, leading=16, spaceBefore=16, spaceAfter=6,
        textColor=colors.HexColor('#1a1a2e'), fontName='Helvetica-Bold'
    )
    s['h3'] = ParagraphStyle(
        'H3', parent=base['Heading3'],
        fontSize=11, leading=14, spaceBefore=10, spaceAfter=4,
        textColor=colors.HexColor('#2c2c54'), fontName='Helvetica-Bold'
    )
    s['body'] = ParagraphStyle(
        'Body', parent=base['Normal'],
        fontSize=10, leading=14, spaceAfter=8,
        alignment=TA_JUSTIFY, fontName='Helvetica'
    )
    s['bold_body'] = ParagraphStyle(
        'BoldBody', parent=base['Normal'],
        fontSize=10, leading=14, spaceAfter=4,
        fontName='Helvetica-Bold'
    )
    s['bullet'] = ParagraphStyle(
        'Bullet', parent=base['Normal'],
        fontSize=10, leading=13, spaceAfter=3,
        leftIndent=14, fontName='Helvetica'
    )
    s['table_header'] = ParagraphStyle(
        'TH', parent=base['Normal'],
        fontSize=9, fontName='Helvetica-Bold', leading=12
    )
    s['table_cell'] = ParagraphStyle(
        'TC', parent=base['Normal'],
        fontSize=9, fontName='Helvetica', leading=12
    )
    return s

STYLES = build_styles()

TABLE_STYLE = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
    ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
    ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE',   (0, 0), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f5f5f5'), colors.white]),
    ('GRID',       (0, 0), (-1, -1), 0.4, colors.HexColor('#cccccc')),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING',  (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
])

BOLD_ROW_STYLE = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
    ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
    ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE',   (0, 0), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f5f5f5'), colors.white]),
    ('GRID',       (0, 0), (-1, -1), 0.4, colors.HexColor('#cccccc')),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING',  (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTNAME',   (0, 5), (-1, 5), 'Helvetica-Bold'),  # HGB tuned row in table1
])

# ---------- markdown parser ----------

def escape_xml(text):
    """Escape XML special characters for ReportLab Paragraph."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

def md_inline_to_rl(text):
    """Convert inline markdown (bold, code) to ReportLab XML."""
    text = escape_xml(text)
    # **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # `code`
    text = re.sub(r'`(.+?)`', r'<font name="Courier" size="9">\1</font>', text)
    return text

def parse_table(lines):
    """Parse markdown table lines into list-of-lists."""
    rows = []
    for line in lines:
        line = line.strip()
        if re.match(r'^\|[-| :]+\|$', line):
            continue  # separator row
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cells)
    return rows

def build_table_flowable(rows, col_widths=None):
    """Build a ReportLab Table from list-of-lists."""
    table_data = []
    for i, row in enumerate(rows):
        style = STYLES['table_header'] if i == 0 else STYLES['table_cell']
        table_data.append([Paragraph(md_inline_to_rl(c), style) for c in row])

    page_width = A4[0] - 4 * cm  # usable width
    if col_widths is None:
        n = len(rows[0])
        col_widths = [page_width / n] * n

    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TABLE_STYLE)
    return t

def md_to_flowables(md_text):
    """Convert full markdown text to list of ReportLab flowables."""
    flowables = []
    lines = md_text.splitlines()
    i = 0
    title_done = False
    subtitle_done = False

    while i < len(lines):
        line = lines[i]

        # --- horizontal rule ---
        if re.match(r'^---+$', line.strip()):
            flowables.append(HRFlowable(width='100%', thickness=0.5,
                                        color=colors.HexColor('#cccccc'),
                                        spaceAfter=6, spaceBefore=6))
            i += 1
            continue

        # --- headings ---
        m = re.match(r'^(#{1,3})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text  = md_inline_to_rl(m.group(2))
            if level == 1 and not title_done:
                flowables.append(Paragraph(text, STYLES['title']))
                title_done = True
            elif level == 2 and not subtitle_done and 'MSIN' in text:
                flowables.append(Paragraph(text, STYLES['subtitle']))
                subtitle_done = True
            elif level == 2:
                flowables.append(Paragraph(text, STYLES['h2']))
            elif level == 3:
                flowables.append(Paragraph(text, STYLES['h3']))
            i += 1
            continue

        # --- markdown table (block starting with |) ---
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].startswith('|'):
                table_lines.append(lines[i])
                i += 1
            rows = parse_table(table_lines)
            if rows:
                # Determine column widths heuristically by column index
                n = len(rows[0])
                page_width = A4[0] - 4 * cm
                if n == 4:
                    col_widths = [page_width * 0.35, page_width * 0.22,
                                  page_width * 0.22, page_width * 0.21]
                elif n == 3:
                    col_widths = [page_width * 0.40, page_width * 0.30,
                                  page_width * 0.30]
                elif n == 2:
                    col_widths = [page_width * 0.45, page_width * 0.55]
                else:
                    col_widths = [page_width / n] * n
                flowables.append(Spacer(1, 4))
                flowables.append(build_table_flowable(rows, col_widths))
                flowables.append(Spacer(1, 8))
            continue

        # --- blank line ---
        if not line.strip():
            i += 1
            continue

        # --- normal paragraph ---
        text = md_inline_to_rl(line.strip())
        if text:
            flowables.append(Paragraph(text, STYLES['body']))
        i += 1

    return flowables


def main():
    md_text = MD_PATH.read_text(encoding='utf-8')
    flowables = md_to_flowables(md_text)

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm,  bottomMargin=2*cm,
        title="Predicting Annual Income — MSIN0097 Individual Coursework",
        author="UCL Student"
    )
    doc.build(flowables)
    print(f"PDF written to: {PDF_PATH}")
    print(f"File size: {PDF_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == '__main__':
    main()
