import platform
import texteditor
import webbrowser
import wx
import wx.adv

from texteditor.tabs import Tabber
from texteditor.backend import logger, constants, get_config

log = logger.Logger("texteditor.mainwindow")
cfg = get_config.GetConfig(get_config.cfg, get_config.file)


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((820, 685))
        self.SetIcon(wx.Icon(texteditor.icon))

        self.notebook = Tabber(self, wx.ID_ANY)
        self.menuitem = {}
        self._StatusBar()

        tabname = self.notebook.GetPageText(self.notebook.GetSelection())
        self.SetTitle(_("Texteditor - %s") % tabname)
        self.SetStatusText(tabname)

        self.PlaceMenu()
        self.Binder()
        self.Layout()

    def _StatusBar(self):
        self.statusbar = self.CreateStatusBar(2)
        w1 = self.statusbar.Size[0] - 50
        self.statusbar.SetStatusWidths([w1, -1])
        self.statusbar.righttext = wx.StaticText(
            self.statusbar, wx.ID_ANY, label="Messages"
        )
        self.statusbar.righttext.SetPosition((w1 + 2, 2))
        self.statusbar.righttext.Bind(wx.EVT_LEFT_DOWN, lambda evt: log.logwindow())

    def PlaceMenu(self):
        # Menu Bar
        self.menubar = wx.MenuBar()

        ## File
        filemenu = wx.Menu()
        addfilecmd = filemenu.Append
        self.menuitem["newtab"] = addfilecmd(wx.ID_NEW, _("New\tCtrl-N"))
        self.menuitem["open"] = addfilecmd(wx.ID_OPEN, _("Open\tCtrl-O"))
        self.menuitem["save"] = addfilecmd(wx.ID_SAVE, _("Save\tCtrl-S"))
        self.menuitem["saveas"] = addfilecmd(
            wx.ID_SAVEAS, _("Save as...\tCtrl-Shift-S")
        )
        self.exitItem = addfilecmd(wx.ID_EXIT)
        self.menubar.Append(filemenu, _("&File"))

        ## Edit
        editmenu = wx.Menu()
        addeditcmd = editmenu.Append
        self.menuitem["copy"] = addeditcmd(wx.ID_ANY, _("Copy\tCtrl-C"))
        self.menuitem["paste"] = addeditcmd(wx.ID_ANY, _("Paste\tCtrl-V"))
        self.menuitem["cut"] = addeditcmd(wx.ID_ANY, _("Cut\tCtrl-X"))
        editmenu.AppendSeparator()
        self.menuitem["selall"] = addeditcmd(wx.ID_ANY, _("Select All\tCtrl-A"))
        self.menuitem["autosv"] = addeditcmd(
            wx.ID_ANY, _("AutoSave"), _("Configure auto-save preferences")
        )
        self.menubar.Append(editmenu, _("&Edit"))

        ## Help
        helpmenu = wx.Menu()
        self.aboutItem = helpmenu.Append(wx.ID_ABOUT)
        self.helpItem = helpmenu.Append(
            wx.ID_ANY, "Help", "Read documents and visit the source code"
        )
        self.menubar.Append(helpmenu, _("&Help"))
        self.SetMenuBar(self.menubar)

    ## Callbacks
    def Binder(self):
        self.menucommand = {
            self.menuitem["newtab"]: lambda evt: self.notebook.AddTab(),
            self.menuitem["open"]: lambda evt: (
                self.notebook.text_editor.fileops.openfile_(),
                self.notebook.OnPageChanged(),
            ),
            self.menuitem[
                "save"
            ]: lambda evt: self.notebook.text_editor.fileops.savefile_(),
            self.menuitem[
                "saveas"
            ]: lambda evt: self.notebook.text_editor.fileops.saveas(),
            self.menuitem["copy"]: lambda evt: self.notebook.text_editor.Copy(),
            self.menuitem["paste"]: lambda evt: self.notebook.text_editor.Paste(),
            self.menuitem["cut"]: lambda evt: self.notebook.text_editor.Cut(),
            self.menuitem["selall"]: lambda evt: self.notebook.text_editor.SelectAll(),
        }
        self.Bind(wx.EVT_MENU, self.Quit, self.exitItem)
        self.Bind(wx.EVT_MENU, self.ShowAbout, self.aboutItem)
        self.Bind(
            wx.EVT_MENU,
            lambda evt: webbrowser.open_new_tab(
                "https://github.com/lebao3105/texteditor"
            ),
            self.helpItem,
        )
        for item in self.menucommand:
            self.Bind(wx.EVT_MENU, self.menucommand[item], item)

    def Quit(self, event):
        self.Close(True)

    def ShowAbout(self, event):
        wxver = wx.__version__
        pyver = platform.python_version()
        ostype = platform.system() if platform.system() != "" or None else _("Unknown")
        msg = _(
            f"""\
        A simple, cross-platform text editor.
        Branch: {constants.STATE}
        wxPython version: {wxver}
        Python verison: {pyver}
        OS type: {ostype}
        """
        )
        license = """\
        This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

        aboutinf = wx.adv.AboutDialogInfo()
        aboutinf.SetName("texteditor")
        aboutinf.SetVersion("1.6 Alpha (wx version)")
        aboutinf.SetIcon(wx.Icon(texteditor.icon))
        aboutinf.SetDescription(msg)
        aboutinf.SetCopyright("(C) 2022-2023")
        aboutinf.SetWebSite("https://github.com/lebao3105/texteditor")
        aboutinf.SetLicence(license)
        aboutinf.AddDeveloper(_("Le Bao Nguyen"))
        return wx.adv.AboutBox(aboutinf)


class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame)
        frame.Show()
        return True
