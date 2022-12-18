import tkinter
from tkinter.filedialog import *
from tkinter.messagebox import askyesno
import os, sys, gettext

from . import constants
from .. import tabs

# Use this for closing the application
is_saved = False
# Saved files
saved_files = []

if sys.platform == "win32":
    searchdir = os.environ["USERPROFILE"] + "\Documents"
    script_type = ("Windows Shell Script", "*.bat, *.cmd, *.ps1")
elif sys.platform == "linux":
    searchdir = os.environ["HOME"] + "/Documents"
    script_type = ("UNIX Shell Script", "*.sh")


def find_text_editor(self):
    if not hasattr(self, "text_editor"):
        raise Exception("Text editor not found!")
    if hasattr(self, "_"):
        _ = self._
    else:
        _ = gettext.gettext


def open_file(self, event=None):
    find_text_editor(self)
    file_name = askopenfilename(
        initialdir=searchdir,
        title=_("Select a file to open"),
        filetypes=((_("All files"), "*.*"), script_type, (_("Text files"), "*.txt")),
    )
    if file_name:

        if not self.text_editor.compare("end-1c", "==", 1.0):
            tabs.TabsViewer(self, do_place=False).add_tab()

        for x in constants.FILES_ARR:
            if file_name in x:
                if asktoopen(self):
                    pass

        openfilename(self, file_name)


def openfilename(tkwin, filename):
    find_text_editor(tkwin)
    with open(filename, "r") as f:
        print("Opening file: ", filename)
        tkwin.text_editor.insert(1.0, f.read())
        tkwin.title(_("Text editor") + " - " + filename)
        tkwin.notebook.tab("current", text=filename)

    constants.FILES_ARR.append(filename)
    if hasattr(tkwin.text_editor, "statusbar"):
        tkwin.text_editor.statusbar.writeleftmessage(_("Opened file %s") % filename)
    # print(constants.FILES_ARR)


def savefilename(tkwin, filename):
    with open(filename, "w") as f:
        try:
            print("Saving file: ", filename)
            if hasattr(tkwin.text_editor, "statusbar"):
                tkwin.text_editor.statusbar.writeleftmessage(
                    _("Saving file %s") % filename
                )
            f.write(tkwin.text_editor.get(1.0, tkinter.END))
        except OSError as e:
            print("Error: Unable to save file ", filename)
            if hasattr(tkwin.text_editor, "statusbar"):
                tkwin.text_editor.statusbar.writeleftmessage(
                    _("Unable to save file %s - %s") % (filename, str(e))
                )
            return False
        else:
            saved_files.append(filename)
            return True


def save_file(self, event=None):
    find_text_editor(self)
    filefind = self.notebook.tab(self.notebook.select(), "text")
    if filefind.endswith(" *"):
        filefind = filefind.removesuffix(" *")
    if self.text_editor.compare("end-1c", "==", 1.0):
        save_as(self)
    elif not (filefind in constants.FILES_ARR):
        save_as(self)
    else:
        savefilename(self, filefind)


def save_as(self, event=None):
    find_text_editor(self)
    file_name = asksaveasfilename(
        initialdir=searchdir,
        title=self._("Save as"),
        filetypes=(("All files", "*.*"), script_type, ("Text files", "*.txt")),
    )
    if file_name:
        if savefilename(self, file_name):
            constants.FILES_ARR.append(file_name)


def asktoopen(self):
    _ = self._
    ask = askyesno(
        _("Infomation"),
        _(
            "This file is opened in another tab. By default we will load the contents to a new tab.\nDo it?"
        ),
    )
    if ask:
        tabs.add_tab(self)
        return True
