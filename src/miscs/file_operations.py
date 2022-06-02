from tkinter import *
from tkinter.filedialog import *
from sys import platform
import os, sys

sys.path.append(os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            )
import tabs

# Made this to prevent the application from 
# running some functions right after the startup.
is_safe_to_do = False

if platform == "win32":
    searchdir = os.getenv("USERPROFILE\Documents")
    script_type = ("Windows Shell Script", "*.bat, *.cmd")
elif platform == "linux":
    searchdir = os.getenv("HOME/Documents")
    script_type = ("UNIX Shell Script", "*.sh")

def find_text_editor(self):
    if hasattr(self, "text_editor"):
        return
    else:
        raise Exception("Text editor not found!")

def open_file(self):
    file_name = askopenfilename(initialdir=searchdir, title=self._("Select a file to open"), 
                                filetypes=(("Text files", "*.txt"), script_type, ("All files", "*.*")))
    if file_name:
        find_text_editor(self)
        if self.text_editor.get(1.0, END) != "\n":
            tabs.add_tab(self)
            pass
        else:
            pass
        
        with open(file_name, "r") as f:
            self.text_editor.insert(1.0, f.read())
            self.title(self._("Text editor") + " - " + file_name)

def save_file(self):
    global is_safe_to_do
    find_text_editor(self)
    if self.text_editor.get(1.0, END) == "\n":
        if is_safe_to_do:
            save_as(self)
        else:
            pass
    else:
        with open(self.title().split(" - ")[1], "w") as f:
            f.write(self.text_editor.get(1.0, END))
            is_safe_to_do = True

def save_as(self):
    if is_safe_to_do:
        find_text_editor(self)
        file_name = asksaveasfilename(initialdir=searchdir, 
                                    title=self._("Save as"),
                                    filetypes=(("Text files", "*.txt"), script_type, 
                                    ("All files", "*.*")))
        if file_name:
            with open(file_name, "w") as f:
                f.write(self.text_editor.get(1.0, END))
    else:
        pass

def copy(self):
    if is_safe_to_do:
        find_text_editor(self)
        self.text_editor.clipboard_clear()
        self.text_editor.clipboard_append(self.text_editor.selection_get())
    else:
        pass

def paste(self):
    if is_safe_to_do:
        find_text_editor(self)
        self.text_editor.insert(INSERT, self.text_editor.clipboard_get())
    else:
        pass

def cut(self):
    if is_safe_to_do:
        find_text_editor(self)
        self.text_editor.clipboard_clear()
        self.text_editor.clipboard_append(self.text_editor.selection_get())
        self.text_editor.delete(SEL_FIRST, SEL_LAST)
    else:
        pass