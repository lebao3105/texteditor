from tkinter import *
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from miscs import init, get_config

class Help(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title(master._("Help"))
        self._ = master._ 
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grab_set()
        self.place_texts()

    def place_texts(self):
        # Create widgets
        self.label_help = Label(self, text=self._("Help"))
        self.label_help_text = Label(self, text=self._("How to use this application?"))
        self.label_help_text_2 = Label(self, text=self._("Just do what you need like any other text editor,"))
        self.label_help_text_3 = Label(self, text=self._("with tabs support."))
        
        # Place widgets + change text color
        items = [self.label_help, self.label_help_text, self.label_help_text_2, self.label_help_text_3]
        for i in range(len(items)):
            nums = [0, 1, 2, 3]
            for k in nums:
                i.grid(row=k, column=0, sticky="ew", padx=5)
            get_config.change_text_color(i)
        init.initialize(self, 2)
