import os
import typing

from hashlib import md5
from tkinter import Misc
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel
from tkinter.ttk import Notebook

from .extensions.generic import global_settings

searchdir = global_settings.get("editor", "searchdir")
if not os.path.isdir(searchdir):
    searchdir = os.path.expanduser("~/Documents")


class FileOperations:
    """
    The extended texteditor.tabs + libtextworker's Tkinter editor
        with text modify-detect function
    This time it's for internal use.
    """

    NoteBook: Misc | Notebook

    SetWindowTitleFn: typing.Callable
    NewTabFn: typing.Callable
    NewTabFn_Args: dict | None = None

    # File touch
    def LoadFile(self, path: str):
        tabname = self.NoteBook.tab("current", "text")

        if (
            os.path.isfile(tabname.removesuffix(_(" (Duplicated)")))
            or self.GetEditorFromCurrTab().Modified
        ):
            if self.NewTabFn_Args is not None:
                self.NewTabFn(**self.NewTabFn_Args)
            else:
                self.NewTabFn()

        self.GetEditorFromCurrTab().LoadFile(path)
        self.NoteBook.tab("current", text=path)

    # GUI-side functions
    def OpenFileDialog(self, evt=None):
        return self.GetEditorFromCurrTab().LoadFile(
            askopenfilename(
                initialdir=searchdir,
                parent=self.NoteBook,
                title=_("Open a file to continue"),
            )
        )

    def SaveFileEvent(self, evt=None):
        tabname = self.NoteBook.tab("current", "text")
        if not os.path.isfile(tabname):
            self.SaveAs()
        else:
            self.GetEditorFromCurrTab().SaveFile(tabname)

    def SaveAs(self, evt=None):
        return self.GetEditorFromCurrTab().SaveFile(
            asksaveasfilename(
                confirmoverwrite=True,
                initialdir=searchdir,
                parent=self.NoteBook,
                title=_("Save this file as..."),
            )
        )

    def OnEditorModify(self, evt):
        self.GetEditorFromCurrTab().Modified = True
        # Nothing else
    
    def OnEditorDestroy(self, evt):
        curreditor = self.GetEditorFromCurrTab()
        path = curreditor.FileLoaded if curreditor.FileLoaded else "this new file"
        if curreditor.Modified and curreditor.Hash.digest() != md5(curreditor.get(1.0, "end").encode("utf-8")).digest():
            ask = askyesnocancel(_("Not saved"),
                     _(f"Save {path}? It has unsaved changes."))
            if ask:
                if path != curreditor.FileLoaded:
                    self.SaveAs()
                else:
                    self.SaveFile(path)
            elif ask == None: return
        curreditor.destroy()
            
    def InitEditor(self):
        currtab = self.GetEditorFromCurrTab()
        currtab.Modified: bool = False
        currtab.bind("<<Modified>>", self.OnEditorModify)
        currtab.bind("<Destroy>", self.OnEditorDestroy)

    def GetEditorFromTab(self, tab) -> Misc:
        return self.NoteBook.nametowidget(tab).winfo_children()[0]

    def GetEditorFromCurrTab(self) -> Misc:
        return self.GetEditorFromTab(self.NoteBook.select())
