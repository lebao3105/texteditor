import gettext
import locale
import os.path
import pathlib

currdir = pathlib.Path(__file__).parent

from libtextworker.general import test_import
from libtextworker.versioning import *

require("libtextworker", "0.1.4")
test_import("wx")
__version__ = "1.6dev1"


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
    branch = "dev"
else:
    branch = "stable"
