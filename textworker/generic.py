import builtins
import json
import logging
import os
import typing

from libtextworker.general import CraftItems, GetCurrentDir
from libtextworker.get_config import GetConfig
from libtextworker.interface import stock_ui_configs, stock_editor_configs
from libtextworker.interface.wx import ColorManager
from libtextworker.versioning import is_development_version_from_project

from libtextworker import EDITOR_DIR, THEMES_DIR, TOPLV_DIR

currPath = GetCurrentDir(__file__)

CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version_from_project("textworker") else ""
    )
)
DATA_PATH: str = CraftItems(currPath, "data")
UIRC_DIR = CraftItems(currPath, "ui")

clrCall: ColorManager
configs: str

# TODO: Rename
# Seems nobody else than generic uses these variables, so cancelled.
_editor_config_load: str
_theme_load: str

global_settings: GetConfig
editorCfg: GetConfig
logger = logging.getLogger("textworker")

# C/C++ users belike:
builtins.true = True
builtins.false = False
builtins.nil = None

moves = json.loads(open(CraftItems(currPath, "merges.json")).read())


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

    logger.debug(f"Themes directory: {THEMES_DIR}")
    logger.debug(f"Editor settings directory: {EDITOR_DIR}")

    return CraftItems(_path, _name)


def ready():
    global _theme_load, _editor_config_load
    global clrCall, configs, global_settings, editorCfg
    global THEMES_DIR, EDITOR_DIR, TOPLV_DIR

    configs = open(CraftItems(DATA_PATH, "appconfig.ini"), "r").read()
    global_settings = GetConfig(configs, file=CONFIGS_PATH)

    TOPLV_DIR = os.path.dirname(CONFIGS_PATH)
    THEMES_DIR = TOPLV_DIR + "/themes/"
    EDITOR_DIR = TOPLV_DIR + "/editorconfigs/"

    _theme_load = find_resource("theme")
    _editor_config_load = find_resource("editor")

    clrCall = ColorManager(stock_ui_configs, _theme_load)
    editorCfg = GetConfig(stock_editor_configs, _editor_config_load)

    logger.info("Ready to go!")
