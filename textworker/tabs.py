import wx
import wx.aui
import wx.stc

from . import _
from .editor import Editor
from .file_operations import FileOperations
from .generic import global_settings, clrCall


class Tabber(wx.aui.AuiNotebook):
    SetStatus: bool = false
    NewTabTitle: str = _("Untitled")

    def __init__(this, *args, **kwds):
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
        this.close_on_no_tab = global_settings.getkey("editor.tabs", "close_on_no_tab")

        if movetabs == true:
            kwds["style"] |= wx.aui.AUI_NB_TAB_MOVE

        if middle_close == true:
            kwds["style"] |= wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE

        if this.close_on_no_tab == true:
            kwds["style"] |= wx.aui.AUI_NB_CLOSE_ON_ALL_TABS
        else:
            kwds["style"] |= wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB

        wx.aui.AuiNotebook.__init__(this, *args, **kwds)

        this.fileops = FileOperations(this)

        this.AddTab()

        this.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, this.OnPageChanged)
        this.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, this.OnPageClosed)
        this.Bind(wx.EVT_WINDOW_DESTROY, this.OnSelfDestroy)

    def AddTab(this, evt=nil, tabname: str = _("New file")):
        newte = Editor(this,
                       style=wx.TE_MULTILINE | wx.EXPAND | wx.HSCROLL | wx.VSCROLL)
        newte.SetZoom(3)

        newte.Bind(wx.EVT_WINDOW_DESTROY, this.fileops.OnEditorDestroy)
        newte.Bind(wx.EVT_CHAR, this.fileops.OnEditorModify)

        clrCall.configure(newte)
        newte.StyleClearAll()

        this.AddPage(newte, tabname, select=true)
        this.SetTitle(tabname)

    def SetTitle(this, title):
        return wx.GetTopLevelParent(this).SetTitle(title)

    """
    Events.
    """

    def OnPageChanged(this, evt):
        tabname = this.GetPageText(evt.GetSelection())
        if this.SetStatus is true:
            wx.GetTopLevelParent(this).SetStatusText(tabname)
        this.SetTitle(tabname)

    def OnPageClosed(this, evt):
        if this.GetPageCount() == 0:
            if this.close_on_no_tab in global_settings.yes_values:
                wx.GetApp().ExitMainLoop()
            else:
                this.AddTab()

    def OnSelfDestroy(this, evt):
        for i in range(this.GetPageCount()):
            this.GetPage(i).SendDestroyEvent()
        evt.Skip()