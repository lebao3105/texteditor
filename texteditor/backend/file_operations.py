import os
import texteditor
import texteditor.backend
import typing

from tkinter import Text
from tkinter.filedialog import *
from tkinter.messagebox import *

searchdir = os.path.expanduser("~/Documents")

texteditor.backend.require_version("1.4a", ">=")
# texteditor.backend.require_version("1.6a", "<") # It doesn't work! Why?


class FileOperations:
    HasContentModified: bool = False
    Editor: object
    NewTabFunc: typing.Callable
    NewTabFunc_Args: typing.Any
    Parent: object

    def OpenFileDialog(self, evt=None):
        ask = askopenfilename(
            initialdir=searchdir, parent=self.Parent, title=_("Open a file")
        )
        if ask:
            return self.Load(ask)

    def LoadFile(self, filepath: str):
        if self.HasContentModified:
            self.NewTabFunc(self.NewTabFunc_Args)

        with open(filepath, "r") as f:
            self.Editor.insert("1.0", "end", filepath)

    def SaveFileEvent(self, evt=None):
        if not self.HasContentModified:
            self.SaveFile()
        self.SaveAs()

    def SaveFile(self):
        with open(self.Editor.FilePath, "w") as f:
            f.write(self.Editor.get("1.0", "end"))

    def SaveAs(self):
        ask = asksaveasfilename(initialdir=searchdir, parent=self.Parent)
        if ask:
            with open(ask, "w") as f:
                f.write(self.Editor.get("1.0", "end"))
