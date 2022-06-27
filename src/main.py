# Import modules
## Tkinter
from tkinter import *
from tkinter import ttk
## Pages
import pages.about
import pages.helpme
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
        self.mainloop()

    def place_menu(self):
        # Menu bar
        self.menu_bar = Menu(self)
        ## File
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        addfilecmd = self.file_menu.add_command
        addfilecmd(label=self._("New"), accelerator="Ctrl+N", command=lambda: tabs.add_tab(self))
        addfilecmd(label=self._("Open"), accelerator="Ctrl+O", command=lambda: miscs.file_operations.open_file(self))
        addfilecmd(label=self._("Save"), accelerator="Ctrl+S", command=lambda: miscs.file_operations.save_file(self))
        addfilecmd(label=self._("Save as"), accelerator="Ctrl+Shift+S", command=lambda: miscs.file_operations.save_as(self))
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
        self.menu_bar.add_cascade(label=self._("Edit"), menu=self.edit_menu)
        
        ## Help & About
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        addhelpcmd = self.help_menu.add_command
        addhelpcmd(label=self._("Help"), 
                                accelerator="Alt+F1",
                                command=lambda: pages.helpme.Help(self))
        addhelpcmd(label=self._("About"), 
                                accelerator="Alt+F3",
                                command=lambda: pages.about.About(self))
        self.menu_bar.add_cascade(label=self._("Help"), menu=self.help_menu)
        self.config(menu=self.menu_bar)


    def place_widgets(self):
        # Create a notebook
        self.notebook = ttk.Notebook(self)
        tabs.add_tab(self)
        self.notebook.pack(expand=True, fill="both")
        # Close & New tab right-click menu for tabs
        self.tab_right_click = Menu(self.notebook, tearoff=0)
        self.tab_right_click.add_command(label=self._("New tab"), accelerator="Ctrl+N", command=lambda: tabs.add_tab(self))
        self.tab_right_click.add_command(label=self._("Close the current opening tab"), accelerator="Ctrl+W", command=lambda: tabs.tabs_close(self))
        self.notebook.bind("<Button-3>", lambda event: self.tab_right_click.post(event.x_root, event.y_root))

    # Add commands to the menu
    def add_event(self):
        self.edit_menu.entryconfigure("Undo", command=lambda: self.event_generate("<Control-z>"))
        self.edit_menu.entryconfigure("Redo", command=lambda: self.event_generate("<Control-y>"))
        self.edit_menu.entryconfigure("Cut", command=lambda: self.event_generate("<Control-x>"))
        self.edit_menu.entryconfigure("Copy", command=lambda: self.event_generate("<Control-c>"))
        self.edit_menu.entryconfigure("Paste", command=lambda: self.event_generate("<Control-v>"))
        self.edit_menu.entryconfigure("Select all", command=lambda: self.event_generate("<Control-a>"))
        self.file_menu.entryconfigure("Open", command=lambda: miscs.file_operations.open_file(self))
        self.file_menu.entryconfigure("Save", command=lambda: miscs.file_operations.save_file(self))
        self.file_menu.entryconfigure("Save as", command=lambda: miscs.file_operations.save_as(self))
        self.file_menu.entryconfigure("Exit", command=lambda: miscs.init.ask_quit(self))

if __name__ == "__main__":
    MainWindow()
