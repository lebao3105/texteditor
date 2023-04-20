import logging
import platform
import webbrowser

import wx
import wx.adv
import wx.stc

import textworker
from libtextworker.general import ResetEveryConfig
from libtextworker.interface.wx.about import AboutDialog
from libtextworker.interface.wx.miscs import CreateMenu
from libtextworker.versioning import *

from .extensions import multiview
from .generic import SettingsWindow, global_settings
from .tabs import Tabber

# https://stackoverflow.com/a/27872625
if platform.system() == "Windows":
    import ctypes

    myappid = "me.lebao3105.texteditor"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

cfg = global_settings.cfg
logger = logging.getLogger("textworker")


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.SetSize((820, 685))
        self.SetIcon(wx.Icon(textworker.icon))

        self.SetupStatusBar()
        self.SetupEditor()
        self.SetupLogger()

        self.sidebar = multiview.MultiViewer(self)
        self.wiz = SettingsWindow(self)

        self.PlaceMenu()
        self.Layout()

    """
    Setup basic components.
    """

    def SetupLogger(self):
        self.logwindow = wx.Frame(self, title=_("Logs"))
        self.logwindow.logs = wx.TextCtrl(
            self.logwindow,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL,
        )
        self.logwindow.Layout()

    def SetupEditor(self):
        self.notebook = Tabber(self, style=wx.EXPAND)
        tabname = self.notebook.GetPageText(self.notebook.GetSelection())
        self.SetTitle(tabname)
        self.SetStatusText(tabname)

    def SetupStatusBar(self):
        self.CreateStatusBar(2)
        righttext_width = self.StatusBar.Size[0] - 50
        self.StatusBar.SetStatusWidths([righttext_width, -1])

        self.messages_text = wx.StaticText(
            self.StatusBar, wx.ID_ANY, label=_("Messages")
        )
        self.messages_text.SetPosition((righttext_width + 2, 2))
        self.messages_text.Bind(wx.EVT_LEFT_DOWN, self.ShowLogWindow)

        del righttext_width

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
                    self.notebook.autosv.Config,
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
                )
            ],
        )
        wrap = wx.MenuItem(viewmenu, wx.ID_ANY, _("Wrap by word"), kind=wx.ITEM_CHECK)
        viewmenu.Append(wrap)
        self.Bind(
            wx.EVT_MENU,
            lambda evt: self.notebook.text_editor.SetWrapMode(wrap.IsChecked()),
            wrap,
        )

        tabgd = wx.MenuItem(viewmenu, wx.ID_ANY, _("Show/hide tab guides (checked = on)"), kind=wx.ITEM_CHECK)
        viewmenu.Append(tabgd)
        self.Bind(
            wx.EVT_MENU,
            lambda evt: self.notebook.text_editor.SetIndentationGuides(False),
            tabgd
        )

        ## Configs
        configsmenu = CreateMenu(
            self,
            [
                (wx.ID_ANY, _("Show all configurations"), None, self.ShowCfgs, None),
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
                    wx.ID_HELP,
                    None,
                    None,
                    lambda evt: webbrowser.open_new_tab(
                        "https://lebao3105.gitbook.io/texteditor_doc"
                    ),
                    None,
                ),
                (
                    None,
                    _("Source code"),
                    _("View the app source code online."),
                    lambda evt: webbrowser.open_new_tab(
                        "https://github.com/lebao3105/texteditor"
                    ),
                    None,
                ),
            ],
        )

        self.menubar.Append(filemenu, _("&File"))
        self.menubar.Append(editmenu, _("&Edit"))
        self.menubar.Append(viewmenu, _("&View"))
        self.menubar.Append(configsmenu, _("&Configs"))
        self.menubar.Append(helpmenu, _("&Help"))
        self.SetMenuBar(self.menubar)

    """
    Logging
    """

    def SetMessageText(self, msg: str):
        self.messages_text.SetLabel(msg)
        self.logwindow.logs.WriteText(msg + "\n")
        self.logwindow.logs.WriteText(msg + "\n")
        wx.CallLater(5000, self.messages_text.SetLabel, _("Got new message(s)!"))
        wx.CallLater(10000, self.messages_text.SetLabel, _("Messages"))

    """
    Event callbacks
    """

    def OpenDir(self, evt):
        ask = wx.DirDialog(
            self,
            _("Select a folder to start"),
        )
        if ask.ShowModal() == wx.ID_OK:
            selected_dir = ask.GetPath()
        else:
            return

        dirs = wx.GenericDirCtrl(self.sidebar.tabs, -1, selected_dir)
        dirs.Bind(
            wx.EVT_DIRCTRL_FILEACTIVATED,
            lambda evt: self.notebook.fileops.Load(dirs.GetFilePath()),
        )
        dirs.SetDefaultPath(selected_dir)
        dirs.Show()
        self.sidebar.RegisterTab(selected_dir, dirs)
        self.sidebar.Show()

    def ShowCfgs(self, evt):
        import os

        dirs = wx.GenericDirCtrl(
            self.sidebar.tabs, -1, os.path.expanduser("~/.config/textworker"),
            style=wx.DIRCTRL_DEFAULT_STYLE | wx.DIRCTRL_EDIT_LABELS
        )
        dirs.Bind(
            wx.EVT_DIRCTRL_FILEACTIVATED,
            lambda evt: self.notebook.fileops.LoadFn(dirs.GetFilePath()),
        )
        dirs.Show()
        self.sidebar.RegisterTab(os.path.expanduser("~/.config/textworker"), dirs)
        self.sidebar.Show()

    def ResetCfgs(self, evt):
        ask = wx.MessageDialog(
            None,
            _(
                "Are you sure want to reset all configurations? There is no way to BACK! The app will close after the operation."
            ),
            _(
                "Are you sure want to reset all configurations? There is no way to BACK! The app will close after the operation."
            ),
            _("Confirm configs reset"),
            wx.YES_NO | wx.ICON_WARNING,
        ).ShowModal()
        if ask == wx.ID_YES:
            return ResetEveryConfig()

    def ShowLogWindow(self, evt):
        return self.logwindow.Show()

    def ShowAbout(self, evt):
        wxver = wx.__version__
        pyver = platform.python_version()
        ostype = platform.system() if platform.system() != "" or None else _("Unknown")
        msg = _(
            """
        A simple, cross-platform text editor.
        Branch: {}
        wxPython version: {}
        Python verison: {}
        OS type: {}
        """.format(
                "DEV" if is_development_version_from_project("textworker") == True else "STABLE",
                wxver,
                pyver,
                ostype,
            )
        )
        aboutdlg = AboutDialog()
        aboutdlg.Parent = self
        aboutdlg.SetName("TextWorker")
        aboutdlg.SetVersion(textworker.__version__)
        aboutdlg.SetIcon(wx.Icon(textworker.icon))
        aboutdlg.SetDescription(msg)
        aboutdlg.SetCopyright("(C) 2022-2023 Le Bao Nguyen")
        aboutdlg.SetWebSite("https://github.com/lebao3105/texteditor")
        aboutdlg.SetLicense("GPL3_short")
        aboutdlg.infos.AddDeveloper("Le Bao Nguyen")
        aboutdlg.infos.AddDocWriter("Le Bao Nguyen")
        return aboutdlg.ShowBox()

    """
    Still event callbacks, but "lambda evt" does not work
    * but not all of them, "Close all tabs" is an example *
    """

    def OpenFile(self, evt) -> bool:
        return self.notebook.fileops.AskToOpen()

    def SaveFile(self, evt) -> bool:
        return self.notebook.fileops.Save(
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

    """
    Still event callbacks, but "lambda evt" does not work
    * but not all of them, "Close all tabs" is an example *
    """

    def OpenFile(self, evt) -> bool:
        return self.notebook.fileops.AskToOpen()

    def SaveFile(self, evt) -> bool:
        return self.notebook.fileops.Save(
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
