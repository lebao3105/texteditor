import wx
import wx.lib.agw.aui as aui
import wx.stc

from textworker.ui.auistyles import AuiFlatTabArt

from . import _
from .editor import Editor
from .file_operations import DNDTarget, FileOperations
from .generic import global_settings, clrCall, editorCfg


class Tabber(aui.AuiNotebook):
    SetStatus: bool = false
    NewTabTitle: str = _("Untitled")

    def __init__(this, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | aui.AUI_NB_WINDOWLIST_BUTTON | aui.AUI_NB_TAB_SPLIT | aui.AUI_NB_DRAW_DND_TAB | aui.AUI_NB_HIDE_ON_SINGLE_TAB | aui.AUI_NB_TAB_FIXED_WIDTH

        # There are many styles (and I love them):
        # AUI_NB_CLOSE_ON_ALL_TABS : Close button on all tabs (disabled by default)
        # AUI_NB_MIDDLE_CLICK_CLOSE : Use middle click to close tabs
        # AUI_NB_TAB_MOVE : Move tab
        movetabs = global_settings.getkey("editor.tabs", "move_tabs")
        middle_close = global_settings.getkey("editor.tabs", "middle_close")
        this.close_on_no_tab = global_settings.getkey("editor.tabs", "close_on_no_tab")

        if movetabs: kwds["style"] |= aui.AUI_NB_TAB_MOVE

        if middle_close: kwds["style"] |= aui.AUI_NB_MIDDLE_CLICK_CLOSE

        match this.close_on_no_tab in global_settings.yes_values:
            case True: kwds["style"] |= aui.AUI_NB_CLOSE_ON_ALL_TABS
            case _: kwds["style"] |= aui.AUI_NB_CLOSE_ON_ACTIVE_TAB      

        aui.AuiNotebook.__init__(this, *args, **kwds)
        this.SetArtProvider(AuiFlatTabArt())

        this.fileops = FileOperations(this)

        this.AddTab()

        if editorCfg.getkey("editor", "dnd_enabled", True, True) in editorCfg.yes_values:
            this.SetDropTarget(DNDTarget(this))

        this.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, this.OnPageChanged)
        this.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, this.OnPageClosed)
        this.Bind(wx.EVT_WINDOW_DESTROY, this.OnSelfDestroy)

    def AddTab(this, evt=nil, tabname: str = _("New file")):
        newte = Editor(this, style=wx.TE_MULTILINE | wx.EXPAND | wx.HSCROLL | wx.VSCROLL)
        newte.SetZoom(3)

        newte.Bind(wx.EVT_WINDOW_DESTROY, this.fileops.OnEditorDestroy)
        newte.Bind(wx.EVT_CHAR, this.fileops.OnEditorModify)

        clrCall.configure(newte)
        clrCall.autocolor_run(newte)
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
        if this.GetPageCount() - 1 == 0:
            match this.close_on_no_tab in global_settings.yes_values:
                case True: wx.GetApp().ExitMainLoop()
                case _: this.AddTab()

    def OnSelfDestroy(this, evt):
        for i in range(this.GetPageCount()):
            this.GetPage(i).SendDestroyEvent()
        evt.Skip()