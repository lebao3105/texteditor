from tkinter import *
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from miscs import init, get_config

def help_run(self):
    help_win = Toplevel(self)
    help_win._ = ""
    init.initialize(help_win, 1)
    help_win.title(help_win._("Help"))
    help_win.geometry("300x300")
    help_win.rowconfigure(0, weight=1)
    help_win.columnconfigure(0, weight=1)
    help_win.resizable(False, False)
    help_win.grab_set()
    place_texts(help_win)

def place_texts(self):
    self.label_help = Label(self, text=self._("Help"))
    self.label_help_text = Label(self, text=self._("How to use this application?"))
    self.label_help_text_2 = Label(self, text=self._("Just do what you need like any other text editor,"))
    self.label_help_text_3 = Label(self, text=self._("with tabs support."))
    self.label_help.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    self.label_help_text.grid(row=1, column=0, sticky="ew", padx=5)
    self.label_help_text_2.grid(row=2, column=0, sticky="ew", padx=5)
    self.label_help_text_3.grid(row=3, column=0, sticky="ew", padx=5)
    init.initialize(self, 2)
    get_config.change_text_color(self.label_help)
    get_config.change_text_color(self.label_help_text)
    get_config.change_text_color(self.label_help_text_2)
    get_config.change_text_color(self.label_help_text_3)
