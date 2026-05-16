"""
Generate a reference.docx with GOST 7.32-2017 + KBTU formatting.
Run: uv run python scripts/make_reference_docx.py
Output: thesis/reference.docx  (used by build_thesis.sh as pandoc --reference-doc)
"""

from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy
from pathlib import Path

OUT = Path(__file__).parent.parent / "thesis" / "reference.docx"


def set_page_margins(doc):
    """Left 30 mm, right 10 mm, top 20 mm, bottom 20 mm — GOST/KBTU."""
    for section in doc.sections:
        section.left_margin = Mm(30)
        section.right_margin = Mm(10)
        section.top_margin = Mm(20)
        section.bottom_margin = Mm(20)
        section.page_width = Mm(210)
        section.page_height = Mm(297)


def style_normal(doc):
    """Body text: Times New Roman 14 pt, single spacing, 1.25 cm first-line indent."""
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(14)
    font.color.rgb = RGBColor(0, 0, 0)

    pf = style.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(14)          # single spacing for 14 pt
    pf.first_line_indent = Mm(12.5)   # 1.25 cm paragraph indent
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def style_heading(doc, name, size, bold, italic=False, caps=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=Pt(12), space_after=Pt(6)):
    if name not in [s.name for s in doc.styles]:
        return
    style = doc.styles[name]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(size)
    font.bold = bold
    font.italic = italic
    font.all_caps = caps
    font.color.rgb = RGBColor(0, 0, 0)

    pf = style.paragraph_format
    pf.space_before = space_before
    pf.space_after = space_after
    pf.first_line_indent = Mm(0)
    pf.alignment = align
    pf.page_break_before = True if name == "Heading 1" else False
    pf.keep_with_next = True


def style_caption(doc):
    """Figure/table captions: Times New Roman 12 pt."""
    for name in ("Caption",):
        if name not in [s.name for s in doc.styles]:
            continue
        style = doc.styles[name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(12)
        style.font.italic = False
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        style.paragraph_format.first_line_indent = Mm(0)


def style_footer(doc):
    """Page numbers: bottom centre, 12 pt."""
    for section in doc.sections:
        footer = section.footer
        if not footer.paragraphs:
            footer.add_paragraph()
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.clear()
        run = p.add_run()
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        # Insert PAGE field
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(qn("w:fldCharType"), "begin")
        instrText = OxmlElement("w:instrText")
        instrText.text = " PAGE "
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(qn("w:fldCharType"), "end")
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)


def main():
    doc = Document()
    set_page_margins(doc)
    style_normal(doc)

    # Heading 1 — chapter title: 16 pt, bold, centred, ALL CAPS, page break before
    style_heading(doc, "Heading 1", size=16, bold=True, caps=True,
                  align=WD_ALIGN_PARAGRAPH.CENTER,
                  space_before=Pt(12), space_after=Pt(6))

    # Heading 2 — section: 14 pt, bold, left-aligned
    style_heading(doc, "Heading 2", size=14, bold=True,
                  align=WD_ALIGN_PARAGRAPH.LEFT,
                  space_before=Pt(10), space_after=Pt(4))

    # Heading 3 — subsection: 14 pt, bold italic, left-aligned
    style_heading(doc, "Heading 3", size=14, bold=True, italic=True,
                  align=WD_ALIGN_PARAGRAPH.LEFT,
                  space_before=Pt(8), space_after=Pt(2))

    style_caption(doc)
    style_footer(doc)

    # Add a placeholder paragraph so the file isn't empty
    doc.add_paragraph("REFERENCE DOCUMENT — do not edit directly.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print(f"✓ reference.docx written to {OUT}")


if __name__ == "__main__":
    main()
