# Initialize for this application
# Including language, and configurations.
from tkinter import PhotoImage, END
from tkinter.messagebox import askyesno
from . import get_config, file_operations
import os

# an array 
icon = ["data/org.lebao3105.texteditor.Devel.png", 
        "../data/org.lebao3105.texteditor.Devel.png", 
        "icon.png", "src/icon.png"]

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
