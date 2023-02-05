import threading
import wx
import wx.aui

from .backend import file_operations
from .extensions import autosave
from .generic import global_settings
from .textwidget import TextWidget

class Tabber(wx.aui.AuiNotebook):

    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.aui.AUI_NB_WINDOWLIST_BUTTON
        # There are many styles (and I love them):
        # AUI_NB_CLOSE_ON_ALL_TABS : Close button on all tabs (disabled by default)
        # AUI_NB_MIDDLE_CLICK_CLOSE : Use middle click to close tabs
        # AUI_NB_{BOTTOM/LEFT/RIGHT/TOP} : Notebook locations (default to top)
        # AUI_NB_TAB_MOVE : Move tab
        side = global_settings.get_setting("interface.tabs", "side", True)
        movetabs = global_settings.get_setting("interface.tabs", "move_tabs")
        middle_close = global_settings.get_setting("interface.tabs", "middle_close")
        close_on_all_tabs = global_settings.get_setting("interface.tabs", "close_on_all_tabs")

        if side == "top" or "default":
            kwds["style"] |= wx.aui.AUI_NB_TOP
        else:
            if not hasattr(wx.aui, "AUI_NB_"+side.upper()):
                kwds["style"] |= wx.aui.AUI_NB_TOP
            else:
                kwds["style"] |= getattr(wx.aui, "AUI_NB"+side.upper())
        
        if movetabs in global_settings.cfg.yes_value or [True]:
            kwds["style"] |= wx.aui.AUI_NB_TAB_MOVE
        
        if middle_close in global_settings.cfg.yes_value or [True]:
            kwds["style"] |= wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE
        
        if close_on_all_tabs in global_settings.cfg.yes_value or [True]:
            kwds["style"] |= wx.aui.AUI_NB_CLOSE_ON_ALL_TABS
        else:
            kwds["style"] |= wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB

        del side, movetabs, middle_close, close_on_all_tabs
    
        super().__init__(*args, **kwds)

        self.setstatus: bool = False

        self.AddTab()
        self.fileops = file_operations.FileOperations(
            self, self.AddTab, self.SetTitle, self.Parent
        )
        self.autosv = autosave.AutoSave(lambda: self.fileops.savefile_dlg(), self.Parent)

        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnPageClose)

        threading.Thread(target=self.SyncFileEdit(), daemon=True).start()

    def AddTab(self, evt=None, tabname=None):
        """Add a new tab.
        If tabname is not specified, use texteditor's new tab label."""

        self.text_editor = TextWidget(self, style=wx.TE_MULTILINE | wx.EXPAND)
        self.text_editor.SetZoom(3)

        if tabname is None:
            _tabname = _("New file")
        else:
            _tabname = tabname

        self.AddPage(self.text_editor, _tabname, select=True)

        textw = self.text_editor
        global_settings.cfg.setcolorfunc(
            "textw", textw, "StyleSetBackground", wx.stc.STC_STYLE_DEFAULT
        )
        global_settings.cfg.setfontcfunc(
            "textw", textw, "StyleSetForeground", wx.stc.STC_STYLE_DEFAULT
        )
        global_settings.cfg.configure(textw)

        self.SetTitle("Textworker - %s" % _tabname)

    def SetTitle(self, title=""):
        return self.Parent.SetTitle(title)

    def OnPageChanged(self, evt):
        tabname = self.GetPageText(evt.GetSelection())
        if self.setstatus is True:
            self.Parent.SetStatusText(tabname)
        self.SetTitle("Textworker - %s" % tabname)

    def OnPageClose(self, evt):
        if self.GetPageCount() == 0:
            self.AddTab()
    
    def SyncFileEdit(self):
        if self.text_editor.IsModified():
            print('edited')
            self.SetPageText(self.GetCurrentPage(), 'test')
        