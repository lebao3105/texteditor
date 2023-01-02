import tkinter.ttk as ttk
import texteditor
from tkinter import BooleanVar, Menu, Text
from texteditor.backend import get_config, logger


class TextWidget(Text):
    """Tkinter Text widget with scrollbars & right-click menu placed by default.\n
    Configurations for the menu:\n
    |-> enableMenu: bool : Enable (default) Menu or not\n
    |-> useUnRedo: bool : Use Undo/Redo in the menu, also make this class able to use them\n
    |-> useWrap : bool : Add wrap button to the menu\n
    |-> enableStatusBar : bool : Add a status bar"""

    enableMenu: bool = True
    useUnRedo: bool = False
    useWrap: bool = False

    def __init__(
        self,
        parent,
        _=None,
        useMenu: bool = None,
        useUnRedo: bool = None,
        addWrap: bool = None,
        useScrollbars: bool = None,
        enableStatusBar: bool = None,
        **kw
    ):
        super().__init__(parent, **kw)

        self.master = parent
        self.wrapbtn = BooleanVar(self)
        self.wrapbtn.set(True)

        if useMenu != None:
            self.enableMenu = useMenu
        if useUnRedo != None:
            self.useUnRedo = useUnRedo
        if addWrap != None:
            self.useWrap = addWrap

        if _ is None:
            self._ = texteditor._
        else:
            self._ = _

        if self.enableMenu is True:
            self.RMenu = Menu(self, tearoff=0)
            self.__menu_init()
            self.bind("<Button-3>", lambda event: self.__open_menu(event))
        if enableStatusBar is True:
            self.statusbar = logger.StatusBar(self, self._)
        if useScrollbars is True:
            self.__place_scrollbar()

        # Do some customization
        self.configure(wrap="word")
        get_config.GetConfig.configure(self)

    # Place scrollbars
    def __place_scrollbar(self):
        xbar = ttk.Scrollbar(self, orient="horizontal", command=self.xview)
        ybar = ttk.Scrollbar(self, orient="vertical", command=self.yview)
        xbar.pack(side="bottom", fill="x")
        ybar.pack(side="right", fill="y")

    # Right click menu
    # Initialize the rightclick menu.
    # By the default we will place Copy, Cut & Paste.
    def __menu_init(self):
        addcmd = self.RMenu.add_command
        root = self.master
        addcmd(
            label=self._("Cut"),
            accelerator="Ctrl+X",
            command=lambda: root.event_generate("<Control-x>"),
        )
        addcmd(
            label=self._("Copy"),
            accelerator="Ctrl+C",
            command=lambda: root.event_generate("<Control-c>"),
        )
        addcmd(
            label=self._("Paste"),
            accelerator="Ctrl+V",
            command=lambda: root.event_generate("<Control-v>"),
        )
        # Wrap button is temporary disabled because
        # texteditor.mainwindow now uses wrapbtn function,
        # and our wrapbtn variable doesnot fit with the
        # mainwindow's one (I need to rename the function)
        """if self.useWrap == True:
            self.RMenu.add_separator()
            self.RMenu.add_checkbutton(
                label=self._("Wrap (by word)"),
                accelerator="Ctrl+W",
                command=lambda: self.wrapmode(self),
                variable=self.wrapbtn,
            )"""
        if self.useUnRedo == True:
            self.RMenu.add_separator()
            addcmd(
                label=self._("Undo"),
                accelerator="Ctrl+Z",
                command=lambda: root.event_generate("<Control-z>"),
            )
            addcmd(
                label=self._("Redo"),
                accelerator="Ctrl+Y",
                command=lambda: root.event_generate("<Control-y>"),
            )
            self.configure(undo=True)

    def __open_menu(self, event=None):
        try:
            self.RMenu.post(event.x_root, event.y_root)
        finally:
            self.RMenu.grab_release()

    # Add commands
    def addMenucmd(self, label: str, acc: str = None, fn: object = None, **kw):
        return self.RMenu.add_command(label=label, accelerator=acc, command=fn, **kw)

    def addMenusepr(self):
        return self.RMenu.add_separator()

    def addMenucheckbtn(
        self, label: str, variable: BooleanVar, fn: object, acc: str = None, **kw
    ):
        return self.RMenu.add_checkbutton(
            label=label, accelerator=acc, variable=variable, command=fn, **kw
        )

    def addMenuradiobtn(
        self, label: str, variable: BooleanVar, fn: object, acc: str = None, **kw
    ):
        return self.RMenu.add_radiobutton(
            label=label, accelerator=acc, variable=variable, command=fn, **kw
        )

    def addMenucascade(self, label: str, menu: Menu, **kw):
        return self.RMenu.add_cascade(label=label, menu=menu, **kw)

    # @staticmethod
    def wrapmode(self, event=None):
        if self.wrapbtn.get() == True:
            self.configure(wrap="none")
            self.statusbar.writeleftmessage(
                "Disabled wrapping on the text widget.")
        else:
            self.configure(wrap="word")
            self.statusbar.writeleftmessage(
                "Enabled wrapping on the text widget")
