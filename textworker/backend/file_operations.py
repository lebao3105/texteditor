import os
import sys
import wx

from ..generic import global_settings, log

config = global_settings.cfg
searchdir = config.getkey("editor", "searchdir", noraiseexp=True, restore=True)
autosave = config.getkey("editor", "autosave", noraiseexp=True, restore=True) or config.getkey("extensions.autosave", "enable", noraiseexp=True)

if searchdir == "" or False:
    if sys.platform == "win32":
        searchdir = os.environ["USERPROFILE"] + "\\Documents"
    else:
        searchdir = os.environ["HOME"] + "/Documents"

__all__ = [
    'FileOperations'
]

class FileOperators:
    _Editor = None
    _AddTab = None
    HasContent: bool = False
    Files = []
    
    @property
    def Editor(self):
        return self._Editor
    
    @Editor.setter
    def Editor(self, textw):
        self._Editor = textw

    @property
    def AddTab(self):
        return self._AddTab
    
    @AddTab.setter
    def AddTab(self, func):
        self._AddTab = func

    def IsEditorModified(self) -> bool:
        self.HasContent = self.Editor.IsModified()
        return self.HasContent

    def Save(self, FilePath: str) -> bool:
        self.IsEditorModified()
        if self.HasContent:
            self.HasContent = self.Editor.SaveFile(FilePath)
        else:
            self.HasContent = self.SaveAs()
        return self.HasContent
    
    def SaveAs(self) -> bool:
        dlg = wx.FileDialog(
            wx.Frame(),
            _("Save file as"),
            searchdir,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        )
        if dlg.ShowModal() == wx.ID_CANCEL:
            return False
        else:
            return self.Save(dlg.GetPath())
        
    def Load(self, FilePath: str) -> bool:
        if not self.Editor.IsModified():
            ask = wx.MessageBox(
                _(
                    f"""The editor has not been saved yet.\n
                    Override (No), Load to a new tab (Yes), or Cancel.
                    """
                ),
                _("Unsaved document"),
                style=wx.YES_NO | wx.CANCEL | wx.ICON_WARNING
            )

            if ask == wx.NO:
                self.Editor.ClearAll()
            elif ask == wx.YES:
                self.AddTab()
            elif ask == wx.CANCEL:
                return False

        if self.Editor.LoadFile(FilePath):
            self.HasContent = True
        else:
            self.HasContent = False
        return self.HasContent
    
    def OpenDialog(self) -> bool:
        dlg = wx.FileDialog(
            wx.Frame(),
            _("Open a file"),
            searchdir,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        if dlg.ShowModal() == wx.ID_CANCEL:
            return False
        else:
            self.Load(dlg.GetPath())