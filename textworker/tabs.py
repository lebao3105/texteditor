import wx
import wx.aui
import wx.stc

from libtextworker.interface.wx.editor import StyledTextControl

from . import file_operations
from .generic import _editor_config_load, global_settings


class Tabber(wx.aui.AuiNotebook):
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
        movetabs = global_settings.get_setting("editor.tabs", "move_tabs")
        middle_close = global_settings.get_setting("editor.tabs", "middle_close")
        close_on_all_tabs = global_settings.get_setting(
            "editor.tabs", "close_on_no_tab"
        )

        if movetabs == True:
            kwds["style"] |= wx.aui.AUI_NB_TAB_MOVE

        if middle_close == True:
            kwds["style"] |= wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE

        if close_on_all_tabs == True:
            kwds["style"] |= wx.aui.AUI_NB_CLOSE_ON_ALL_TABS
        else:
            kwds["style"] |= wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB

        del movetabs, middle_close, close_on_all_tabs

        super().__init__(*args, **kwds)

        self.setstatus: bool = False

        self.AddTab()

        self.fileops = file_operations.FileOperations(
            self,
            {
                "AddTab": self.AddTab,
                "IndependentAutoSave": True,
                "SetTabName": True,
                "SetWindowTitle": True,
            },
        )

        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnPageClose)

    def AddTab(self, evt=None, tabname: str = _("New file")):
        self.text_editor = StyledTextControl(
            parent=self, style=wx.TE_MULTILINE | wx.EXPAND | wx.HSCROLL | wx.VSCROLL
        )
        self.text_editor.EditorInit(_editor_config_load)
        self.text_editor.SetZoom(3)
        self.text_editor.FileLoaded: str = ""

        self.AddPage(self.text_editor, tabname, select=True)
        self.SetTitle(tabname)

    def SetTitle(self, title=""):
        if hasattr(wx.GetTopLevelParent(self), "SetTitle"):
            return wx.GetTopLevelParent(self).SetTitle(title)

    def OnPageChanged(self, evt):
        tabname = self.GetPageText(evt.GetSelection())
        if self.setstatus is True:
            self.Parent.SetStatusText(tabname)
        self.SetTitle(tabname)

    def OnPageClose(self, evt):
        def repoen(event):
            nonlocal btn
            btn.Hide()
            self.Show(True)

        if self.GetPageCount() == 0:
            if global_settings.get_setting("editor.tabs", "close_on_no_tab") in [
                True,
                "yes",
            ]:
                self.Hide()
            if not hasattr(self.Parent, "AddChild"):
                return self.Show(True)

            btn = wx.Button(self.Parent, label=_("Show again"))
            self.Parent.Bind(wx.EVT_BUTTON, repoen, btn)
            self.AddTab()
