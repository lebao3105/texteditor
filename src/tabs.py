from tkinter import *
from tkinter import ttk
import miscs.init
import gettext
_ = gettext.gettext

# For example:
# We have 2 tabs: Untitled and Untitled 2. You close Untitled
# and create a new tab. The new tab's name is Untitled 2 - not 3.
# This is because tab_name = tabs number + 1, which can occur problem
# like that.
def checker(self):
    # get the current tab name
    find_tab = self.notebook.tab(self.notebook.select(), "text")
    # if the number in find_tab = tabs index, return True
    if str(self.notebook.index("end")) in find_tab:
        return True
    # if this is the first tab yet
    elif find_tab == _("Untitled "):
        return True
    # what I mentioned before
    elif str(self.notebook.index("end") + 1) in find_tab:
        return False

def add_tab(self, root):
    if checker(self):
        tab_name = self.notebook.index("end") + 1
    else:
        tab_name = self.notebook.index("end") + 2
    new_tab = Frame(self.notebook)
    self.notebook.add(new_tab, text=_("Untitled ") + str(tab_name))
    place_textbox(new_tab, root)
    self.notebook.select(new_tab)

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
        print(_("No other tabs left, asking for close the window..."))
        miscs.init.ask_quit(self)
    # If not, just close the selected tab and keep
    # the main window open
    else:
        self.notebook.forget(self.notebook.select())