# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Qat Spy application
"""

from pathlib import Path
import os
import tkinter as tk
try:
    import sv_ttk
except ImportError:
    print('SunValley theme unavailable: using default ttk theme')

from qat.gui.application_manager import ApplicationManager


def generate_root_window() -> tk.Tk:
    """
    Create the main window
    """
    current_path = Path(os.path.dirname(__file__)).resolve().absolute()
    image_dir = current_path / 'images'
    root = tk.Tk()
    root.iconphoto(True, tk.PhotoImage(file=image_dir / "icon.png"))
    root.title('Qat Gui')
    root.withdraw()

    return root


def open_gui():
    """
    Open the main window
    """

    window = generate_root_window()
    ApplicationManager(window)

    try:
        sv_ttk.set_theme('light')
    except NameError:
        pass
    window.mainloop()


if __name__ == "__main__":

    open_gui()
