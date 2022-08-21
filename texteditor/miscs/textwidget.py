from tkinter import BooleanVar, Menu, Text
import tkinter.ttk as ttk
import gettext
import texteditor.miscs.file_operations as file_operations
_ = gettext.gettext

class TextWidget(Text):
    """Tkinter Text widget with scrollbars & right-click menu placed by default.\n
    Configurations for the menu:\n
    |-> Right click menu:\n
        |-> enableMenu: bool : Enable (default) Menu or not\n
        |-> useUnRedo: bool : Use Undo/Redo in the menu, also make this class able to use them\n
    |-> useWrap : Add wrap button into the menu"""
    enableMenu: bool = True
    useUnRedo: bool = False
    useWrap: bool = False

    def __init__(self, parent, useMenu:bool=None, useUnRedo:bool=None, addWrap:bool=None, **kw):
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

        if self.enableMenu == True:
            self.RMenu = Menu(self, tearoff=0)
            self.__menu_init()
            self.bind("<Button-3><ButtonRelease-3>", lambda event:self.__open_menu(event))
        
        # Whetever we still need to use wrap
        self.configure(wrap='word')
        self.share()

    # Place scrollbars
    def __place_scrollbar(self):
        xbar = ttk.Scrollbar(self, orient='horizontal', command=self.xview)
        ybar = ttk.Scrollbar(self, orient='vertical', command=self.yview)
        xbar.pack(side="bottom", fill="x")
        ybar.pack(side="right", fill="y")
    
    def share(self):
        return self.wrapbtn

    ## Right click menu
    # Initialize the rightclick menu.
    # By the default we will place Copy, Cut & Paste.
    def __menu_init(self):
        addcmd = self.RMenu.add_command
        root = self.master
        addcmd(label=_("Cut"), accelerator="Ctrl+X", command=lambda: root.event_generate("<Control-x>"))
        addcmd(label=_("Copy"), accelerator="Ctrl+C", command=lambda: root.event_generate("<Control-c>"))
        addcmd(label=_("Paste"), accelerator="Ctrl+V", command=lambda: root.event_generate("<Control-v>"))
        if self.useWrap == True:
            self.RMenu.add_separator()
            self.RMenu.add_checkbutton(label=_("Wrap (by word)"), accelerator="Ctrl+W", command=lambda: self.wrapmode(self), variable=self.wrapbtn)
        if self.useUnRedo == True:
            self.RMenu.add_separator()
            addcmd(label=_("Undo"), accelerator="Ctrl+Z", command=lambda: root.event_generate("<Control-z>"))
            addcmd(label=_("Redo"), accelerator="Ctrl+Y", command=lambda: root.event_generate("<Control-y>"))
            self.configure(undo=True)

    def __open_menu(self, event=None):
        try:
            self.RMenu.post(event.x_root, event.y_root)
        finally:
            self.RMenu.grab_release()
    
    # Add commands
    def addMenucmd(self, label:str, acc:str=None, fn:object=None, **kw):
        return self.RMenu.add_command(label=label, accelerator=acc, command=fn, **kw)
    
    def addMenusepr(self):
        return self.RMenu.add_separator()

    def addMenucheckbtn(self, label:str, variable:BooleanVar, fn:object, acc:str=None, **kw):
        return self.RMenu.add_checkbutton(label=label, accelerator=acc, variable=variable, command=fn, **kw)
    
    def addMenuradiobtn(self, label:str, variable:BooleanVar, fn:object, acc:str=None, **kw):
        return self.RMenu.add_radiobutton(label=label, accelerator=acc, variable=variable, command=fn, **kw)
    
    def addMenucascade(self, label:str, menu:Menu, **kw):
        return self.RMenu.add_cascade(label=label, menu=menu, **kw)
    
    #@staticmethod
    def wrapmode(self, event=None):
        file_operations.find_text_editor(self)
        # Find the button first:)
        if not hasattr(self, "wrapbtn"):
            print("Couldn't find Wrap mode button!")
        else: pass
        if self.wrapbtn.get() == True:
            self.text_editor.configure(wrap='word')
            print('Enabled wrapping on the text widget')
        else:
            self.text_editor.configure(wrap='none')
            print('Disabled wrapping on the text widget.')