import gettext
import locale
import os
import pathlib
import sys
from tkinter import messagebox as msgbox

sys.path.append(str(pathlib.Path(__file__).parent / ".." / "libtextworker"))
from libtextworker.general import GetCurrentDir
from libtextworker.versioning import is_development_version

from . import mainwindow
from .backend import configs

currdir = GetCurrentDir(__file__, True)
__version__ = "1.5a0"


if is_development_version(__version__):
    icon = currdir / "icons" / "texteditor.Devel.png"
else:
    icon = currdir / "icons" / "texteditor.png"


LOCALE_DIR = currdir / "po"

if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = currdir / ".." / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")


# Startup functions
def __filenotfound(filepath):
    return msgbox.askyesno(
        _("File not found"), _("Cannot find the file %s - create it?" % str(filepath))
    )


def start_app(argv=None):
    if not argv:  # For __main__
        argv = sys.argv[1:]
    root = mainwindow.MainWindow()
    n = len(argv)

    if n > 0:
        if os.path.isfile(argv[1]):
            root.notebook.fileops.openfile(argv[1])
        else:
            if __filenotfound(argv[1]):
                f = open(argv[1], mode="w")
                root.notebook.fileops.openfile(argv[1])
                del f

        for i in range(2, n):
            if os.path.isfile(argv[i]):
                root.add_tab()
                root.notebook.fileops.openfile(argv[i])
            elif __filenotfound(argv[i]):
                f = open(argv[i], mode="w")
                root.add_tab()
                root.notebook.fileops.openfile(argv[i])
                del f
    else:
        pass

    root.mainloop()
