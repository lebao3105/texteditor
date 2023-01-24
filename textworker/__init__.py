import gettext
import locale
import os.path
import pathlib
import sys
import wx

from . import mainwindow
from .backend import is_development_build, get_config, __version__ as version, logger

currdir = pathlib.Path(__file__).parent

# Setup translation first
try:
    from textworker.defs import LOCALE_DIR, ICON_DIR
except ImportError:
    LOCALE_DIR = currdir / "po"
    ICON_DIR = currdir / "icons"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")
_ = gettext.gettext

# Icon
if is_development_build() == True:
    icon = str(ICON_DIR / "textworker.Devel.png")
else:
    icon = str(ICON_DIR / "textworker.png")


# Version
__version__ = version

cfg = get_config.GetConfig(get_config.cfg, get_config.file, default_section="interface")

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

    root = wx.App(0, filename=logger.logfile_)
    fm = mainwindow.MainFrame(None)
    root.SetTopWindow(fm)

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
    fm.Show()
    root.MainLoop()


if __name__ == "__main__":
    start_app()
