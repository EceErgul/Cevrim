from tkinter import filedialog
import customtkinter as ctk
from modules.data_converter import convert
from . import dnd
from .widgets import ConverterTab, PathField, resolve_output, section_label

FORMATS = {"CSV (.csv)": ".csv", "Excel (.xlsx)": ".xlsx", "JSON (.json)": ".json"}


class DataTab(ConverterTab):
    def __init__(self, master):
        super().__init__(master)
        section_label(self, "Input file (.csv, .xlsx, .xls or .json)")
        self.src = PathField(self, dnd.hint("Choose or drop a file…", "Choose a file…"), self._browse_in)
        self.src.pack(fill="x")
        section_label(self, "Convert to")
        self.fmt = ctk.CTkOptionMenu(self, values=list(FORMATS), width=200)
        self.fmt.pack(anchor="w")
        section_label(self, "Output file (optional, defaults to next to the input)")
        self.dst = PathField(self, "Output path…", self._browse_out)
        self.dst.pack(fill="x")
        ctk.CTkButton(self, text="Convert", height=36, command=self._convert).pack(fill="x", pady=20)
        dnd.enable_drop(self, lambda paths: self.src.set(paths[0]))

    def _browse_in(self):
        return filedialog.askopenfilename(filetypes=[("Data files", "*.csv *.xlsx *.xls *.json")])

    def _browse_out(self):
        ext = FORMATS[self.fmt.get()]
        return filedialog.asksaveasfilename(defaultextension=ext, filetypes=[("Output", f"*{ext}")])

    def _convert(self):
        src = self.src.get()
        if not src:
            self.set_status("Choose an input file first.", "error")
            return
        try:
            dst = resolve_output(src, self.dst.get(), FORMATS[self.fmt.get()])
        except ValueError as exc:
            self.set_status(f"Error: {exc}", "error")
            return
        self.execute(
            lambda: convert(src, dst),
            lambda shape: f"Saved {shape[0]} rows × {shape[1]} columns → {dst}",
        )