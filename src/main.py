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
        self.file_menu.add_command(label=self._("New"), 
                                accelerator="Ctrl+N",
                                command=lambda: tabs.add_tab(self))
        self.file_menu.add_command(label=self._("Open"), 
                                accelerator="Ctrl+O",
                                command=lambda: miscs.file_operations.open_file(self))
        self.file_menu.add_command(label=self._("Save"),
                                accelerator="Ctrl+S",
                                command=miscs.file_operations.save_file(self))
        self.file_menu.add_command(label=self._("Save as"), 
                                accelerator="Ctrl+Shift+S",
                                command=miscs.file_operations.save_as(self))
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self._("Exit"), 
                                accelerator="Alt+F4",
                                command=lambda: miscs.init.ask_quit(self))
        self.menu_bar.add_cascade(label=self._("File"), menu=self.file_menu)
        ## Edit
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label=self._("Undo"), accelerator="Ctrl+Z",
                                #event=lambda: self.event_generate("<Control-z>")
                                )
        self.edit_menu.add_command(label=self._("Redo"), accelerator="Ctrl+Y",
                                #command=lambda event: self.event_generate("<Control-y>")
                                )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=self._("Cut"), accelerator="Ctrl+X",
                                #command=lambda event: self.event_generate("<Control-x>")
                                )
        self.edit_menu.add_command(label=self._("Copy"), accelerator="Ctrl+C",
                                #command=lambda event: self.event_generate("<Control-c>")
                                )
        self.edit_menu.add_command(label=self._("Paste"), accelerator="Ctrl+V",
                                #command=lambda event: self.event_generate("<Control-v>")
                                )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label=self._("Select all"), accelerator="Ctrl+A")
        self.menu_bar.add_cascade(label=self._("Edit"), menu=self.edit_menu)
        ## Help & About
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label=self._("Help"), 
                                accelerator="Alt+F1",
                                command=lambda: pages.helpme.Help(self))
        self.help_menu.add_command(label=self._("About"), 
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
        self.tab_right_click.add_command(label=self._("New tab"), 
                                    accelerator="Ctrl+N",    
                                    command=lambda: tabs.add_tab(self))
        self.tab_right_click.add_command(label=self._("Close the current opening tab"), 
                                    accelerator="Ctrl+W",
                                    command=lambda: tabs.tabs_close(self))
        self.notebook.bind("<Button-3>", lambda event: self.tab_right_click.post(event.x_root, event.y_root))
        # Bind the function to the event
        self.binder()

    # Add commands to the menu
    def add_event(self):
        self.edit_menu.entryconfigure("Undo", command =lambda: self.event_generate("<Control-z>"))
        self.edit_menu.entryconfigure("Redo", command =lambda: self.event_generate("<Control-y>"))
        self.edit_menu.entryconfigure("Cut", command =lambda: self.event_generate("<Control-x>"))
        self.edit_menu.entryconfigure("Copy", command =lambda: self.event_generate("<Control-c>"))
        self.edit_menu.entryconfigure("Paste", command =lambda: self.event_generate("<Control-v>"))
        self.edit_menu.entryconfigure("Select all", command =lambda: self.event_generate("<Control-a>"))
        self.file_menu.entryconfigure("Open", command =lambda: miscs.file_operations.open_file(self))
        self.file_menu.entryconfigure("Save", command =miscs.file_operations.save_file(self))
        self.file_menu.entryconfigure("Save as", command =miscs.file_operations.save_as(self))
        self.file_menu.entryconfigure("Exit", command =lambda: miscs.init.ask_quit(self))


    def binder(self):
        self.bind("<Control-n>", lambda event: tabs.add_tab(self))
        self.bind("<Control-o>", lambda event: miscs.file_operations.open_file(self))
        self.bind("<Control-s>", lambda event: miscs.file_operations.save_file(self))
        self.bind("<Control-Shift-s>", lambda event: miscs.file_operations.save_as(self))
        self.bind("<Alt-F4>", lambda event: miscs.init.ask_quit(self))
        self.bind("<Alt-F1>", lambda event: pages.helpme.Help(self))
        self.bind("<Alt-F3>", lambda event: pages.about.About(self))
        self.bind("<Alt-F4>", lambda event: miscs.init.ask_quit(self))
        self.bind("<Control-w>", lambda event: tabs.tabs_close(self))
        self.protocol("WM_DELETE_WINDOW", lambda: miscs.init.ask_quit(self))

if __name__ == "__main__":
    MainWindow()
