import os
import wx
import wx.lib.agw.aui as aui
import wx.stc

from hashlib import md5
from libtextworker.interface.wx.editor import DragNDropTarget

from .. import _
from .editor import Editor
from ..generic import global_settings, clrCall
from .auistyles import AuiFlatTabArt

searchdir = global_settings.Get("editor", "searchdir", noraiseexp=True, make=True)
if not os.path.isdir(searchdir):
    searchdir = os.path.expanduser("~/Documents")

class Tabber(aui.AuiNotebook, DragNDropTarget):
    """
    Internal notebook class than handles both windows managing and file operations for them.
    """

    SetStatus: bool = False
    NewTabTitle: str = _("Untitled")

    file_dialog = wx.FileDialog(None, defaultDir=searchdir)
    message = wx.MessageDialog(None, "")

    def __init__(this, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | aui.AUI_NB_WINDOWLIST_BUTTON | aui.AUI_NB_TAB_SPLIT | aui.AUI_NB_DRAW_DND_TAB | aui.AUI_NB_HIDE_ON_SINGLE_TAB | aui.AUI_NB_TAB_FIXED_WIDTH

        # There are many styles (and I love them):
        # AUI_NB_CLOSE_ON_ALL_TABS : Close button on all tabs (disabled by default)
        # AUI_NB_MIDDLE_CLICK_CLOSE : Use middle click to close tabs
        # AUI_NB_TAB_MOVE : Move tab
        movetabs = global_settings['editor.tabs']["move_tabs"]
        middle_close = global_settings['editor.tabs']["middle_close"]
        this.close_on_no_tab = global_settings['editor.tabs']["close_on_no_tab"]

        if movetabs in global_settings.yes_values: kwds["style"] |= aui.AUI_NB_TAB_MOVE

        if middle_close in global_settings.yes_values: kwds["style"] |= aui.AUI_NB_MIDDLE_CLICK_CLOSE

        if this.close_on_no_tab in global_settings.yes_values: kwds["style"] |= aui.AUI_NB_CLOSE_ON_ALL_TABS
        else: kwds["style"] |= aui.AUI_NB_CLOSE_ON_ACTIVE_TAB

        aui.AuiNotebook.__init__(this, *args, **kwds)
        this.SetArtProvider(AuiFlatTabArt())


        this.AddTab()

        this.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, this.OnPageChanged)
        this.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, this.OnPageClosed)
        this.Bind(wx.EVT_WINDOW_DESTROY, this.OnSelfDestroy)

    def AddTab(this, evt=None, tabname: str = _("New file")):
        newte = Editor(this, style=wx.TE_MULTILINE | wx.EXPAND | wx.HSCROLL | wx.VSCROLL)
        newte.SetZoom(3)

        newte.Bind(wx.EVT_WINDOW_DESTROY, this.OnEditorDestroy)
        newte.Bind(wx.EVT_CHAR, this.OnEditorModify)

        clrCall.configure(newte)
        clrCall.autocolor_run(newte)
        newte.StyleClearAll()

        this.AddPage(newte, tabname, select=True)
        this.SetTitle(tabname)

    def SetTitle(this, title):
        return wx.GetTopLevelParent(this).SetTitle(title)
    
    def AskToOpen(this, evt=None):
        this.file_dialog.SetName(_("Open a file"))
        if this.file_dialog.ShowModal() == wx.ID_OK:
            this.OpenFile(this.file_dialog.GetPath())

    def AskToSave(this, evt=None):
        this.file_dialog.SetName(_("Save this to..."))

        if this.file_dialog.ShowModal() == wx.ID_OK:
            this.GetCurrentPage().SaveFile(this.file_dialog.GetPath())

    def SaveFileEvent(this, evt=None):
        tablabel = this.GetPageText(this.GetSelection())
        if not os.path.isfile(tablabel):
            return this.AskToSave()
        else:
            return this.SaveFile(tablabel)

    def OpenFile(this, path: str):
        if this.GetCurrentPage().IsModified:
            this.AddTab()

        this.GetCurrentPage().LoadFile(path) # Load the content
        this.GetCurrentPage().FileLoaded = path

        this.SetPageText(this.GetSelection(), path) # Set tab title
        wx.GetTopLevelParent(this).SetTitle(path) # Set the window title

    def SaveFile(this, path: str):
        return this.GetCurrentPage().SaveFile(path)

    """
    Events.
    """

    def OnPageChanged(this, evt):
        tabname = this.GetPageText(evt.GetSelection())
        if this.SetStatus: wx.GetTopLevelParent(this).SetStatusText(tabname)
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

    def OnDropFiles(this, x, y, filenames):
        
        for i in range(0, len(filenames)):
            this.AddTab()
            this.OpenFile(filenames[i])
        
        return True
    
    def OnEditorDestroy(this, evt):
        curreditor = evt.GetWindow()
        path = curreditor.FileLoaded if curreditor.FileLoaded else "this new file"

        if curreditor.IsModified:
            match wx.MessageBox(_(f"Save {path}? It has unsaved changes."),
                                _("Not saved"), wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT):
            
                case wx.YES:
                    if curreditor.FileLoaded != path: this.AskToSave()
                    else: this.SaveFile(path)

                case wx.CANCEL:
                    return

        evt.Skip()
    
    def OnEditorModify(this, evt: wx.KeyEvent):
        editor = evt.GetEventObject()

        editor.Hash = md5(editor.GetText().encode("utf-8"))
        if editor.FileLoaded:
            if not this.GetPageText(this.GetPageIndex(editor)).endswith(" *"):
                this.SetPageText(this.GetPageIndex(editor), editor.FileLoaded + " *")

        evt.Skip()