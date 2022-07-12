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
        img = Label(frame, image=self.p2)
        header = Label(frame, text=self._("About this application"), font=("Arial", 16))
        name = Label(frame, text=self._("Text editor"))
        version = Label(frame, text=self._("Version 1.1-dev."))
        author = Label(frame, text=self._("Author: ")+("Le Bao Nguyen"))
        license_text = Label(frame, text=self._("License: ")+("GPLv3"))
    
        # Place widgets
        frame.grid(row=0, column=0, sticky="nsew")
        header.grid(row=0, column=0, sticky="nsew")
        img.grid(row=1, column=0, sticky="nsew")
        name.grid(row=2, column=0, sticky="nsew")
        version.grid(row=3, column=0, sticky="nsew")
        author.grid(row=4, column=0, sticky="nsew")
        license_text.grid(row=5, column=0, sticky="nsew")

        # Change text + window color
        items = [name, version, author, license_text, header]
        for i in range(len(items)):
            get_config.change_text_color(i)
        init.initialize(self, 2)