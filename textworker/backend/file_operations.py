import os
import sys
import wx

from typing import Any, Callable
from ..generic import global_settings

config = global_settings.cfg

if sys.platform == "win32":
    searchdir = os.environ["USERPROFILE"] + "\\Documents"
else:
    searchdir = os.environ["HOME"] + "/Documents"

__all__ = ["FileOperations", "searchdir"]


class FileOperators:
    HasContent: bool

    Editor = Any
    NewTabFunc = Callable

    def IsEditorModified(self) -> bool:
        self.HasContent = self.Editor.IsModified()
        return self.HasContent

    def Save(self, FilePath: str = "") -> bool:
        self.IsEditorModified()
        if self.HasContent:
            if self.Editor.FileLoaded != "":
                self.HasContent = self.Editor.SaveFile(FilePath)
        self.HasContent = self.SaveAs()
        return self.HasContent

    def SaveAs(self) -> bool:
        dlg = wx.FileDialog(
            wx.Frame(),
            _("Save file as"),
            searchdir,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )
        if dlg.ShowModal() == wx.ID_CANCEL:
            return False
        else:
            return self.Save(dlg.GetPath())

    def Load(self, FilePath: str) -> bool:
        if self.Editor.IsModified():
            ask = wx.MessageBox(
                _(
                    f"""The editor has not been saved yet.\n
                Override (No), Load to a new tab (Yes), or Cancel.
                """
                ),
                _("Unsaved document"),
                style=wx.YES_NO | wx.CANCEL | wx.ICON_WARNING,
            )

            if ask == wx.NO:
                self.Editor.ClearAll()
            elif ask == wx.YES:
                self.NewTabFunc()
            elif ask == wx.CANCEL:
                return False

        if self.Editor.LoadFile(FilePath):
            self.Editor.FileLoaded = FilePath
            self.HasContent = True
        else:
            self.HasContent = False
        return self.HasContent

    def OpenDialog(self) -> bool:
        dlg = wx.FileDialog(
            wx.Frame(),
            _("Open a file"),
            searchdir,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        )
        if dlg.ShowModal() == wx.ID_CANCEL:
            return False
        else:
            self.Load(dlg.GetPath())
