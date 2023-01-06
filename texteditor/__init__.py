import gettext
import locale
import os.path
import pathlib
import sys
import wx

import texteditor
from . import mainwindow
from .backend import constants

currdir = pathlib.Path(__file__).parent

# Setup translation first
try:
    from texteditor.defs import LOCALE_DIR
except ImportError:
    LOCALE_DIR = currdir / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")
_ = gettext.gettext

# Icon
if constants.STATE == "DEV":
    texteditor.icon = str(currdir / "icons/texteditor.Devel.png")
elif constants.STATE == "STABLE":
    texteditor.icon = str(currdir / "icons/texteditor.png")
else:
    constants.STATE = "UNKNOWN (%s)" % constants.STATE
    texteditor.icon = None


# Start
def _file_not_found(filename):
    return wx.MessageDialog(
        None,
        message=_("File not found"),
        caption=_("File not found %s") % filename,
        style=wx.OK_DEFAULT | wx.ICON_INFORMATION,
    ).ShowModal()


def start_app():
    """Start the application."""
    argv = sys.argv
    argc = len(argv) - 1
    root = mainwindow.MyApp(0)
    root.MainLoop()

    if argc > 0:
        if os.path.isfile(argv[1]):
            root.notebook.text_editor.fileops.openfile(argv[1])
        else:
            _file_not_found(argv[1])
        for i in range(2, argc + 1):
            if os.path.isfile(argv[i]):
                root.notebook.AddTab()
                root.notebook.text_editor.fileops.openfile(argv[i])
            else:
                _file_not_found(argv[i])


if __name__ == "__main__":
    start_app()
