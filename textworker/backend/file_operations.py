import os
import threading
import typing
import wx

from ..generic import global_settings
config = global_settings.cfg
searchdir = config.getkey("editor", "searchdir", noraiseexp=True, restore=True, getbool=False)
autosave = config.getkey("editor", "autosave", noraiseexp=True, restore=True) or config.getkey("extensions.autosave", "enable", noraiseexp=True)

if searchdir == "" or isinstance(searchdir, bool):
    searchdir = os.path.expanduser("~/Documents")

class FileOperations:

    # Functions
    Editor : typing.Any
    SaveFn : typing.Callable
    LoadFn : typing.Callable
    IsModifiedFn : typing.Callable

    # Booleans
    IsModified : bool = False

    def DynamicEditorChanges(self):
        def subfn():
            self.IsModified = self.IsModifiedFn()

        self.thread = threading.Thread(
            target=subfn(),
            daemon=True
        )
        self.thread.run()
    
    def StopThreading(self):
        if self.thread:
            del self.thread

class MultiEditorsSupport(FileOperations):
    """
    Class to provide wx.*Book* support for editors.
    """
    tabs : typing.Any | wx.Notebook

    configs = {
        "AddTab": typing.Callable,
        "Editor": typing.Any,
        "IndependentAutoSave": True
    }

    file_dialog = wx.FileDialog(
        None, defaultDir=searchdir
    )

    message = wx.MessageDialog(
        None, ""
    )

    def __init__(self, Tabber: typing.Any | wx.Notebook, configs: dict[str,typing.Any]):
        self.tabs = Tabber
        self.configs = configs

        self.Editor = self.configs["Editor"]
        self.LoadFn = self.Editor.LoadFile
        self.SaveFn = self.Editor.SaveFile
        self.IsModifiedFn = self.Editor.IsModified
    
    def AskToOpen(self, evt=None):
        self.file_dialog.SetName(_("Open a file"))
        result = self.file_dialog.ShowModal()
        if result == wx.ID_OK:
            self.LoadFn(self.file_dialog.GetPath())
    
    def AskToSave(self, evt=None):
        self.file_dialog.SetName(_("Save this to..."))
        result = self.file_dialog.ShowModal()
        if result == wx.ID_OK:
            self.SaveFn(self.file_dialog.GetPath())