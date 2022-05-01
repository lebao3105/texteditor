from tkinter import *
import gettext

vi = gettext.translation('base', localedir='po', languages=['vi'])
vi.install()
_ = vi.gettext

def about_run():
    about_win = Tk()
    about_win.title(_("About"))
    about_win.geometry("300x300")
    about_win.rowconfigure(0, weight=1)
    about_win.columnconfigure(0, weight=1)
    about_win.resizable(False, False)
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