from tkinter import Frame, Menu, END
from tkinter.messagebox import askyesnocancel
from tkinter.ttk import Notebook, Scrollbar
from texteditor.backend import constants, file_operations
from libtextworker.interface.tk.editor import TextWidget
from libtextworker.interface.tk.miscs import CreateMenu


class TabsViewer(Notebook):
    def __init__(self, master, do_place: bool, newtablabel: str = None, **kw):
        super().__init__(master, **kw)
        self.parent = master
        if newtablabel == None:
            self.newtablabel = _("Untitled")
        else:
            self.newtablabel = newtablabel

        self.fileops = file_operations.FileOperations()

        # Add an initial tab
        self.add_tab()

        self.fileops.Editor = self.parent.text_editor
        self.fileops.NewTabFunc = self.add_tab
        self.fileops.NewTabFunc_Args = {"idx": "default"}

        # A tab but it's used to add a new tab
        # Idea from StackOverflow.. I don't know there was something like this
        dummy = Frame()
        self.add(dummy, text="+")

        # Tab name
        self.tabname = self.tab(self.select(), "text")

        # Now, make a right-click menu
        self.right_click_menu = CreateMenu(
            [
                (
                    _("New tab"),
                    "Ctrl+N",
                    lambda: self.add_tab(idx="default"),
                    None,
                    None,
                ),
                (
                    _("Close the current tab"),
                    "",
                    lambda: self.close_tab(self),
                    None,
                    None,
                ),
                (
                    _("Duplicate the current opening tab"),
                    "",
                    self.duplicate_tab,
                    None,
                    None,
                ),
                (_("Reopen the file"), "", lambda: self.reopenfile(self), None, None),
            ]
        )
        self.bind(
            "<Button-3>",
            lambda event: self.right_click_menu.post(event.x_root, event.y_root),
        )
        self.bind("<<NotebookTabChanged>>", lambda evt: self.tab_changed)

        # Place the notebook, if you want
        if do_place is True:
            self.pack(expand=True, fill="both")

    def add_right_click_command(
        self, label: str = None, fn: object = None, acc: str = None
    ):
        return self.right_click_menu.add_command(label, fn, acc)

    def add_tab(self, event=None, idx=None):
        newtab_name = self.newtablabel

        # Add a new tab
        textframe = Frame(self)
        if isinstance(idx, int):
            self.insert(idx, textframe, text=newtab_name)
        elif idx == "default":
            self.insert(len(self.tabs()) - 1, textframe, text=newtab_name)
        else:
            self.add(textframe, text=newtab_name)

        # Add contents
        self.parent.text_editor = TextWidget(textframe)

        ## Right-click menu
        self.parent.text_editor.addMenusepr()
        self.parent.text_editor.addMenucmd(
            label=_("Save"),
            acc="Ctrl+S",
            fn=lambda: self.fileops.SaveFileEvent,
        )
        self.parent.text_editor.addMenucmd(
            label=_("Save as"),
            acc="Ctrl+Shift+S",
            fn=self.fileops.SaveAs,
        )
        self.parent.text_editor.bind("<KeyRelease>", self.__bindkey)
        self.parent.text_editor.pack(expand=True, fill="both")

        # Post setup
        self.select(textframe)
        self.parent.text_editor.focus()

        if self.parent.winfo_class() == "Tk" or "TopLevel":
            self.parent.title(newtab_name)

    def __bindkey(self, event=None):
        textw = self.parent.text_editor
        textw.statusbar.keypress()
        tabname = self.tab(self.select(), "text")
        if not tabname.endswith(" *"):
            self.tab("current", text=tabname + " *")
            if self.parent.winfo_class() == "Tk" or "TopLevel":
                self.parent.title(tabname + " *")

    def close_tab(self, event=None):
        # This function won't work if the first tab is not selected
        tabname = self.tab(self.select(), "text")
        if tabname.endswith(" *"):
            result = askyesnocancel(
                title=_("Tab close"),
                message=_("The content of this tab is modified. Save it?"),
                icon="info",
            )
            if result == True:
                self.fileops.savefile(self.parent)
                self.forget(self.select())
            elif result == None:
                return
            else:
                self.forget(self.select())
        else:
            self.forget(self.select())

    def tab_changed(self, event):
        if self.select() == self.tabs()[-1]:
            self.add_tab(idx=(len(self.tabs()) - 1))
        tabname = event.widget.tab("current")["text"]
        # Check if the tab name is + (new tab button)
        if tabname == "+":
            self.add_tab(idx=(len(self.tabs())))
        if self.parent.winfo_class() == "Tk":
            self.parent.title(tabname)

    def duplicate_tab(self, event=None):
        content = self.parent.text_editor.get(1.0, END)
        tabname = self.tab(self.select(), "text")

        self.add_tab(idx="default")
        self.parent.text_editor.insert(1.0, content)
        self.tab("current", text=tabname + _(" (Duplicated)"))

    def reopenfile(self, event=None):
        filename = self.tab(self.select(), "text")
        if filename not in constants.FILES_ARR:
            self.parent.text_editor.statusbar.writeleftmessage(
                _("Cannot reopen this tab because it opens no file.")
            )
            return  # Whetever we can reload the tab content
        else:
            with open(filename, "r") as f:
                print("Opening file: ", filename)
                self.parent.text_editor.insert(1.0, f.read())
                self.parent.title(filename)
                self.tab("current", text=filename)
