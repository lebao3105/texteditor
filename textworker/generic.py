# For texteditor's local use only.
import builtins
import json
import logging
import os
import sys
import typing

from libtextworker.general import CraftItems, GetCurrentDir
from libtextworker.get_config import GetConfig
from libtextworker.interface import stock_ui_configs
from libtextworker.interface.wx import ColorManager
from libtextworker.versioning import is_development_version_from_project

from libtextworker import EDITOR_DIR, THEMES_DIR
import libtextworker
CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version_from_project("textworker") else ""
    )
)
DATA_PATH: str = CraftItems(GetCurrentDir(__file__), "data")
UIRC_DIR = CraftItems(GetCurrentDir(__file__), "ui")

clrcall: ColorManager
configs: str
_editor_config_load: str
_theme_load: str
global_settings: GetConfig
logger = logging.getLogger("textworker")

builtins.true = True
builtins.false = False
builtins.nil = None

moves = json.loads(open(CraftItems(GetCurrentDir(__file__), "merges.json")).read())

def find_resource(t: typing.Literal["theme", "editor"]) -> str:
    if t == "theme":
        _name = global_settings["config-paths.ui"]["theme"]
        _path = global_settings["config-paths.ui"]["path"]

    else:
        _name = global_settings["config-paths.editor"]["name"]
        _path = global_settings["config-paths.editor"]["path"]

    _name += ".ini"

    if _path != "unchanged":
        _path = os.path.normpath(os.path.expanduser(_path))
    else:
        print(THEMES_DIR, EDITOR_DIR)
        _path = THEMES_DIR if t == "theme" else EDITOR_DIR

    return CraftItems(_path, _name)


def ready():
    global _theme_load, _editor_config_load, clrcall, configs, global_settings
    
    configs = open(CraftItems(DATA_PATH, "appconfig.ini"), "r").read()
    global_settings = GetConfig(configs, file=CONFIGS_PATH)

    _theme_load = find_resource("theme")
    print(_theme_load)
    _editor_config_load = find_resource("editor")
    clrcall = ColorManager(stock_ui_configs, _theme_load)