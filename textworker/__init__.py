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

from libtextworker._importer import test_import
from libtextworker.general import CraftItems
from libtextworker.versioning import *

require("libtextworker", "0.1.2")
test_import("wx")
__version__ = "1.6a2"

LOCALE_DIR = currdir / "po"
ICON_DIR = currdir / "icons"

if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = currdir / ".." / "po"

# Setup translation
locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("textworker", LOCALE_DIR)
gettext.textdomain("textworker")
gettext.install("textworker")

# Icon
if is_development_version(__version__) == True:
    icon = CraftItems(ICON_DIR, "textworker.Devel.png")
else:
    icon = CraftItems(ICON_DIR, "textworker.png")
# --- ---

del LOCALE_DIR, ICON_DIR
