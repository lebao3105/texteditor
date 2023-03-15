import pathlib
import platform
import wx
import wx.xml
import wx.xrc
import wx.adv

currdir = pathlib.Path(__file__).parent
UIRC_DIR = str(currdir / "ui")

from .backend import logger, configpath
from libtextworker import get_config
from libtextworker.general import CraftItems
from libtextworker.interface.wx.miscs import XMLBuilder

# Default configs
cfg = {}

## Interface
cfg["interface"] = {"color": "light", "autocolor": "yes", "textcolor": "default"}

cfg["interface.tabs"] = {
    "move_tabs": "yes",
    "middle_close": "no",
    "close_on_all_tabs": "no",
}

cfg["interface.font"] = {
    "style": "normal",
    "weight": "normal",
    "family": "default",
    "size": "normal",
}

## Editor
cfg["editor"] = {
    "indentation": "tabs",
    "size": "4",
    "autosave": "yes",
    "autosave_time": "120"
}

## Extensions
cfg["extensions.cmd"] = {"enable": "yes", "console": "xterm" if platform.system() != "Windows" else "cmd"}
# cfg["extensions.autosave"] = {"enable": "no", "time": "120"}
cfg["extensions.multiview"] = {"notebook_location": "bottom"}

## ----- ##

# Classes
class Error(Exception):
    def __init__(self, objname: str, title: str, msg: str, *args: object):
        fullmsg = "Object {} error: ({}) {}".format(objname, title, msg)
        log.throwerr(title, True, msg)
        super().__init__(fullmsg, *args)


class AppSettings(object):
    def __init__(
        self,
        cfg: dict = cfg,
        file: str = configpath,
        default_section: str = (item[0] for item in cfg),
        **kwds,
    ):
        self.cfg = get_config.GetConfig(
            cfg, file, default_section=default_section, **kwds
        )
        self.file = file

    def get_setting(self, *args, **kwds):
        return self.cfg.getkey(*args, **kwds)

    def set_setting(self, section, option, value):
        self.cfg.set(section, option, value)
        with open(self.file, "w") as f:
            self.cfg.write(f)

    def register_section(self, section_name, options: dict, write: bool=False):
        """
        Registers a new section on the configuration file.
        """
        self.cfg.add_section(section_name)
        for option in options:
            self.cfg.set(section_name, option, options[option])
        if write:
            self.cfg.write(open(self.file, "w"))

    def unregister_section(self, section_name, write: bool=False):
        """
        Unregisters a section on the configuration file.
        """
        self.cfg.remove_section(section_name)
        if write:
            self.cfg.write(open(self.file, "w"))


global_settings = AppSettings()
log = logger.Logger()

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
        self.Font.SetSelectedFont(global_settings.cfg._get_font())
        self.TextPreview = wx.xrc.XRCCTRL(self.Frame, "m_staticText6")
        global_settings.cfg.configure(self.TextPreview)

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
                global_settings.set_setting(
                    "interface",
                    "textcolor",
                    evt.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
                )
            ),
        )
        self.AppTheme.Bind(wx.EVT_CHOICE, self.SetTheme)

    def SelectFont(self, evt):
        selected_font = self.Font.GetSelectedFont()
        selected_color = self.Font.GetSelectedColour()

        style = selected_font.GetStyle()
        family = selected_font.GetFaceName()
        weight = selected_font.GetWeight()

        styles = {
            wx.FONTSTYLE_NORMAL: "normal",
            wx.FONTSTYLE_ITALIC: "italic",
        }

        weights = {
            wx.FONTWEIGHT_LIGHT: "light",
            wx.FONTWEIGHT_NORMAL: "normal",
            wx.FONTWEIGHT_SEMIBOLD: "semibold",
            wx.FONTWEIGHT_BOLD: "bold",
            wx.FONTWEIGHT_EXTRALIGHT: "maxlight",
            wx.FONTWEIGHT_EXTRABOLD: "maxbold",
        }

        global_settings.set_setting(
            "interface", "textcolor", selected_color.GetAsString(wx.C2S_HTML_SYNTAX)
        )
        global_settings.set_setting("interface.font", "weight", weights[weight])
        global_settings.set_setting("interface.font", "style", styles[style])
        global_settings.set_setting("interface.font", "family", family)

        self.TextPreview.SetFont(selected_font)

    def SetFontColor(self, evt):
        selected_item = self.FontColorChoices.GetStringSelection()
        self.ColorPicker.Enable(False)
        if selected_item == _("Default"):
            return global_settings.set_setting("interface", "textcolor", "default")
        elif selected_item == _("Red"):
            return global_settings.set_setting("interface", "textcolor", "red")
        elif selected_item == _("Green"):
            return global_settings.set_setting("interface", "textcolor", "green")
        elif selected_item == _("Custom"):
            self.ColorPicker.Enable()
            return

    def SetTheme(self, evt):
        selected_item = self.AppTheme.GetStringSelection()
        if selected_item == _("Dark"):
            return global_settings.set_setting("interface", "color", "dark")
        elif selected_item == _("Light"):
            return global_settings.set_setting("interface", "color", "light")
        elif selected_item == _("Automatic"):
            return global_settings.set_setting("interface", "autocolor", "yes")

    def Run(self):
        self.Frame.RunWizard(self.Page1)
        self.Frame.Destroy()


    