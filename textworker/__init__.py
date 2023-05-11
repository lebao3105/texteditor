"""
Ahoy, this is textworker 1.6alpha3 - wxPython port of the texteditor/textworker program!
Working-on features:
* Command Window (cancelled?)
* File modification(s) check
* Sidebar
* Remake statusbar
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

require("libtextworker", "0.1.3")
test_import("wx")
__version__ = "1.6a3"


LOCALE_DIR = currdir / "po"
ICON_DIR = currdir / "data" / "icons"

if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = currdir / ".." / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("textworker", LOCALE_DIR)
gettext.textdomain("textworker")
gettext.install("textworker")

if not os.path.isdir(ICON_DIR):
    ICON_DIR = ""

if is_development_version(__version__) == True:
    icon = CraftItems(ICON_DIR, "me.lebao3105.textworker.Devel.svg")
else:
    icon = CraftItems(ICON_DIR, "me.lebao3105.textworker.svg")


del LOCALE_DIR, ICON_DIR

if not os.path.isdir(currdir / "data"):
    raise Exception("git submodules update is needed! Exiting.")
    exit(-1)