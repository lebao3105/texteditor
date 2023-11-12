import platform
import webbrowser

import wx
import wx.adv
import wx.aui
import wx.html2
import wx.lib.splitter
import wx.xrc

try:
    from cairosvg import svg2png  # type: ignore
except ImportError:
    CAIRO_AVAILABLE = False
else:
    CAIRO_AVAILABLE = True

from libtextworker import __version__ as libver
from libtextworker.general import (
    ResetEveryConfig,
    logger,
    CraftItems,
    GetCurrentDir,
)
from libtextworker.interface.wx.about import AboutDialog
from libtextworker.interface.wx.dirctrl import PatchedDirCtrl
from libtextworker.interface.wx.miscs import XMLBuilder, BindMenuEvents
from libtextworker.versioning import *

from . import __version__ as appver, icon
from .extensions import autosave, multiview, gitsp, mergedialog, settings
from .generic import global_settings, TOPLV_DIR
from .tabs import Tabber

# https://stackoverflow.com/a/27872625
if platform.system() == "Windows":
    import ctypes

    myappid = "me.lebao3105.textworker"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MainFrame(XMLBuilder):
    cfg = global_settings
    logfmter = wx.LogFormatter()

    def __init__(self):
        XMLBuilder.__init__(
            self, nil, CraftItems(GetCurrentDir(__file__), "ui", "mainmenu.xrc")
        )

        self.mainFrame = self.loadObject("mainFrame", "wxFrame")
        self.mainFrame.SetSize((860, 640))

        if CAIRO_AVAILABLE:
            svg2png(open(icon, "r").read(), write_to="./icon.png")
            self.mainFrame.SetIcon(wx.Icon("./icon.png"))

        self.Show = self.mainFrame.Show
        self.Hide = self.mainFrame.Hide
        self.Close = self.mainFrame.Close

        mainboxer = wx.BoxSizer(wx.VERTICAL)
        editorBox = wx.lib.splitter.MultiSplitterWindow(self.mainFrame, style=wx.SP_LIVE_UPDATE)

        # Editor
        self.notebook = Tabber(editorBox)

        # Side bar

        ## Container
        self.multiviewer = multiview.MultiViewer(editorBox)

        ## Explorer
        self.dirs = PatchedDirCtrl(self.multiviewer.tabs)
        self.dirs.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OpenFileFromTree)
        self.multiviewer.RegisterTab("Explorer", self.dirs)

        ## Git
        self.gitsp = gitsp.GitSupportGUI(self.multiviewer.tabs)
        self.multiviewer.RegisterTab("Git", self.gitsp.Panel)

        ## Always show Explorer on startup
        self.multiviewer.tabs.SetSelection(0)

        # Other stuff
        self.wiz = settings.SettingsDialog(self.mainFrame).dlg
        self.file_history = wx.FileHistory()
        self.autosv_cfg = autosave.AutoSaveConfig(self.mainFrame)
        self.logwindow = wx.LogWindow(self.mainFrame, _("Log"), false)
        self.logwindow.SetFormatter(self.logfmter)
        self.logwindow.SetVerbose(true)
        # mergedialog.MergeDialog(self.mainFrame).ShowModal()

        # Place everything
        editorBox.AppendWindow(self.multiviewer.tabs, 246)
        editorBox.AppendWindow(self.notebook)
        mainboxer.Add(editorBox, 1, wx.GROW, 5)

        self.LoadMenu()
        self.mainFrame.Bind(wx.EVT_CLOSE, self.OnClose)

        self.mainFrame.SetSizer(mainboxer)

        self.mainFrame.Layout()
        self.mainFrame.Centre()

    def LoadMenu(self):
        def ToggleAutoSave(evt):
            wx.MessageBox(
                _("This will only affect to this session"), parent=self.mainFrame
            )
            autosave.TOGGLE = not autosave.TOGGLE
            evt.Skip()

        filemenu = self.mainFrame.GetMenuBar().GetMenu(0)
        editmenu = self.mainFrame.GetMenuBar().GetMenu(1)
        viewmenu = self.mainFrame.GetMenuBar().GetMenu(2)
        cfgmenu = self.mainFrame.GetMenuBar().GetMenu(3)
        helpmenu = self.mainFrame.GetMenuBar().GetMenu(4)

        # File menu
        # Remember to skip separators!
        filemenu_events = [
            (self.notebook.AddTab, 0),
            (self.NewWindow, 1),
            # Sep
            (self.OpenFile, 3),
            # Open folder (submenu)
            # Recents
            # Sep
            (self.notebook.fileops.SaveFileEvent, 7),
            (self.notebook.fileops.AskToSave, 8),
            # Sep
            (self.CloseAllPages, 10),
            (
                lambda evt: wx.PostEvent(
                    self.mainFrame, wx.CommandEvent(wx.wxEVT_CLOSE_WINDOW)
                ),
                11,
            ),
        ]

        for callback, pos in [
            (self.OpenDir, 0),
            (lambda evt: self.OpenDir(evt, newwind=true), 1),
        ]:
            self.mainFrame.Bind(
                wx.EVT_MENU,
                callback,
                filemenu.FindItemByPosition(4).GetSubMenu().FindItemByPosition(pos),
            )

        ## Setup wxFileHistory
        self.file_history.UseMenu(filemenu.FindItemByPosition(5).GetSubMenu())
        self.mainFrame.Bind(
            wx.EVT_MENU_RANGE, self.OnFileHistory, id=wx.ID_FILE1, id2=wx.ID_FILE9
        )

        # Edit menu
        editmenu_events = [
            (lambda evt: self.notebook.GetCurrentPage().Undo(), 0),
            (lambda evt: self.notebook.GetCurrentPage().Redo(), 1),
            (lambda evt: self.notebook.GetCurrentPage().Cut(), 3),
            (lambda evt: self.notebook.GetCurrentPage().Copy(), 4),
            (lambda evt: self.notebook.GetCurrentPage().Paste(), 5),
            (lambda evt: self.notebook.GetCurrentPage().SelectAll(), 7)
            # Find & Replace dialogs are not implemented yet
        ]

        ## Auto-save menus
        ## This. REALLY.
        global_autosv = (
            editmenu.FindItemByPosition(12)
            .GetSubMenu()
            .FindItemByPosition(0)
            .GetSubMenu()
        )
        editor_autosv = (
            editmenu.FindItemByPosition(12)
            .GetSubMenu()
            .FindItemByPosition(1)
            .GetSubMenu()
        )

        self.mainFrame.Bind(
            wx.EVT_MENU,
            lambda evt: self.autosv_cfg.ConfigWindow(),
            global_autosv.FindItemByPosition(0),
        )

        self.mainFrame.Bind(
            wx.EVT_MENU,
            lambda evt: self.notebook.GetCurrentPage().ConfigWindow(),
            editor_autosv.FindItemByPosition(0),
        )

        if autosave.enabled in global_settings.yes_values:
            global_autosv.FindItemByPosition(1).Check(true)
            editor_autosv.FindItemByPosition(1).Check(true)
            self.notebook.GetCurrentPage().Start()  # On init only 1 tab opened, so we can do this

        self.mainFrame.Bind(
            wx.EVT_MENU,
            lambda evt: self.notebook.GetCurrentPage().Toggle(
                editor_autosv.FindItemByPosition(1).IsChecked()
            ),
            editor_autosv.FindItemByPosition(1),
        )

        self.mainFrame.Bind(
            wx.EVT_MENU,
            lambda evt: ToggleAutoSave(evt),
            global_autosv.FindItemByPosition(1),
        )

        # View menu
        viewmenu_events = [
            (lambda evt: self.notebook.GetCurrentPage().ZoomIn(), 0),
            (lambda evt: self.notebook.GetCurrentPage().ZoomOut(), 1),
            (self.ShowMarkdown, 4),
        ]

        viewmenu.FindItemByPosition(2).Check(
            bool(
                self.notebook.GetCurrentPage().cfg.getkey(
                    "editor", "wordwrap", true, true, true
                )
            )
        )
        self.mainFrame.Bind(
            wx.EVT_MENU,
            lambda evt: self.notebook.GetCurrentPage().SetWrapMode(
                viewmenu.FindItemByPosition(2).IsChecked()
            ),
            viewmenu.FindItemByPosition(2),
        )

        if self.notebook.GetCurrentPage().GetIndentationGuides():
            viewmenu.FindItemByPosition(3).Check()

        self.mainFrame.Bind(
            wx.EVT_MENU,
            lambda evt: self.notebook.GetCurrentPage().SetIndentationGuides(
                viewmenu.FindItemByPosition(3).IsChecked()
            ),
            viewmenu.FindItemByPosition(3),
        )

        # Settings menu
        cfgmenu_events = [
            (lambda evt: self.wiz.ShowModal(), 0),
            (self.ResetCfgs, 1),
            (lambda evt: self.OpenDir(evt, TOPLV_DIR, true), 2),
        ]

        # Help menu
        helpmenu_events = [
            (self.ShowAbout, 0),
            (self.SysInf_Show, 1),
            (lambda evt: self.logwindow.Show(), 2),
            (
                lambda evt: webbrowser.open(
                    "https://github.com/lebao3105/texteditor/issues"
                ),
                4,
            ),
            (
                lambda evt: webbrowser.open(
                    "https://lebao3105.gitbook.io/texteditor_doc"
                ),
                5,
            ),
        ]

        BindMenuEvents(self.mainFrame, filemenu, filemenu_events)
        BindMenuEvents(self.mainFrame, editmenu, editmenu_events)
        BindMenuEvents(self.mainFrame, viewmenu, viewmenu_events)
        BindMenuEvents(self.mainFrame, cfgmenu, cfgmenu_events)
        BindMenuEvents(self.mainFrame, helpmenu, helpmenu_events)

    """
    Event callbacks
    """

    def OnClose(self, evt):
        evt.Skip()
        wx.GetApp().ExitMainLoop()

    def OpenDir(self, evt, path: str = "", newwind: bool = false):
        if not path:
            ask = wx.DirDialog(
                self.mainFrame,
                _("Select a folder to start"),
            )
            if ask.ShowModal() == wx.ID_OK:
                selected_dir = ask.GetPath()
            else:
                return
        else:
            selected_dir = path

        if not newwind:
            self.dirs.SetFolder(selected_dir)
            self.gitsp.InitFolder(selected_dir)
        else:
            new = wx.Frame(self.mainFrame)
            newctrl = PatchedDirCtrl(new)
            newctrl.SetFolder(selected_dir)
            newctrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OpenFileFromTree)
            new.Show()

    def OpenFileFromTree(self, evt):
        path = self.dirs.GetFullPath()
        self.notebook.fileops.OpenFile(self.gitsp.currdir + "/" + path)

    def ShowMarkdown(self, evt):
        def autorefresh(event):
            event.Skip()
            nonlocal wind, content, newwind
            if not wind:
                return  # Window closed
            content = markdown(self.notebook.GetCurrentPage().GetText())
            newwind.SetPage(content, "")
            wind.Refresh()

        try:
            from markdown2 import markdown
        except ImportError:
            wx.MessageBox(
                _(
                    "You need to get markdown2 package from Pypi first!\n"
                    "If you're running a packaged version, tell us."
                ),
                _("Extra package required"),
                parent=self.mainFrame,
            )
            return false

        content = markdown(self.notebook.GetCurrentPage().GetText())

        wind = wx.Frame(self.mainFrame)
        newwind = wx.html2.WebView.New(wind)
        newwind.SetPage(content, "")

        wind.Show()
        newwind.Show(true)

        self.notebook.GetCurrentPage().Bind(wx.EVT_CHAR, autorefresh)

    def ResetCfgs(self, evt):
        ask = wx.MessageDialog(
            self.mainFrame,
            _(
                "Are you sure want to reset every settings?\n"
                "If so, finish your work first since the app will close after"
                "the operation.\n(and you will need to reopen yourself)"
            ),
            style=wx.YES_NO | wx.ICON_WARNING,
        ).ShowModal()

        if ask == wx.ID_YES:
            logger.info("App reset requested.")
            ResetEveryConfig()

    def ShowAbout(self, evt):
        aboutdlg = AboutDialog()
        aboutdlg.SetName("TextWorker")
        aboutdlg.SetVersion(appver)
        if CAIRO_AVAILABLE:
            aboutdlg.SetIcon(wx.Icon("./icon.png"))
        aboutdlg.SetDescription(_("A simplified text editor."))
        aboutdlg.SetCopyright("(C) 2022-2023 Le Bao Nguyen")
        aboutdlg.SetWebSite("https://github.com/lebao3105/texteditor")
        aboutdlg.SetLicense("GPL3_short")
        aboutdlg.infos.AddDeveloper("Le Bao Nguyen")
        aboutdlg.infos.AddDocWriter("Le Bao Nguyen")
        return aboutdlg.ShowBox()

    def SysInf_Show(self, evt):
        ostype = platform.system() if platform.system() != "" or nil else _("Unknown")
        msg = _(
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
        )
        newdlg = wx.Dialog(self.mainFrame, title=_("System specs"))
        wx.StaticText(newdlg, label=msg)
        newdlg.ShowModal()

    def NewWindow(self, evt):
        # cloned = wx.App()
        # cloned.SetAppName("textworker")
        # newwind = MainFrame()
        # cloned.SetTopWindow(newwind.mainFrame)
        # newwind.Show()
        # cloned.MainLoop()
        wx.MessageBox("Fixes needed")

    def OnFileHistory(self, evt):  # cre: wxdemo program
        # get the file based on the menu ID
        fileNum = evt.GetId() - wx.ID_FILE1
        path = self.file_history.GetHistoryFile(fileNum)
        self.notebook.fileops.OpenFile(path)

        # add it back to the history so it will be moved up the list
        self.file_history.AddFileToHistory(path)

    def OpenFile(self, evt):
        self.notebook.fileops.AskToOpen(evt)
        self.file_history.AddFileToHistory(
            self.notebook.GetPageText(self.notebook.GetSelection())
        )

    def CloseAllPages(self, evt):
        self.notebook.DeleteAllPages()
        wx.PostEvent(
            self.notebook, wx.CommandEvent(wx.aui.wxEVT_AUINOTEBOOK_PAGE_CLOSED)
        )
