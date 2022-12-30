import platform
import texteditor
import webbrowser
import wx

from .tabs import Tabber
from .backend import logger, constants

log = logger.Logger('texteditor.mainwindow')

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((820, 685))
        self.SetIcon(wx.Icon(texteditor.icon))

        self.notebook = Tabber(self, wx.ID_ANY)
        self.menuitem = {}
        self.SetTitle(_("Texteditor - %s") % self.notebook.GetPageText(self.notebook.GetSelection()))
        self.PlaceMenu()
        self.Binder()
        self.Layout()
    
    def PlaceMenu(self):
        # Menu Bar
        self.menubar = wx.MenuBar()

        ## File
        filemenu = wx.Menu()
        addfilecmd = filemenu.Append
        self.menuitem["newtab"] = addfilecmd(wx.ID_NEW, _("New\tCtrl-N"))
        self.menuitem["open"] = addfilecmd(wx.ID_OPEN, _("Open\tCtrl-O"))
        self.menuitem["save"] = addfilecmd(wx.ID_SAVE, _("Save\tCtrl-S"))
        self.menuitem["saveas"] = addfilecmd(wx.ID_SAVEAS, _("Save as...\tCtrl-Shift-S"))
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
        self.menuitem["autosv"] = addeditcmd(wx.ID_ANY, _("AutoSave"), _("Configure auto-save preferences"))
        self.menubar.Append(editmenu, _("&Edit"))

        ## Help
        helpmenu = wx.Menu()
        self.aboutItem = helpmenu.Append(wx.ID_ABOUT)
        self.helpItem = helpmenu.Append(wx.ID_ANY, "Help", "Read documents and visit the source code")
        self.menubar.Append(helpmenu, _("&Help"))
        self.SetMenuBar(self.menubar)


        self.statusbar = self.CreateStatusBar(1)
        self.statusbar.SetStatusWidths([-1])
        self.SetStatusText(self.notebook.GetPageText(self.notebook.GetSelection()))

    
        ## Callbacks
    def Binder(self):
        self.menucommand = {
            self.menuitem["newtab"]: lambda evt: self.notebook.AddTab(),
            self.menuitem["open"]: lambda evt: (self.notebook.text_editor.fileops.openfile_(), self.notebook.OnPageChanged()),
            self.menuitem["save"]: lambda evt: self.notebook.text_editor.fileops.savefile_(),
            self.menuitem["saveas"]: lambda evt: self.notebook.text_editor.fileops.saveas(),
            self.menuitem["copy"]: lambda evt: self.notebook.text_editor.Copy(),
            self.menuitem["paste"]: lambda evt: self.notebook.text_editor.Paste(),
            self.menuitem["cut"]: lambda evt: self.notebook.text_editor.Cut(),
            self.menuitem["selall"]: lambda evt: self.notebook.text_editor.SelectAll(),
        }
        self.Bind(wx.EVT_MENU, self.Quit, self.exitItem)
        self.Bind(wx.EVT_MENU, self.ShowAbout, self.aboutItem)
        self.Bind(wx.EVT_MENU, lambda evt: webbrowser.open_new_tab("https://github.com/lebao3105/texteditor"), self.helpItem)
        for item in self.menucommand:
            self.Bind(wx.EVT_MENU, self.menucommand[item], item)
    
    def Quit(self, event):
        self.Close(True)
    
    def ShowAbout(self, event):
        wxver = wx.__version__
        pyver = platform.python_version()
        ostype = platform.system() if platform.system() != '' or None else _("Unknown")
        msg = _(f'''texteditor 1.6 Alpha (wx version)
A simple, cross-platform text editor.
Branch: {constants.STATE}
wxPython version: {wxver}
Python version: {pyver}
OS type: {ostype}''')
        return wx.MessageBox(
            message=msg,
            caption=_("About this app"),
            style=wx.OK|wx.ICON_INFORMATION
        )

class MyApp(wx.App):

    def OnInit(self):
        frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame)
        frame.Show()
        return True
