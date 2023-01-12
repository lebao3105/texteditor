import os
import sys
import texteditor
import texteditor.backend

from tkinter.filedialog import *
from tkinter.messagebox import *

from . import constants

if sys.platform == "win32":
    searchdir = os.environ["USERPROFILE"] + "\Documents"
else:
    searchdir = os.environ["HOME"] + "/Documents"

texteditor.backend.require_version("1.4a0", ">=")


class FileOperations:
    def __init__(self, notebook, newtabfn, textw=None, statusbar=None):
        """File operations unit for texteditor.
        :param textw=None : text widget
        :param notebook : notebook widget
        :param newtabfn : create new tab function for the notebook
        :param statusbar=None : status bar (texteditor.backend.textwidget.StatusBar)

        Variable(s):
        files : Open files (not implemented yet, but everything is loaded into this"""
        self.textw = textw
        self.files = []  # TODO:Manage saves and unsaved-edits
        self.notebook = notebook
        self.newtabfn = newtabfn
        self.statusbar = statusbar if statusbar is not None else None

    def tabname(self):
        """Returns the current tab name."""
        return self.notebook.tab(self.notebook.select(), "text")

    def saveas(self, event=None):
        filename = asksaveasfilename(
            initialdir=searchdir, initialfile=self.tabname().removesuffix(" *")
        )
        if filename:
            self.savefile(filename)

    def throwerr(self, title, err):
        showerror(title=_(title), message=err)

    def asktoopen(self):
        ask = askyesno(
            _("Infomation"),
            _(
                """It seems that the file you're trying to open is in another tab.\n
                Load anyway? (to a new tab)"""
            ),
        )
        return ask

    def savefile(self, filename):
        """Saves a file (filename parameter)."""
        if self.statusbar is not None:
            self.statusbar.writeleftmessage(
                _("Saving file %s") % filename, nowrite=True
            )
        with open(filename, "w") as f:
            try:
                f.write(self.textw.get(1.0, "end"))
            except Exception:
                self.throwerr("Unable to save file {}".format(filename))
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

    def openfile(self, filename): # TODO: Set window title
        """Opens a file then show it to the text editor."""
        if self.statusbar is not None:
            self.statusbar.writeleftmessage(_("Opening file %s") % filename)
        with open(filename, "r") as f:
            try:
                self.textw.insert(1.0, f.read())
            except Exception:
                self.throwerr("Unable to open file {}".format(filename))
            else:
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
