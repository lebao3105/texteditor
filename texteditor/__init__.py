import gettext
import locale
import os.path
import pathlib
import sys
import tkinter.messagebox as msgbox

from . import mainwindow
from .backend import __version__ as version, is_development_build

currdir = pathlib.Path(__file__).parent
__version__ = version

# Icon
if is_development_build():
    icon = currdir / "icons" / "texteditor.Devel.png"
else:
    icon = currdir / "icons" / "texteditor.png"
# --- ---

# Translation
LOCALE_DIR = "@LOCALE_DIR@"
MESONTOUCH = "@MESONTOUCH@"
LOCALE_DIR = currdir / "po"

if MESONTOUCH != True:
    if LOCALE_DIR == "@LOCALEDIR@":
        LOCALE_DIR = currdir / "po"

if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = currdir / ".." / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")
# --- ---

# Startup functions
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
        argv = sys.argv[1:]
    root = mainwindow.MainWindow()
    n = len(argv)

    if n > 0:

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
