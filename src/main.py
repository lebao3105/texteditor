from tkinter import *
from tkinter.messagebox import askyesno
import pages.about
import pages.helpme
import gettext

language = ""

def main_win():
    if language == "en":
        en = gettext.translation('base', localedir='po', languages=['en'])
        en.install()
        _ = en.gettext
    elif language == "vi":
        vi = gettext.translation('base', localedir='po', languages=['vi'])
        vi.install()
        _ = vi.gettext
    window = Tk()
    window.title(_("Text editor"))
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

def place_widgets(self):
    # Create a text editor widget
    self.text_editor = Text(self)
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
    self.text_editor.grid(row=0, column=0, sticky="nsew")
