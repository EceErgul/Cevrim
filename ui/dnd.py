"""Optional drag & drop support (tkinterdnd2). Every function is a no-op without it."""
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = TkinterDnD = None

enabled = False


def app_bases():
    """Extra base classes for the main window."""
    return (TkinterDnD.DnDWrapper,) if TkinterDnD else ()


def init(root):
    """Load the tkdnd extension into the root window. Returns True when drag & drop works."""
    global enabled
    if TkinterDnD:
        try:
            root.TkdndVersion = TkinterDnD._require(root)
            enabled = True
        except Exception:
            enabled = False
    return enabled


def hint(with_dnd, without_dnd):
    return with_dnd if enabled else without_dnd


def enable_drop(widget, callback):
    """Make `widget` and all its children accept file drops; callback(list_of_paths)."""
    if not enabled:
        return
    root = widget.winfo_toplevel()

    def handler(event):
        paths = list(widget.tk.splitlist(event.data))
        root.after(10, lambda: callback(paths))
        return event.action

    def register(w):
        try:
            w.drop_target_register(DND_FILES)
            w.dnd_bind("<<Drop>>", handler)
        except Exception:
            pass
        for child in w.winfo_children():
            register(child)

    register(widget)