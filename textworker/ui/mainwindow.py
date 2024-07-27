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
from libtextworker.general import ResetEveryConfig, logger
from libtextworker.interface.wx.dirctrl import *
from libtextworker.versioning import *

from textworker import __version__ as appver, _
from textworker.generic import global_settings, TOPLV_DIR, clrCall
from textworker.ui import autosave, mainmenu_generated, multiview, settings, about, tabs
from textworker.ui.auistyles import AuiFlatDockArt, AuiFlatTabArt


class MainFrame(mainmenu_generated.mainFrame):
    cfg = global_settings
    logfmter = wx.LogFormatter()

    def __init__(this):
        mainmenu_generated.mainFrame.__init__(this, None)
        this.SetSize((860, 640))

        this._mgr = aui.AuiManager(this, aui.AUI_MGR_ALLOW_FLOATING | \
                                         aui.AUI_MGR_ALLOW_ACTIVE_PANE | \
                                         aui.AUI_MGR_ANIMATE_FRAMES)
        this._mgr.SetArtProvider(AuiFlatDockArt())
        this._mgr.SetAutoNotebookTabArt(AuiFlatTabArt())

        # Editor area
        this.notebook = tabs.Tabber(this)

        # Side bar

        ## Container
        this.multiviewer = multiview.MultiViewer(this)

        ## Explorer
        this.dirs = DirCtrl(this.multiviewer.tabs, w_styles=DC_HIDEROOT | DC_EDIT)
        this.dirs.Bind(wx.EVT_TREE_SEL_CHANGED, lambda evt: this.OpenFileFromTree(evt, this.dirs))
        this.multiviewer.RegisterTab("Explorer", this.dirs)

        ## Always show Explorer on startup
        this.multiviewer.tabs.SetSelection(0)

        # Other stuff
        this.wiz = settings.SettingsDialog(this)
        this.file_history = wx.FileHistory()
        this.autosv_cfg = autosave.AutoSaveConfig(this)
        
        this.logwindow = wx.Frame(this, title=_("Log"))
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
        
        this.Layout()

        # "Post init"
        this.Bind(wx.EVT_CLOSE, this.OnClose)

        clrCall.configure(this)
        clrCall.autocolor_run(this)

    def LoadMenu(this):
        def BindMenuEvents(tuples: list[tuple[Callable, wx.MenuItem]]):
            for callback, item in tuples:
                this.Bind(wx.EVT_MENU, callback, item)
            
        def ToggleAutoSave(evt):
            wx.MessageBox(_("This will only affect to this session"),
                          parent=this)
            autosave.TOGGLE = not autosave.TOGGLE
            evt.Skip()

        # File menu
        filemenu_events = [ (this.notebook.AddTab, this.newtab),
                            (this.OpenFile, this.openf),
                            (this.notebook.SaveFileEvent, this.save),
                            (this.notebook.AskToSave, this.save_as),
                            (this.CloseAllPages, this.closeall),
                            (lambda evt:
                                wx.PostEvent(this, wx.CommandEvent(wx.wxEVT_CLOSE_WINDOW)),
                            this.quit),
                            (this.OpenDir, this.openfd),
                            (lambda evt: this.OpenDir(evt, newwind=True), this.openfd_w) ]

        ## Setup wxFileHistory
        this.file_history.UseMenu(this.recents_menu)
        this.Bind(wx.EVT_MENU_RANGE, this.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9)
        
        if os.path.isfile(os.path.expanduser("~/.textworker_history")):
            with open(os.path.expanduser("~/.textworker_history"), "r") as f:
                for line in f.readlines():
                    if os.path.isfile(line):
                        this.file_history.AddFileToHistory(line)

        # Edit menu
        editmenu_events = [(lambda evt: this.notebook.GetCurrentPage().Undo(), this.undo),
                           (lambda evt: this.notebook.GetCurrentPage().Redo(), this.redo),
                           (lambda evt: this.notebook.GetCurrentPage().Cut(), this.cut),
                           (lambda evt: this.notebook.GetCurrentPage().Copy(), this.copy),
                           (lambda evt: this.notebook.GetCurrentPage().Paste(), this.paste),
                           (lambda evt: this.notebook.GetCurrentPage().SelectAll(), this.selectall),
                           (lambda evt: this.autosv_cfg.ConfigWindow(), this.as_global),
                           (lambda evt: this.notebook.GetCurrentPage().asDlg.ASConfig(), this.as_local),
                           (lambda evt: this.notebook.GetCurrentPage().asDlg.Toggle(this.as_local_tg.IsChecked()), this.as_local_tg),
                           (ToggleAutoSave, this.as_global_tg)]

        if autosave.enabled in global_settings.yes_values:
            this.as_global_tg.Check(True)
            this.as_local_tg.Check(True)

        # View menu
        viewmenu_events = [(lambda evt: this.notebook.GetCurrentPage().ZoomIn(), this.zoomin),
                           (lambda evt: this.notebook.GetCurrentPage().ZoomOut(), this.zoomout),
                           (lambda evt: this.notebook.GetCurrentPage().SetWrapMode(this.wrap.IsChecked()), this.wrap),
                           (lambda evt: this.notebook.GetCurrentPage().SetIndentationGuides(this.showguides.IsChecked()), this.showguides),
                           (this.ShowMarkdown, this.preview)]

        this.wrap.Check(
            this.notebook.GetCurrentPage().cfg.getkey(
                "editor", "wordwrap", True, True, True
            ) in global_settings.yes_values
        )

        if this.notebook.GetCurrentPage().GetIndentationGuides():
            this.showguides.Check()

        # Settings menu
        cfgmenu_events = [(lambda evt: this.wiz.ShowModal(), this.settings),
                          (this.ResetCfgs, this.reset),
                          (lambda evt: this.OpenDir(evt, TOPLV_DIR, True), this.opencfg)]

        # Help menu
        helpmenu_events = [(this.ShowAbout, this.about),
                           (this.SysInf_Show, this.sysspecs),
                           (lambda evt: this.logwindow.Show(), this.logs),
                           (this.OpenInspector, this.showinsp),
                           (lambda evt: webbrowser.open("https://gitlab.com/textworker/legacy-python/textworker/issues"), this.report),
                           (lambda evt: webbrowser.open("https://lebao3105.gitbook.io/texteditor_doc"), this.docs)]

        BindMenuEvents(filemenu_events)
        BindMenuEvents(editmenu_events)
        BindMenuEvents(viewmenu_events)
        BindMenuEvents(cfgmenu_events)
        BindMenuEvents(helpmenu_events)

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
            ask = wx.DirDialog(this, _("Select a folder to start"))
            if ask.ShowModal() == wx.ID_OK:
                selected_dir = ask.GetPath()
            else:
                return
        else:
            selected_dir = path

        if not newwind:
            this.dirs.SetFolder(selected_dir)
        else:
            new = wx.Frame(this)
            newctrl = DirCtrl(new, w_styles = DC_MULTIPLE | DC_ONEROOT | DC_HIDEROOT)
            newctrl.SetFolder(selected_dir)
            newctrl.Bind(wx.EVT_TREE_SEL_CHANGED, lambda evt: this.OpenFileFromTree(evt, newctrl))
            new.Show()

    def OpenFileFromTree(this, evt, tree: DirCtrl):
        path = tree.GetFullPath()
        import os
        if not os.path.isdir(path): this.notebook.OpenFile(path)
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
                            wx.YES_NO | wx.ICON_WARNING, this)

        if ask == wx.YES:
            logger.info("App reset requested.")
            ResetEveryConfig()

    def ShowAbout(this, evt):
        aboutdlg = about.AboutDialog(this)
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
        """
        ))
        newdlg = wx.Dialog(this, title=_("System specs"))
        wx.TextCtrl(newdlg, value=msg, style=wx.TE_MULTILINE | wx.TE_READONLY)
        newdlg.ShowModal()

    def NewWindow(this, evt):
        wx.MessageBox("Not implemented")

    def OnFileHistory(this, evt):  # cre: wxdemo program
        # get the file based on the menu ID
        fileNum = evt.GetId() - wx.ID_FILE1
        path = this.file_history.GetHistoryFile(fileNum)
        this.notebook.OpenFile(path)

        # add it back to the history so it will be moved up the list
        this.file_history.AddFileToHistory(path)

    def OpenFile(this, evt):
        this.notebook.AskToOpen(evt)
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
        if not wnd: wnd = this
        InspectionTool().Show(wnd, True)