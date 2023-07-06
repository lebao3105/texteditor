import platform
import pygubu
import sys
import texteditor

from tkinter import TkVersion, TclVersion
from tkinter.ttk import *

from ..editor import Editor
from ..extensions.generic import clrcall

from libtextworker import LICENSES, __version__ as libver
from libtextworker.general import CraftItems, GetCurrentDir


class AboutDialog:
    app_description: str = \
        _(
        "A text editor in Python, with customizable and easy-to-use user interface." \
        "View this project on GitHub: https://github.com/lebao3105/texteditor" \
        "On GitLab (mirrored from GitHub): https://gitlab.com/lebao3105/texteditor" \
        "Read documents online: https://lebao3105.gitbook.io/texteditor_doc"
        )
    
    app_license: str = \
        '(C) Le Bao Nguyen 2022-2023' \
        'By using this application, you agree to texteditor license below:\n\n' \
        f'{open(CraftItems(LICENSES, "GPL3_full.txt"), "r").read()}'

    app_builds: str = \
        f'Libtextworker {libver}' \
        f'Tk {TkVersion}' \
        f'Tcl {TclVersion}' \
        f'Operating system: {platform.system()} version {platform.version()}' \
        f'Python {sys.version}'

    def __init__(self, master):
        builder = pygubu.Builder(_)

        # Load the UI layout
        builder.add_from_file(CraftItems(GetCurrentDir(__file__), "about.ui"))

        # Get objects
        self.dialog = builder.get_object("aboutdlg", master)
        self.version = builder.get_object("label2", self.dialog)
        self.notebook = builder.get_object("notebook", self.dialog)

        # Description
        fm1 = Frame(self.notebook)
        des = Editor(fm1, state="disabled")
        des.EditorInit(True, True, False)
        des.insert(1.0, self.app_description)
        des.pack(expand=True, fill="both")
        self.notebook.add(fm1, text=_("Description"))

        # License
        fm2 = Frame(self.notebook)
        lcs = Editor(fm2, state="disabled")
        lcs.EditorInit(True, True, False)
        lcs.insert(1.0, self.app_license)
        lcs.pack(expand=True, fill="both")
        self.notebook.add(fm2, text=_("License"))

        # Inspect versions
        fm3 = Frame(self.notebook)
        ins = Editor(fm3, state="disabled")
        ins.EditorInit(True, True, False)
        ins.insert(1.0, self.app_builds)
        ins.pack(expand=True, fill="both")
        self.notebook.add(fm3, text=_("System specs"))

        self.version.configure(text=_("Version {}".format(texteditor.__version__)))

        clrcall.configure(self.notebook, True)
        clrcall.configure(builder.get_object("frame1", self.dialog), True)

    def run(self):
        self.dialog.mainloop()

    def quit(self, event=None):
        return self.destroy()