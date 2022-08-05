# Initialize for this application
# Including language, and configurations.
<<<<<<< HEAD
from tkinter import PhotoImage, END
from tkinter.messagebox import askyesno
from . import get_config, file_operations
=======
from tkinter import END
from PIL import ImageTk, Image
from tkinter.messagebox import askyesno
from . import file_operations, constant
>>>>>>> b35a36977b88c3114d7f544fec4c57ce48b0658f
import os

# an array 
icon = ["data/org.lebao3105.texteditor.Devel.png", 
        "../data/org.lebao3105.texteditor.Devel.png", 
        "icon.png", "src/icon.png"]

<<<<<<< HEAD
def initialize(self, config=None):
    if config == None:
        # Initialize the icon
        for k in range(len(icon)):
            if os.path.isfile(icon[k]):
                p1 = PhotoImage(file=icon[k])
                self.iconphoto(True, p1)
                #print(icon[k])
                break
            else:
                break # Ignore it
    else:
        # Initialize the configurations.
        # (Why did I used "configures"??? Crazy)
        get_config.set_window_color(self)

def check_is_saved(self):
    if self.text_editor.get(1.0, END) != "\n":
        # TODO: Fix is_saved value
        if file_operations.is_saved == True:
            return True
        else:
            if askyesno(self._("Text editor"), self._("Do you want to save the file?")):
                file_operations.save_file(self)
                return True
            else:
                return False # exit without saving
=======
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
>>>>>>> b35a36977b88c3114d7f544fec4c57ce48b0658f
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
