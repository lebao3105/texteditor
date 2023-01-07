import tkinter.ttk as ttk
import texteditor
import texteditor.backend

from tkinter import BooleanVar, Menu, Text
from texteditor.backend import get_config, logger

texteditor.backend.require_version("1.4a", ">=")


class TextWidget(Text):
    enableMenu: bool = True
    unRedo: bool = False

    def __init__(
        self,
        parent,
        _=None,
        useMenu: bool = None,
        useScrollbars: bool = None,
        enableStatusBar: bool = None,
        unRedo: bool = False,
        **kwds
    ):
        """Customized Tkinter Text widget with a basic right-click menu.
        :param parent : Where to place this widget
        :param _=None : Translator, will remove in 1.5
        :param useMenu:bool=None : Enable right-click menu or not (default is true)
        :param unredo:bool=False : Undo Redo
        :param useScrollbars:bool=None : Use scrollbars (default is true)
        :param enableStatusBar:bool=None : Show a statusbar (default is false)
        :param **kwds : Other configurations (tkinter.Text)

        You can set TextWidget.wrapbtn to your own wrapbtn to use the wrap feature.
        The wrap function is wrapmode(event=None)."""
        super().__init__(parent, **kwds)

        self.master = parent
        self.wrapbtn = BooleanVar(self)
        self.wrapbtn.set(True)

        if useMenu != None:
            self.enableMenu = useMenu

        if _ is None:
            self._ = texteditor._
        else:
            self._ = _
        self.statusbar = logger.StatusBar(self, self._)

        if self.enableMenu is True:
            self.RMenu = Menu(self, tearoff=0)
            self._menu_init()
            self.bind("<Button-3>", lambda event: self._open_menu(event))

        if useScrollbars is True:
            self._place_scrollbar()

        if enableStatusBar is True:
            self.statusbar.pack(side="bottom", fill="x")

        self.unRedo = unRedo
        self.config(undo=self.unRedo)

        # Do some customization
        self.configure(wrap="word")
        get_config.GetConfig.configure(self)

    # Place scrollbars
    def _place_scrollbar(self):
        xbar = ttk.Scrollbar(self, orient="horizontal", command=self.xview)
        ybar = ttk.Scrollbar(self, orient="vertical", command=self.yview)
        xbar.pack(side="bottom", fill="x")
        ybar.pack(side="right", fill="y")

    # Right click menu
    def _menu_init(self):
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
        if self.unRedo:
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

    def _open_menu(self, event=None):
        try:
            self.RMenu.post(event.x_root, event.y_root)
        finally:
            self.RMenu.grab_release()

    # Add menu item commands
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

    # Wrap mode
    def wrapmode(self, event=None):
        if self.wrapbtn.get() == True:
            self.configure(wrap="none")
            self.wrapbtn.set(False)
            self.statusbar.writeleftmessage("Disabled wrapping on the text widget.")
        else:
            self.configure(wrap="word")
            self.wrapbtn.set(True)
            self.statusbar.writeleftmessage("Enabled wrapping on the text widget")
