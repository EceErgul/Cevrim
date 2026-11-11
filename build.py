"""Build a standalone Çevrim app with PyInstaller:  python build.py"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main():
    cmd = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed",
        "--name", "Cevrim",
        "--collect-all", "customtkinter",
        "--collect-all", "tkinterdnd2",
        "--collect-data", "docx",
        "--collect-data", "pdfminer",
    ]
    if sys.platform != "darwin":
        cmd.append("--onefile")
    icon = ROOT / "assets" / ("icon.icns" if sys.platform == "darwin" else "icon.ico")
    if icon.exists():
        cmd += ["--icon", str(icon)]
    cmd.append("main.py")
    subprocess.run(cmd, cwd=ROOT, check=True)
    print("\nDone. Look in the dist/ folder.")


if __name__ == "__main__":
    main()