from tkinter import *
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from miscs import init, get_config

class About(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title(master._("About"))
        self._ = master._
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        init.initialize(self, 1)
        init.initialize(self, 2)
        self.grab_set()
        self.place_texts()
        
    def place_texts(self):
        frame = Frame(self)
        #img = Label(frame, image=self.p1)
        header = Label(frame, text=self._("About this application"), font=("Arial", 16))
        name = Label(self, text=self._("Text editor"))
        version = Label(self, text=self._("Version 1.0."))
        author = Label(self, text=self._("Author: ")+("Le Bao Nguyen"))
        license_text = Label(self, text=self._("License: ")+("GPLv3"))
    
        # Place widgets
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        #img.grid(row=1, column=0)
        header.grid(row=0, column=0)
        name.grid(row=0, column=1, sticky="ew")
        version.grid(row=1, column=1, sticky="ew")
        author.grid(row=2, column=1, sticky="ew")
        license_text.grid(row=3, column=1, sticky="ew")
        init.initialize(self, 2)

        # Change text color
        get_config.change_text_color(header)
        get_config.change_text_color(name)
        get_config.change_text_color(version)
        get_config.change_text_color(author)
        get_config.change_text_color(license_text)

def about_run(master):
    win = About(master)