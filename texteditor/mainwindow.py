import os
import pygubu
import webbrowser

from typing import NoReturn
from tkinter import messagebox as msgbox
from tkinter import Tk, PhotoImage, TclError, Menu

try:
    from cairosvg import svg2png
except ImportError:
    CAIRO_AVAILABLE = False
else:
    CAIRO_AVAILABLE = True

import texteditor
from .tabs import TabsViewer
from .extensions import autosave, finding, generic
from .extensions.generic import clrcall, global_settings
from .views import about

from libtextworker.general import logger, ResetEveryConfig

logger.UseGUIToolKit("tk")


class MainWindow(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("810x610")

        # Set the application icon
        if os.path.isfile(texteditor.icon) and CAIRO_AVAILABLE:
            svg2png(open(texteditor.icon, "r").read(), write_to="./icon.png")
            try:
                self.wm_iconphoto(False, PhotoImage(file="./icon.png"))
            except TclError:
                self.log.exception("Unable to set application icon", "TCLError occured")

        # Build the UI
        self.builder = pygubu.Builder(_)
        self.builder.add_from_file(texteditor.currdir / "views" / "menubar.ui")

        self.notebook = TabsViewer(self, do_place=True)
        self.autosv = autosave.AutoSaveConfig(self)

        self.GetColor()
        self.LoadMenu()
        self.BindEvents()

        # BooleanVar_s
        self.wrapbtn = self.builder.get_variable("wrapbtn")
        self.autosave_local = self.builder.get_variable("autosave_local")
        self.autosave_global = self.builder.get_variable("autosave_global")

        if global_settings.getkey("editor.autosave", "enable") in global_settings.yes_values:
            self.autosave_global.set(True)
            self.autosave_local.set(True)

    def LoadMenu(self):

        # Configure some required menu items callback
        self.callbacks = {
            "add_tab": lambda: self.add_tab(),
            "gofind": lambda: finding.Finder(self, "find"),
            "goreplace": lambda: finding.Finder(self, ""),
            "toggle_autocolor": lambda: self.toggle_autocolor(),
            "toggle_wrap": lambda: self.toggle_wrap(),
            "destroy": lambda: self.destroy(),
            "opencfg": lambda: self.opencfg(),
            "resetcfg": lambda: self.resetcfg(),
            "change_color": lambda: self.change_color(),
            "open_doc": lambda: webbrowser.open(
                "https://lebao3105.gitbook.io/texteditor_doc"
            ),
            "aboutdlg": lambda: about.AboutDialog(self).run(),
        }

        menu = Menu(self)
        self.config(menu=menu)

        ## Get all menus
        self.menu1 = self.builder.get_object("menu1", self)
        self.menu2 = self.builder.get_object("menu2", self)
        self.menu3 = self.builder.get_object("menu3", self)
        self.menu4 = self.builder.get_object("menu4", self)

        ## Add menus to the main one
        menu.add_cascade(menu=self.menu1, label=_("File"))
        menu.add_cascade(menu=self.menu2, label=_("Edit"))
        menu.add_cascade(menu=self.menu3, label=_("Config"))
        menu.add_cascade(menu=self.menu4, label=_("Help"))

        ## Do stuff
        self.callbacks["openfile"] = lambda: self.notebook.fileops.OpenFileDialog()
        self.callbacks["savefile"] = lambda: self.notebook.fileops.SaveFileEvent()
        self.callbacks["savefileas"] = lambda: self.notebook.fileops.SaveAs()
        self.builder.connect_callbacks(self.callbacks)

        self.autosv.ShowWind()

    def BindEvents(self):
        bindcfg = self.bind
        bindcfg("<Control-n>", lambda event: self.add_tab(self))
        bindcfg("<Control-f>", lambda event: finding.Finder(self, "find"))
        bindcfg("<Control-r>", lambda event: finding.Finder(self, ""))
        bindcfg("<Control-Shift-S>", lambda event: self.notebook.fileops.SaveAs())
        bindcfg("<Control-s>", self.notebook.fileops.SaveFileEvent)
        bindcfg("<Control-o>", self.notebook.fileops.OpenFileDialog)
        bindcfg("<Control-w>", lambda event: self.text_editor.wrapmode())

    # Menu bar callbacks
    def resetcfg(self, event=None) -> NoReturn:
        if msgbox.askyesno(
            _("Warning"),
            _("This will reset ALL configurations you have ever made. Continue?"),
        ):
            ResetEveryConfig()

    def opencfg(self, event=None):
        self.add_tab()
        self.notebook.fileops.LoadFile(generic.CONFIGS_PATH)

    def GetColor(self):
        if clrcall.getkey("color", "background") == "dark":
            self.lb = "light"
        else:
            self.lb = "dark"
        clrcall.configure(self, True)

    def change_color(self, event=None):
        if self.autocolor.get() == True:
            if not msgbox.askyesno(
                _("Warning"),
                _(
                    """\
                Changing the application color requires the autocolor function to be turned off.
                Don't worry, this change is only for this session.
                """
                ),
            ):
                return
        clrcall.set("color", "background", self.lb)
        clrcall.set("color", "autocolor", "no")
        self.GetColor()

    def add_tab(self, event=None):
        return self.notebook.add_tab(idx="default")

    def toggle_wrap(self, event=None):
        toggle = self.wrapbtn.get()
        if toggle:
            self.notebook.nametowidget(self.notebook.select()).editor.configure("word")
        else:
            self.notebook.nametowidget(self.notebook.select()).editor.configure("none")