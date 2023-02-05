import platform
import time
import textworker
import webbrowser
import wx
import wx.adv
import wx.stc

from .textwidget import TextWidget
from .generic import global_settings, log, MenuBar
from .tabs import Tabber
from .backend import get_config, is_development_build
from .extensions import cmd, multiview

# https://stackoverflow.com/a/27872625
if platform.system() == "Windows":
    import ctypes
    myappid = u'me.lebao3105.texteditor' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

cfg = global_settings.cfg

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((820, 685))
        self.SetIcon(wx.Icon(textworker.icon))

        self.notebook = Tabber(self, wx.ID_ANY, style=wx.EXPAND)
        self.menuitem = {}
        self.sidebar = multiview.MultiViewer(self)
        self.islogwindopen : bool = False
        self._StatusBar()

        tabname = self.notebook.GetPageText(self.notebook.GetSelection())
        self.SetTitle("Texteditor - %s" % tabname)
        self.SetStatusText(tabname)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.PlaceMenu()
        self.Layout()

    def _StatusBar(self):
        self.CreateStatusBar(2)
        w1 = self.StatusBar.Size[0] - 50
        self.StatusBar.SetStatusWidths([w1, -1])
        righttext = wx.StaticText(
            self.StatusBar, wx.ID_ANY, label=_("Messages")
        )
        righttext.SetPosition((w1 + 2, 2))
        righttext.Bind(wx.EVT_LEFT_DOWN, self.OpenLogWind)

    def PlaceMenu(self):
        # Menu Bar
        self.menubar = MenuBar()
        self.menubar.SetParent(self)

        ## File
        self.menubar.AddMenu(_("&File"), [
            (wx.ID_NEW, None, None, self.notebook.AddTab, None),
            (wx.ID_OPEN, None, None, self.notebook.fileops.openfile_dlg, None),
            (wx.ID_ANY, _("Open directory\tCtrl+Shift+D"), None, self.OpenDir, None),
            (wx.ID_ANY, _("Close all tabs"), None, lambda evt: (self.notebook.DeleteAllPages(), self.notebook.AddTab()), None),
            (None, None, None, None, None), # Separator
            (wx.ID_SAVE, None, None, self.notebook.fileops.savefile_dlg, None),
            (wx.ID_SAVEAS, _("Save as...\tCtrl+Shift+S"), None, self.notebook.fileops.saveas, None),
            (None, None, None, None, None),
            (wx.ID_EXIT, _("Quit\tAlt+F4"), None, self.OnClose, None)
        ])

        ## Edit
        self.menubar.AddMenu(_("&Edit"), [
            (wx.ID_COPY, None, None, lambda evt: self.notebook.text_editor.Copy, None),
            (wx.ID_PASTE, None, None, lambda evt: self.notebook.text_editor.Paste, None),
            (wx.ID_CUT, None, None, lambda evt: self.notebook.text_editor.Cut, None),
            (None, None, None, None, None),
            (wx.ID_SELECTALL, None, None, lambda evt: self.notebook.text_editor.SelectAll, None),
            (wx.ID_DELETE, _("Delete\tDelete"), None, lambda evt: self.notebook.text_editor.DeleteBack, None),
            (None, None, None, None, None),
            (wx.ID_ANY, _("Auto save"), _("Configure auto-saving file function"), lambda evt: self.notebook.autosv.askwind, None),
        ])
        for menu, name in self.menubar.GetMenus():
            if name == _("&Edit"):
                if global_settings.get_setting("extensions.cmd", "enable") in cfg.yes_value or [True]:
                    item = menu.Append(wx.ID_ANY, _("Command prompt"))
                    self.Bind(wx.EVT_MENU, self.OpenCmd, item)

        ## View
        self.menubar.AddMenu(_("&View"), [
            (wx.ID_ZOOM_IN, _("Zoom it\tCtrl++"), None, lambda evt: self.notebook.text_editor.ZoomIn, None),
            (wx.ID_ZOOM_OUT, _("Zoom out\tCtrl+-"), None, lambda evt: self.notebook.text_editor.ZoomIn, None),
            (wx.ID_ANY, _("Word wrap"), None, lambda evt: print("not implemented yet"), wx.ITEM_CHECK), # Not completed
        ])

        ## Configs
        self.menubar.AddMenu(_("&Configs"), [
            (wx.ID_ANY, _("Show all configurations"), None, self.ShowCfgs, None),
            (wx.ID_ANY, _("Reset all configs"), None, self.ResetCfgs, None),
        ])

        ## Help
        self.menubar.AddMenu(_("&Help"), [
            (wx.ID_ABOUT, None, None, self.ShowAbout, None),
            (wx.ID_HELP, None, None, lambda evt: webbrowser.open_new_tab("https://lebao3105.gitbook.io/texteditor_doc"), None)
        ])
        self.SetMenuBar(self.menubar)

    def OnClose(self, evt):
        if hasattr(self.notebook.autosv, "fm"):
            try:
                self.notebook.autosv.fm.Close()
            except RuntimeError:
                pass
            self.notebook.autosv.shown = False
        evt.Skip()

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
            lambda evt: self.notebook.fileops.openfile(dirs.GetFilePath())
        )
        dirs.Show()
        self.sidebar.RegisterTab(selected_dir, dirs)
        self.sidebar.Show()
    
    def OpenLogWind(self, evt):
        def onwindowclose(evt):
            self.islogwindopen = False
            logwind.fm.Destroy()

        if self.islogwindopen == True:
            return

        logwind = LogsWindow(log.logs, self)
        logwind.fm.Bind(wx.EVT_CLOSE, onwindowclose)

        logwind.Show()
        self.islogwindopen = True

    def OpenCmd(self, evt):
        wind = wx.Frame(self)
        wind.SetTitle(_("Command Window"))
        wind.SetSize((600, 400))
        wind.CreateStatusBar(2)
        notebook = cmd.Tabb(wind)
        notebook.setstatus = True
        wind.Show()

    def ShowCfgs(self, evt):
        if not self.notebook.text_editor.IsEmpty():
            self.notebook.AddTab()
        self.notebook.fileops.openfile(get_config.file)

    def ResetCfgs(self, evt):
        ask = wx.MessageDialog(
            None,
            _("Are you sure want to reset all configurations?"),
            _("Confirm configs reset"),
            wx.YES_NO | wx.ICON_WARNING,
        ).ShowModal()
        if ask == wx.ID_YES:
            if cfg.reset():
                currst = self.StatusBar.GetStatusText()
                self.SetStatusText(_("Restored all default app configurations."))
                time.sleep(1)
                self.SetStatusText(currst)

    def ShowAbout(self, evt):
        wxver = wx.__version__
        pyver = platform.python_version()
        ostype = platform.system() if platform.system() != "" or None else _("Unknown")
        msg = _(
        f"""\
        A simple, cross-platform text editor.
        Branch: {"DEV" if is_development_build() == True else "STABLE"}
        wxPython version: {wxver}
        Python verison: {pyver}
        OS type: {ostype}
        """
        )
        license = \
        """
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License   
        along with this program.  If not, see <https://www.gnu.org/licenses/>.
        """

        aboutinf = wx.adv.AboutDialogInfo()
        aboutinf.SetName("TextWorker")
        aboutinf.SetVersion(textworker.__version__)
        aboutinf.SetIcon(wx.Icon(textworker.icon))
        aboutinf.SetDescription(msg)
        aboutinf.SetCopyright("(C) 2022-2023 Le Bao Nguyen")
        aboutinf.SetWebSite("https://github.com/lebao3105/texteditor")
        aboutinf.SetLicence(license)
        aboutinf.AddDeveloper("Le Bao Nguyen")
        return wx.adv.AboutBox(aboutinf)


