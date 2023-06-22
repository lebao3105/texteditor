import os
import typing
import wx

from .generic import global_settings

searchdir = global_settings.getkey("editor", "searchdir", noraiseexp=True, restore=True)
if not os.path.isdir(searchdir):
    searchdir = os.path.expanduser("~/Documents")


class FileOperations:
    Tabber: wx.Window

    configs = {
        "AddTab": typing.Callable,
        "SetTabName": True,
        "SetWindowTitle": True,
    }

    file_dialog = wx.FileDialog(None, defaultDir=searchdir)
    message = wx.MessageDialog(None, "")

    def __init__(
        self, Tabber: wx.Window, configs: dict[str, typing.Any]
    ):
        self.Tabber = Tabber
        self.configs = configs

    def AskToOpen(self, evt=None):
        self.file_dialog.SetName(_("Open a file"))
        result = self.file_dialog.ShowModal()
        if result == wx.ID_OK:
            self.OpenFile(self.file_dialog.GetPath())

    def AskToSave(self, evt=None):
        self.file_dialog.SetName(_("Save this to..."))
        result = self.file_dialog.ShowModal()
        if result == wx.ID_OK:
            self.Tabber.GetCurrentPage().SaveFile(self.file_dialog.GetPath())
    
    def SaveFileEvent(self, evt=None):
        tablabel = self.Tabber.GetPageText(self.Tabber.GetSelection())
        if not os.path.isfile(tablabel):
            return self.AskToSave()
        else:
            return self.SaveFile(tablabel)

    def OpenFile(self, path: str):
        self.Tabber.GetCurrentPage().LoadFile(path)
        if self.configs["SetTabName"] == True:
            self.Tabber.SetPageText(self.Tabber.GetSelection(), path)
        if self.configs["SetWindowTitle"] == True and hasattr(
            self.Tabber.Parent, "SetTitle"
        ):
            self.Tabber.Parent.SetTitle(path)
        self.Tabber.GetCurrentPage().FileLoaded = path

    def SaveFile(self, path: str):
        return self.Tabber.GetCurrentPage().SaveFile(path)
