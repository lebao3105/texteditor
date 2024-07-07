import json
import logging
import os
import typing

from libtextworker.general import CraftItems, GetCurrentDir, Logger, formatter, strhdlr
from libtextworker.get_config import GetConfig
from libtextworker.interface import stock_ui_configs, stock_editor_configs
from libtextworker.interface.wx import ColorManager
from libtextworker.versioning import is_development_version_from_project
from libtextworker import EDITOR_DIR, THEMES_DIR, TOPLV_DIR


currPath = GetCurrentDir(__file__, True)
clrCall: ColorManager
configs: str

_editor_config_load: str
_theme_load: str

global_settings: GetConfig
editorCfg: GetConfig

# Setup a logger
logger = Logger("textworker", logging.INFO)
logger.UseGUIToolKit("wx")
logging.captureWarnings(True)

## Log to file
filehdlr = logging.FileHandler(os.path.expanduser("~/.logs/textworker.log"))
filehdlr.setFormatter(formatter)

logger.addHandler(filehdlr)
logger.addHandler(strhdlr)

# Settings system changes
moves = json.loads(open(CraftItems(currPath, "merges.json")).read())

CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version_from_project("textworker") else ""
    )
)
DATA_PATH: str = str(currPath / "data")
UIRC_DIR: str = str(currPath / "ui")

def find_resource(t: typing.Literal["ui", "editor"]) -> str:
    _name = global_settings[f'config-paths.{t}']['name' if t == "editor" else "theme"]
    _path = global_settings[f'config-paths.{t}']['path']

    _name += ".ini"

    if _path != "unchanged":
        _path = os.path.normpath(os.path.expanduser(_path))
    else:
        _path = THEMES_DIR if t == "ui" else EDITOR_DIR

    return CraftItems(_path, _name)

def ready():
    """
    Get ready for the application window to start.
    It must be ran before the main window module import.
    """
    global _theme_load, _editor_config_load
    global clrCall, configs, global_settings, editorCfg
    global THEMES_DIR, EDITOR_DIR, TOPLV_DIR

    configs = open(CraftItems(DATA_PATH, "appconfig.ini"), "r").read()

    global_settings = GetConfig(defaults=configs, load=CONFIGS_PATH)

    TOPLV_DIR = os.path.dirname(CONFIGS_PATH)
    EDITOR_DIR = CraftItems(TOPLV_DIR, "editorconfigs")
    THEMES_DIR = CraftItems(TOPLV_DIR, "themes")

    logger.info(f"Settings path: {CONFIGS_PATH}")
    logger.info(f"Application datas (icon, updater, default settings) are stored in {DATA_PATH}")

    _theme_load = find_resource("ui")
    _editor_config_load = find_resource("editor")

    logger.info(f"Themes directory: {THEMES_DIR}")
    logger.info(f"Editor settings directory: {EDITOR_DIR}")

    clrCall = ColorManager(default_configs=stock_ui_configs, customfilepath=_theme_load)
    editorCfg = GetConfig(defaults=stock_editor_configs, load=_editor_config_load)

    import wx.stc
    logger.debug("Setting background + foregroud functions for editors...")
    
    clrCall.setcolorfunc(wx.stc.StyledTextCtrl, "StyleSetBackground",
                         {"style": wx.stc.STC_STYLE_DEFAULT,
                         "back":"%(color)"})
    clrCall.setfontcfunc(wx.stc.StyledTextCtrl, "StyleSetForeground",
                         {"style": wx.stc.STC_STYLE_DEFAULT,
                         "fore":"%(font)"})
    clrCall.setcolorfunc(wx.stc.StyledTextCtrl, "StyleSetSpec",
                         {"styleNum": wx.stc.STC_STYLE_DEFAULT, "spec": "fore:%(font),back:%(color)"})
    
    # clrCall.setfontandcolorfunc(wx.stc.StyledTextCtrl, "StyleSetSpec",
    #                             (wx.stc.STC_STYLE_DEFAULT, "fore:%(font),back:%(color)"))

    # clrCall.setfontandcolorfunc(wx.stc.StyledTextCtrl, "StyleSetSpec",
    #                             (wx.stc.STC_STYLE_LINENUMBER, "fore:%(font),back:%(color)"))
    # t = dict(clrCall)
    logger.info("Ready to go!")
