from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
import pages.about
import pages.helpme
import miscs.init
import tabs

def main_win():
    window = Tk()
    window._ = ""
    p1 = PhotoImage(file = "data/org.lebao3105.texteditor.Devel.png")
    window.iconphoto(False, p1)
    miscs.init.initialize(window, 1)
    window.geometry("810x610")
    window.title(window._("Text editor"))
    place_menu(window)
    place_widgets(window)
    window.mainloop()

def do_nothing():
    print("Nothing")

def ask_quit(self):
    answer = askyesno(self._("Quit"), self._("Are you sure want to quit?"))
    if answer == True:
        self.quit()
        self.destroy()
        exit()

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
                                command=do_nothing)
    self.file_menu.add_command(label=self._("Save"),
                                accelerator="Ctrl+S",
                                command=do_nothing)
    self.file_menu.add_command(label=self._("Save as"), 
                                accelerator="Ctrl+Shift+S",
                                command=do_nothing)
    self.file_menu.add_separator()
    self.file_menu.add_command(label=self._("Exit"), 
                                accelerator="Alt+F4",
                                command=lambda: ask_quit(self))
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
                                accelerator="Alt+F2",
                                command=lambda: pages.about.about_run(self))
    self.menu_bar.add_cascade(label=self._("Help"), menu=self.help_menu)
    self.config(menu=self.menu_bar)
    # Create a notebook
    self.notebook = ttk.Notebook(self)
    self.firsttab = Frame(self.notebook)
    tabs.place_textbox(self.firsttab)
    self.notebook.add(self.firsttab, text=self._("Untitled "))


def place_widgets(self):
    self.notebook.pack(expand=True, fill="both")
    # Close & New tab right-click menu for tabs
    self.tab_right_click = Menu(self.notebook, tearoff=0)
    self.tab_right_click.add_command(label=self._("New tab"), command=lambda: tabs.add_tab(self))
    self.tab_right_click.add_command(label=self._("Close the current opening tab"), command=lambda: tabs.tabs_close(self))
    self.bind("<Button-3>", lambda event: self.tab_right_click.post(event.x_root, event.y_root))

def binder(self):
    # Menu items
    self.bind("<Control-n>", lambda event: tabs.add_tab(self))
    self.bind("<Control-o>", lambda event: do_nothing)
    self.bind("<Control-s>", lambda event: do_nothing)
    self.bind("<Control-Shift-s>", lambda event: do_nothing)
    self.bind("<Alt-F4>", lambda event: ask_quit(self))
    self.bind("<Control-a>", lambda event: do_nothing)
    self.bind("<Control-z>", lambda event: do_nothing)
    self.bind("<Control-y>", lambda event: do_nothing)
    self.bind("<Control-x>", lambda event: do_nothing)
    self.bind("<Control-c>", lambda event: do_nothing)
    self.bind("<Control-v>", lambda event: do_nothing)
    self.bind("<Alt-F1>", lambda event: pages.helpme.help_run(self))
    self.bind("<Alt-F2>", lambda event: pages.about.about_run(self))

# Still keep this
if __name__ == "__main__":
    main_win()
