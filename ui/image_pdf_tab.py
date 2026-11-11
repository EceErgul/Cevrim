from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk
from modules.pdf_converter import IMAGE_EXTS, images_to_pdf
from . import dnd
from .widgets import ConverterTab, FileList


class ImagePdfTab(ConverterTab):
    def __init__(self, master):
        super().__init__(master)
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", pady=(0, 8))
        ctk.CTkButton(bar, text="Add images…", command=self._add).pack(side="left")
        ctk.CTkButton(bar, text="Clear", width=70, fg_color="gray40", command=lambda: self.files.clear()).pack(side="left", padx=8)
        self.page = ctk.CTkOptionMenu(bar, values=["Fit to image", "A4"], width=130)
        self.page.pack(side="right")
        ctk.CTkLabel(bar, text="Page size:").pack(side="right", padx=8)

        ctk.CTkButton(self, text="Create PDF", height=36, command=self._convert).pack(side="bottom", fill="x", pady=(8, 0))
        self.files = FileList(self, dnd.hint("Drag & drop JPG / PNG images (or a folder) here, then reorder with ↑ ↓",
                                              "Add JPG / PNG images, then reorder them with ↑ ↓"))
        self.files.pack(fill="both", expand=True)
        setattr(self.files, "drop_handler", self._on_drop)
        dnd.enable_drop(self, self._on_drop)

    def _add(self):
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        self.files.add(paths)

    def _on_drop(self, paths):
        images, skipped = [], 0
        for p in map(Path, paths):
            if p.is_dir():
                images += sorted(f for f in p.iterdir() if f.suffix.lower() in IMAGE_EXTS)
            elif p.suffix.lower() in IMAGE_EXTS:
                images.append(p)
            else:
                skipped += 1
        self.files.add(images)
        if skipped:
            self.set_status(f"Skipped {skipped} unsupported file(s).", "error")

    def _convert(self):
        paths = list(self.files.paths)
        if not paths:
            self.set_status("Add at least one image first.", "error")
            return
        out = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="images.pdf", filetypes=[("PDF", "*.pdf")])
        if not out:
            return
        size = "a4" if self.page.get() == "A4" else "fit"
        self.execute(lambda: images_to_pdf(paths, out, size), lambda n: f"Saved {n} page(s) → {out}")