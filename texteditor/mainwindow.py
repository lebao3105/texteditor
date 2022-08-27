# Import modules
import gettext, tabs, os
from tkinter import *
import tkinter.ttk as ttk
from texteditor.extensions import finding, cmd
from texteditor.miscs import file_operations, get_config, \
    constants, textwidget, autosave
                         
gettext.bindtextdomain('base', 'po')
gettext.textdomain('base')

# Note that icon variable assume that we are in texteditor/texteditor (where is this file in the repository).
# Please change it manually if needed.
currdir = os.path.dirname(os.path.abspath(__file__))

if constants.STATE == "DEV":
    icon = currdir + '/icons/texteditor.Devel.png'
elif constants.STATE == "STABLE":
    icon = currdir + '/icons/texteditor.png'
else:
    print('Warning: Wrong application branch (STABLE/DEV) in miscs.constants module')
    icon = None

class MainWindow(Tk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ = gettext.gettext

        if os.path.isfile(icon):
            self.iconphoto(False, PhotoImage(file=icon))
        else:
            print('Warning: Application icon', icon, 'not found!')

        # Whetever we still need a booleanvar
        self.wrapbtn = BooleanVar()
        self.wrapbtn.set(True)
        self.title(self._("Text editor"))
        self.geometry("810x610")
        self.place_menu()
        self.place_widgets()
        self.add_event()

    def place_menu(self):
        # Menu bar
        self.menu_bar = Menu(self)
        ## File
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        addfilecmd = self.file_menu.add_command
        addfilecmd(label=self._("New"), command=lambda: tabs.add_tab(self), accelerator="Ctrl+N")
        addfilecmd(label=self._("Open"), command=lambda: file_operations.open_file(self), accelerator="Ctrl+O")
        addfilecmd(label=self._("Save"), command=lambda: file_operations.save_file(self), accelerator="Ctrl+S")
        addfilecmd(label=self._("Save as"), command=lambda: file_operations.save_as(self), accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        addfilecmd(label=self._("Exit"), accelerator="Alt+F4")
        self.menu_bar.add_cascade(label=self._("File"), menu=self.file_menu)

        ## Edit
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        addeditcmd = self.edit_menu.add_command
        addeditcmd(label=self._("Undo"), accelerator="Ctrl+Z")
        addeditcmd(label=self._("Redo"), accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        addeditcmd(label=self._("Cut"), accelerator="Ctrl+X")
        addeditcmd(label=self._("Copy"), accelerator="Ctrl+C")
        addeditcmd(label=self._("Paste"), accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        addeditcmd(label=self._("Select all"), accelerator="Ctrl+A")

        if get_config.GetConfig.getvalue("cmd", "isenabled") == "yes":
            self.edit_menu.add_separator()
            addeditcmd(label=self._("Open System Shell"), command=lambda: cmd.CommandPrompt(self), accelerator="Ctrl+T")
        
        self.menu_bar.add_cascade(label=self._("Editing"), menu=self.edit_menu)

        ## Find & Replace
        self.find_menu = Menu(self.menu_bar, tearoff=0)
        addfindcmd = self.find_menu.add_command
        addfindcmd(label=self._("Find"), command=lambda: finding.Finder(self, "find"), accelerator="Ctrl+F")
        addfindcmd(label=self._("Replace"), command=lambda: finding.Finder(self, ""), accelerator="Ctrl+R")
        self.menu_bar.add_cascade(label=self._("Find"), menu=self.find_menu)

        ## Config
        self.config_menu = Menu(self.menu_bar, tearoff=0)
        addcfgcmd = self.config_menu.add_command
        addcfgcmd(label=self._("Reset configurations"), command=lambda: self.resetcfg(self))
        addcfgcmd(label=self._("Autosave"), command=lambda: autosave.AutoSave(self).openpopup())
        # This should be added to View menu in the future
        self.config_menu.add_checkbutton(label=self._("Wrap (by word)"),
                command=lambda: textwidget.TextWidget.wrapmode(self),
                accelerator="Ctrl+W", variable=self.wrapbtn)
        self.menu_bar.add_cascade(label=self._("Config"), menu=self.config_menu)
        # Add menu to the application
        self.config(menu=self.menu_bar)

    def place_widgets(self):
        # Create a notebook
        self.notebook = ttk.Notebook(self)
        tabs.add_tab(self)
        self.notebook.pack(expand=True, fill="both")
        # Close & New tab right-click menu for tabs
        self.tab_right_click = Menu(self.notebook, tearoff=0)
        self.tab_right_click.add_command(label=self._("New tab"), command=lambda: tabs.add_tab(self))
        self.tab_right_click.add_command(label=self._("Close the current opening tab"), accelerator="Ctrl+W", command=lambda: tabs.tabs_close(self))
        self.notebook.bind("<Button-3><ButtonRelease-3>", lambda event: self.tab_right_click.post(event.x_root, event.y_root))
        self.notebook.bind("<<NotebookTabChanged>>", lambda event: tabs.on_tab_changed(self, event))

    # Binding commands to the application
    def add_event(self):
        bindcfg = self.bind
        bindcfg("<Control-n>", lambda evnet: tabs.add_tab(self))
        if get_config.GetConfig.getvalue("cmd", "isenabled") == "yes":
            bindcfg("<Control-t>", lambda event: cmd.CommandPrompt(self))
        bindcfg("<Control-f>", lambda event: finding.Finder(self, "find"))
        bindcfg("<Control-r>", lambda event: finding.Finder(self, ""))
        bindcfg("<Control-Shift-S>", lambda event: file_operations.save_as(self))
        bindcfg("<Control-s>", lambda event: file_operations.save_file(self))
        bindcfg("<Control-o>", lambda event: file_operations.open_file(self))
        #bindcfg("<Control-w>", lambda event: textwidget.TextWidget.wrapmode(self))
    
    def resetcfg(self, event=None):
        import tkinter.messagebox as msgbox
        message = msgbox.askyesno("Warning", "This will reset ALL configurations you have ever made. Continue?")
        if message:
            get_config.GetConfig.reset()
            msgbox.showinfo("Completed", "Completed resetting texteditor configurations.\nRestart the application to take effect.")


if __name__ == "__main__":
    print('Warning: You are running texteditor.mainwindow directly. You can open file with that.')
    app = MainWindow()
    app.mainloop()
