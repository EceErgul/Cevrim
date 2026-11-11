import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from PIL import Image
from modules.data_converter import convert
from modules.doc_converter import docx_to_txt, txt_to_docx
from modules.pdf_converter import images_to_pdf


def test_data_roundtrip(tmp_path):
    csv = tmp_path / "a.csv"
    pd.DataFrame({"ad": ["Çağlar", "Işık"], "yaş": [30, 25]}).to_csv(csv, index=False)
    assert convert(csv, tmp_path / "a.xlsx") == (2, 2)
    assert convert(tmp_path / "a.xlsx", tmp_path / "a.json") == (2, 2)
    assert json.loads((tmp_path / "a.json").read_text(encoding="utf-8"))[0]["ad"] == "Çağlar"


def test_docs_roundtrip(tmp_path):
    (tmp_path / "t.txt").write_text("Merhaba\nDünya", encoding="utf-8")
    txt_to_docx(tmp_path / "t.txt", tmp_path / "t.docx")
    docx_to_txt(tmp_path / "t.docx", tmp_path / "o.txt")
    assert (tmp_path / "o.txt").read_text(encoding="utf-8") == "Merhaba\nDünya"


def test_images_to_pdf(tmp_path):
    Image.new("RGBA", (50, 50), (255, 0, 0, 80)).save(tmp_path / "a.png")
    Image.new("RGB", (80, 40), "blue").save(tmp_path / "b.jpg")
    for size in ("fit", "a4"):
        out = tmp_path / f"{size}.pdf"
        assert images_to_pdf([tmp_path / "a.png", tmp_path / "b.jpg"], out, size) == 2
        assert out.read_bytes().startswith(b"%PDF")