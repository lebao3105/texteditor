# For texteditor's local use only.
import os
import typing

from libtextworker.general import CraftItems, GetCurrentDir
from libtextworker.get_config import GetConfig
from libtextworker.interface import stock_ui_configs
from libtextworker.interface.tk import ColorManager
from libtextworker.versioning import is_development_version_from_project

from libtextworker import EDITOR_DIR, THEMES_DIR, TOPLV_DIR

CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version_from_project("texteditor") else ""
    )
)
DATA_PATH: str = CraftItems(GetCurrentDir(__file__), "..", "data")

clrcall: ColorManager
configs: str
_editor_config_load: str
_theme_load: str
global_settings: GetConfig


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
        _path = THEMES_DIR if t == "theme" else EDITOR_DIR

    return CraftItems(_path, _name)


def ready():
    global _theme_load, _editor_config_load
    global clrcall, configs, global_settings
    global THEMES_DIR, EDITOR_DIR, TOPLV_DIR

    configs = open(CraftItems(DATA_PATH, "appconfig.ini"), "r").read()
    global_settings = GetConfig(configs, file=CONFIGS_PATH)

    TOPLV_DIR = os.path.dirname(CONFIGS_PATH)
    THEMES_DIR = TOPLV_DIR + "/themes/"
    EDITOR_DIR = TOPLV_DIR + "/editorconfigs/"

    _theme_load = find_resource("theme")
    _editor_config_load = find_resource("editor")
    clrcall = ColorManager(stock_ui_configs, _theme_load)
