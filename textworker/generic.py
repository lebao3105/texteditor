import builtins
import json
import logging
import typing

from libtextworker import get_config, THEMES_DIR, EDITOR_DIR
from libtextworker.general import CraftItems, GetCurrentDir, TOPLV_DIR
from libtextworker.interface.wx import ColorManager
from libtextworker.versioning import is_development_version_from_project

"""
Defines (for local use.)
Adding they to builtins is legit lmao:v
"""

builtins.true = True
builtins.false = False
builtins.nil = None

currdir = GetCurrentDir(__file__, true)
UIRC_DIR = str(currdir / "ui")
datadir = str(currdir / "data")
logger = logging.getLogger("textworker")

# Config file path
configpath = TOPLV_DIR + "/configs{}.ini".format(
    "" if not is_development_version_from_project("textworker") else "_dev"
)

# Default configs
cfg = open(CraftItems(datadir, "appconfig.ini")).read()

# App settings
global_settings = get_config.GetConfig(cfg, file=configpath)

# TODO (libtextworker): Detect changes
moves = json.loads(open(CraftItems(GetCurrentDir(__file__), "merges.json")).read())
# global_settings.move(moves)


def find_resource(t: typing.Literal["theme", "editor"]) -> str:
    import os

    if t == "theme":
        _name = global_settings.get("config-paths.ui", "theme")
        _path = global_settings.get("config-paths.ui", "path")
    else:
        _name = global_settings.get("config-paths.editor", "name")
        _path = global_settings.get("config-paths.editor", "path")

    _name += ".ini"

    if _path != "unchanged":
        _path = os.path.abspath(os.path.expanduser(_path))
    else:
        _path = THEMES_DIR if t == "theme" else EDITOR_DIR

    return CraftItems(_path, _name)


_theme_load = find_resource("theme")
_editor_config_load = find_resource("editor")
clrcall = ColorManager(customfilepath=_theme_load)

