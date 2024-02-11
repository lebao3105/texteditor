import gettext
import locale
import os.path
import pathlib

currdir = pathlib.Path(__file__).parent

from libtextworker.general import test_import
from libtextworker.versioning import *

require("libtextworker", "0.1.4")
test_import("wx")
__version__ = "1.6b0"

if not os.path.isdir(LOCALE_DIR := currdir / "po"):
    LOCALE_DIR = currdir / ".." / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("textworker", LOCALE_DIR)
gettext.textdomain("textworker")
_ = gettext.gettext
del LOCALE_DIR

if is_development_version(__version__) == True:
    branch = "dev"
else:
    branch = "stable"

ICON = None # Will create later

# Here goes the credit section!
# (Only me though)
DEVS = ARTISTS = DOCWRITERS = {
    "Le Bao Nguyen (@lebao3105)": "https://github.com/lebao3105"
}

# License path
LICENSE = currdir / "../LICENSE"

# URLs
HOMEPAGE = "https://github.com/lebao3105/texteditor"