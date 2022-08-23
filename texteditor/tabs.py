"""This module adds tab to the tkinter.Notebook widget.
It also handles what's happening in the child widget of the tab (tkinter.Text)...
"""
from tkinter import Frame
from texteditor.miscs import constants, file_operations, get_config, textwidget
import gettext

_ = gettext.gettext

window_title = _("Text Editor") + " - "

# TODO: Add this module to a class

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
    # or we just opened some files with main.py
    elif find_tab == _(constants.UNTITLED) or (_(constants.UNTITLED) not in find_tab):
        return True
    # what I have mentioned before
    elif str(self.notebook.index("end") + 1) in find_tab:
        return False

def add_tab(self, event=None):
    if self.notebook.index('end') == 0:
        tabname = _(constants.UNTITLED)
    else:
        if checker(self):
            tabname = _(constants.UNTITLED) + str(self.notebook.index("end") + 1)
        else:
            tabname = _(constants.UNTITLED) + str(self.notebook.index("end") + 2)

    textframe = Frame(self.notebook)
    self.notebook.add(textframe, text=tabname)

    # Create text widget
    textd = textwidget.TextWidget(textframe, useMenu=True, useUnRedo=True)
    textd.addMenusepr()
    textd.addMenucmd(label=_("Save"), acc="Ctrl+S", fn=lambda: file_operations.save_file(self))
    textd.addMenucmd(label=_("Save as"), acc="Ctrl+Shift+S", fn=lambda: file_operations.save_as(self))
    self.text_editor = textd
    textd.pack(expand=True, fill="both")

    self.notebook.select(textframe)
    self.titletext = window_title + tabname
    self.title(self.titletext)

def tabs_close(self):
    # Automatically close the window if there's only one tab
    if self.notebook.index("end") == 1:
        print(_("No other tabs left, asking for close the window..."))
    # If not, just close the selected tab and keep
    # the main window open
    else:
        self.notebook.forget(self.notebook.select())

def on_tab_changed(root, event):
    tab = event.widget.tab('current')['text']
    root.title(_("Text Editor") + " - " + tab)