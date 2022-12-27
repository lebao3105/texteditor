import texteditor
from tkinter import Frame, Menu, END
from tkinter.messagebox import askyesnocancel
from tkinter.ttk import Notebook, Scrollbar
from texteditor.backend import constants, file_operations, textwidget


class TabsViewer(Notebook):
    def __init__(self, master, do_place: bool, _=None, **kw):
        super().__init__(master, **kw)

        if _ is None:
            self._ = texteditor._
        else:
            self._ = _

        self.parent = master

        # A tab but it's used to add a new tab
        # Idea from StackOverflow.. I don't know there was something like this
        dummy = Frame()
        self.add(dummy, text="+")

        # Tab name
        self.tabname = self.tab(self.select(), "text")

        # Now, make a right-click menu
        self.right_click_menu = Menu(self, tearoff=0)
        self.right_click_menu.add_command(
            label=self._("New tab"),
            command=lambda: self.add_tab(idx="default"),
            accelerator="Ctrl+N",
        )
        self.right_click_menu.add_command(
            label=self._("Close the current opening tab"),
            command=lambda: self.close_tab(self),
        )
        self.right_click_menu.add_command(
            label=self._("Duplicate the current opening tab"),
            command=lambda: self.duplicate_tab(self),
        )
        self.right_click_menu.add_command(
            label=self._("Reopen the file"), command=lambda: self.reopenfile(self)
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

    def add_tab(self, event=None, idx=None):
        newtab_name = self._("Untitled")

        # Add a new tab
        textframe = Frame(self)
        if isinstance(idx, int):
            self.insert(idx, textframe, text=newtab_name)
        elif idx == "default":
            self.insert(len(self.tabs()) - 1, textframe, text=newtab_name)
        else:
            self.add(textframe, text=newtab_name)

        # Add contents
        self.parent.text_editor = textwidget.TextWidget(
            parent=textframe,
            _=self._,
            useMenu=True,
            useUnRedo=True,
            useScrollbars=False,
            enableStatusBar=True,
        )
        self.fileops = file_operations.FileOperations(
            textw=self.parent.text_editor,
            notebook=self,
            newtabfn=lambda: self.add_tab(idx="default"),
            statusbar=self.parent.text_editor.statusbar,
        )
        ## Scroll bars
        xbar = Scrollbar(
            textframe, orient="horizontal", command=self.parent.text_editor.xview
        )
        ybar = Scrollbar(
            textframe, orient="vertical", command=self.parent.text_editor.yview
        )
        xbar.pack(side="bottom", fill="x")
        ybar.pack(side="right", fill="y")
        ## Right-click menu
        self.parent.text_editor.addMenusepr()
        self.parent.text_editor.addMenucmd(
            label=self._("Save"),
            acc="Ctrl+S",
            fn=lambda: self.fileops.savefile_,
        )
        self.parent.text_editor.addMenucmd(
            label=self._("Save as"),
            acc="Ctrl+Shift+S",
            fn=self.fileops.saveas,
        )
        self.parent.text_editor.bind("<KeyRelease>", self.__bindkey)
        self.parent.text_editor.pack(expand=True, fill="both")

        # Post setup
        self.select(textframe)
        self.parent.text_editor.focus()

        if self.parent.winfo_class() == "Tk" or "TopLevel":
            window_title = self._("Text Editor") + " - "
            self.titletext = window_title + newtab_name
            self.parent.title(self.titletext)

    def __bindkey(self, event=None):
        textw = self.parent.text_editor
        textw.statusbar.keypress()
        tabname = self.tab(self.select(), "text")
        if not tabname.endswith(" *"):
            self.tab("current", text=tabname + " *")
            if self.parent.winfo_class() == "Tk" or "TopLevel":
                self.parent.title(self._("Text Editor") + " - " + tabname + " *")

    def close_tab(self, event=None):
        # This function won't work if the first tab is not selected
        tabname = self.tab(self.select(), "text")
        if tabname.endswith(" *"):
            result = askyesnocancel(
                title=self._("Tab close"),
                message=self._("The content of this tab is modified. Save it?"),
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
            self.add_tab(idx=(len(self.tabs())))  # Will this work?
        if self.parent.winfo_class() == "Tk":
            self.parent.title(self._("Text Editor") + " - " + tabname)

    def duplicate_tab(self, event=None):
        content = self.parent.text_editor.get(1.0, END)
        tabname = self.tab(self.select(), "text")

        self.add_tab(idx="default")
        self.parent.text_editor.insert(1.0, content)
        self.tab("current", text=tabname + self._(" (Duplicated)"))

    def reopenfile(self, event=None):
        filename = self.tab(self.select(), "text")
        if filename not in constants.FILES_ARR:
            self.parent.text_editor.statusbar.writeleftmessage(
                self._("Cannot reopen this tab because it opens no file.")
            )
            return  # Whether we can reload the tab content
        else:
            with open(filename, "r") as f:
                print("Opening file: ", filename)
                self.parent.text_editor.insert(1.0, f.read())
                self.parent.title(self._("Text editor") + " - " + filename)
                self.tab("current", text=filename)
