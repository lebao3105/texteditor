# Import modules
from tkinter import Menu, Tk, ttk
from pages import cmd
from miscs import init, file_operations
from extensions import finding
import tabs
import gettext

gettext.bindtextdomain('base', 'po')
gettext.textdomain('base')

class MainWindow(Tk):
    """Main application class.
    Todo: Bind keyboard accelerator for File + Find menu items
    """
    def __init__(self):
        super().__init__()
        self._ = gettext.gettext
        init.initialize(self)
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
        addfilecmd(label=self._("Open"), command=lambda: file_operations.open_file(self))
        addfilecmd(label=self._("Save"), command=lambda: file_operations.save_file(self))
        addfilecmd(label=self._("Save as"), command=lambda: file_operations.save_as(self))
        self.file_menu.add_separator()
        addfilecmd(label=self._("Exit"), accelerator="Alt+F4", command=lambda: init.ask_quit(self))
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
        self.menu_bar.add_cascade(label=self._("Editing"), menu=self.edit_menu)

        ## Find & Replace
        self.find_menu = Menu(self.menu_bar, tearoff=0)
        addfindcmd = self.find_menu.add_command
        addfindcmd(label=self._("Find"), command=lambda: finding.Finder(self, "find"))
        addfindcmd(label=self._("Replace"), command=lambda: finding.Finder(self, ""))
        self.menu_bar.add_cascade(label=self._("Find"), menu=self.find_menu)
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
        filecfg("Open", command=lambda: file_operations.open_file(self))
        filecfg("Save", command=lambda: file_operations.save_file(self))
        filecfg("Save as", command=lambda: file_operations.save_as(self))
        filecfg("Exit", command=lambda: init.ask_quit(self))

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
