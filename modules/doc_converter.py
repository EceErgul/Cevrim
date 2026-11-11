from pathlib import Path
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from .utils import read_text


def docx_to_txt(src, dst):
    """Word -> plain text, keeping paragraphs and tables (tab-separated) in order."""
    doc = Document(src)
    lines = []
    for child in doc.element.body.iterchildren():
        if child.tag.endswith("}p"):
            lines.append(Paragraph(child, doc).text)
        elif child.tag.endswith("}tbl"):
            for row in Table(child, doc).rows:
                lines.append("\t".join(c.text.strip() for c in row.cells))
    Path(dst).write_text("\n".join(lines), encoding="utf-8")
    return len(lines)


def txt_to_docx(src, dst):
    """Plain text (any common encoding) -> Word, one paragraph per line."""
    doc = Document()
    lines = read_text(src).splitlines()
    for line in lines:
        doc.add_paragraph(line)
    doc.save(dst)
    return len(lines)