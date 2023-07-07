import platform
import webbrowser

import wx
import wx.adv
import wx.aui
import wx.html2
import wx.xrc

try:
    from cairosvg import svg2png  # type: ignore
except ImportError:
    CAIRO_AVAILABLE = False
else:
    CAIRO_AVAILABLE = True

from libtextworker import __version__ as libver
from libtextworker.general import (
    TOPLV_DIR,
    ResetEveryConfig,
    logger,
    CraftItems,
    GetCurrentDir,
)
from libtextworker.interface.wx.about import AboutDialog
from libtextworker.interface.wx.dirctrl import PatchedDirCtrl
from libtextworker.interface.wx.miscs import XMLBuilder, BindMenuEvents
from libtextworker.versioning import *

from textworker import __version__ as appver, icon
from .extensions import autosave, multiview, gitsp, mergedialog
from .generic import SettingsWindow, global_settings, LogFormatter
from .tabs import Tabber

# https://stackoverflow.com/a/27872625
if platform.system() == "Windows":
    import ctypes

    myappid = "me.lebao3105.textworker"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class MainFrame(XMLBuilder):
    cfg = global_settings
    logger.UseGUIToolKit("wx")
    logfmter = LogFormatter()

    def __init__(self):
        super().__init__(
            None, CraftItems(GetCurrentDir(__file__), "ui", "mainmenu.xrc")
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
        editorBox = wx.SplitterWindow(self.mainFrame)

        # wxInfoBar
        self.infer = wx.InfoBar(self.mainFrame)

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

        # Other stuffs
        self.wiz = SettingsWindow(self.mainFrame)
        self.file_history = wx.FileHistory()
        self.autosv_cfg = autosave.AutoSaveConfig(self.mainFrame)
        self.logwindow = wx.LogWindow(self.mainFrame, "Log", False)
        self.logwindow.SetFormatter(self.logfmter)
        self.logwindow.SetVerbose()
        # mergedialog.MergeDialog(self.mainFrame).ShowModal()

        # Place everything
        editorBox.SplitVertically(self.multiviewer.tabs, self.notebook, 246)
        mainboxer.Add(self.infer, wx.EXPAND)
        mainboxer.Add(editorBox, 1, wx.GROW, 5)

        self.LoadMenu()
        self.mainFrame.Bind(wx.EVT_CLOSE, self.OnClose)
        self.mainFrame.SetSizer(mainboxer)
        self.mainFrame.Layout()
        self.mainFrame.Centre()

    def LoadMenu(self):

        def ToggleAutoSave(evt):
            wx.MessageBox(_("This will only affect to this session"), parent=self.mainFrame)
            autosave.TOGGLE = False
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
            (lambda evt: self.OpenDir(evt, newwind=True), 1),
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
            global_autosv.FindItemByPosition(1).Check(True)
            editor_autosv.FindItemByPosition(1).Check(True)
            self.notebook.GetCurrentPage().Start()  # On init only 1 tab opened, so we can do this
        
        self.mainFrame.Bind(
            wx.EVT_MENU,
            lambda evt: self.notebook.GetCurrentPage().Toggle(editor_autosv.FindItemByPosition(1).IsChecked()),
            editor_autosv.FindItemByPosition(1)
        )

        self.mainFrame.Bind(
            wx.EVT_MENU,
            lambda evt: ToggleAutoSave(evt),
            global_autosv.FindItemByPosition(1)
        )

        # View menu
        viewmenu_events = [
            (lambda evt: self.notebook.GetCurrentPage().ZoomIn(), 0),
            (lambda evt: self.notebook.GetCurrentPage().ZoomOut(), 1),
            (self.ShowMarkdown, 4),
        ]

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
            # OMG Settings window! But not this time:) (index 0)
            (self.ResetCfgs, 1),
            (lambda evt: self.OpenDir(evt, TOPLV_DIR, True), 2),
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

    def OpenDir(self, evt, path: str = "", newwind: bool = False):
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
            PatchedDirCtrl(new).SetFolder(selected_dir)
            new.Show()

    def OpenFileFromTree(self, evt):
        path = self.dirs.GetFullPath()
        self.notebook.fileops.OpenFile(self.gitsp.currdir + "/" + path)

    def ShowMarkdown(self, evt):
        try:
            from markdown2 import markdown  # type: ignore
        except ImportError:
            wx.MessageBox(
                _("You need to get markdown2 package from Pypi first!"),
                _("Extra package required"),
                parent=self.mainFrame,
            )
            return False

        content = markdown(self.notebook.text_editor.GetText())

        wind = wx.Frame(self.mainFrame)
        newwind = wx.html2.WebView.New(wind)
        newwind.SetPage(content, "")

        wind.Show()
        newwind.Show(True)

    def ResetCfgs(self, evt):
        ask = wx.MessageDialog(
            self.mainFrame,
            _(
                "Are you sure want to reset every settings?\n"
                "If so, finish your work first since the app will close after"
                "the operation. (and you will need to reopen yourself)"
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
        ostype = platform.system() if platform.system() != "" or None else _("Unknown")
        msg = _(
            f"""
        Textworker version {appver}
        Branch: {"DEV" if is_development_version(appver) else "STABLE"}
        libtextworker verison {libver}
        wxPython version: {wx.__version__}
        Python verison: {platform.python_version()}
        OS type: {ostype}
        OS version {platform.version()}
        Machine architecture: {platform.machine()}
        """
        )
        newdlg = wx.Dialog(self.mainFrame, title=_("System specs"))
        wx.StaticText(newdlg, label=msg)
        newdlg.ShowModal()

    def NewWindow(self, evt):
        cloned = wx.App()
        cloned.SetAppName("textworker")
        newwind = MainFrame()
        cloned.SetTopWindow(newwind.mainFrame)
        newwind.Show()
        cloned.MainLoop()

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
