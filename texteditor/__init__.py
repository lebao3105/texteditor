import gettext
import locale
import os

import libtextworker
from libtextworker.general import GetCurrentDir, test_import, CraftItems
from libtextworker.versioning import is_development_version_from_project, require

currdir = GetCurrentDir(__file__, True)
__version__ = "1.5a0"

require("libtextworker", "0.1.4")
test_import("tkinter")

icon = currdir / "data" / "icons"

if is_development_version_from_project("texteditor"):
    icon = icon / "me.lebao3105.textworker.Devel.svg"
else:
    icon = icon / "me.lebao3105.textworker.svg"

LOCALE_DIR = currdir / "po"
VIEWS_DIR = currdir / "views"

if not os.path.isdir(LOCALE_DIR):
    LOCALE_DIR = currdir / ".." / "po"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain("me.lebao3105.texteditor", LOCALE_DIR)
gettext.textdomain("me.lebao3105.texteditor")
gettext.install("me.lebao3105.texteditor")

libtextworker.EDITOR_DIR = CraftItems(libtextworker.TOPLV_DIR, "editorconfigs")
libtextworker.THEMES_DIR = CraftItems(libtextworker.TOPLV_DIR, "themes")