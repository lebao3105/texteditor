import wx
import wx.aui
import wx.stc

from .backend import file_operations
from .extensions import autosave
from .generic import global_settings

from libtextworker.interface.wx.editor import StyledTextControl


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
        movetabs = global_settings.get_setting("interface.tabs", "move_tabs")
        middle_close = global_settings.get_setting("interface.tabs", "middle_close")
        close_on_all_tabs = global_settings.get_setting(
            "interface.tabs", "close_on_all_tabs"
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

        self.fileops = file_operations.MultiEditorsSupport(
            self,
            {
                "AddTab": self.AddTab,
                "Editor": self.text_editor,
                "IndependentAutoSave": True
            }
        )
        # self.fileops.AddTab = getattr(self, "AddTab")
        
        # self.autosv = autosave.AutoSave(
        #     self.Parent
        # )
        # self.autosv.Function = self.fileops.Save(self.GetPageText(self.GetSelection()))

        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnPageClose)

    def AddTab(self, evt=None, tabname=None):
        """
        Add a new tab.
        If tabname is not specified, use texteditor's new tab label.
        """

        self.text_editor = StyledTextControl(
            parent=self, style=wx.TE_MULTILINE | wx.EXPAND
        )
        self.text_editor.SetZoom(3)
        self.text_editor.FileLoaded: str = ""

        if tabname is None:
            _tabname = _("New file")
        else:
            _tabname = tabname

        self.AddPage(self.text_editor, _tabname, select=True)
        self.SetTitle(_tabname)

    def SetTitle(self, title=""):
        """
        Set the title of the parent widget, if able.
        """
        if hasattr(self.Parent, "SetTitle"):
            return self.Parent.SetTitle(title)

    def OnPageChanged(self, evt):
        tabname = self.GetPageText(evt.GetSelection())
        if self.setstatus is True:
            self.Parent.SetStatusText(tabname)
        self.SetTitle(tabname)
        self.SetTitle(tabname)

    def OnPageClose(self, evt):

        def repoen(event):
            nonlocal btn
            btn.Hide()
            self.Show(True)

        if self.GetPageCount() == 0:
            if global_settings.get_setting("fun", "empty_page_on_last_tab_close") in [True, "yes"]:
                self.Hide()
            if not hasattr(self.Parent, "AddChild"):
                return self.Show(True)
            
            btn = wx.Button(self.Parent, label=_("Show again"))
            self.Parent.Bind(wx.EVT_BUTTON, repoen, btn)
            self.AddTab()