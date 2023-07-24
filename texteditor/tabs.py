import os
from tkinter import END, Frame
from tkinter.messagebox import askyesnocancel
from tkinter.ttk import Notebook
from typing import Literal

from libtextworker.interface.tk.miscs import CreateMenu

from . import editor, file_operations
from .extensions.generic import _editor_config_load, _theme_load


class TabsViewer(Notebook):
    newtablabel: str = _("Untitled")

    def __init__(self, master, do_place: bool, *args, **kw):
        super().__init__(master, *args, **kw)

        # Setup FileOperations
        self.fileops = file_operations.FileOperations()
        self.fileops.NoteBook = self
        self.fileops.NewTabFn = self.add_tab
        self.fileops.NewTabFn_Args = {"idx": "default"}

        # Add an initial tab
        self.add_tab()

        # A tab but it's used to add a new tab
        # Idea from StackOverflow.. I don't know there was something like that
        dummy = Frame()
        self.add(dummy, text="+")

        # Now, make a right-click menu
        self.right_click_menu = CreateMenu(
            [
                (
                    _("New tab"),
                    "Ctrl+N",
                    lambda evt: self.add_tab(idx="default"),
                    None,
                    None,
                    None,
                    "normal",
                    None,
                ),
                (
                    _("Close the current tab"),
                    "",
                    lambda: self.close_tab(self),
                    None,
                    None,
                    None,
                    "normal",
                    None,
                ),
                (
                    _("Duplicate the current opening tab"),
                    "",
                    self.duplicate_tab,
                    None,
                    None,
                    None,
                    "normal",
                    None,
                ),
                (
                    _("Reopen the file"),
                    "",
                    lambda: self.reopenfile(self),
                    None,
                    None,
                    None,
                    "normal",
                    None,
                ),
            ]
        )
        self.bind(
            "<Button-3>",
            lambda event: self.right_click_menu.post(event.x_root, event.y_root),
        )
        self.bind("<<NotebookTabChanged>>", self.tab_changed)

        # Place the notebook, if you want
        if do_place is True:
            self.pack(expand=True, fill="both")

    def add_right_click_command(
        self, label: str = None, fn: object = None, acc: str = None
    ):
        return self.right_click_menu.add_command(label, fn, acc)

    def add_tab(
        self,
        event=None,
        idx: int | None | Literal["default"] = None,
        newtabtitle: str = newtablabel,
    ):
        neweditor = editor.Editor(self)
        neweditor.EditorInit(
            custom_config_path=_editor_config_load, custom_theme_path=_theme_load
        )
        neweditor.pack(expand=True, fill="both")

        if isinstance(idx, int):
            self.insert(idx, neweditor._frame, text=newtabtitle)
        elif idx == "default":
            self.insert(len(self.tabs()) - 1, neweditor._frame, text=newtabtitle)
        else:
            self.add(neweditor._frame, text=newtabtitle)

        self.select(neweditor._frame)
        self.fileops.InitEditor()
        neweditor.focus()
        self.nametitle(newtabtitle)

    def nametitle(self, title: str):
        if hasattr(self.master, "title"):
            self.master.title(title)

    def close_tab(self, event=None):
        tabname = self.tab(self.select(), "text")
        if tabname.endswith(" *"):
            result = askyesnocancel(
                title=_("Tab close"),
                message=_("The content of this tab is modified. Save it?"),
                icon="info",
            )
            if result is True:
                self.fileops.SaveFile(tabname.removesuffix(" *"))
            elif result is None:
                return
        self.forget(self.select())

    def tab_changed(self, event):
        # Check if by somehow we are in the last tab
        if self.select() == self.tabs()[-1]:
            self.add_tab(idx="default")

        tabname = event.widget.tab("current")["text"]

        # Check if the tab name is + (new tab button)
        if tabname == "+":
            self.add_tab(idx=len(self.tabs()))
            return

        self.nametitle(tabname)

    def duplicate_tab(self, event=None):
        content = self.nametowidget(self.select()).get(1.0, END)
        tabname = self.tab(self.select(), "text")

        self.add_tab(idx="default")
        self.nametowidget(self.select()).insert(1.0, content)
        self.tab("current", text=tabname + _(" (Duplicated)"))

    def reopenfile(self, event=None):
        filename = self.tab(self.select(), "text")
        if not os.path.isfile(filename):
            with open(filename, "r") as f:
                # print("Opening file: ", filename)
                self.nametowidget(self.select()).insert(1.0, f.read())
            self.nametitle(filename)
            self.tab("current", text=filename)
