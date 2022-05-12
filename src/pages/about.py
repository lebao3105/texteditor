from tkinter import *
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from miscs import init, get_config

def about_run(self):
    about_win = Toplevel(self)
    about_win.title(_("About"))
    about_win.rowconfigure(0, weight=1)
    about_win.columnconfigure(0, weight=1)
    init.initialize(about_win, 1)
    place_texts(about_win)

def place_texts(self):
    name = Label(self, text=_("Text editor"))
    version = Label(self, text=_("Version 1.0."))
    author = Label(self, text=_("Author: ")+("Le Bao Nguyen"))
    license_text = Label(self, text=_("License: ")+("GPLv3"))

    name.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    version.grid(row=1, column=0, sticky="ew", padx=5)
    author.grid(row=2, column=0, sticky="ew", padx=5)
    license_text.grid(row=3, column=0, sticky="ew", padx=5)
    init.initialize(self, 2)
    get_config.change_text_color(name)
    get_config.change_text_color(version)
    get_config.change_text_color(author)
    get_config.change_text_color(license_text)