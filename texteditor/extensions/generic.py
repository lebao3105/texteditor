# For texteditor's local use only.
import os

from libtextworker import EDITOR_DIR, THEMES_DIR
from libtextworker.general import CraftItems, GetCurrentDir
from libtextworker.get_config import GetConfig
from libtextworker.interface import stock_ui_configs
from libtextworker.interface.tk import ColorManager
from libtextworker.versioning import is_development_version_from_project


CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version_from_project("texteditor") else ""
    )
)
configs = (
    open(CraftItems(GetCurrentDir(__file__), "..", "data", "appconfig.ini"), "r")
    .read()
)

# App settings
global_settings = GetConfig(configs, file=CONFIGS_PATH)

# Find theme resource
_theme = global_settings["config-paths.ui"]["theme"]
_theme_path = global_settings["config-paths.ui"]["path"]

if _theme_path and _theme:
    _theme += ".ini"
    if _theme_path != "unchanged" and "none":
        _theme_load = CraftItems(_theme_path, _theme)
    else:
        _theme_load = CraftItems(THEMES_DIR, _theme)
else:
    _theme_load = CraftItems(THEMES_DIR, "default.ini")

clrcall = ColorManager(stock_ui_configs, _theme_load)

# Editor config
_editor_config_name = global_settings["config-paths.editor"]["name"]
_editor_config_path = global_settings["config-paths.editor"]["path"]

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
