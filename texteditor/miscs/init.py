# Initialize for this application
# Including language, and configurations.
from tkinter import END
from PIL import ImageTk, Image
from tkinter.messagebox import askyesno
from . import file_operations, constant
import os

# an array 
icon = ["data/org.lebao3105.texteditor.Devel.png", 
        "../data/org.lebao3105.texteditor.Devel.png", 
        "icon.png", "src/icon.png"]

def initialize(self):
    """Initialize the icon."""
    for k in range(len(icon)):
        if os.path.isfile(icon[k]):
            ico = Image.open(icon[k])
            p1 = ImageTk.PhotoImage(ico)
            self.wm_iconphoto(False, p1)
            #print(icon[k])
            break
        else:
            break # Ignore it

def check_is_saved(self):
    """Checks if the document is saved.
    TODO: Use this function with multiple tabs (save them all or not)."""
    if self.text_editor.get(1.0, END) != ("\n" or ""):
        for items in constant.UNSAVED:
            if self.notebook.tab(self.notebook.select(), "text") in items:
                if askyesno(self._("Notification"),
                    self._("There are unsaved files. Are you want to save them?")):
                    file_operations.save_file(self)
                    return True
                else: return False
    else:
        return True

def ask_quit(self):
    if check_is_saved(self):
        if askyesno(self._("Text editor"), 
                self._("Are you sure want to quit the application?")):
            self.destroy()
            #exit()
        else:
            pass
    else:
        self.destroy()
