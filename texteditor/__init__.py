import gettext
import pathlib
import locale
import os.path
import sys
from tkinter.messagebox import showinfo

import texteditor
from . import mainwindow
from .backend import file_operations, constants

currdir = pathlib.Path(__file__).parent

if constants.STATE == "DEV":
    texteditor.icon = currdir / "icons/texteditor.Devel.png"
elif constants.STATE == "STABLE":
    texteditor.icon = currdir / "icons/texteditor.png"
else:
    print("Warning: Wrong application branch (STABLE/DEV) in miscs.constants module")
    texteditor.icon = None

try:
    from texteditor.defs import LOCALE_DIR
except ImportError:
    LOCALE_DIR = currdir / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
texteditor._ = gettext.gettext


def start_app(argv: sys.argv = None):
    if not argv:  # For __main__
        argv = sys.argv
    root = mainwindow.MainWindow()
    n = len(argv)
    if n - 1 > 0:
        if os.path.isfile(argv[1]):
            file_operations.openfilename(root, argv[1])
        else:
            showinfo(message="File not found : %s" % str(argv[1]))
        for i in range(2, n):
            if os.path.isfile(argv[i]):
                root.add_tab()
                file_operations.openfilename(root, argv[i])
            else:
                showinfo(message="File not found : %s" % str(argv[i]))
    else:
        pass

    root.mainloop()


if __name__ == "__main__":
    start_app(sys.argv)
