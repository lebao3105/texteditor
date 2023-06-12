import os
import platform
import webbrowser

import wx
import wx.adv
import wx.html2
import wx.stc

try:
    from cairosvg import svg2png
except ImportError:
    CAIRO_AVAILABLE = False
else:
    CAIRO_AVAILABLE = True

from libtextworker import __version__ as libver
from libtextworker.general import TOPLV_DIR, ResetEveryConfig, logger
from libtextworker.interface.wx.about import AboutDialog
from libtextworker.interface.wx.dirctrl import PatchedDirCtrl
from libtextworker.interface.wx.miscs import CreateMenu
from libtextworker.versioning import *
from textworker import __version__ as appver
from textworker import icon

from .extensions import autosave, multiview, gitsp
from .generic import SettingsWindow, global_settings, LogFormatter
from .tabs import Tabber

# https://stackoverflow.com/a/27872625
if platform.system() == "Windows":
    import ctypes

    myappid = "me.lebao3105.textworker"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

cfg = global_settings
logger.UseGUIToolKit("wx")
logfmter = LogFormatter()


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((860, 640))

        if CAIRO_AVAILABLE:
            svg2png(open(icon, "r").read(), write_to="./icon.png")
            self.SetIcon(wx.Icon("./icon.png"))

        """ Main box sizer ever . """
        mainboxer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainboxer)

        # wxInfoBar
        self.infer = wx.InfoBar(self)
        mainboxer.Add(self.infer)

        """ Main editor frame """
        editorbox = wx.SplitterWindow(self)

        # Editor
        self.notebook = Tabber(editorbox)

        # Side bar

        ## Container
        self.multiviewer = multiview.MultiViewer(editorbox)

        ## Explorer
        self.dirs = PatchedDirCtrl(self.multiviewer.tabs)
        self.dirs.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OpenFileFromTree)
        self.multiviewer.RegisterTab("Explorer", self.dirs)

        ## Git
        self.gitsp = gitsp.GitSupportGUI(self.multiviewer.tabs)
        self.multiviewer.RegisterTab("Git", self.gitsp.Panel)

        ## Always show Explorer on startup
        self.multiviewer.tabs.SetSelection(0)

        editorbox.SplitVertically(self.multiviewer.tabs, self.notebook, 246)

        mainboxer.Add(editorbox, 1, wx.GROW, 5)

        # Else things
        self.wiz = SettingsWindow(self)
        self.autosv_cfg = autosave.AutoSaveConfig(self)
        self.logwindow = wx.LogWindow(self, "Log", False)
        self.logwindow.SetFormatter(logfmter)
        self.logwindow.SetVerbose()

        self.PlaceMenu()
        self.Layout()

    def PlaceMenu(self):
        self.menubar = wx.MenuBar()

        ## File
        filemenu = CreateMenu(
            self,
            [
                (wx.ID_NEW, None, None, self.notebook.AddTab, None),
                (wx.ID_OPEN, None, None, self.OpenFile, None),
                (
                    wx.ID_ANY,
                    _("Open directory\tCtrl+Shift+D"),
                    None,
                    self.OpenDir,
                    None,
                ),
                (
                    wx.ID_ANY,
                    _("Close all tabs"),
                    None,
                    lambda evt: (
                        self.notebook.DeleteAllPages(),
                        self.notebook.AddTab(),
                    ),
                    None,
                ),
                (None, None, None, None, None),  # Separator
                (wx.ID_SAVE, None, None, self.SaveFile, None),
                (
                    wx.ID_SAVEAS,
                    _("Save as...\tCtrl+Shift+S"),
                    None,
                    self.SaveAs,
                    None,
                ),
                (None, None, None, None, None),
                (wx.ID_EXIT, _("Quit\tAlt+F4"), None, lambda evt: self.Close, None),
            ],
        )

        ## Edit
        editmenu = CreateMenu(
            self,
            [
                (
                    wx.ID_COPY,
                    None,
                    None,
                    lambda evt: self.TextEditOps(evt, "copy"),
                    None,
                ),
                (
                    wx.ID_PASTE,
                    None,
                    None,
                    lambda evt: self.TextEditOps(evt, "paste"),
                    None,
                ),
                (
                    wx.ID_CUT,
                    None,
                    None,
                    lambda evt: self.TextEditOps(evt, "cut"),
                    None,
                ),
                (None, None, None, None, None),
                (
                    wx.ID_SELECTALL,
                    None,
                    None,
                    lambda evt: self.TextEditOps(evt, "selall"),
                    None,
                ),
                (
                    wx.ID_DELETE,
                    _("Delete\tDelete"),
                    None,
                    lambda evt: self.TextEditOps(evt, "delback"),
                    None,
                ),
                (None, None, None, None, None),
                (
                    wx.ID_ANY,
                    _("Auto save"),
                    _("Configure auto-saving file function"),
                    lambda evt: self.autosv_cfg.ConfigWindow(),
                    None,
                ),
            ],
        )

        ## View
        viewmenu = CreateMenu(
            self,
            [
                (
                    wx.ID_ZOOM_IN,
                    _("Zoom in\tCtrl++"),
                    None,
                    lambda evt: self.ZoomEditor(evt, "zoomin"),
                    None,
                ),
                (
                    wx.ID_ZOOM_OUT,
                    _("Zoom out\tCtrl+-"),
                    None,
                    lambda evt: self.ZoomEditor(evt, "zoomout"),
                    None,
                ),
                (
                    None,
                    _("View markdown document"),
                    None,
                    lambda evt: self.ShowMarkdown(evt),
                    None,
                ),
            ],
        )
        wrap = wx.MenuItem(viewmenu, wx.ID_ANY, _("Wrap by word"), kind=wx.ITEM_CHECK)
        viewmenu.Append(wrap)
        self.Bind(
            wx.EVT_MENU,
            lambda evt: self.notebook.text_editor.SetWrapMode(wrap.IsChecked()),
            wrap,
        )

        tabgd = wx.MenuItem(
            viewmenu,
            wx.ID_ANY,
            _("Show tab guides"),
            kind=wx.ITEM_CHECK,
        )
        viewmenu.Append(tabgd)
        if self.notebook.text_editor.GetIndentationGuides():
            tabgd.Check()
        self.Bind(
            wx.EVT_MENU,
            lambda evt: (
                self.notebook.text_editor.SetIndentationGuides(tabgd.IsChecked())
            ),
            tabgd,
        )

        ## Configs
        configsmenu = CreateMenu(
            self,
            [
                (
                    wx.ID_ANY,
                    _("Show all configurations"),
                    None,
                    lambda evt: self.OpenDir(None, TOPLV_DIR),
                    None,
                ),
                (wx.ID_ANY, _("Reset all configs"), None, self.ResetCfgs, None),
                (wx.ID_ANY, _("Run Setup"), None, self.wiz.Run, None),
            ],
        )

        ## Help
        helpmenu = CreateMenu(
            self,
            [
                (wx.ID_ABOUT, None, None, self.ShowAbout, None),
                (
                    None,
                    _("Documentation"),
                    _("Read app documents online."),
                    lambda evt: webbrowser.open_new_tab(
                        "https://lebao3105.gitbook.io/texteditor_doc"
                    ),
                    None,
                ),
                (
                    None,
                    _("System specs"),
                    _("Show system specs found - helpful for bug reports or questions"),
                    self.SysInf_Show,
                    None,
                ),
                (
                    None,
                    _("Source code"),
                    _("View the app source code online."),
                    lambda evt: webbrowser.open_new_tab(
                        "https://github.com/lebao3105/texteditor/tree/wip/wx"
                    ),
                    None,
                ),
                (None, _("View log"), None, lambda evt: self.logwindow.Show(), None),
            ],
        )

        self.menubar.Append(filemenu, _("&File"))
        self.menubar.Append(editmenu, _("&Edit"))
        self.menubar.Append(viewmenu, _("&View"))
        self.menubar.Append(configsmenu, _("&Config"))
        self.menubar.Append(helpmenu, _("&Help"))
        self.SetMenuBar(self.menubar)

    """
    Event callbacks
    """

    def OnClose(self, evt):
        evt.Skip()
        wx.GetApp().ExitMainLoop()

    def OpenDir(self, evt, path: str = ""):
        if not path:
            ask = wx.DirDialog(
                self,
                _("Select a folder to start"),
            )
            if ask.ShowModal() == wx.ID_OK:
                selected_dir = ask.GetPath()
            else:
                return
        else:
            selected_dir = path

        self.dirs.SetFolder(selected_dir)
        self.gitsp.InitFolder(selected_dir)

    def OpenFileFromTree(self, evt):
        path = self.dirs.GetFullPath()
        if not os.path.isfile(path):
            return
        self.notebook.fileops.OpenFile(path)

    def ShowMarkdown(self, evt):
        try:
            from markdown2 import markdown
        except ImportError:
            wx.MessageBox(
                _("You need to get markdown2 package from Pypi first!"),
                _("Extra package required"),
                parent=self,
            )
            return False

        content = markdown(self.notebook.text_editor.GetText())

        wind = wx.Frame(self, title=_("Markdown to HTML"))
        newwind = wx.html2.WebView.New(wind)
        newwind.SetPage(content, "")

        wind.Show()
        newwind.Show(True)

    def ResetCfgs(self, evt):
        ask = wx.MessageDialog(
            self,
            _(
                "Are you sure want to reset all configurations?\nThere is no way BACK!\nThe app will close after the operation."
            ),
            _("Confirm configs reset"),
            wx.YES_NO | wx.ICON_WARNING,
        ).ShowModal()
        if ask == wx.ID_YES:
            logger.info(_("Done resetting all configs. App restart required."))
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
        newdlg = wx.Dialog(self, title=_("System specs"))
        wx.StaticText(newdlg, label=msg)
        newdlg.ShowModal()

    """
    Still event callbacks, but "lambda evt" does not work
    * but not all of them, "Close all tabs" is an example *
    """

    # File operations
    def OpenFile(self, evt) -> bool:
        return self.notebook.fileops.AskToOpen()

    def SaveFile(self, evt) -> bool:
        return self.notebook.fileops.SaveFile(
            self.notebook.GetPageText(self.notebook.GetSelection())
        )

    def SaveAs(self, evt) -> bool:
        return self.notebook.fileops.AskToSave()

    # Text edit
    def TextEditOps(self, evt, action: str):
        acts = {
            "copy": self.notebook.text_editor.Copy(),
            "paste": self.notebook.text_editor.Paste(),
            "cut": self.notebook.text_editor.Cut(),
            "selall": self.notebook.text_editor.SelectAll(),
            "delback": self.notebook.text_editor.DeleteBack(),
        }
        return acts.get(action)

    def ZoomEditor(self, evt, i: str):
        if i == "zoomin":
            return self.notebook.text_editor.ZoomIn()
        elif i == "zoomout":
            return self.notebook.text_editor.ZoomOut()
