import os
import pygubu
import webbrowser

from typing import NoReturn
from tkinter import messagebox as msgbox
from tkinter import Tk, BooleanVar, PhotoImage, TclError, Menu

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

        # Set the application icon
        if os.path.isfile(texteditor.icon) and CAIRO_AVAILABLE:
            svg2png(open(texteditor.icon, "r").read(), write_to="./icon.png")
            try:
                self.wm_iconphoto(False, PhotoImage(file="./icon.png"))
            except TclError:
                self.log.exception("Unable to set application icon", "TCLError occured")

        # BooleanVar_s
        self.wrapbtn = BooleanVar(value=global_settings.getkey("editor.autosave", "enable") in global_settings.yes_values)  # Wrap button
        self.autocolor = BooleanVar(value=clrcall.getkey("color", "autocolor") in clrcall.yes_values)  # Auto change color

        self.get_color()
        self.load_ui()
        self.add_event()

    def load_ui(self):
        """Load the "menu bar" defined from a .ui file,
        then place other widgets."""

        viewsdir = texteditor.currdir / "views"
        builder = pygubu.Builder(_)

        menu = Menu(self)
        self.config(menu=menu)

        ## Read all menus
        builder.add_resource_path(texteditor.currdir)
        builder.add_resource_path(viewsdir)
        builder.add_from_file(viewsdir / "menubar.ui")

        self.menu1 = builder.get_object("menu1", self)
        self.menu2 = builder.get_object("menu2", self)
        self.menu3 = builder.get_object("menu3", self)
        self.menu4 = builder.get_object("menu4", self)

        ## Add menus to the main one
        menu.add_cascade(menu=self.menu1, label=_("File"))
        menu.add_cascade(menu=self.menu2, label=_("Edit"))
        menu.add_cascade(menu=self.menu3, label=_("Config"))
        menu.add_cascade(menu=self.menu4, label="?")

        ## Do stuff
        self.callbacks["openfile"] = lambda: self.notebook.fileops.OpenFileDialog()
        self.callbacks["savefile"] = lambda: self.notebook.fileops.SaveFileEvent()
        self.callbacks["savefileas"] = lambda: self.notebook.fileops.SaveAs()
        builder.connect_callbacks(self.callbacks)

        self.notebook = TabsViewer(self, do_place=True)
        self.autosv = autosave.AutoSaveConfig(self)
        self.autosv.ShowWind()

    # Bind commands to the application
    def add_event(self):
        bindcfg = self.bind
        bindcfg("<Control-n>", lambda event: self.add_tab(self))
        bindcfg("<Control-f>", lambda event: finding.Finder(self, "find"))
        bindcfg("<Control-r>", lambda event: finding.Finder(self, ""))
        bindcfg("<Control-Shift-S>", lambda event: self.notebook.fileops.SaveAs())
        bindcfg("<Control-s>", self.notebook.fileops.SaveFileEvent)
        bindcfg("<Control-o>", self.notebook.fileops.OpenFileDialog)
        bindcfg("<Control-w>", lambda event: self.text_editor.wrapmode())

    # Menu bar callbacks
    def resetcfg(self, event=None) -> False | NoReturn:
        message = msgbox.askyesno(
            _("Warning"),
            _("This will reset ALL configurations you have ever made. Continue?"),
        )
        if message:
            try:
                ResetEveryConfig()
            except:
                msgbox.showerror(
                    _("Error occured!"),
                    _(
                        "Unable to reset configuration file: Backed up default variables not found"
                    ),
                )
                return False

    def opencfg(self, event=None):
        self.add_tab()
        self.notebook.fileops.LoadFile(generic.CONFIGS_PATH)

    def get_color(self):
        if clrcall.getkey("color", "background") == "dark":
            self.lb = "light"
        else:
            self.lb = "dark"
        clrcall.configure(self, True)

    def change_color(self, event=None):
        if self.autocolor.get() == True:
            if msgbox.askyesno(
                _("Warning"),
                _(
                    """\
                Changing the application color requires the autocolor function to be turned off.
                Don't worry, this change is only for this session.
                """
                ),
            ):
                self.toggle_autocolor()
            else:
                return
        clrcall.set("color", "background", self.lb)
        clrcall.update()
        self.get_color()

    def add_tab(self, event=None):
        return self.notebook.add_tab(idx="default")

    def toggle_autocolor(self, event=None, permanent: bool = False):
        toggle = self.autocolor.get()
        clrcall.threads = {}
        if toggle == True:
            if permanent:
                clrcall.set_and_update("color", "autocolor", "no")
        elif toggle == False:
            if permanent:
                clrcall.set_and_update("color", "autocolor", "yes")
        self.get_color()

    def toggle_wrap(self, event=None):
        toggle = self.wrapbtn.get()
        if toggle:
            self.notebook.nametowidget(self.notebook.select()).editor.configure("word")
        else:
            self.notebook.nametowidget(self.notebook.select()).editor.configure("none")