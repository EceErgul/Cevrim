import codecs
from pathlib import Path
from charset_normalizer import from_bytes

_TURKISH_BYTES = bytes([0xD0, 0xDE, 0xF0, 0xFE])
_LOOKALIKES = {"cp1250", "cp1252", "latin_1", "iso8859_1", "iso8859_2", "iso8859_15"}

def detect_encoding(path, default="utf-8"):
    """Best-effort text encoding detection (UTF-8, UTF-8 BOM, windows-1254, ...)."""
    raw = Path(path).read_bytes()[:200_000]
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    try:  # final=False tolerates a multi-byte character cut off at the end of the sample
        codecs.getincrementaldecoder("utf-8")().decode(raw)
        return "utf-8"
    except UnicodeDecodeError:
        pass
    best = from_bytes(raw).best()
    if best is None:
        return default
    name = best.encoding.lower().replace("-", "_")
    if name in _LOOKALIKES and any(b in raw for b in _TURKISH_BYTES):
        return "cp1254"
    return best.encoding

def read_text(path):
    return Path(path).read_text(encoding=detect_encoding(path), errors="replace")

def resolve_output(src, out, ext):
    """Use the chosen output path, or derive one next to the input without overwriting."""
    src = Path(src)
    if out:
        dst = Path(out)
    else:
        dst = src.with_suffix(ext)
        if dst.exists():
            dst = src.with_name(f"{src.stem}_converted{ext}")
    if dst.resolve() == src.resolve():
        raise ValueError("Output would overwrite the input file.")
    return dst