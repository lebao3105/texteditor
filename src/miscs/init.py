# Initialize for this application
# Including language, and configures.
from email import message
import gettext
from tkinter import PhotoImage
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno
from . import get_config, file_operations
import os

# Arrays
language = ["po", "../po", "../../po"] # Added ../../po for files in ../pages
icon = ["data/org.lebao3105.texteditor.Devel.png", 
        "../data/org.lebao3105.texteditor.Devel.png", 
        "icon.png", "src/icon.png"]

def initialize(self, part):
    if part == 0:
        # Initialize the language
        for i in range(len(language)):
            if os.path.isdir(language[i]):
                gettext.bindtextdomain('base', 'po')
                gettext.textdomain('base')
                self._ = gettext.gettext
                gettext.install(language[i])
                break
            else:
                print("Directory " + language[i] + " not found!")
                break
    elif part == 1:
        # Initialize the icon
        # Note: This may not working on Linux - Why?
        for k in range(len(icon)):
            if os.path.isfile(icon[k]):
                p1 = PhotoImage(file=icon[k])
                self.p2 = ImageTk.PhotoImage(Image.open(icon[k]))
                self.iconphoto(True, p1)
                #print(icon[k])
                break
            else:
                if self._ == gettext.gettext:
                    print(self._("Could not find the icon!"))
                    messagebox.showinfo(self._("Warning"), self._("No icon file detected. The application will show files it has checked."))
                    messagebox.showinfo(self._("Info"), icon[k])
                    break
                else:
                    print("Could not find the icon!")
                    messagebox.showinfo("Warning", "No icon file detected. The application will show files it has checked.")
                    messagebox.showinfo("Info", icon[k])
                    break
    elif part == 2:
        # Initialize the configures
        get_config.set_windows_color(self)

def check_is_saved(self):
    if self.text_editor.get(1.0, END) != "\n":
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
        if askyesno(self._("Text editor"), self._("Do you want to quit?")):
            self.destroy()
            #exit()
        else:
            pass
    else:
        self.destroy()