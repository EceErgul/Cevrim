# Çevrim – File & Media Desktop Converter

A cross-platform desktop application built with **Python** and **CustomTkinter** for converting
images, documents and data files with a clean, modern interface (dark / light / system theme).
Everything runs locally: your files are never uploaded anywhere.

## Features

| Tab | What it does |
|-----|--------------|
| **Image → PDF** | Bundle multiple JPG / PNG images into one PDF. Reorder or remove images, choose *Fit to image* or *A4* pages. Plain JPEGs are embedded losslessly; transparent PNGs are flattened onto white. |
| **Documents** | Word (`.docx`) → Text, Text → Word (`.docx`), PDF → Text. Tables in Word files are kept in order (tab-separated). |
| **Data** | Convert between CSV, Excel (`.xlsx`) and JSON using Pandas. Legacy `.xls` files can be read (input only). |

Highlights:

- **Drag & drop** files onto any tab (or a whole folder of images on the Image tab). The Documents tab picks the matching conversion automatically.
- **Encoding-aware**: CSV and text files are detected as UTF-8, UTF-8 with BOM or Turkish `windows-1254`. CSV output uses UTF-8 with BOM, so Excel shows `ç ğ ı ö ş ü` correctly.
- **Safe outputs**: if you leave the output path empty, the result is saved next to the input and never overwrites an existing file (`name_converted.ext` is used instead).
- **Responsive UI**: conversions run in a background thread, with a progress bar and status line.

## Requirements

- Python 3.9 or newer
- Windows, macOS or Linux (on Linux you may need `sudo apt install python3-tk`)

## Installation

```bash
git clone https://github.com/<your-username>/cevrim.git
cd cevrim

python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
python main.py
```

## Usage

1. **Image → PDF**: click *Add images…* (or drop files / a folder), reorder with ↑ ↓, remove with ✕, pick the page size and click *Create PDF*.
2. **Documents**: pick the conversion, choose or drop the input file, optionally set an output path, click *Convert*.
3. **Data**: choose or drop a `.csv`, `.xlsx`, `.xls` or `.json` file, pick the target format, click *Convert*.

### Notes and limitations

- DOCX → PDF is not included: it needs Microsoft Word or LibreOffice, which would break the cross-platform, dependency-free goal.
- PDF → Text works on PDFs that contain real text. Scanned PDFs (images of pages) need OCR, which is not supported yet.
- `.xls` is read-only because the format is legacy; convert it to `.xlsx`, CSV or JSON.
- JSON input is flattened with `pandas.json_normalize`; JSON output is a list of records.
- Drag & drop needs `tkinterdnd2`. Without it, the app works normally using the Browse buttons.

## Project structure

```
cevrim/
├── main.py                 # entry point, tabbed CustomTkinter window
├── build.py                # PyInstaller build script
├── requirements.txt        # runtime dependencies
├── requirements-dev.txt    # + pytest, pyinstaller
├── pytest.ini
├── assets/                 # icons (icon.ico for Windows, icon.icns for macOS)
├── ui/                     # interface: one file per tab, shared widgets, drag & drop
│   ├── widgets.py
│   ├── dnd.py
│   ├── image_pdf_tab.py
│   ├── document_tab.py
│   └── data_tab.py
├── modules/                # conversion logic, no GUI imports
│   ├── pdf_converter.py
│   ├── doc_converter.py
│   ├── data_converter.py
│   └── utils.py
└── tests/
```

The `modules/` package knows nothing about the GUI, so it can be tested and reused (for example in a CLI).

## Development

```bash
pip install -r requirements-dev.txt
pytest
```

## Building a standalone app

```bash
python build.py
```

The result is placed in `dist/` (a single executable on Windows and Linux, a `.app` bundle on macOS).
Put `assets/icon.ico` (Windows) or `assets/icon.icns` (macOS) in place first if you want a custom icon.

## Roadmap

- PDF merge / split
- Turkish interface language
- OCR for scanned PDFs
- More image formats (WebP, BMP, TIFF)

## License

Add a license of your choice (for example MIT) as a `LICENSE` file before publishing.