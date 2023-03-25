"""
Ahoy, this is textworker 1.6alpha2 - wxPython port of the texteditor/textworker program!
Working-on features:
* Command Window
* File modification(s) check
"""
import gettext
import locale
import os.path
import pathlib
import sys

currdir = pathlib.Path(__file__).parent
sys.path.append(str(currdir / ".." / "libtextworker"))

from libtextworker.general import CraftItems
from .backend import is_development_build, require_version, __version__ as version

require_version("1.6a2")
__version__ = version

try:
    from textworker.defs import LOCALE_DIR, ICON_DIR  # type: ignore
except ImportError:
    LOCALE_DIR = currdir / "po"
    ICON_DIR = currdir / "icons"

if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = currdir / ".." / "po"

# Setup translation
locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.textworker", LOCALE_DIR)
gettext.textdomain("me.lebao3105.textworker")
gettext.install("me.lebao3105.textworker")

# Icon
if is_development_build() == True:
    icon = CraftItems(ICON_DIR, "textworker.Devel.png")
else:
    icon = CraftItems(ICON_DIR, "textworker.png")
# --- ---

del LOCALE_DIR, ICON_DIR
