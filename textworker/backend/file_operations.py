import os
import pathlib
import time
import sys
import wx

from . import logger

if sys.platform == "win32":
    searchdir = os.environ["USERPROFILE"] + "\\Documents"
else:
    searchdir = os.environ["HOME"] + "/Documents"


class FileOperations:
    def __init__(self, notebook, newtabfn, settitle=None, statusbar=None):
        self.files = []
        self.notebook = notebook
        self.newtabfn = newtabfn
        self.statusbar = statusbar if statusbar is not None else None
        self.settitle = settitle
        self.dummyfm = wx.Frame()  # Dummy frame for dialogs

    def tabname(self):
        return self.notebook.GetPageText(self.notebook.GetSelection())

    def savefile(self, filename):
        self.notebook.GetCurrentPage().SaveFile(filename)
        if self.statusbar is not None:
            self.statusbar.SetStatusText(_("Saving file %s...") % filename)
            time.sleep(1)
            self.statusbar.SetStatusText(_("%s saved.") % filename)
            time.sleep(1)
            self.statusbar.SetStatusText(filename)

    def openfile(self, filename):
        filename = str(pathlib.Path(filename).resolve(True).absolute())
        try:
            f = open(filename, "r")
        except:
            logger.Logger().throwerr(
                title=_("Error occured"),
                msg=_("Error occured while opening file %s") % filename,
                showdialog=True,
            )
            return
        else:
            del f
            self.notebook.GetCurrentPage().LoadFile(str(filename))

            if self.statusbar is not None:
                self.statusbar.SetStatusText(_("Opening file %s") % filename)
                time.sleep(0.5)
                self.statusbar.SetStatusText("%s" % filename)

            self.notebook.SetPageText(
                page=self.notebook.GetSelection(), text=str(filename)
            )
            self.files.append(str(filename))
            if self.settitle != None:
                self.settitle()

    # Dialogs
    def savefile_dlg(self, event=None):
        """Checks if the file is a new file or not, then make the choice."""
        tabname = self.tabname()
        if tabname not in self.files:
            self.saveas()
        else:
            self.savefile(tabname)

    def saveas(self, event=None):
        filedlg = wx.FileDialog(
            self.dummyfm,
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
            self.dummyfm,
        )
        if ask == wx.YES:
            return True
        else:
            return False

    def openfile_dlg(self, event=None):
        """Asks the user to open a file."""
        filedlg = wx.FileDialog(
            self.dummyfm,
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

            if not self.notebook.GetCurrentPage().IsEmpty():
                self.newtabfn()
            self.openfile(filename)
