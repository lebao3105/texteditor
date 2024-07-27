import gettext
import locale

from libtextworker.general import test_import
from libtextworker.versioning import *

require("libtextworker", "0.1.4b0")
test_import("wx")
__version__ = "1.6b0"

if is_development_version(__version__):
    branch = "dev"
else:
    branch = "stable"

from textworker.generic import currPath

locale.setlocale(locale.LC_ALL, None)

gettext.bindtextdomain("textworker", currPath / ".." / "po")
gettext.textdomain("textworker")
_ = gettext.gettext

ICON = None # Will create later

# Here goes the credit section!
# (Only me though)
DEVS = ARTISTS = DOCWRITERS = {
    "Le Bao Nguyen (@lebao3105)": "https://github.com/lebao3105"
}

# License path
LICENSE = str(currPath / ".." / "LICENSE")

# URLs
HOMEPAGE = "https://gitlab.com/textworker/legacy-python/textworker"
