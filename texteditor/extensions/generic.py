# For texteditor's local use only.
import os
import typing

from libtextworker.general import CraftItems, GetCurrentDir
from libtextworker.get_config import GetConfig
from libtextworker.interface import stock_ui_configs
from libtextworker.interface.tk import ColorManager
from libtextworker.versioning import is_development_version_from_project

from libtextworker import EDITOR_DIR, THEMES_DIR

CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version_from_project("texteditor") else ""
    )
)
configs = open(
    CraftItems(GetCurrentDir(__file__), "..", "data", "appconfig.ini"), "r"
).read()

# App settings
global_settings = GetConfig(configs, file=CONFIGS_PATH)

# Find theme resource

def find_resource(t: typing.Literal["theme", "editor"]) -> str:
    
    if t == "theme":
        _name = global_settings["config-paths.ui"]["theme"]
        _path = global_settings["config-paths.ui"]["path"]
    
    else:
        _name = global_settings["config-paths.editor"]["name"]
        _path = global_settings["config-paths.editor"]["path"]
    
    _name += ".ini"

    if _path != "unchanged":
        _path = os.path.abspath(os.path.expanduser(_path))
    else:
        _path = THEMES_DIR if t == "theme" else EDITOR_DIR
    
    return CraftItems(_path, _name)


clrcall = ColorManager(stock_ui_configs, _theme_load)

# Editor config

if _editor_config_name and _editor_config_path:
    _editor_config_name += ".ini"
    if _editor_config_name == "default":
        _editor_config_name = "editor"

    if _editor_config_path != "unchanged":
        _editor_config_load = CraftItems(_editor_config_path, _editor_config_name)
    else:
        _editor_config_load = CraftItems(EDITOR_DIR, _editor_config_name)
else:
    _editor_config_load = CraftItems(EDITOR_DIR, "editor.ini")
