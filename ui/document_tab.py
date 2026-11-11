from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk
from modules.doc_converter import docx_to_txt, txt_to_docx
from modules.pdf_converter import pdf_to_text
from . import dnd
from .widgets import ConverterTab, PathField, resolve_output, section_label

MODES = {
    "Word (.docx) → Text (.txt)": ([("Word", "*.docx")], ".txt", docx_to_txt),
    "Text (.txt) → Word (.docx)": ([("Text", "*.txt")], ".docx", txt_to_docx),
    "PDF → Text (.txt)": ([("PDF", "*.pdf")], ".txt", pdf_to_text),
}

MODE_BY_EXT = {".docx": "Word (.docx) → Text (.txt)", ".txt": "Text (.txt) → Word (.docx)",
               ".pdf": "PDF → Text (.txt)"}


class DocumentTab(ConverterTab):
    def __init__(self, master):
        super().__init__(master)
        section_label(self, "Conversion")
        self.mode = ctk.CTkOptionMenu(self, values=list(MODES), width=280)
        self.mode.pack(anchor="w")
        section_label(self, "Input file")
        self.src = PathField(self, dnd.hint("Choose or drop a file…", "Choose a file…"), self._browse_in)
        self.src.pack(fill="x")
        section_label(self, "Output file (optional, defaults to next to the input)")
        self.dst = PathField(self, "Output path…", self._browse_out)
        self.dst.pack(fill="x")
        ctk.CTkButton(self, text="Convert", height=36, command=self._convert).pack(fill="x", pady=20)
        dnd.enable_drop(self, self._on_drop)

    def _on_drop(self, paths):
        path = paths[0]
        self.src.set(path)
        mode = MODE_BY_EXT.get(Path(path).suffix.lower())
        if mode:  # pick the matching conversion automatically
            self.mode.set(mode)

    def _browse_in(self):
        return filedialog.askopenfilename(filetypes=MODES[self.mode.get()][0])

    def _browse_out(self):
        ext = MODES[self.mode.get()][1]
        return filedialog.asksaveasfilename(defaultextension=ext, filetypes=[("Output", f"*{ext}")])

    def _convert(self):
        src = self.src.get()
        if not src:
            self.set_status("Choose an input file first.", "error")
            return
        _, ext, func = MODES[self.mode.get()]
        try:
            dst = resolve_output(src, self.dst.get(), ext)
        except ValueError as exc:
            self.set_status(f"Error: {exc}", "error")
            return
        self.execute(lambda: func(src, dst), lambda _: f"Saved → {dst}")