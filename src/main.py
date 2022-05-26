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

def main_win():
    window = Tk()
    window._ = ""
    miscs.init.initialize(window, 1)
    window.geometry("810x610")
    window.title(window._("Text editor"))
    place_widgets(window)
    place_menu(window)
    window.mainloop()

def do_nothing():
    print("Nothing")


def place_menu(self):
    # Menu bar
    self.menu_bar = Menu(self)
    ## File
    self.file_menu = Menu(self.menu_bar, tearoff=0)
    self.file_menu.add_command(label=self._("New"), 
                                accelerator="Ctrl+N",
                                command=lambda: tabs.add_tab(self, self))
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
    self.edit_menu.add_command(label=self._("Undo"), 
                                accelerator="Ctrl+Z",
                                command=do_nothing)
    self.edit_menu.add_command(label=self._("Redo"), 
                                accelerator="Ctrl+Y",
                                command=do_nothing)
    self.edit_menu.add_separator()
    self.edit_menu.add_command(label=self._("Cut"), 
                                accelerator="Ctrl+X",
                                command=do_nothing)
    self.edit_menu.add_command(label=self._("Copy"), 
                                accelerator="Ctrl+C",
                                command=do_nothing)
    self.edit_menu.add_command(label=self._("Paste"), 
                                accelerator="Ctrl+V",
                                command=do_nothing)
    self.edit_menu.add_separator()
    self.edit_menu.add_command(label=self._("Select all"), 
                                accelerator="Ctrl+A",
                                command=do_nothing)
    self.menu_bar.add_cascade(label=self._("Edit"), menu=self.edit_menu)
    ## Help & About
    self.help_menu = Menu(self.menu_bar, tearoff=0)
    self.help_menu.add_command(label=self._("Help"), 
                                accelerator="Alt+F1",
                                command=lambda: pages.helpme.help_run(self))
    self.help_menu.add_command(label=self._("About"), 
                                accelerator="Alt+F3",
                                command=lambda: pages.about.about_run(self))
    self.menu_bar.add_cascade(label=self._("Help"), menu=self.help_menu)
    self.config(menu=self.menu_bar)


def place_widgets(self):
    # Create a notebook
    self.notebook = ttk.Notebook(self)
    self.firsttab = Frame(self.notebook)
    tabs.place_textbox(self.firsttab, self)
    self.notebook.add(self.firsttab, text=self._("Untitled "))
    self.notebook.pack(expand=True, fill="both")
    # Close & New tab right-click menu for tabs
    self.tab_right_click = Menu(self.notebook, tearoff=0)
    self.tab_right_click.add_command(label=self._("New tab"), 
                                    accelerator="Ctrl+N",    
                                    command=lambda: tabs.add_tab(self, self))
    self.tab_right_click.add_command(label=self._("Close the current opening tab"), 
                                    accelerator="Ctrl+W",
                                    command=lambda: tabs.tabs_close(self))
    self.bind("Button-release", lambda event: tabs.move_tabs(self, event))
    # Bind the function to the event
    binder(self)

def binder(self):
    self.bind("<Control-n>", lambda event: tabs.add_tab(self, self))
    self.bind("<Control-o>", lambda event: miscs.file_operations.open_file(self))
    self.bind("<Control-s>", lambda event: miscs.file_operations.save_file(self))
    self.bind("<Control-Shift-s>", lambda event: miscs.file_operations.save_as(self))
    self.bind("<Alt-F4>", lambda event: miscs.init.ask_quit(self))
    self.bind("<Control-a>", lambda event: do_nothing)
    self.bind("<Control-z>", lambda event: do_nothing)
    self.bind("<Control-y>", lambda event: do_nothing)
    self.bind("<Control-x>", lambda event: do_nothing)
    self.bind("<Control-c>", lambda event: do_nothing)
    self.bind("<Control-v>", lambda event: do_nothing)
    self.bind("<Alt-F1>", lambda event: pages.helpme.help_run(self))
    self.bind("<Alt-F3>", lambda event: pages.about.about_run(self))
    self.bind("<Control-w>", lambda event: tabs.tabs_close(self))

if __name__ == "__main__":
    main_win()
