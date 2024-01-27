import os
import typing
import wx

from . import _
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

    def __init__(this, Tabber: wx.Window, configs: dict[str, typing.Callable | bool]):
        this.Tabber = Tabber
        this.configs = configs

    def AskToOpen(this, evt=nil):
        this.file_dialog.SetName(_("Open a file"))
        result = this.file_dialog.ShowModal()
        if result == wx.ID_OK:
            this.OpenFile(this.file_dialog.GetPath())

    def AskToSave(this, evt=nil):
        this.file_dialog.SetName(_("Save this to..."))
        result = this.file_dialog.ShowModal()
        if result == wx.ID_OK:
            this.Tabber.GetCurrentPage().SaveFile(this.file_dialog.GetPath())

    def SaveFileEvent(this, evt=nil):
        tablabel = this.Tabber.GetPageText(this.Tabber.GetSelection())
        if not os.path.isfile(tablabel):
            return this.AskToSave()
        else:
            return this.SaveFile(tablabel)

    def OpenFile(this, path: str):
        this.Tabber.GetCurrentPage().LoadFile(path)
        if this.configs["SetTabName"]:
            this.Tabber.SetPageText(this.Tabber.GetSelection(), path)
        if this.configs["SetWindowTitle"] and hasattr(
            this.Tabber.Parent, "SetTitle"
        ):
            this.Tabber.Parent.SetTitle(path)
        this.Tabber.GetCurrentPage().FileLoaded = path

    def SaveFile(this, path: str):
        return this.Tabber.GetCurrentPage().SaveFile(path)
