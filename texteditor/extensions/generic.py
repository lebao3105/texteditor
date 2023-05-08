# For texteditor's local use only.

import json
import logging
import os
import platform

from libtextworker import EDITOR_DIR, THEMES_DIR
from libtextworker.general import CraftItems, GetCurrentDir
from libtextworker.get_config import GetConfig
from libtextworker.interface.manager import default_configs
from libtextworker.interface.tk import ColorManager
from libtextworker.versioning import is_development_version_from_project


CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version_from_project("texteditor") else ""
    )
)
log = logging.getLogger("textworker")
configs = f"""
[config-paths]
    [config-paths.ui]
        theme = default
        path = unchanged
    [config-paths.editor]
        name = default
        path = unchanged

[editor]
    [editor.autosave]
        enable = yes
        time = 120
    [editor.tabs]
        move_tabs = yes
        middle_close = yes
        close_on_no_tab = no ; Close the program on last tab close - will override fun->allow_restore_notebook

[extensions]
    [extensions.textwkr.multiview]
        notebook_location = bottom
    
    [extensions.cmd]
        enable = yes
        term = {"cmd" if platform.system() == "Windows" else "xterm"}

[fun]
allow_restore_notebook = yes
"""

# App settings
global_settings = GetConfig(configs, file=CONFIGS_PATH)
global_settings.call = global_settings.getkey

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

clrcall = ColorManager(default_configs, _theme_load)

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
