# Initialize for this application
# Including language, and configures.
import gettext
from tkinter import PhotoImage
from tkinter.messagebox import askyesno
from . import get_config
import os

def initialize(self, part):
    if part == 1:
        # Initialize the language
        if os.path.isdir("po"):
            gettext.bindtextdomain('base', 'po')
            gettext.textdomain('base')
            self._ = gettext.gettext
        else:
            raise Exception("Could not find the language directory!")

        if os.path.isfile("data/org.lebao3105.texteditor.Devel.png"):
            p1 = PhotoImage(file="data/org.lebao3105.texteditor.Devel.png")
        elif os.path.isfile("icon.png"):
            p1 = PhotoImage(file="icon.png")
        elif os.path.isfile("src/icon.png"):
            p1 = PhotoImage(file="src/icon.png")

        self.iconphoto(False, p1)
    elif part == 2:
        # Initialize the configures
        get_config.set_windows_color(self)

def ask_quit(self):
    answer = askyesno(self._("Quit"), self._("Are you sure want to quit?"))
    if answer == True:
        self.quit()
        self.destroy()
        exit()