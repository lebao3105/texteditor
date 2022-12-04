import tkinter.ttk as ttk
import gettext
from tkinter import BooleanVar, Menu, Text
from texteditor.backend import file_operations, get_config


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
    enableStatusBar: bool = True

    def __init__(
        self,
        parent,
        _=None,
        useMenu: bool = None,
        useUnRedo: bool = None,
        addWrap: bool = None,
        enableStatusBar: bool = None,
        **kw
    ):
        super().__init__(parent, **kw)

        self.__place_scrollbar()
        self.master = parent
        self.wrapbtn = BooleanVar(self)
        self.wrapbtn.set(True)

        if useMenu != None:
            self.enableMenu = useMenu
        if useUnRedo != None:
            self.useUnRedo = useUnRedo
        if addWrap != None:
            self.useWrap = addWrap
        if enableStatusBar != None:
            self.enableStatusBar = enableStatusBar

        if _ is None:
            self._ = gettext.gettext
        else:
            self._ = _

        if self.enableMenu is True:
            self.RMenu = Menu(self, tearoff=0)
            self.__menu_init()
            self.bind(
                "<Button-3>", lambda event: self.__open_menu(event)
            )
        if self.enableStatusBar is True:
            self.statusbar = StatusBar(self, self._)

        # Do some customization
        self.configure(
            wrap="word"
        )  # This is enabled by the default in this application
        get_config.GetConfig.configure(self)

    # Place scrollbars
    def __place_scrollbar(self):
        xbar = ttk.Scrollbar(self, orient="horizontal", command=self.xview)
        ybar = ttk.Scrollbar(self, orient="vertical", command=self.yview)
        xbar.pack(side="bottom", fill="x")
        ybar.pack(side="right", fill="y")

    ## Right click menu
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
        if self.useWrap == True:
            self.RMenu.add_separator()
            self.RMenu.add_checkbutton(
                label=self._("Wrap (by word)"),
                accelerator="Ctrl+W",
                command=lambda: self.wrapmode(self),
                variable=self.wrapbtn,
            )
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
        file_operations.find_text_editor(self)
        # Find the button first:)
        if not hasattr(self, "wrapbtn"):
            print("Couldn't find Wrap mode button!")
            return
        if self.wrapbtn.get() == True:
            self.text_editor.configure(wrap="word")
            self.statusbar.writeleftmessage("Enabled wrapping on the text widget")
        else:
            self.text_editor.configure(wrap="none")
            self.statusbar.writeleftmessage("Disabled wrapping on the text widget.")


class StatusBar(ttk.Frame):

    def __init__(self, parent, _=None, bindsignal:bool=None, **kwargs):
        super().__init__(master=parent, **kwargs)

        if _ is None:
            self._ = gettext.gettext
        else:
            self._ = _

        self.lefttext = ttk.Label(self)
        self.righttext = ttk.Label(self)
        self.lefttext.configure(state="readonly")
        self.righttext.configure(state="readonly")
        
        if bindsignal is True:
            self.righttext.bind("<KeyRelease>", self.keypress)
        
        self.lefttext.pack(side="left")
        self.righttext.pack(side="right")

        get_config.GetConfig.configure(self)
        get_config.GetConfig.configure(self.lefttext)
        get_config.GetConfig.configure(self.righttext)

        self.textw = parent
        self.keypress()
        self.writeleftmessage(self._("No new message."))

        self.pack(side="bottom", fill="x")

    def keypress(self, event=None):
        row, col = self.textw.index("insert").split(".")
        self.righttext.config(text=self._("Line %s : Col %s") % (str(row), str(col)))

    def writeleftmessage(self, message:str, event=None):
        self.lefttext.config(text=message) # TODO: Collect all messages then clear this box after a period
