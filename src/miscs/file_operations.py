from tkinter import *
from tkinter.filedialog import askopenfilename
from sys import platform
import os

if platform == "win32":
    searchdir = os.getenv("USERPROFILE\Documents")
    script_type = ("UNIX Shell Script", "*.sh")
elif platform == "linux":
    searchdir = os.getenv("HOME/Documents")
    script_type = ("Windows Shell Script", "*.bat, *.cmd")

def open_file(self):
    file_name = askopenfilename(initialdir=searchdir, title=self._("Select a file to open"), 
                                filetypes=(("Text files", "*.txt"), script_type, ("All files", "*.*")))
    if file_name:
        self.text_editor.delete(1.0, END)
        with open(file_name, "r") as f:
            self.text_editor.insert(1.0, f.read())