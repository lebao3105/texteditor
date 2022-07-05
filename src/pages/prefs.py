from tkinter import *
from tkinter import font
from tkinter import ttk
import sys
from os import path
sys.path.append(
    path.dirname(
        path.dirname(path.abspath(__file__))
    )
)
from miscs import init, get_config

class Prefs(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title(master._("Preferences"))
        self._ = master._
        init.initialize(self, 2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        #self.grab_set()
        self.make_widgets()
    
    def make_widgets(self):
        # Frame & header
        frame = Frame(self)
        header = Label(frame, text=self._("Preferences"), 
                        font=("Arial", 20))
        # Language
        lang_arr = [self._("English"), self._("Vietnamese")]
        lang_var = StringVar()
        lang_var.set(lang_arr[0])
        lang_label = Label(frame, text=self._("Language"))
        lang_menu = ttk.Combobox(frame, textvariable=lang_var)
        # Font
        a_fonts = font.families()
        available_fonts = [self._("Select it here")]
        for fonts in a_fonts:
            available_fonts.append(fonts)
        font_var = StringVar()
        font_var.set(available_fonts[0])
        font_label = Label(frame, text=self._("Font"))
        font_menu = ttk.Combobox(frame, textvariable=font_var)
        # Color
        color_arr = [self._("Select it here"), "Red", "Green", "Blue"]
        color_var = StringVar()
        color_var.set(color_arr[0])
        color_label = Label(frame, text=self._("Color"))
        color_menu = ttk.Combobox(frame, textvariable=color_var)
    
        # Place widgets
        frame.pack(padx=20, pady=20)
        header.grid(row=0, column=0)
        lang_label.grid(row=1, column=0, sticky="ew")
        lang_menu.grid(row=1, column=1, sticky="ew")
        font_label.grid(row=2, column=0, sticky="ew")
        font_menu.grid(row=2, column=1, sticky="ew")
        color_label.grid(row=3, column=0, sticky="ew")
        color_menu.grid(row=3, column=1, sticky="ew")
        init.initialize(self, 2)
        # Change text color
        get_config.change_text_color(header)
        get_config.change_text_color(lang_label)
        get_config.change_text_color(font_label)
        get_config.change_text_color(color_label)

def prefs_run(self):
    prefs_win = Prefs(self)

if __name__ == "__main__":
    root = Tk()
    root.title("Preferences")
    root.geometry("300x300")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root._ = lambda x: x
    init.initialize(root, 0)
    prefs_run(root)
    root.mainloop()
