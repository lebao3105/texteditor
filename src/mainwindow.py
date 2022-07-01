# Import modules
## Tkinter
from tkinter import *
from tkinter import ttk
## Pages
from pages import about, helpme, cmd
## Some needed functions
import miscs.init
import miscs.file_operations
import tabs

class MainWindow(Tk):

    def __init__(self):
        super().__init__()
        self._ = ""
        miscs.init.initialize(self, 0)
        miscs.init.initialize(self, 1)
        self.geometry("810x610")
        self.title(self._("Text editor"))
        self.place_widgets()
        self.place_menu()
        self.add_event()

    def place_menu(self):
        # Menu bar
        self.menu_bar = Menu(self)
        ## File
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        addfilecmd = self.file_menu.add_command
        addfilecmd(label=self._("New"), command=lambda: tabs.add_tab(self))
        addfilecmd(label=self._("Open"), command=lambda: miscs.file_operations.open_file(self))
        addfilecmd(label=self._("Save"), command=lambda: miscs.file_operations.save_file(self))
        addfilecmd(label=self._("Save as"), command=lambda: miscs.file_operations.save_as(self))
        self.file_menu.add_separator()
        addfilecmd(label=self._("Exit"), accelerator="Alt+F4", command=lambda: miscs.init.ask_quit(self))
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
        self.edit_menu.add_separator()
        addeditcmd(label=self._("Open System Shell"), command=lambda: cmd.CommandPrompt(self))
        self.menu_bar.add_cascade(label=self._("Edit"), menu=self.edit_menu)

        ## Help & About
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        addhelpcmd = self.help_menu.add_command
        addhelpcmd(label=self._("Help"), command=lambda: helpme.Help(self))
        addhelpcmd(label=self._("About"), command=lambda: about.About(self))
        self.menu_bar.add_cascade(label=self._("Help"), menu=self.help_menu)
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
        self.notebook.bind("<Button-3>", lambda event: self.tab_right_click.post(event.x_root, event.y_root))
        self.notebook.bind("<B1-Motion>", lambda event: tabs.move_tab)
        self.notebook.bind("<<NotebookTabChanged>>", lambda event: tabs.on_tab_changed(self, event))

    # Add commands to the menu
    def add_event(self):
        editcfg = self.edit_menu.entryconfigure
        filecfg = self.file_menu.entryconfigure
        editcfg("Open System Shell", command=lambda: cmd.CommandPrompt(self))
        editcfg("Undo", command=lambda: self.event_generate("<Control-z>"))
        editcfg("Redo", command=lambda: self.event_generate("<Control-y>"))
        editcfg("Cut", command=lambda: self.event_generate("<Control-x>"))
        editcfg("Copy", command=lambda: self.event_generate("<Control-c>"))
        editcfg("Paste", command=lambda: self.event_generate("<Control-v>"))
        editcfg("Select all", command=lambda: self.event_generate("<Control-a>"))
        filecfg("Open", command=lambda: miscs.file_operations.open_file(self))
        filecfg("Save", command=lambda: miscs.file_operations.save_file(self))
        filecfg("Save as", command=lambda: miscs.file_operations.save_as(self))
        filecfg("Exit", command=lambda: miscs.init.ask_quit(self))

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
