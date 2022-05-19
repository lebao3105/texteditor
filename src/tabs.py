from tkinter import *
from tkinter import ttk
import miscs.init
import gettext
_ = gettext.gettext

def add_tab(self, root):
    tab_name = self.notebook.index("end") + 1
    new_tab = Frame(self.notebook)
    self.notebook.add(new_tab, text=_("Untitled ") + str(tab_name))
    place_textbox(new_tab, root)
    self.notebook.select(tab_name)
    self.tab_name_entry.delete(0, END)

def place_textbox(self, root):
    # Text box
    self.text_editor = Text(self, wrap="word", undo=True, font=("Arial", 12))
    self.text_editor.pack(expand=True, fill="both")
    # Scrollbar
    self.scroll = ttk.Scrollbar(self.text_editor, orient="vertical", command=self.text_editor.yview)
    self.scroll2 = ttk.Scrollbar(self.text_editor, orient="horizontal", command=self.text_editor.xview)
    self.scroll.pack(side="right", fill="y")
    self.scroll2.pack(side="bottom", fill="x")
    self.text_editor.configure(yscrollcommand=self.scroll.set, xscrollcommand=self.scroll2.set, undo=True, autoseparators=True)
    root.text_editor = self.text_editor
    miscs.init.initialize(self.text_editor, 2)

def tabs_close(self):
    # Automatically close the window if there's only one tab
    if self.notebook.index("end") == 1:
        print(_("No other tabs left, closing the window..."))
        miscs.init.ask_quit(self)
    # If not, just close the selected tab and keep
    # the main window open
    else:
        self.notebook.forget(self.notebook.select())

def move_tabs(self):
    # If there's more than one tab, move the selected tab to the right
    if self.notebook.index("end") > 1:
        y = self.get_tab().winfo_y() - 5

        try:
            self.notebook.insert(self.notebook.index("current") + 1, self.get_tab(), text=self.get_tab().winfo_children()[0].get(1.0, END))
        except TclError:
            return

    # If there's only one tab, do nothing
    else:
        print(_("No other tabs left, cannot move the tab to the right."))   