class LogsWindow:
    def __init__(self, logs: list[str], parent=None):
        """Logs window - use wx.Frame
        :param logs (list) : All logs
        :param parent=None : Parent of the frame

        Objects:
        * fm : Main frame
        * label1, label2 : Message text
        * text : Log object

        Press F5 to refresh the log window.
        """

        self._curridx: int = 0
        self._istexthere: bool = False
        self.logs = logs

        self.fm = wx.Frame(parent, title="Logs")

        panel = wx.Panel(self.fm, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label1 = wx.StaticText(
            panel, wx.ID_ANY, _("No new message collected."), style=wx.TE_READONLY
        )
        sizer.Add(self.label1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 52, wx.EXPAND)

        self.label2 = wx.StaticText(
            panel, wx.ID_ANY, _("Press F5 to refresh."), style=wx.TE_READONLY
        )
        sizer.Add(self.label2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0, wx.EXPAND)

        self.text = TextWidget(
            panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.EXPAND
        )
        self.text.Hide()

        for item in [self.label1, self.label2, self.fm]:
            cfg.configure(item)

        self.label1.SetFont(
            cfg._get_font().MakeBold()
        )

        self.label1.SetFont(
            cfg._get_font().MakeUnderlined()
        )
        
        panel.SetSizerAndFit(sizer)
        self.fm.Bind(wx.EVT_CHAR_HOOK, self.onkeypressed)
        self.refresh()

        self.fm.Layout()

    def onkeypressed(self, evt):
        key = evt.GetKeyCode()
        if key == wx.WXK_F5:
            self.refresh()
            print('hello')
        else:
            evt.Skip()

    def refresh(self):
        if self._istexthere == False and self.logs:
            self.text.Show()
            for i in range(self._curridx, len(self.logs)):
                self.text.AppendText(self.logs[i] + "\n")
            self._curridx = len(self.logs)
            self._istexthere = True
        else:
            self.text.Hide()
            self.label1.SetLabelText(_("No new message collected."))
            self.label2.SetLabelText(_("Press F5 to refresh."))
            self._istexthere = False

    def Show(self, show: bool = True):
        """Show the window."""
        return self.fm.Show(show)