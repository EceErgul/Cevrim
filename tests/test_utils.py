import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from modules.data_converter import read_table
from modules.pdf_converter import images_to_pdf, pdf_to_text
from modules.utils import detect_encoding, resolve_output


def test_resolve_output_default_and_no_overwrite(tmp_path):
    src = tmp_path / "a.csv"
    src.write_text("x\n1")
    assert resolve_output(src, "", ".json") == tmp_path / "a.json"
    (tmp_path / "a.json").write_text("[]")
    assert resolve_output(src, "", ".json") == tmp_path / "a_converted.json"
    assert resolve_output(src, "", ".csv") == tmp_path / "a_converted.csv"
    with pytest.raises(ValueError):
        resolve_output(src, str(src), ".csv")


def test_turkish_windows_1254_csv(tmp_path):
    p = tmp_path / "tr.csv"
    p.write_bytes("ad;şehir\nÇağlar;İzmir\nIşık;Ağrı\n".encode("cp1254"))
    assert detect_encoding(p) == "cp1254"
    df = read_table(p)
    assert list(df.columns) == ["ad", "şehir"] and df["ad"][0] == "Çağlar"
    rows = "Şule;Muğla\nÖzgür;Çanakkale\nGüneş;Isparta\n" * 60
    p.write_bytes(("ad;şehir\n" + rows).encode("cp1254"))
    assert read_table(p)["ad"][0] == "Şule"


def test_utf8_and_bom_detection(tmp_path):
    p = tmp_path / "u.csv"
    p.write_text("ad;şehir\nÇağlar;İzmir\n", encoding="utf-8")
    assert detect_encoding(p) == "utf-8"
    p.write_text("ad;şehir\nÇağlar;İzmir\n", encoding="utf-8-sig")
    assert detect_encoding(p) == "utf-8-sig"


def test_pdf_without_text_raises(tmp_path):
    from PIL import Image
    Image.new("RGB", (40, 40), "white").save(tmp_path / "i.png")
    images_to_pdf([tmp_path / "i.png"], tmp_path / "i.pdf")
    with pytest.raises(ValueError):
        pdf_to_text(tmp_path / "i.pdf", tmp_path / "o.txt")