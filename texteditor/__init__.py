import gettext
import locale
import os.path
import pathlib
import sys

import texteditor
from . import mainwindow
from .backend import constants

currdir = pathlib.Path(__file__).parent

if constants.STATE == "DEV":
    texteditor.icon = str(currdir / "icons/texteditor.Devel.png")
elif constants.STATE == "STABLE":
    texteditor.icon = str(currdir / "icons/texteditor.png")
else:
    print("Warning: Unknown application branch (STABLE/DEV) in miscs.constants module")
    texteditor.icon = None

try:
    from texteditor.defs import LOCALE_DIR
except ImportError:
    LOCALE_DIR = currdir / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")
texteditor._ = gettext.gettext


def start_app():
    """Start initializing the application."""
    argv = sys.argv
    argc = len(argv) - 1
    root = mainwindow.MyApp(0)
    root.MainLoop()


if __name__ == "__main__":
    start_app()
