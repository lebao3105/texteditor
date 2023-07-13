import wx
import wx.aui
import wx.stc

from .editor import Editor
from .file_operations import FileOperations
from .generic import global_settings


class Tabber(wx.aui.AuiNotebook):
    SetStatus: bool = False
    NewTabTitle: str = _("Untitled")

    def __init__(self, *args, **kwds):
        kwds["style"] = (
            kwds.get("style", 0)
            | wx.aui.AUI_NB_WINDOWLIST_BUTTON
            | wx.aui.AUI_NB_TAB_SPLIT
        )
        # There are many styles (and I love them):
        # AUI_NB_CLOSE_ON_ALL_TABS : Close button on all tabs (disabled by default)
        # AUI_NB_MIDDLE_CLICK_CLOSE : Use middle click to close tabs
        # AUI_NB_TAB_MOVE : Move tab
        movetabs = global_settings.getkey("editor.tabs", "move_tabs")
        middle_close = global_settings.getkey("editor.tabs", "middle_close")
        self.close_on_no_tab = global_settings.getkey(
            "editor.tabs", "close_on_no_tab"
        )

        if movetabs == True:
            kwds["style"] |= wx.aui.AUI_NB_TAB_MOVE

        if middle_close == True:
            kwds["style"] |= wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE

        if self.close_on_no_tab == True:
            kwds["style"] |= wx.aui.AUI_NB_CLOSE_ON_ALL_TABS
        else:
            kwds["style"] |= wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB

        wx.aui.AuiNotebook.__init__(self, *args, **kwds)

        self.AddTab()

        self.fileops = FileOperations(
            self,
            {
                "AddTab": self.AddTab,
                "SetTabName": True,
                "SetWindowTitle": True,
            },
        )

        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnPageClose)

    def AddTab(self, evt=None, tabname: str = _("New file")):
        newte = Editor(
            self, style=wx.TE_MULTILINE | wx.EXPAND | wx.HSCROLL | wx.VSCROLL
        )
        newte.SetZoom(3)
        newte.FileLoaded: str = ""

        self.AddPage(newte, tabname, select=True)
        self.SetTitle(tabname)

    def SetTitle(self, title=""):
        if hasattr(wx.GetTopLevelParent(self), "SetTitle"):
            return wx.GetTopLevelParent(self).SetTitle(title)

    def OnPageChanged(self, evt):
        tabname = self.GetPageText(evt.GetSelection())
        if self.SetStatus is True:
            wx.GetTopLevelParent(self).SetStatusText(tabname)
        self.SetTitle(tabname)

    def OnPageClose(self, evt):
        if self.GetPageCount() == 0:
            if self.close_on_no_tab in global_settings.yes_values:
                wx.GetApp().ExitMainLoop()
            else:
                self.AddTab()
