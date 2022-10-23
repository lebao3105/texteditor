# Import modules
import os
import pygubu
from tkinter import *

import texteditor
from .tabs import TabsViewer
from .extensions import autosave, cmd, finding
from .miscs import file_operations, get_config, textwidget
from .views import about


class MainWindow(Tk):
    """The main application class."""

    def __init__(self, _=None, **kwargs):
        super().__init__(**kwargs)

        if _ == None:
            self._ = texteditor._
        else:
            self._ = _

        # Configure ALL menu items callbacks
        self.callbacks = {
            "openfile": lambda: file_operations.open_file(self),
            "add_tab": lambda: self.add_tab(),
            "savefile": lambda: file_operations.save_file(self),
            "savefileas": lambda: file_operations.save_as(self),
            "gofind": lambda: finding.Finder(self, "find"),
            "goreplace": lambda: finding.Finder(self, ""),
            "destroy": lambda: self.destroy(),
            "opencfg": lambda: self.opencfg(),
            "resetcfg": lambda: self.resetcfg(),
            "change_color": lambda: self.change_color(),
            "autocolor_mode": lambda: self.autocolor_mode(),
            "set_wrap": lambda: textwidget.TextWidget.wrapmode(self),
            "aboutdlg": lambda: self.aboutdlg(),
        }

        # Set icon
        if os.path.isfile(texteditor.icon):
            self.wm_iconphoto(False, PhotoImage(file=texteditor.icon))
        else:
            print("Warning: Application icon", texteditor.icon, "not found!")

        # Get color mode
        if get_config.GetConfig.getvalue("global", "color") == "dark":
            self.lb = "light"
        else:
            self.lb = "dark"

        # Wrap button
        self.wrapbtn = BooleanVar()
        self.wrapbtn.set(True)
        # Auto change color
        self.autocolor = BooleanVar
        self.wrapbtn.set(False)

        # Window title and size
        self.title(self._("Text editor"))
        self.geometry("810x610")

        # Place widgets then handle events
        self.autosv = autosave.AutoSave(self, self._)
        self.load_ui()
        self.add_event()

    def load_ui(self):
        """Loads the "menu bar" defined from a .ui file,
        then place other widgets."""
        viewsdir = texteditor.currdir / "views"
        builder = pygubu.Builder(self._)
        # Load the menu bar
        builder.add_resource_path(texteditor.currdir)
        builder.add_resource_path(viewsdir)
        builder.add_from_file(viewsdir / "menubar.ui")
        builder.import_variables(self, ["autocolor", "wrapbtn"])
        # Get objects
        self.fm = builder.get_object("fm", self)
        self.menu2 = builder.get_object("menu2", self)
        self.menu3 = builder.get_object("menu3", self)
        # Add menu items
        addeditcmd = self.menu2.add_command
        if get_config.GetConfig.getvalue("filemgr", "autosave") == "yes":
            addeditcmd(
                label=self._("Autosave"),
                command=lambda: self.autosv.openpopup(),
            )

        if get_config.GetConfig.getvalue("cmd", "isenabled") == "yes":
            self.menu2.add_separator()
            addeditcmd(
                label=self._("Open System Shell"),
                command=lambda: cmd.CommandPrompt(self),
                accelerator="Ctrl+T",
            )
        self.menu3.entryconfig(2, label=self._("Toggle %s mode") % self.lb)
        # Do stuff
        self.fm.rowconfigure(0, weight=1)
        self.fm.columnconfigure(0, weight=1)
        self.notebook = TabsViewer(self, do_place=True)
        builder.connect_callbacks(self.callbacks)

    # Binding commands to the application
    def add_event(self):
        bindcfg = self.bind
        bindcfg("<Control-n>", lambda event: self.add_tab(self))
        if get_config.GetConfig.getvalue("cmd", "isenabled") == "yes":
            bindcfg("<Control-t>", lambda event: cmd.CommandPrompt(self))
        bindcfg("<Control-f>", lambda event: finding.Finder(self, "find"))
        bindcfg("<Control-r>", lambda event: finding.Finder(self, ""))
        bindcfg("<Control-Shift-S>", lambda event: file_operations.save_as(self))
        bindcfg("<Control-s>", lambda event: file_operations.save_file(self))
        bindcfg("<Control-o>", lambda event: file_operations.open_file(self))
        bindcfg("<Control-w>", lambda event: self.set_wrap(self))

    # Functions for the Menu bar
    def resetcfg(self, event=None):
        import tkinter.messagebox as msgbox

        message = msgbox.askyesno(
            self._("Warning"),
            self._("This will reset ALL configurations you have ever made. Continue?"),
        )
        if message:
            check = get_config.GetConfig.reset()
            if not check:
                msgbox.showerror(
                    self._("Error occured!"),
                    self._(
                        "Unable to reset configuration file: Backed up default variables not found"
                    ),
                )
                return
            else:
                msgbox.showinfo(
                    self._("Completed"),
                    self._(
                        "Completed resetting texteditor configurations.\nRestart the application to take effect."
                    ),
                )
                self.setcolorvar()

    def opencfg(self, event=None):
        self.add_tab()
        file_operations.openfilename(self, get_config.file)

    def aboutdlg(self, event=None):
        about.AboutDialog().run()

    def change_color(self, event=None):
        get_config.GetConfig.change_config("global", "color", self.lb)
        get_config.GetConfig.configure(self.text_editor)
        self.setcolorvar()

    # Set wrap mode (keyboard shortcut)
    # It is different from the textwidget's default function. A lot.
    def set_wrap(self, event=None):
        if self.wrapbtn.get() == True:
            self.text_editor.configure(wrap="none")
            self.wrapbtn.set(False)
            print("Disabled wrapping on the text widget.")
        else:
            self.text_editor.configure(wrap="word")
            self.wrapbtn.set(True)
            print("Enabled wrapping on the text widget.")

    def add_tab(self, event=None):
        return self.notebook.add_tab(idx="default")

    def autocolor_mode(self, event=None):
        if self.autocolor.get() is False:
            get_config.autocolormode = False
            get_config.AutoColor.stopasync()
            get_config.GetConfig.configure(self.text_editor)
            tel = False
        else:
            get_config.autocolormode = True
            get_config.GetConfig.configure(self.text_editor)
            tel = True
        self.setcolorvar()
        if tel is True:
            self.menu3.entryconfig(2, state="disabled")
        else:
            self.menu3.entryconfig(2, state="normal")

    def setcolorvar(self):
        theme = get_config.sv_ttk.get_theme()
        if theme == "dark":
            self.lb = "light"
        else:
            self.lb = "dark"
        self.menu3.entryconfig(2, label="Toggle %s mode" % self.lb)
