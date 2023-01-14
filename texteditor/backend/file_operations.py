import os
import pathlib
import sys
import wx

from texteditor.backend import logger

if sys.platform == "win32":
    searchdir = os.environ["USERPROFILE"] + "\Documents"
else:
    searchdir = os.environ["HOME"] + "/Documents"


class FileOperations:
    """File operations unit for texteditor.\n
    Paramaters:
    textw : text widget
    notebook : wx.notebook widget
    newtabfn : create new tab function for the notebook
    settitle : function to set an object's title (optional)
    statusbar = None : Your wx.Frame's (or other wxPython widget) statusbar
    """

    def __init__(self, textw, notebook, newtabfn, settitle=None, statusbar=None):
        self.textw = textw
        self.files = []  # TODO:Manage saves and unsaved-edits
        self.notebook = notebook
        self.newtabfn = newtabfn
        self.statusbar = statusbar if statusbar is not None else None
        self.settitle = settitle

    def tabname(self):
        """Returns the current tab name."""
        return self.notebook.GetPageText(self.notebook.GetSelection())

    def savefile(self, filename):
        """Saves a file (filename parameter)."""
        if self.statusbar is not None:
            self.statusbar.SetStatusText(_("Saving file %s...") % filename)
        self.textw.SaveFile(filename)

    def openfile(self, filename):
        """Opens a file then show it to the text editor."""
        filename = str(pathlib.Path(filename).resolve(True).absolute())
        if self.statusbar is not None:
            self.statusbar.SetStatusText(_("Opening file %s") % filename)
        try:
            f = open(filename, "r")
        except:
            logger.Logger("texteditor.backend.file_operations").throwerr(
                _("Error occured"),
                msg=_("Error occured while opening file %s") % filename,
                showdialog=True,
            )
            return
        else:
            del f
            self.textw.LoadFile(str(filename))
            self.notebook.SetPageText(
                page=self.notebook.GetSelection(), text=str(filename)
            )
            self.files.append(str(filename))
            if self.settitle != None:
                self.settitle()

    # Dialogs
    def savefile_(self, event=None):
        """Checks if the file is a new file or not, then make the choice."""
        tabname = self.tabname()
        if tabname not in self.files:
            self.saveas()
        else:
            self.savefile(tabname)

    def saveas(self, event=None):
        filedlg = wx.FileDialog(
            self.textw,
            _("Save file"),
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            defaultDir=searchdir,
        )
        if filedlg.ShowModal() == wx.ID_CANCEL:
            return
        else:
            filename = filedlg.GetPath()
            self.savefile(filename)

    def asktoopen(self):
        ask = wx.MessageBox(
            _(
                f"""It seems that the file you're trying to open is in another tab.\n
Load anyway? (to a new tab)"""
            ),
            _("Infomation"),
            wx.ICON_QUESTION | wx.YES_NO,
            self.textw,
        )
        if ask == wx.YES:
            return True
        else:
            return False

    def openfile_(self, event=None):
        """Asks the user to open a file."""
        filedlg = wx.FileDialog(
            self.textw,
            _("Open a file"),
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
            defaultDir=searchdir,
        )
        if filedlg.ShowModal() == wx.ID_CANCEL:
            return
        else:
            filename = filedlg.GetPath()
            for x in self.files:
                if filename in x:
                    if self.asktoopen():
                        self.newtabfn()
            if self.textw.GetValue() != "":
                self.newtabfn()
            self.openfile(filename)
