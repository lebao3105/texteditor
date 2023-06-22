import json
import logging
import os

import wx
import wx.xml
import wx.xrc
import wx.adv

from libtextworker import get_config, THEMES_DIR, EDITOR_DIR
from libtextworker.versioning import *
from libtextworker.general import CraftItems, GetCurrentDir, TOPLV_DIR
from libtextworker.interface.manager import default_configs
from libtextworker.interface.wx import ColorManager
from libtextworker.interface.wx.constants import FONTST, FONTWT
from libtextworker.interface.wx.miscs import XMLBuilder

currdir = GetCurrentDir(__file__, True)
UIRC_DIR = str(currdir / "ui")
logger = logging.getLogger("textworker")

# Config file path
configpath = TOPLV_DIR + "/configs{}.ini".format(
        "" if not is_development_version_from_project("textworker") else "_dev"
    )

# Default configs

## Early work.
## Because there is no sub-sections support here, so...
## Maybe switching to toml? Or not?
cfg = open(CraftItems(GetCurrentDir(__file__), "data", "appconfig.ini")).read()

# App settings
global_settings = get_config.GetConfig(cfg, file=configpath)

# Move old configs, if any
# (Compare with versions < 1.6a2)
moves = json.loads(open(CraftItems(GetCurrentDir(__file__), "merges.json")).read())

global_settings.move(moves)

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


# Classes
class Error(Exception):
    def __init__(self, objname: str, title: str, msg: str, *args: object):
        fullmsg = "Object {} error: ({}) {}".format(objname, title, msg)
        logger.exception(title + ":" + msg)  # Is it?
        super().__init__(fullmsg, *args)


class SettingsWindow(XMLBuilder):
    def __init__(self, Parent):
        super().__init__(Parent, CraftItems(UIRC_DIR, "preferences.xrc"), _)

        # Load initial items
        self.Frame = self.loadObject("Preferences", "wxWizard")
        self.Page1 = wx.xrc.XRCCTRL(self.Frame, "WelcomeScreen")
        self.Frame.SetPageSize((595, 424))

        # Images
        self.Img1 = wx.xrc.XRCCTRL(self.Frame, "m_bitmap1")
        self.Img2 = wx.xrc.XRCCTRL(self.Frame, "m_bitmap2")
        self.Img3 = wx.xrc.XRCCTRL(self.Frame, "m_bitmap3")

        self.Img1.SetBitmap(wx.Icon(str(currdir / "images" / "terminal.png")))
        self.Img2.SetBitmap(wx.Icon(str(currdir / "images" / "logs.png")))
        self.Img3.SetBitmap(wx.Icon(str(currdir / "images" / "configs.png")))

        # Font
        self.Font = wx.xrc.XRCCTRL(self.Frame, "m_fontPicker1")
        self.Font.SetSelectedFont(clrcall.GetFont)
        self.TextPreview = wx.xrc.XRCCTRL(self.Frame, "m_staticText6")
        clrcall.configure(self.TextPreview)

        # Color choices
        self.FontColorChoices = wx.xrc.XRCCTRL(self.Frame, "m_choice1")
        self.ColorPicker = wx.xrc.XRCCTRL(self.Frame, "m_colourPicker1")
        self.AppTheme = wx.xrc.XRCCTRL(self.Frame, "m_choice2")

        # Bind events
        self.Font.Bind(wx.EVT_FONTPICKER_CHANGED, self.SelectFont)
        self.FontColorChoices.Bind(wx.EVT_CHOICE, self.SetFontColor)
        self.ColorPicker.Bind(
            wx.EVT_COLOURPICKER_CHANGED,
            lambda evt: (
                clrcall.set_and_update(
                    "interface",
                    "textcolor",
                    evt.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
                )
            ),
        )
        self.AppTheme.Bind(wx.EVT_CHOICE, self.SetTheme)
        clrcall.configure(self.Page1, True)

    def SelectFont(self, evt):
        selected_font = self.Font.GetSelectedFont()
        selected_color = self.Font.GetSelectedColour()

        style = selected_font.GetStyle()
        family = selected_font.GetFaceName()
        weight = selected_font.GetWeight()

        styles = {val: key for key, val in FONTST}
        weights = {val: key for key, val in FONTWT}

        clrcall.set(
            "interface", "textcolor", selected_color.GetAsString(wx.C2S_HTML_SYNTAX)
        )
        clrcall.set("interface.font", "weight", weights[weight])
        clrcall.set("interface.font", "style", styles[style])
        clrcall.set("interface.font", "family", family)
        clrcall.update()
        self.TextPreview.SetFont(selected_font)

    def SetFontColor(self, evt):
        selected_item = self.FontColorChoices.GetStringSelection()
        self.ColorPicker.Enable(False)
        if selected_item == _("Default"):
            return clrcall.set_and_update("interface", "textcolor", "default")
        elif selected_item == _("Red"):
            return clrcall.set_and_update("interface", "textcolor", "red")
        elif selected_item == _("Green"):
            return clrcall.set_and_update("interface", "textcolor", "green")
        elif selected_item == _("Custom"):
            self.ColorPicker.Enable()
            return

    def SetTheme(self, evt):
        selected_item = self.AppTheme.GetStringSelection()
        if selected_item == _("Dark"):
            return clrcall.set_and_update("interface", "color", "dark")
        elif selected_item == _("Light"):
            return clrcall.set_and_update("interface", "color", "light")
        elif selected_item == _("Automatic"):
            return clrcall.set_and_update("interface", "autocolor", "yes")

    def Run(self, evt):
        self.Frame.RunWizard(self.Page1)
        self.Frame.Destroy()


# TODO: Move to libtextworker
# wxLog Formatter
class LogFormatter(wx.LogFormatter):
    def Format(level, msg, info):
        return "[%d] %s line %d : %s" % (info.threadId, info.filename, info.line, msg)
