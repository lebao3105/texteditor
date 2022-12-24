import os
import sys
import texteditor
import traceback

from tkinter.filedialog import *
from tkinter.messagebox import *

from . import constants

if sys.platform == "win32":
    searchdir = os.environ["USERPROFILE"] + "\Documents"
else:
    searchdir = os.environ["HOME"] + "/Documents"


class FileOperations:
    """File operations unit for texteditor.\n
    Paramaters:
    textw : text widget
    notebook : notebook widget
    newtabfn : create new tab function for the notebook
    statusbar=None : status bar (texteditor.backend.textwidget.StatusBar)
    _=None : gettext translator\n
    Variable(s):
    files : Open files (not implemented yet, but everything is loaded into this"""

    def __init__(self, textw, notebook, newtabfn, statusbar=None, _=None):
        if _ is None:
            self._ = texteditor._
        else:
            self._ = _

        self.textw = textw
        self.files = []  # TODO:Manage saves and unsaved-edits
        self.notebook = notebook
        self.newtabfn = newtabfn
        self.statusbar = statusbar if statusbar is not None else None

    def tabname(self):
        """Returns the current tab name."""
        return self.notebook.tab(self.notebook.select(), "text")

    def saveas(self, event=None):
        filename = asksaveasfile(
            initialdir=searchdir, initialfile=self.tabname().removesuffix(" *")
        )
        if filename:
            self.savefile(filename)

    def throwerr(self, title, err):
        showerror(title=self._(title), message=err)

    def asktoopen(self):
        ask = askyesno(
            self._("Infomation"),
            self._(
                "Seems that the file you're trying to open is in another tab.\nLoad anyway? (to a new tab)"
            ),
        )
        return ask

    def savefile(self, filename):
        """Saves a file (filename parameter)."""
        if self.statusbar is not None:
            self.statusbar.writeleftmessage(self._("Saving file %s") % filename)
        with open(filename, "w") as f:
            try:
                f.write(self.textw.get(1.0, "end"))
            except Exception:
                self.throwerr("Unable to save file")
            else:
                self.notebook.tab("current", text=filename)
                self.files.append(filename)

    def savefile_(self, event=None):
        """Checks if the file is a new file or not, then make the choice."""
        tabname = self.tabname()
        if tabname not in constants.FILES_ARR:
            self.saveas()
        else:
            self.savefile()

    def openfile(self, filename):
        """Opens a file then show it to the text editor."""
        if self.statusbar is not None:
            self.statusbar.writeleftmessage(self._("Opening file %s") % filename)
        with open(filename, "r") as f:
            try:
                self.textw.insert(1.0, f.read())
            except Exception:
                self.throwerr("Unable to open file")
            else:
                self.notebook.event_generate("<<NotebookTabChanged>>")
                self.files.append(filename)
                self.notebook.tab("current", text=filename)

    def openfile_(self, event=None):
        """Asks the user to open a file."""
        filename = askopenfilename(initialdir=searchdir)
        if filename is not None:
            for x in constants.FILES_ARR:
                if filename in x:
                    if self.asktoopen():
                        self.newtabfn()
                        self.openfile(filename)
                else:
                    self.openfile(filename)
                return
            if not self.textw.compare("end-1c", "==", 1.0):
                self.newtabfn()
                self.openfile(filename)
