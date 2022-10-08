# Import modules
import os
from tkinter import *
from tkinter import messagebox
from texteditor import tabs
import texteditor
from texteditor.extensions import autosave, cmd, finding
from texteditor.miscs import file_operations, get_config, textwidget


class MainWindow(Tk):
    """The main application class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ = texteditor._

        # Set icon
        if os.path.isfile(texteditor.icon):
            self.iconphoto(False, PhotoImage(file=texteditor.icon))
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
        self.autocolor = BooleanVar()
        self.autocolor.set(False)

        # Window title and size
        self.title(self._("Text editor"))
        self.geometry("810x610")

        # Place widgets then handle events
        self.autosv = autosave.AutoSave(self)
        self.notebook = tabs.TabsViewer(self, do_place=True)
        self.place_menu()
        self.add_event()

    def place_menu(self):
        # Menu bar
        self.menu_bar = Menu(self)
        ## File
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        addfilecmd = self.file_menu.add_command
        addfilecmd(
            label=self._("New"),
            command=lambda: self.add_tab(self),
            accelerator="Ctrl+N",
        )
        addfilecmd(
            label=self._("Open"),
            command=lambda: file_operations.open_file(self),
            accelerator="Ctrl+O",
        )
        addfilecmd(
            label=self._("Save"),
            command=lambda: file_operations.save_file(self),
            accelerator="Ctrl+S",
        )
        addfilecmd(
            label=self._("Save as"),
            command=lambda: file_operations.save_as(self),
            accelerator="Ctrl+Shift+S",
        )
        self.file_menu.add_separator()
        addfilecmd(label=self._("Exit"), accelerator="Alt+F4")
        self.menu_bar.add_cascade(label=self._("File"), menu=self.file_menu)

        ## Edit
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        addeditcmd = self.edit_menu.add_command
        addeditcmd(label=self._("Undo"), accelerator="Ctrl+Z")
        addeditcmd(label=self._("Redo"), accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        addeditcmd(label=self._("Cut"), accelerator="Ctrl+X")
        addeditcmd(label=self._("Copy"), accelerator="Ctrl+C")
        addeditcmd(label=self._("Paste"), accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        addeditcmd(label=self._("Select all"), accelerator="Ctrl+A")
        if get_config.GetConfig.getvalue("filemgr", "autosave") == "yes":
            addeditcmd(
                label=self._("Autosave"),
                command=lambda: self.autosv.openpopup(),
            )

        if get_config.GetConfig.getvalue("cmd", "isenabled") == "yes":
            self.edit_menu.add_separator()
            addeditcmd(
                label=self._("Open System Shell"),
                command=lambda: cmd.CommandPrompt(self),
                accelerator="Ctrl+T",
            )

        self.menu_bar.add_cascade(label=self._("Editing"), menu=self.edit_menu)

        ## Find & Replace
        self.find_menu = Menu(self.menu_bar, tearoff=0)
        addfindcmd = self.find_menu.add_command
        addfindcmd(
            label=self._("Find"),
            command=lambda: finding.Finder(self, "find"),
            accelerator="Ctrl+F",
        )
        addfindcmd(
            label=self._("Replace"),
            command=lambda: finding.Finder(self, ""),
            accelerator="Ctrl+R",
        )
        self.menu_bar.add_cascade(label=self._("Find"), menu=self.find_menu)

        ## Config
        self.config_menu = Menu(self.menu_bar, tearoff=0)
        addcfgcmd = self.config_menu.add_command
        addcfgcmd(
            label=self._("Open configuration file"), command=lambda: self.opencfg(self)
        )
        addcfgcmd(
            label=self._("Reset configurations"), command=lambda: self.resetcfg(self)
        )
        addcfgcmd(
            label=self._("Toggle %s mode") % self.lb,
            command=lambda: self.change_color(self),
        )
        self.config_menu.add_checkbutton(
            label=self._("Auto change the color"),
            command=lambda: self.autocolor_mode(self),
            variable=self.autocolor,
        )
        # This should be added to View menu in the future
        self.config_menu.add_checkbutton(
            label=self._("Wrap (by word)"),
            command=lambda: textwidget.TextWidget.wrapmode(self),
            variable=self.wrapbtn,
            accelerator="Ctrl+W",
        )
        self.menu_bar.add_cascade(label=self._("Config"), menu=self.config_menu)
        # Add menu to the application
        self.config(menu=self.menu_bar)

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
            "Warning",
            "This will reset ALL configurations you have ever made. Continue?",
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
            else:
                msgbox.showinfo(
                    self._("Completed"),
                    self._(
                        "Completed resetting texteditor configurations.\nRestart the application to take effect."
                    ),
                )
                self.lb == "dark"
                self.config_menu.entryconfig(2, "Toggle %s mode" % self.lb)

    def opencfg(self, event=None):
        self.add_tab()
        file_operations.openfilename(self, get_config.file)

    def change_color(self, event=None):
        """Change theme color of the application. Restart the entrie application is needed."""
        try:
            get_config.GetConfig.change_config("global", "color", self.lb)
        finally:
            self.config_menu.delete(2)
            messagebox.showinfo(
                "Restart required",
                "The application theme is changed. Please restart this app to take effect.",
            )

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
            self.config_menu.entryconfig(2, state="normal")
            get_config.GetConfig.configure(self.text_editor)
        else:
            get_config.autocolormode = True
            self.config_menu.entryconfig(2, state="disabled")
            get_config.GetConfig.configure(self.text_editor)
