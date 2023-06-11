import os
from tkinter.ttk import Notebook
import typing

from tkinter import Misc
from tkinter.filedialog import *
from tkinter.messagebox import *

from .extensions.autosave import AutoSave
from .extensions.generic import global_settings

searchdir = global_settings.get("editor", "searchdir") or os.path.expanduser(
    "~/Documents"
)


class FileOperations:
    """
    The extended texteditor.tabs + libtextworker's Tkinter editor
        with (auto)save and text modify-detect functions
    """

    NoteBook: Misc | Notebook
    AutoSave: bool = True

    SetWindowTitleFn: typing.Callable
    NewTabFn: typing.Callable
    NewTabFn_Args: dict | None = None

    # File touch
    def LoadFile(self, path: str):
        tabname = self.NoteBook.tab("current", "text")

        if (
            os.path.isfile(tabname.removesuffix(_(" (Duplicated)")))
            or self.NoteBook.select().editor.Modified
        ):
            if self.NewTabFn_Args is not None:
                self.NewTabFn(**self.NewTabFn_Args)
            else:
                self.NewTabFn()

        self.NoteBook.nametowidget(self.NoteBook.select()).editor.insert(
            1.0, open(path, "r").read()
        )

    def SaveFile(self, path: str):
        return open(path, "w").write(
            self.NoteBook.nametowidget(self.NoteBook.select()).editor.get(1.0, "end")
        )

    # GUI-side functions
    def OpenFileDialog(self, evt=None):
        return self.LoadFile(
            askopenfilename(
                initialdir=searchdir,
                parent=self.NoteBook,
                title=_("Open a file to continue"),
            )
        )

    def SaveFileEvent(self, evt=None):
        tabname = self.NoteBook.tab("current", "text")
        if not os.path.isfile(tabname):
            return self.SaveAs()
        else:
            return self.SaveFile(tabname)

    def SaveAs(self, evt=None):
        return self.SaveFile(
            asksaveasfilename(
                confirmoverwrite=True,
                initialdir=searchdir,
                parent=self.NoteBook,
                title=_("Save this file as..."),
            )
        )

    def OnEditorModified(self, evt):
        self.NoteBook.nametowidget(self.NoteBook.select()).editor.Modified = True
        # Nothing else

    def InitEditor(self):
        currtab = self.NoteBook.select()
        self.NoteBook.nametowidget(currtab).editor.Modified: bool = False
        self.NoteBook.nametowidget(currtab).editor.bind(
            "<<Modified>>", self.OnEditorModified
        )

    def AutoSaveSetup(self):
        if self.AutoSave:
            for fm in self.NoteBook.tabs():
                obj = AutoSave(
                    self.NoteBook.nametowidget(fm).editor, self.SaveFileEvent
                )
                # obj.start() # Not this time
