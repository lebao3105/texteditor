import logging
import os
import pygubu
import webbrowser
import tkinter.messagebox as msgbox
from tkinter import *

import texteditor
from .tabs import TabsViewer
from .extensions import autosave, cmd, finding, generic
from .views import about

global_settings = generic.global_settings
clrcall = generic.clrcall
logger = logging.getLogger("textworker")


class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure some required menu items callback
        self.callbacks = {
            "add_tab": lambda: self.add_tab(),
            "gofind": lambda: finding.Finder(self, "find"),
            "goreplace": lambda: finding.Finder(self, ""),
            "destroy": lambda: self.destroy(),
            "opencfg": lambda: self.opencfg(),
            "resetcfg": lambda: self.resetcfg(),
            "change_color": lambda: self.change_color(),
            "open_doc": lambda: webbrowser.open(
                "https://lebao3105.gitbook.io/texteditor_doc"
            ),
            "aboutdlg": lambda: self.aboutdlg(),
        }

        self.log = logger

        # Set icon
        if os.path.isfile(texteditor.icon):
            try:
                self.wm_iconphoto(False, PhotoImage(file=texteditor.icon))
            except TclError:
                self.log.throwerr("Unable to set application icon", "TCLError occured")
        else:
            self.log.throwwarn(
                "Warning: Application icon %s not found" % texteditor.icon
            )

        # Wrap button
        self.wrapbtn = BooleanVar(value=True)

        # Auto change color
        self.autocolor = BooleanVar()
        if clrcall.getkey("color", "autocolor") == "yes":
            self.autocolor.set(True)
        else:
            self.autocolor.set(False)

        # Window size
        self.geometry("810x610")

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

        ## Add "code-only" menu items
        addeditcmd = self.menu2.add_command
        if global_settings.call("editor.autosave", "enable") == "yes":
            addeditcmd(
                label=_("Autosave"),
                command=lambda: self.autosv.openpopup(),
            )

        if global_settings.call("extensions.cmd", "enable") == "yes":
            self.menu2.add_separator()
            addeditcmd(
                label=_("Open System Shell"),
                command=lambda: cmd.showcmd(self),
                accelerator="Ctrl+T",
            )
        self.menu3.add_checkbutton(
            label=_("Autocolor mode"),
            command=lambda: self.autocolor_mode(),
            variable=self.autocolor,
        )
        self.menu3.add_checkbutton(
            label=_("Word wrap"),
            command=lambda: self.text_editor.wrapmode(),
            variable=self.wrapbtn,
            accelerator="Ctrl+W",
        )

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
        self.autosv = autosave.AutoSave(
            self, savefile_fn=lambda: self.notebook.fileops.SaveFileEvent()
        )

    # Binding commands to the application
    def add_event(self):
        bindcfg = self.bind
        bindcfg("<Control-n>", lambda event: self.add_tab(self))
        if global_settings.call("extensions.cmd", "enable") == "yes":
            bindcfg("<Control-t>", lambda event: cmd.showcmd(self))
        bindcfg("<Control-f>", lambda event: finding.Finder(self, "find"))
        bindcfg("<Control-r>", lambda event: finding.Finder(self, ""))
        bindcfg("<Control-Shift-S>", lambda event: self.notebook.fileops.SaveAs())
        bindcfg("<Control-s>", self.notebook.fileops.SaveFileEvent)
        bindcfg("<Control-o>", self.notebook.fileops.OpenFileDialog)
        bindcfg("<Control-w>", lambda event: self.text_editor.wrapmode())

    # Menu bar callbacks
    def resetcfg(self, event=None):
        message = msgbox.askyesno(
            _("Warning"),
            _("This will reset ALL configurations you have ever made. Continue?"),
        )
        if message:
            check = global_settings.cfg.reset()
            if not check:
                msgbox.showerror(
                    _("Error occured!"),
                    _(
                        "Unable to reset configuration file: Backed up default variables not found"
                    ),
                )
                # self.text_editor.statusbar.writeleftmessage(
                #     _("Error: Unable to reset all configurations!")
                # )
                return
            else:
                msgbox.showinfo(
                    _("Completed"),
                    _(
                        "Resetted texteditor configurations.\nRestart the application to take effect."
                    ),
                )
                # self.text_editor.statusbar.writeleftmessage(
                #     _("Resetted all configurations. Restart the app to take effect.")
                # )

    def opencfg(self, event=None):
        self.add_tab()
        # self.notebook.fileops.LoadFile(get_config.file)

    def aboutdlg(self, event=None):
        return about.AboutDialog(self).run()

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
                self.autocolor_mode()
            else:
                return
        clrcall.set("color", "background", self.lb)
        clrcall.update()
        self.get_color()

    def add_tab(self, event=None):
        return self.notebook.add_tab(idx="default")

    def autocolor_mode(self, event=None, permanent: bool = False):
        toggle = self.autocolor.get()
        if toggle == True:
            del clrcall.threads
            if permanent:
                clrcall.set("color", "autocolor", "no")
                clrcall.update()
        elif toggle == False:
            print("turned 2")
            clrcall.threads = {}
            if permanent:
                clrcall.set("color", "autocolor", "yes")
                clrcall.update()
        self.get_color()
