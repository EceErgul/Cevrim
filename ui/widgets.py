import queue
import threading
from functools import partial
from pathlib import Path
import customtkinter as ctk
from modules.utils import resolve_output
from .dnd import enable_drop

OK = ("#1a7f37", "#3fb950")
ERROR = ("#cf222e", "#ff7b72")


def run_async(widget, work, done):
    """Run work() in a thread; call done(ok, value) on the Tk thread when finished."""
    q = queue.Queue()

    def target():
        try:
            q.put((True, work()))
        except Exception as exc:
            q.put((False, exc))

    def poll():
        try:
            ok, value = q.get_nowait()
        except queue.Empty:
            widget.after(100, poll)
            return
        done(ok, value)

    threading.Thread(target=target, daemon=True).start()
    poll()


def section_label(parent, text):
    ctk.CTkLabel(parent, text=text, anchor="w").pack(fill="x", pady=(10, 2))


class ConverterTab(ctk.CTkFrame):
    """Base tab: status line and progress bar pinned to the bottom, async runner."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(side="bottom", fill="x", pady=(6, 0))
        self.progress.set(0)
        self.status = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status.pack(side="bottom", fill="x")
        self._default_color = self.status.cget("text_color")
        self.busy = False

    def set_status(self, text, kind=None):
        color = OK if kind == "ok" else ERROR if kind == "error" else self._default_color
        self.status.configure(text=text, text_color=color)

    def execute(self, work, on_success):
        if self.busy:
            return
        self.busy = True
        self.set_status("Working…")
        self.progress.start()

        def done(ok, value):
            self.busy = False
            self.progress.stop()
            self.progress.set(0)
            if ok:
                self.set_status(on_success(value), "ok")
            else:
                self.set_status(f"Error: {value}", "error")

        run_async(self, work, done)


class PathField(ctk.CTkFrame):
    """Entry + Browse button. `browse` is a callable returning a path or ''."""

    def __init__(self, master, placeholder, browse):
        super().__init__(master, fg_color="transparent")
        self.entry = ctk.CTkEntry(self, placeholder_text=placeholder)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(self, text="Browse…", width=90, command=partial(self._browse, browse)).pack(side="left")

    def _browse(self, browse):
        path = browse()
        if path:
            self.set(path)

    def get(self):
        return self.entry.get().strip()

    def set(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)


class FileList(ctk.CTkScrollableFrame):
    """Ordered list of files with move up / move down / remove controls."""

    def __init__(self, master, empty_text="No files added yet"):
        super().__init__(master)
        self.paths = []
        self.empty_text = empty_text
        self.drop_handler = None
        self.refresh()

    def add(self, paths):
        self.paths += [p for p in map(str, paths) if p not in self.paths]
        self.refresh()

    def clear(self):
        self.paths = []
        self.refresh()

    def _move(self, i, step):
        j = i + step
        if 0 <= j < len(self.paths):
            self.paths[i], self.paths[j] = self.paths[j], self.paths[i]
            self.refresh()

    def _remove(self, i):
        del self.paths[i]
        self.refresh()

    def refresh(self):
        for child in self.winfo_children():
            child.destroy()
        if not self.paths:
            ctk.CTkLabel(self, text=self.empty_text, text_color="gray").pack(pady=20)
        for i, path in enumerate(self.paths):
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=f"{i + 1}. {Path(path).name}", anchor="w").pack(
                side="left", fill="x", expand=True, padx=(4, 0)
            )
            for text, cmd in (("✕", partial(self._remove, i)),
                              ("↓", partial(self._move, i, 1)),
                              ("↑", partial(self._move, i, -1))):
                ctk.CTkButton(row, text=text, width=28, height=24, command=cmd).pack(side="right", padx=2)
        if self.drop_handler:
            enable_drop(self, self.drop_handler)