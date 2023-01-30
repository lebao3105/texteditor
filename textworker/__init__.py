import gettext
import locale
import os.path
import pathlib

from . import main
from .backend import is_development_build, __version__ as version

currdir = pathlib.Path(__file__).parent

# Setup translation first
try:
    from textworker.defs import LOCALE_DIR, ICON_DIR
except ImportError:
    LOCALE_DIR = currdir / "po"
    ICON_DIR = currdir / "icons"

if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = currdir / ".." / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")

# Icon
if is_development_build() == True:
    icon = str(ICON_DIR / "textworker.Devel.png")
else:
    icon = str(ICON_DIR / "textworker.png")


# Version
__version__ = version
start_app = main.start_app()

del LOCALE_DIR, ICON_DIR
