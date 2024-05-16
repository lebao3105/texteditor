import os
import platform
import webbrowser

import wx
import wx.html2
import wx.lib.splitter
import wx.xrc
import wx.lib.agw.aui as aui

from textwrap import dedent
from wx.lib.inspection import InspectionTool
from libtextworker import __version__ as libver
from libtextworker.general import ResetEveryConfig, logger, CraftItems
from libtextworker.interface.wx.dirctrl import *
from libtextworker.interface.wx.miscs import XMLBuilder, BindMenuEvents
from libtextworker.versioning import *
from textworker.ui.auistyles import AuiFlatDockArt, AuiFlatTabArt

from . import __version__ as appver, _
from .extensions import autosave, multiview, settings, AboutDialog
from .generic import global_settings, TOPLV_DIR, UIRC_DIR, clrCall
from .tabs import Tabber

# https://stackoverflow.com/a/27872625
if platform.system() == "Windows":
    import ctypes

    myappid = "me.lebao3105.textworker"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainFrame(XMLBuilder):
    cfg = global_settings
    logfmter = wx.LogFormatter()

    def __init__(this):
        XMLBuilder.__init__(this, None, CraftItems(UIRC_DIR, "mainmenu.xrc"), _)

        this.mainFrame = this.loadObject("mainFrame", "wxFrame")
        this.mainFrame.SetSize((860, 640))

        this._mgr = aui.AuiManager(this.mainFrame, aui.AUI_MGR_ALLOW_FLOATING | \
                                   aui.AUI_MGR_ALLOW_ACTIVE_PANE | aui.AUI_MGR_ANIMATE_FRAMES)
        this._mgr.SetArtProvider(AuiFlatDockArt())
        this._mgr.SetAutoNotebookTabArt(AuiFlatTabArt())

        this.Show = this.mainFrame.Show
        this.Hide = this.mainFrame.Hide
        this.Close = this.mainFrame.Close

        # Editor area
        this.notebook = Tabber(this.mainFrame)

        # Side bar

        ## Container
        this.multiviewer = multiview.MultiViewer(this.mainFrame)

        ## Explorer
        this.dirs = DirCtrl(this.multiviewer.tabs, w_styles=DC_HIDEROOT | DC_EDIT)
        this.dirs.Bind(wx.EVT_TREE_SEL_CHANGED, lambda evt: this.OpenFileFromTree(evt, this.dirs))
        this.multiviewer.RegisterTab("Explorer", this.dirs)

        ## Always show Explorer on startup
        this.multiviewer.tabs.SetSelection(0)

        # Other stuff
        this.wiz = settings.SettingsDialog(this.mainFrame)
        this.file_history = wx.FileHistory()
        this.autosv_cfg = autosave.AutoSaveConfig(this.mainFrame)
        
        this.logwindow = wx.Frame(this.mainFrame, title=_("Log"))
        this.logwindow.Bind(wx.EVT_CLOSE, lambda evt: this.logwindow.Hide())
        this.log = wx.TextCtrl(this.logwindow, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.HSCROLL)
        wx.Log.SetActiveTarget(wx.LogTextCtrl(this.log))

        # Place everything

        this.LoadMenu()

        minsz = (150, 200)
        def makePaneInf(title: str):
            return aui.AuiPaneInfo().Caption(title).MinimizeButton(True) \
                                    .MaximizeButton(True).MinSize(minsz) \
                                    .PinButton(True).NotebookDockable(True)
        
        this._mgr.AddPane(this.multiviewer.tabs, makePaneInf("Multiview").Left())
        this._mgr.AddPane(this.notebook, makePaneInf("Notebook").CenterPane())
        this._mgr.Update()
        
        this.mainFrame.Layout()

        # "Post init"
        this.mainFrame.Bind(wx.EVT_CLOSE, this.OnClose)

        clrCall.configure(this.mainFrame)
        clrCall.autocolor_run(this.mainFrame)

    def LoadMenu(this):
        def ToggleAutoSave(evt):
            wx.MessageBox(_("This will only affect to this session"),
                          parent=this.mainFrame)
            autosave.TOGGLE = not autosave.TOGGLE
            evt.Skip()

        filemenu = this.mainFrame.GetMenuBar().GetMenu(0)
        editmenu = this.mainFrame.GetMenuBar().GetMenu(1)
        viewmenu = this.mainFrame.GetMenuBar().GetMenu(2)
        cfgmenu = this.mainFrame.GetMenuBar().GetMenu(3)
        helpmenu = this.mainFrame.GetMenuBar().GetMenu(4)

        # File menu
        filemenu_events = [(this.notebook.AddTab, 0), (this.NewWindow, 1), # Separator
                           (this.OpenFile, 3), # Open folder (submenu) and Recents
                           # Separator
                           (this.notebook.fileops.SaveFileEvent, 7),
                           (this.notebook.fileops.AskToSave, 8),
                           # Separator
                           (this.CloseAllPages, 10),
                           (lambda evt: wx.PostEvent(this.mainFrame,
                                                     wx.CommandEvent(wx.wxEVT_CLOSE_WINDOW)), 11)]

        for callback, pos in [(this.OpenDir, 0), (lambda evt: this.OpenDir(evt, newwind=True), 1)]:
            this.mainFrame.Bind(wx.EVT_MENU, callback,
                                filemenu.FindItemByPosition(4).GetSubMenu().FindItemByPosition(pos))

        ## Setup wxFileHistory
        this.file_history.UseMenu(filemenu.FindItemByPosition(5).GetSubMenu())
        this.mainFrame.Bind(wx.EVT_MENU_RANGE, this.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        
        if os.path.isfile(os.path.expanduser("~/.textworker_history")):
            with open(os.path.expanduser("~/.textworker_history"), "r") as f:
                for line in f.readlines():
                    if os.path.isfile(line):
                        this.file_history.AddFileToHistory(line)

        # Edit menu
        editmenu_events = [(lambda evt: this.notebook.GetCurrentPage().Undo(), 0),
                           (lambda evt: this.notebook.GetCurrentPage().Redo(), 1),
                           (lambda evt: this.notebook.GetCurrentPage().Cut(), 3),
                           (lambda evt: this.notebook.GetCurrentPage().Copy(), 4),
                           (lambda evt: this.notebook.GetCurrentPage().Paste(), 5),
                           (lambda evt: this.notebook.GetCurrentPage().SelectAll(), 7)]

        ## Auto-save menus
        global_autosv = editmenu.FindItemByPosition(12).GetSubMenu() \
                                .FindItemByPosition(0).GetSubMenu()
        
        editor_autosv = editmenu.FindItemByPosition(12).GetSubMenu() \
                                .FindItemByPosition(1).GetSubMenu()

        this.mainFrame.Bind(wx.EVT_MENU,
                            lambda evt: this.autosv_cfg.ConfigWindow(),
                            global_autosv.FindItemByPosition(0))

        this.mainFrame.Bind(wx.EVT_MENU,
                            lambda evt: this.notebook.GetCurrentPage().ConfigWindow(),
                            editor_autosv.FindItemByPosition(0))

        if autosave.enabled in global_settings.yes_values:
            global_autosv.FindItemByPosition(1).Check(True)
            editor_autosv.FindItemByPosition(1).Check(True)
            this.notebook.GetCurrentPage().Start()  # On init only 1 tab opened, so we can do this

        this.mainFrame.Bind(wx.EVT_MENU,
                            lambda evt: this.notebook.GetCurrentPage().Toggle(
                                editor_autosv.FindItemByPosition(1).IsChecked()),
                            editor_autosv.FindItemByPosition(1))

        this.mainFrame.Bind(wx.EVT_MENU, lambda evt: ToggleAutoSave(evt),
                            global_autosv.FindItemByPosition(1))

        # View menu
        viewmenu_events = [(lambda evt: this.notebook.GetCurrentPage().ZoomIn(), 0),
                           (lambda evt: this.notebook.GetCurrentPage().ZoomOut(), 1),
                           (this.ShowMarkdown, 4)]

        viewmenu.FindItemByPosition(2).Check(
            bool(
                this.notebook.GetCurrentPage().cfg.getkey(
                    "editor", "wordwrap", True, True, True
                )
            )
        )
        this.mainFrame.Bind(wx.EVT_MENU,
                            lambda evt: this.notebook.GetCurrentPage().SetWrapMode(
                                viewmenu.FindItemByPosition(2).IsChecked()
                            ),
                            viewmenu.FindItemByPosition(2))

        if this.notebook.GetCurrentPage().GetIndentationGuides():
            viewmenu.FindItemByPosition(3).Check()

        this.mainFrame.Bind(wx.EVT_MENU,
                            lambda evt: this.notebook.GetCurrentPage().SetIndentationGuides(
                                viewmenu.FindItemByPosition(3).IsChecked()
                            ),
                            viewmenu.FindItemByPosition(3))

        # Settings menu
        cfgmenu_events = [(lambda evt: this.wiz.ShowModal(), 0),
                          (this.ResetCfgs, 1),
                          (lambda evt: this.OpenDir(evt, TOPLV_DIR, True), 2)]

        # Help menu
        helpmenu_events = [(this.ShowAbout, 0), (this.SysInf_Show, 1),
                           (lambda evt: this.logwindow.Show(), 2), (this.OpenInspector, 3),
                           (lambda evt: webbrowser.open("https://github.com/lebao3105/texteditor/issues"), 5),
                           (lambda evt: webbrowser.open("https://lebao3105.gitbook.io/texteditor_doc"), 6)]

        BindMenuEvents(this.mainFrame, filemenu, filemenu_events)
        BindMenuEvents(this.mainFrame, editmenu, editmenu_events)
        BindMenuEvents(this.mainFrame, viewmenu, viewmenu_events)
        BindMenuEvents(this.mainFrame, cfgmenu, cfgmenu_events)
        BindMenuEvents(this.mainFrame, helpmenu, helpmenu_events)

    """
    Event callbacks
    """

    def OnClose(this, evt):
        this._mgr.UnInit()
        if this.file_history.GetCount() > 0:
            with open(os.path.expanduser("~/.textworker_history"), "w") as f:
                for i in range(this.file_history.GetCount()):
                    f.write(this.file_history.GetHistoryFile(i) + "\n")
        evt.Skip()

    def OpenDir(this, evt, path: str = "", newwind: bool = False):
        if not path:
            ask = wx.DirDialog(this.mainFrame, _("Select a folder to start"))
            if ask.ShowModal() == wx.ID_OK:
                selected_dir = ask.GetPath()
            else:
                return
        else:
            selected_dir = path

        if not newwind:
            this.dirs.SetFolder(selected_dir)
        else:
            new = wx.Frame(this.mainFrame)
            newctrl = DirCtrl(new, w_styles = DC_MULTIPLE | DC_ONEROOT | DC_HIDEROOT)
            newctrl.SetFolder(selected_dir)
            newctrl.Bind(wx.EVT_TREE_SEL_CHANGED, lambda evt: this.OpenFileFromTree(evt, newctrl))
            new.Show()

    def OpenFileFromTree(this, evt, tree: DirCtrl):
        path = tree.GetFullPath()
        import os
        if not os.path.isdir(path): this.notebook.fileops.OpenFile(path)
        else: evt.Skip()

    def ShowMarkdown(this, evt): # vNext: Open in a new tab
        def autorefresh(event):
            nonlocal wind, content, newwind
            if not wind:
                return  # Window closed
            content = markdown(this.notebook.GetCurrentPage().GetText())
            newwind.SetPage(content, "")
            wind.Refresh()
            event.Skip()

        from markdown2 import markdown

        content = markdown(this.notebook.GetCurrentPage().GetText())

        wind = wx.Panel(this.notebook)
        newwind = wx.html2.WebView.New(wind)
        newwind.SetPage(content, "")

        wind.Show()
        this.notebook.AddPage(wind, this.notebook.GetPageText(this.notebook.GetSelection()), True)
        newwind.Show(True)

        this.notebook.GetCurrentPage().Bind(wx.EVT_CHAR, autorefresh)

    def ResetCfgs(this, evt):
        ask = wx.MessageBox(_("Are you sure want to reset every settings?\n"
                              "If so, finish your work first.\n"
                              "(and you will need to reopen yourself)"),
                            _("Reset confirmation"),
                            wx.YES_NO | wx.ICON_WARNING, this.mainFrame)

        if ask == wx.YES:
            logger.info("App reset requested.")
            ResetEveryConfig()

    def ShowAbout(this, evt):
        aboutdlg = AboutDialog(this.mainFrame)
        aboutdlg.Customize()
        aboutdlg.ShowModal()

    def SysInf_Show(this, evt):
        ostype = platform.system() if platform.system() else _("Unknown")
        msg = dedent(_(
            f"""
        Textworker version {appver}
        Branch: {"Nightly" if is_development_version(appver) else "Stable"}
        libtextworker verison {libver}
        wxPython version: {wx.__version__}
        Python version: {platform.python_version()}
        OS type: {ostype}
        OS version {platform.version()}
        Machine architecture: {platform.machine()}
        Is bytecode compiled: {'__compiled__' in __dict__}
        """
        ))
        newdlg = wx.Dialog(this.mainFrame, title=_("System specs"))
        wx.TextCtrl(newdlg, value=msg, style=wx.TE_MULTILINE | wx.TE_READONLY)
        newdlg.ShowModal()

    def NewWindow(this, evt):
        wx.MessageBox("Not implemented")

    def OnFileHistory(this, evt):  # cre: wxdemo program
        # get the file based on the menu ID
        fileNum = evt.GetId() - wx.ID_FILE1
        path = this.file_history.GetHistoryFile(fileNum)
        this.notebook.fileops.OpenFile(path)

        # add it back to the history so it will be moved up the list
        this.file_history.AddFileToHistory(path)

    def OpenFile(this, evt):
        this.notebook.fileops.AskToOpen(evt)
        this.file_history.AddFileToHistory(
            this.notebook.GetPageText(this.notebook.GetSelection())
        )

    def CloseAllPages(this, evt):
        for i in range(this.notebook.GetPageCount()):
            this.notebook.DeletePage(i)
        wx.PostEvent(this.notebook,
                     wx.CommandEvent(aui.wxEVT_AUI_PANE_CLOSED))

    def OpenInspector(this, evt):
        wnd = wx.FindWindowAtPointer()
        if not wnd: wnd = this.mainFrame
        InspectionTool().Show(wnd, True)