import gettext
import locale
import os.path
import pathlib
import sys
import tkinter.messagebox as msgbox

import texteditor
from . import mainwindow
from .backend import __version__ as version, is_development_build

currdir = pathlib.Path(__file__).parent
__version__ = version

if is_development_build():
    texteditor.icon = currdir / "icons/texteditor.Devel.png"
else:
    texteditor.icon = currdir / "icons/texteditor.png"

try:
    from texteditor.defs import LOCALE_DIR
except ImportError:
    LOCALE_DIR = currdir / "po"
# LOCALE_DIR = "build/po/"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")
_ = gettext.gettext


def __filenotfound(filepath):
    ask = msgbox.askyesno(
        _("File not found"), _("Cannot find the file %s - create it?" % str(filepath))
    )
    if ask:
        return "add_tab"
    else:
        return "cancel"


def start_app(argv=None):
    if not argv:  # For __main__
        argv = sys.argv
    root = mainwindow.MainWindow()
    n = len(argv)

    if n - 1 > 0:

        if os.path.isfile(argv[1]):
            root.notebook.fileops.openfile(argv[1])
        else:
            if __filenotfound(argv[1]) == "add_tab":
                f = open(argv[1], mode="w")
                root.notebook.fileops.openfile(argv[1])
                del f

        for i in range(2, n):
            if os.path.isfile(argv[i]):
                root.add_tab()
                root.notebook.fileops.openfile(argv[i])
            elif __filenotfound(argv[i]) == "add_tab":
                f = open(argv[i], mode="w")
                root.add_tab()
                root.notebook.fileops.openfile(argv[i])
                del f
    else:
        pass

    root.mainloop()


if __name__ == "__main__":
    start_app(sys.argv)
