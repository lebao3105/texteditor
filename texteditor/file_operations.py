import os
import typing

from tkinter.filedialog import *
from tkinter.messagebox import *

from .extensions.generic import global_settings

searchdir = global_settings.get("editor", "searchdir") or os.path.expanduser("~/Documents")

class FileOperations:
    HasContentModified: bool = False
    Editor: object
    NewTabFunc: typing.Callable
    NewTabFunc_Args: typing.Any
    Parent: object

    def InitEditor(self):
        self.Editor.bind("<<Modified>>", self.OnTextModified)

    def OnTextModified(self, evt):
        self.HasContentModified = True
        # Nothing else

    def OpenFileDialog(self, evt=None):
        ask = askopenfilename(
            initialdir=searchdir, parent=self.Parent, title=_("Open a file")
        )
        if ask:
            return self.LoadFile(ask)

    def LoadFile(self, filepath: str):
        if self.HasContentModified:
            self.NewTabFunc(self.NewTabFunc_Args)

        with open(filepath, "r") as f:
            self.Editor.insert("1.0", filepath)

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
