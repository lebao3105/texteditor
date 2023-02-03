# Import modules
import os
import webbrowser
import pygubu
import tkinter.messagebox as msgbox
from tkinter import *

import texteditor
from .tabs import TabsViewer
from .extensions import autosave, cmd, finding
from .backend import file_operations, get_config, logger
from .views import about


class MainWindow(Tk):
    """The main application class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

        self.notebook = TabsViewer(self, do_place=True)
        self.autosv = autosave.AutoSave(
            self, savefile_fn=lambda: self.notebook.fileops.savefile_()
        )
        self.log = logger.LoggerWithStatusbar(self.text_editor.statusbar, showlog=True)

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
        if get_config.GetConfig.getvalue("global", "autocolor") == "yes":
            self.autocolor.set(True)
        else:
            self.autocolor.set(False)

        self.autocolormode = get_config.AutoColor(self)

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
        if get_config.GetConfig.getvalue("filemgr", "autosave") == "yes":
            addeditcmd(
                label=_("Autosave"),
                command=lambda: self.autosv.openpopup(),
            )

        if get_config.GetConfig.getvalue("cmd", "isenabled") == "yes":
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
        self.callbacks["openfile"] = lambda: self.notebook.fileops.openfile_()
        self.callbacks["savefile"] = lambda: self.notebook.fileops.savefile_()
        self.callbacks["savefileas"] = lambda: self.notebook.fileops.saveas()
        builder.connect_callbacks(self.callbacks)

    # Binding commands to the application
    def add_event(self):
        bindcfg = self.bind
        bindcfg("<Control-n>", lambda event: self.add_tab(self))
        if get_config.GetConfig.getvalue("cmd", "isenabled") == "yes":
            bindcfg("<Control-t>", lambda event: cmd.CommandPrompt(self))
        bindcfg("<Control-f>", lambda event: finding.Finder(self, "find"))
        bindcfg("<Control-r>", lambda event: finding.Finder(self, ""))
        bindcfg("<Control-Shift-S>", lambda event: self.notebook.fileops.saveas())
        bindcfg("<Control-s>", lambda event: self.notebook.fileops.savefile_())
        bindcfg("<Control-o>", lambda event: self.notebook.fileops.openfile_())
        bindcfg("<Control-w>", lambda event: self.text_editor.wrapmode())

    # Menu bar callbacks
    def resetcfg(self, event=None):
        message = msgbox.askyesno(
            _("Warning"),
            _("This will reset ALL configurations you have ever made. Continue?"),
        )
        if message:
            check = get_config.GetConfig.reset()
            if not check:
                msgbox.showerror(
                    _("Error occured!"),
                    _(
                        "Unable to reset configuration file: Backed up default variables not found"
                    ),
                )
                self.text_editor.statusbar.writeleftmessage(
                    _("Error: Unable to reset all configurations!")
                )
                return
            else:
                msgbox.showinfo(
                    _("Completed"),
                    _(
                        "Resetted texteditor configurations.\nRestart the application to take effect."
                    ),
                )
                self.text_editor.statusbar.writeleftmessage(
                    _("Resetted all configurations. Restart the app to take effect.")
                )

    def opencfg(self, event=None):
        self.add_tab()
        file_operations.openfilename(self, get_config.file)

    def aboutdlg(self, event=None):
        return about.AboutDialog(self).run()

    def get_color(self):
        if get_config.GetConfig.getvalue("global", "color") == "dark":
            self.lb = "light"
        else:
            self.lb = "dark"

    def change_color(self, event=None):
        if self.autocolor.get() == True:
            if msgbox.askyesno(
                _("Warning"),
                _(
                    """\
                Changing the application color requires the autocolor function to be turned off.
                Turn off autocolor then change the application color (permanently)?
                """
                ),
            ):
                pass
            else:
                return
        get_config.GetConfig.change_config("global", "color", self.lb)
        self.get_color()
        get_config.GetConfig.configure(self.text_editor)

    def add_tab(self, event=None):
        return self.notebook.add_tab(idx="default")

    def autocolor_mode(self, event=None):
        get_config.autocolormode = self.autocolor.get()
        if self.autocolor.get() == False:
            self.autocolormode.stopasync()
            self.text_editor.statusbar.writeleftmessage(_("Stopped autocolor service."))
            self.menu3.entryconfig(2, state="disabled")
        else:
            self.autocolormode.startasync()
            self.text_editor.statusbar.writeleftmessage(_("Started autocolor service."))
            self.menu3.entryconfig(2, state="normal")
        get_config.GetConfig.configure(self.text_editor)
        self.get_color()
