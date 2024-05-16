"""
@package textworker.generic
@brief Stores most internal and public variables for the project.
"""

import json
import logging
import os
import typing

from jsonschema import validate
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
    "~/.config/textworker/configs{}.json".format(
        "_dev" if is_development_version_from_project("textworker") else ""
    )
)
DATA_PATH: str = str(currPath / "data")
UIRC_DIR: str = str(currPath / "ui")

def find_resource(t: typing.Literal["ui", "editor"]) -> str:
    _name = eval(global_settings['config-paths'][t])['name']
    _path = eval(global_settings['config-paths'][t])['path']

    _name += ".ini"

    if _path != "unchanged":
        _path = os.path.normpath(os.path.expanduser(_path))
    else:
        _path = THEMES_DIR if t == "theme" else EDITOR_DIR

    return CraftItems(_path, _name)

# THIS IS PAIN THIS IS PAIN
def defaults_from_schema() -> tuple[str, dict]:
    """
    Creates a dictionary of the application's defaults from the current JSON schema.
    """

    result = {}
    data = json.loads(open(CraftItems(DATA_PATH, "schema")).read())

    def get_defaults(iterable):
        if not 'properties' in iterable:
            return iterable['default'] if 'default' in iterable else ''
        res = {}
        for property in iterable['properties']:
            res[property] = iterable['properties'][property]['default']
        return res
    
    result['base'] = get_defaults(data['properties']['base']).copy()
    for tp in [('config-paths', ['ui', 'editor']),
               ('editor', ['searchdir', 'autosave', 'tabs']),
               ('extensions', ['multiview'])]:
        for i in range(len(tp[1])):
            if not tp[0] in result: result[tp[0]] = {}
            result[tp[0]][tp[1][i]] = get_defaults(data['properties'][tp[0]]['properties'][tp[1][i]])
    
    return data, result

def ready():
    """
    Get ready for the application window to start.
    It must be ran before the main window module import.
    """
    global _theme_load, _editor_config_load
    global clrCall, configs, global_settings, editorCfg
    global THEMES_DIR, EDITOR_DIR, TOPLV_DIR

    schema, configs = defaults_from_schema()

    if os.path.isfile(CONFIGS_PATH) and (content := open(CONFIGS_PATH).read()):
        if content.startswith('{'):
            content = json.loads(content)
            validate(content, schema)
        global_settings = GetConfig(defaults=configs, load=content)
    else:
        global_settings = GetConfig(defaults=configs, load=configs)

    global_settings._file = CONFIGS_PATH
    global_settings.update()

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
    t = dict(global_settings)
    logger.info("Ready to go!")
