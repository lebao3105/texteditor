from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
import pages.about
import pages.helpme
import gettext
import tabs

def main_win():
    vi = gettext.translation('base', localedir='po', languages=['vi'])
    vi.install()
    _ = vi.gettext

    window = Tk()
    window.title(_("Text editor"))
    place_menu(window)
    place_widgets(window)
    window.mainloop()

def do_nothing():
    print("Nothing")

def ask_quit(self):
    answer = askyesno(_("Quit"), _("Do you really want to quit?"))
    if answer == True:
        self.quit()
        self.destroy()
        exit()

def place_menu(self):
    # Menu bar
    self.menu_bar = Menu(self)
    ## File
    self.file_menu = Menu(self.menu_bar, tearoff=0)
    self.file_menu.add_command(label=_("New"), command=do_nothing)
    self.file_menu.add_command(label=_("Open"), command=do_nothing)
    self.file_menu.add_command(label=_("Save"), command=do_nothing)
    self.file_menu.add_command(label=_("Save as"), command=do_nothing)
    self.file_menu.add_separator()
    self.file_menu.add_command(label=_("Exit"), command=lambda: ask_quit(self))
    self.menu_bar.add_cascade(label=_("File"), menu=self.file_menu)
    ## Edit
    self.edit_menu = Menu(self.menu_bar, tearoff=0)
    self.edit_menu.add_command(label=_("Undo"), command=do_nothing)
    self.edit_menu.add_command(label=_("Redo"), command=do_nothing)
    self.edit_menu.add_separator()
    self.edit_menu.add_command(label=_("Cut"), command=do_nothing)
    self.edit_menu.add_command(label=_("Copy"), command=do_nothing)
    self.edit_menu.add_command(label=_("Paste"), command=do_nothing)
    self.edit_menu.add_separator()
    self.edit_menu.add_command(label=_("Select all"), command=do_nothing)
    self.menu_bar.add_cascade(label=_("Edit"), menu=self.edit_menu)
    ## Help & About
    self.help_menu = Menu(self.menu_bar, tearoff=0)
    self.help_menu.add_command(label=_("Help"), command=lambda: pages.helpme.help_run(self))
    self.help_menu.add_command(label=_("About"), command=lambda: pages.about.about_run(self))
    self.menu_bar.add_cascade(label=_("Help"), menu=self.help_menu)
    self.config(menu=self.menu_bar)
    # Create a notebook
    self.notebook = ttk.Notebook(self)
    self.firsttab = Frame(self.notebook)
    tabs.place_textbox(self.firsttab)
    self.notebook.add(self.firsttab, text=_("Untitled"))

def place_widgets(self):
    self.notebook.pack(expand=True, fill="both")
    # Close & New tab right-click menu for tabs
    self.tab_right_click = Menu(self.notebook, tearoff=0)
    self.tab_right_click.add_command(label=_("New tab"), command=lambda: tabs.add_tab(self))
    self.tab_right_click.add_command(label=_("Close"), command=lambda: self.notebook.forget(self.notebook.select()))
    self.bind("<Button-3>", lambda event: self.tab_right_click.post(event.x_root, event.y_root))

# Still keep this
if __name__ == "__main__":
    main_win()