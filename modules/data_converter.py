import json
from pathlib import Path
import pandas as pd
from .utils import detect_encoding

FORMATS = (".csv", ".xlsx", ".json")
INPUT_FORMATS = FORMATS + (".xls",)


def read_table(path):
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path, sep=None, engine="python", encoding=detect_encoding(path))
    if ext == ".xlsx":
        return pd.read_excel(path, engine="openpyxl")
    if ext == ".xls":
        return pd.read_excel(path, engine="xlrd")
    if ext == ".json":
        with open(path, encoding=detect_encoding(path)) as f:
            return pd.json_normalize(json.load(f))
    raise ValueError(f"Unsupported input format: {ext or 'unknown'}")


def write_table(df, path):
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":  # BOM so Excel shows Turkish characters correctly
        df.to_csv(path, index=False, encoding="utf-8-sig")
    elif ext == ".xlsx":
        df.to_excel(path, index=False, engine="openpyxl")
    elif ext == ".json":
        df.to_json(path, orient="records", indent=2, force_ascii=False, date_format="iso")
    else:
        raise ValueError(f"Unsupported output format: {ext or 'unknown'}")


def convert(src, dst):
    """Convert between CSV / XLSX / JSON. Returns (rows, columns)."""
    df = read_table(src)
    write_table(df, dst)
    return df.shape