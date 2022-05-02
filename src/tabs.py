from tkinter import *
from tkinter import ttk
import gettext
_ = gettext.gettext

def add_tab(self):
    tab_name = self.notebook.index("end") + 1
    new_tab = Frame(self.notebook)
    self.notebook.add(new_tab, text=_("Untitled ") + str(tab_name))
    place_textbox(new_tab)
    self.notebook.select(tab_name)
    self.tab_name_entry.delete(0, END)

def place_textbox(self):
    # Text box
    self.text_editor = Text(self, wrap="word", undo=True, font=("Arial", 12))
    self.text_editor.pack(expand=True, fill="both")
    # Scrollbar
    self.scroll = ttk.Scrollbar(self.text_editor, orient="vertical", command=self.text_editor.yview)
    self.scroll.pack(side="right", fill="y")
    self.text_editor.configure(yscrollcommand=self.scroll.set)

def tabs_close(self):
    # Automatically close the window if there's only one tab
    if self.notebook.index("end") == 1:
        print(_("No other tabs left, closing the window..."))
        self.destroy()
    # If not, just close the selected tab and keep
    else:
        index = str(self.notebook.index(self.notebook.select()))
        print(_("Closing tab ") + index + "...")
        self.notebook.forget(self.notebook.select())