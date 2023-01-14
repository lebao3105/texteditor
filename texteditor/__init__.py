import gettext
import locale
import os.path
import pathlib
import sys
import wx

import texteditor
from . import mainwindow
from .backend import is_development_build

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
if is_development_build() == True:
    texteditor.icon = str(currdir / "icons/texteditor.Devel.png")
else:
    texteditor.icon = str(currdir / "icons/texteditor.png")


# Start
def _file_not_found(filename):
    return wx.MessageDialog(
        None,
        message=_("File not found"),
        caption=_("Cannot find file name %s - create it?") % filename,
        style=wx.YES_NO | wx.ICON_INFORMATION,
    ).ShowModal()


def start_app():
    """Start the application."""
    argv = sys.argv
    argc = len(argv) - 1
    root = mainwindow.MyApp(0)

    if argc > 0:
        textw = root.frame.notebook.text_editor
        if os.path.isfile(argv[1]):
            textw.fileops.openfile(argv[1])
        else:
            if _file_not_found(argv[1]) == wx.ID_YES:
                f = open(argv[1], mode="w")
                textw.fileops.openfile(argv[1])
                del f

        for i in range(2, argc + 1):

            if os.path.isfile(argv[i]):
                root.frame.notebook.AddTab()
                textw.fileops.openfile(argv[i])
            else:
                if _file_not_found(argv[i]) == wx.ID_YES:
                    root.frame.notebook.AddTab()
                    textw.fileops.openfile(argv[i])
                    del f

    root.MainLoop()


if __name__ == "__main__":
    start_app()
