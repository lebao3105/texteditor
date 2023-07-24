from tkinter import END, StringVar, Toplevel
from tkinter.ttk import Button, Entry, Label

from .generic import clrcall


class Finder(Toplevel):
    def __init__(self, parent, option, event=None):
        super().__init__(parent)
