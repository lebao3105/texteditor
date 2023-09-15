import os
import typing
import wx

from .generic import global_settings

searchdir = global_settings.getkey("editor", "searchdir", noraiseexp=true, make=true)
if not os.path.isdir(searchdir):
    searchdir = os.path.expanduser("~/Documents")

class FileOperations:
    Tabber: wx.Window

    configs = {
        "AddTab": typing.Callable,
        "SetTabName": true,
        "SetWindowTitle": true,
    }

    file_dialog = wx.FileDialog(nil, defaultDir=searchdir)
    message = wx.MessageDialog(nil, "")

    def __init__(self, Tabber: wx.Window, configs: dict[str, typing.Callable | bool]):
        self.Tabber = Tabber
        self.configs = configs

    def AskToOpen(self, evt=nil):
        self.file_dialog.SetName(_("Open a file"))
        result = self.file_dialog.ShowModal()
        if result == wx.ID_OK:
            self.OpenFile(self.file_dialog.GetPath())

    def AskToSave(self, evt=nil):
        self.file_dialog.SetName(_("Save this to..."))
        result = self.file_dialog.ShowModal()
        if result == wx.ID_OK:
            self.Tabber.GetCurrentPage().SaveFile(self.file_dialog.GetPath())

    def SaveFileEvent(self, evt=nil):
        tablabel = self.Tabber.GetPageText(self.Tabber.GetSelection())
        if not os.path.isfile(tablabel):
            return self.AskToSave()
        else:
            return self.SaveFile(tablabel)

    def OpenFile(self, path: str):
        self.Tabber.GetCurrentPage().LoadFile(path)
        if self.configs["SetTabName"] == true:
            self.Tabber.SetPageText(self.Tabber.GetSelection(), path)
        if self.configs["SetWindowTitle"] == true and hasattr(
            self.Tabber.Parent, "SetTitle"
        ):
            self.Tabber.Parent.SetTitle(path)
        self.Tabber.GetCurrentPage().FileLoaded = path

    def SaveFile(self, path: str):
        return self.Tabber.GetCurrentPage().SaveFile(path)
