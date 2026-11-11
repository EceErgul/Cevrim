import sys
from pathlib import Path
import customtkinter as ctk
from ui import DataTab, DocumentTab, ImagePdfTab, dnd

APP_NAME = "Çevrim"
ASSETS = Path(__file__).parent / "assets"


class App(ctk.CTk, *dnd.app_bases()):
    def __init__(self):
        super().__init__()
        dnd.init(self)
        self.title(f"{APP_NAME} – File & Media Converter")
        self.geometry("820x560")
        self.minsize(720, 480)

        icon = ASSETS / "icon.ico"
        if icon.exists() and sys.platform.startswith("win"):
            self.iconbitmap(icon)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 0))
        ctk.CTkLabel(header, text=APP_NAME, font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        theme = ctk.CTkOptionMenu(header, values=["System", "Light", "Dark"], width=100,
                                  command=ctk.set_appearance_mode)
        theme.set("System")
        theme.pack(side="right")

        tabs = ctk.CTkTabview(self)
        tabs.pack(fill="both", expand=True, padx=20, pady=12)
        for name, tab_cls in (("Image → PDF", ImagePdfTab), ("Documents", DocumentTab), ("Data", DataTab)):
            tabs.add(name)
            tab_cls(tabs.tab(name)).pack(fill="both", expand=True)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    App().mainloop()