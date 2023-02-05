import platform
import textworker
import webbrowser
import wx
import wx.adv
import wx.stc

from .textwidget import TextWidget
from .generic import global_settings, log
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
        self.Binder()
        self.Layout()

    def _StatusBar(self):
        self.statusbar = self.CreateStatusBar(2)
        w1 = self.statusbar.Size[0] - 50
        self.statusbar.SetStatusWidths([w1, -1])
        self.statusbar.righttext = wx.StaticText(
            self.statusbar, wx.ID_ANY, label=_("Messages")
        )
        self.statusbar.righttext.SetPosition((w1 + 2, 2))
        self.statusbar.righttext.Bind(wx.EVT_LEFT_DOWN, self.OpenLogWind)

    def PlaceMenu(self):
        # Menu Bar
        self.menubar = wx.MenuBar()

        ## File
        filemenu = wx.Menu()
        addfilecmd = filemenu.Append
        self.menuitem["newtab"] = addfilecmd(wx.ID_NEW)
        self.menuitem["open"] = addfilecmd(wx.ID_OPEN)
        self.menuitem["opendir"] = addfilecmd(wx.ID_ANY, _("Open directory"))
        self.menuitem["closeall"] = addfilecmd(wx.ID_ANY, _("Close all..."))
        filemenu.AppendSeparator()
        self.menuitem["save"] = addfilecmd(wx.ID_SAVE)
        self.menuitem["saveas"] = addfilecmd(wx.ID_SAVEAS)
        filemenu.AppendSeparator()
        self.exitItem = addfilecmd(wx.ID_EXIT)
        self.menubar.Append(filemenu, _("&File"))

        ## Edit
        editmenu = wx.Menu()
        addeditcmd = editmenu.Append
        self.menuitem["copy"] = addeditcmd(wx.ID_COPY)
        self.menuitem["paste"] = addeditcmd(wx.ID_PASTE)
        self.menuitem["cut"] = addeditcmd(wx.ID_CUT)
        editmenu.AppendSeparator()
        self.menuitem["selall"] = addeditcmd(wx.ID_SELECTALL)
        editmenu.AppendSeparator()
        self.menuitem["autosv"] = addeditcmd(
            wx.ID_ANY, _("AutoSave"), _("Configure auto-saving file function")
        )
        if global_settings.get_setting("extensions.cmd", "enable") in cfg.yes_value or [True]:
            self.menuitem["cmd"] = addeditcmd(wx.ID_ANY, _("Command prompt"))
        self.menubar.Append(editmenu, _("&Edit"))

        ## Views
        viewsmenu = wx.Menu()
        addviewscmd = viewsmenu.Append
        self.menuitem["zoomin"] = addviewscmd(wx.ID_ZOOM_IN)
        self.menuitem["zoomout"] = addviewscmd(wx.ID_ZOOM_OUT)
        self.menuitem["wrap"] = viewsmenu.AppendCheckItem(wx.ID_ANY, _("Word wrap"))
        self.menubar.Append(viewsmenu, _("&View"))

        ## Configs
        cfgmenu = wx.Menu()
        addcfgmenu = cfgmenu.Append
        self.menuitem["showcfgs"] = addcfgmenu(wx.ID_ANY, _("Show all configurations"))
        self.menuitem["reset"] = addcfgmenu(wx.ID_ANY, _("Reset all configs"))
        self.menubar.Append(cfgmenu, _("&Config"))

        ## Help
        helpmenu = wx.Menu()
        self.menuitem["about"] = helpmenu.Append(wx.ID_ABOUT)
        self.menuitem["help"] = helpmenu.Append(wx.ID_HELP)
        self.menubar.Append(helpmenu, _("&Help"))

        self.SetMenuBar(self.menubar)

    ## Callbacks
    def Binder(self):
        self.menucommand = {
            self.menuitem["newtab"]: lambda evt: self.notebook.AddTab(),
            self.menuitem["open"]: lambda evt: (
                self.notebook.fileops.openfile_dlg(),
                self.notebook.OnPageChanged(evt),
            ),
            self.menuitem["opendir"]: lambda evt: self.OpenDir(),
            self.menuitem["closeall"]: lambda evt: (
                self.notebook.DeleteAllPages(),
                self.notebook.AddTab(),
            ),
            self.menuitem[
                "save"
            ]: lambda evt: self.notebook.fileops.savefile_dlg(),
            self.menuitem[
                "saveas"
            ]: lambda evt: self.notebook.fileops.saveas(),
            self.menuitem["copy"]: lambda evt: self.notebook.text_editor.Copy(),
            self.menuitem["paste"]: lambda evt: self.notebook.text_editor.Paste(),
            self.menuitem["cut"]: lambda evt: self.notebook.text_editor.Cut(),
            self.menuitem["autosv"]: lambda evt: self.notebook.autosv.askwind(),
            self.menuitem["zoomin"]: lambda evt: self.notebook.text_editor.ZoomIn(),
            self.menuitem["zoomout"]: lambda evt: self.notebook.text_editor.ZoomOut(),
            self.menuitem["selall"]: lambda evt: self.notebook.text_editor.SelectAll(),
            self.menuitem["showcfgs"]: lambda evt: self.ShowCfgs(),
            self.menuitem["reset"]: lambda evt: self.ResetCfgs(),
            self.menuitem["about"]: lambda evt: self.ShowAbout(),
            self.menuitem["help"]: lambda evt: webbrowser.open_new_tab(
                "https://lebao3105.gitbook.io/texteditor_doc"
            ),
        }

        if global_settings.get_setting("extensions.cmd", "enable") in cfg.yes_value or [True]:
            self.menucommand[self.menuitem["cmd"]] = lambda evt: self.OpenCmd()

        self.Bind(wx.EVT_MENU, self.OnClose, self.exitItem)
        
        for item in self.menucommand:
            self.Bind(wx.EVT_MENU, self.menucommand[item], item)

    def OnClose(self, evt):
        if hasattr(self.notebook.autosv, "fm"):
            try:
                self.notebook.autosv.fm.Close()
            except RuntimeError:
                pass
            self.notebook.autosv.shown = False
        evt.Skip()

    def OpenDir(self):
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

        logwind = LogsWindow(log.logs)
        logwind.fm.Bind(wx.EVT_CLOSE, onwindowclose)

        logwind.Show()
        self.islogwindopen = True

    def OpenCmd(self):
        wind = wx.Frame(self)
        wind.SetTitle(_("Command Window"))
        wind.SetSize((600, 400))
        wind.CreateStatusBar(2)
        notebook = cmd.Tabb(wind)
        notebook.setstatus = True
        wind.Show()

    def ShowCfgs(self):
        if not self.notebook.text_editor.IsEmpty():
            self.notebook.AddTab()
        self.notebook.fileops.openfile(get_config.file)

    def ResetCfgs(self):
        ask = wx.MessageDialog(
            None,
            _("Are you sure want to reset all configurations?"),
            _("Confirm configs reset"),
            wx.YES_NO | wx.ICON_WARNING,
        ).ShowModal()
        if ask == wx.ID_YES:
            if cfg.reset():
                self.SetStatusText(_("Restored all default app configurations."))

    def ShowAbout(self):
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

        Press F5 to refresh the log window (not tested.)
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
        self.label1.SetFont(
            wx.Font(
                14,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                0,
                "",
            )
        )
        sizer.Add(self.label1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 52, wx.EXPAND)

        self.label2 = wx.StaticText(
            panel, wx.ID_ANY, _("Press F5 to refresh."), style=wx.TE_READONLY
        )
        self.label2.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                1,
                "",
            )
        )
        sizer.Add(self.label2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0, wx.EXPAND)

        self.text = TextWidget(
            panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.EXPAND
        )
        self.text.Hide()

        for item in [self.label1, self.label2, self.fm]:
            cfg.configure(item)
        
        panel.SetSizerAndFit(sizer)
        self.fm.Bind(wx.EVT_CHAR_HOOK, self.onkeypressed)
        self.refresh()

        self.fm.Layout()

    def onkeypressed(self, evt):
        key = evt.GetKeyCode()
        if key == wx.WXK_F5:
            self.refresh()
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