from tkinter import *
import gettext

vi = gettext.translation('base', localedir='po', languages=['vi'])
vi.install()
_ = vi.gettext

def help_run(self):
    help_win = Toplevel(self)
    help_win.title(_("Help"))
    help_win.geometry("300x300")
    help_win.rowconfigure(0, weight=1)
    help_win.columnconfigure(0, weight=1)
    help_win.resizable(False, False)
    place_texts(help_win)

def place_texts(self):
    self.label_help = Label(self, text=_("Help"))
    self.label_help_text = Label(self, text=_("How to use this application?"))
    self.label_help_text_2 = Label(self, text=_("Just do what you need like any other text editor,"))
    self.label_help_text_3 = Label(self, text=_("but no tabs support."))
    self.label_help.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    self.label_help_text.grid(row=1, column=0, sticky="ew", padx=5)
    self.label_help_text_2.grid(row=2, column=0, sticky="ew", padx=5)
    self.label_help_text_3.grid(row=3, column=0, sticky="ew", padx=5)
