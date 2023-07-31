import builtins
import json
import logging
import typing

import wx
import wx.xml
import wx.xrc
import wx.adv

from libtextworker import get_config, THEMES_DIR, EDITOR_DIR
from libtextworker.general import CraftItems, GetCurrentDir, TOPLV_DIR
from libtextworker.interface.wx import ColorManager
from libtextworker.interface.wx.constants import FONTST, FONTWT
from libtextworker.interface.wx.miscs import XMLBuilder
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


"""
Classes.
"""

class Error(Exception):
    def __init__(self, objname: str, title: str, msg: str, *args: object):
        fullmsg = "Object {} error: ({}) {}".format(objname, title, msg)
        logger.exception(title + ":" + msg)  # Is it?
        super().__init__(fullmsg, *args)


class FirstRunWindow(XMLBuilder):
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
        self.Font.SetSelectedFont(clrcall.GetFont())
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
                    "color",
                    "foreground",
                    evt.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
                )
            ),
        )
        self.AppTheme.Bind(wx.EVT_CHOICE, self.SetTheme)
        clrcall.configure(self.Frame, true)

    def SelectFont(self, evt):
        selected_font = self.Font.GetSelectedFont()
        selected_color = self.Font.GetSelectedColour()

        style = selected_font.GetStyle()
        family = selected_font.GetFaceName()
        weight = selected_font.GetWeight()

        styles = {val: key for key, val in FONTST}
        weights = {val: key for key, val in FONTWT}

        clrcall.set(
            "color", "foreground", selected_color.GetAsString(wx.C2S_HTML_SYNTAX)
        )
        clrcall.set("font", "weight", weights[weight])
        clrcall.set("font", "style", styles[style])
        clrcall.set("font", "family", family)
        clrcall.update()
        self.TextPreview.SetFont(selected_font)

    def SetFontColor(self, evt):
        selected_item = self.FontColorChoices.GetStringSelection()
        self.ColorPicker.Enable(false)
        if selected_item == _("Default"):
            return clrcall.set_and_update("color", "foreground", "default")
        elif selected_item == _("Red"):
            return clrcall.set_and_update("color", "foreground", "red")
        elif selected_item == _("Green"):
            return clrcall.set_and_update("color", "foreground", "green")
        elif selected_item == _("Custom"):
            self.ColorPicker.Enable()
            return

    def SetTheme(self, evt):
        selected_item = self.AppTheme.GetStringSelection()
        if selected_item == _("Dark"):
            return clrcall.set_and_update("color", "background", "dark")
        elif selected_item == _("Light"):
            return clrcall.set_and_update("color", "background", "light")
        elif selected_item == _("Automatic"):
            return clrcall.set_and_update("color", "auto", "yes")

    def Run(self, evt):
        self.Frame.RunWizard(self.Page1)
        self.Frame.Destroy()
