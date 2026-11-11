import io
from pathlib import Path

import img2pdf
import pdfplumber
from PIL import Image, ImageOps

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
A4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))


def _prepare(path):
    """Return image bytes img2pdf can embed. Plain JPEGs are embedded losslessly;
    everything else (PNG, alpha, palette, CMYK...) is flattened onto white."""
    path = Path(path)
    with Image.open(path) as im:
        if im.format == "JPEG" and im.mode in ("RGB", "L"):
            return path.read_bytes()
        im = ImageOps.exif_transpose(im)
        rgba = im.convert("RGBA")
        flat = Image.new("RGB", rgba.size, "white")
        flat.paste(rgba, mask=rgba.getchannel("A"))
        buf = io.BytesIO()
        flat.save(buf, "PNG")
        return buf.getvalue()


def images_to_pdf(paths, output, page_size="fit"):
    """Bundle images (in the given order) into one PDF. page_size: 'fit' or 'a4'."""
    if not paths:
        raise ValueError("No images selected.")
    kwargs = {}
    if page_size == "a4":
        kwargs["layout_fun"] = img2pdf.get_layout_fun(
            A4, fit=img2pdf.FitMode.into, auto_orient=True
        )
    pdf = img2pdf.convert([_prepare(p) for p in paths], **kwargs)
    if pdf is None:
        raise RuntimeError("Failed to generate PDF.")
    Path(output).write_bytes(pdf)
    return len(paths)


def pdf_to_text(src, dst):
    """Extract text from a PDF into a UTF-8 text file. Returns page count."""
    with pdfplumber.open(src) as pdf:
        pages = [(page.extract_text() or "") for page in pdf.pages]
    if not any(p.strip() for p in pages):
        raise ValueError("No extractable text found (scanned PDF?).")
    Path(dst).write_text("\n\n".join(pages), encoding="utf-8")
    return len(pages)