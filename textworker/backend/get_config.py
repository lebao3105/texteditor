import configparser
import darkdetect
import os
import os.path
import platform
import wx

from PIL import ImageColor
from . import constants, require_version, is_development_build

require_version("1.6a", ">=")

# Configuration file
if platform.system() == "Windows":
    dir_to_use = os.environ["USERPROFILE"] + "\\.config\\texteditor\\"
    defconsole = "cmd"
else:
    dir_to_use = os.environ["HOME"] + "/.config/texteditor/"
    defconsole = "xterm"

if is_development_build():
    file = dir_to_use + "configs_dev.ini"
else:
    file = dir_to_use + "configs.ini"

# Default configs
cfg = {}

cfg["interface"] = {"color": "light", "autocolor": "yes", "textcolor": "default"}
cfg["interface.tabs"] = {"side": "default", "move_tabs": "yes", "middle_close": "no", "close_on_all_tabs": "no"}

cfg["interface.font"] = {
    "style": "normal",
    "weight": "normal",
    "family": "default",
    "size": "normal",
}

cfg["extensions.cmd"] = {"enable": "yes", "console": defconsole}

cfg["extensions.autosave"] = {"enable": "no", "time": "120"}
cfg["extensions.multiview"] = {"notebook_location": "bottom"}


class ConfigurationError(Exception):
    def __init__(
        self, section: str = "", option: str = "", msg: str = "", *args: object
    ):
        prefix = "Error in the configuration file: "
        if not msg:
            msg = "*UNKNOW ERROR*"
        else:
            msg = "[{}->{}] : {}".format(section, "(None)" if option == "" else option, "No Message" if msg == "" else msg)
        full = prefix + msg
        super().__init__(full, *args)


class GetConfig(configparser.ConfigParser):
    # Values
    yes_value: list = ["yes"]
    no_value: list = ["no"]
    returnbool = True
    aliases = {}

    # Functions
    setfontfn = {}
    setcolorfn = {}

    def __init__(self, config: dict, file: str, **kwds):
        """Customized configuration parser.
        :param config : Default configurations, used to reset the file or do some comparisions
        :param file : Configuration file
        :param **kwds : To pass to configparser.ConfigParser (base class)

        When initialized, GetConfig loads all default configs (from config param) and store it in
        a dictionary for further actions (backup/restore file).

        How to use:
        * Just call it once for your project, pass everything needed to the contrucstor and do things
        your self!
        * Always set default_section to one of your section (in str format)
        * Configure function is used to config wxPython widgets - so override it if needed

        For the configure function (must do):
        * Use setcolorfunc function to set the color (background)-set function
        * Use setfontcfunc function to set the font color(foreground)-set function

        Both of them will be used in configure function.
        """
        super().__init__(**kwds)

        self.cfg = {}

        for key in config:
            self[key] = config[key]
            self.cfg[key] = config[key]

        self.readf(file)
        self.__file = file

    # File tasks
    def readf(self, file, encoding: str | None = None):
        if os.path.isfile(file):
            self.read(file, encoding)
        else:
            with open(file, mode="w") as f:
                try:
                    self.write(f)
                except OSError:
                    raise Exception("Unable to access to the file name %s" % file)
                else:
                    self.read(file, encoding)
            del f

            # raise Exception("Unable to read configuration file")

    def reset(self, evt=None) -> bool:
        try:
            os.remove(self.__file)
        except:
            return False
        else:
            for key in self.cfg:
                self[key] = self.cfg[key]
            with open(self.__file, mode="w") as f:
                self.write(f)
            return True

    # Options
    def getkey(self, section, option, needed:bool = False):
        """
        Try to get the value of an option under the spectified section.
        
        If the option does not exist and needed parameter is set to True,
        GetConfig will add that option automatically with the value based on
        its previously initialized backup configs.

        Otherwise it will check for the value's alias, then return the value.
        """
        try:
            value = self.get(section, option)
        except KeyError or configparser.NoOptionError:
            if needed == True:
                self.set(section, option, self.cfg[section][option])
            else:
                raise ConfigurationError(section, option, "No option found ({})".format(option))
        except configparser.NoSectionError:
            if needed == True:
                self.add_section(section)
                self.set(section, option, self.cfg[section][option])
            else:
                raise configparser.NoSectionError(section)
        else:
            pass

        if value in self.yes_value:
            if self.returnbool == True:
                return True
        elif value in self.no_value:
            if self.returnbool == True:
                return False
        elif value in self.aliases:
            return self.aliases[value]
        else:
            return value

    def aliasyesno(self, yesvalue, novalue, enable: bool = True) -> None:
        """
        Use a custom yes/no value, for example:
        There is an option under [section], and GetConfig will return
        True if the options is 'yes', False if the options is 'no'.
        You can change 'yes' and 'no' value for your use.
        If you dont want the parser return a boolean, set enable to false.
        """
        self.yes_value = yesvalue
        self.no_value = novalue
        self.returnbool = enable

    def alias(self, value, value2) -> None:
        self.aliases[value] = value2

    # Configure widgets
    def _get_font(self):
        family = self.get("interface.font", "family")
        size = self.get("interface.font", "size")
        weight = self.get("interface.font", "weight")
        style = self.get("interface.font", "style")

        weight_ = constants.FONTWT[weight]
        style_ = constants.FONTST[style]

        if family == "default":
            family = ""

        try:
            int(size)
        except ValueError:
            size_ = constants.FONTSZ[size]
        else:
            size_ = int(size)

        return wx.Font(size_, wx.FONTFAMILY_DEFAULT, style_, weight_, 0, family)
    

    def _get_color(self):
        def _get_sys_mode():
            return darkdetect.theme().lower()

        # Get values
        color = self.getkey("interface", "color")
        fontcolor = self.getkey("interface", "textcolor")
        autocolor = self.getkey("interface", "autocolor")

        # Interface color
        ## Default color modes
        colors = {
            "light": "#ffffff",
            "dark": "#1c1c1c",
        }

        ## Check
        if autocolor == True:
            color_ = colors[_get_sys_mode()]
        elif color in colors:
            color_ = colors[color]

        # Text color
        colors["green"] = "#00ff00"
        colors["red"] = "#ff0000"
        if fontcolor == "default":
            if autocolor == False:
                if color == "light":
                    fontcolor_ = colors["dark"]
                elif color == "dark":
                    fontcolor_ = colors["light"]
            else:
                if _get_sys_mode() == "dark":
                    fontcolor_ = colors["light"]
                else:
                    fontcolor_ = colors["dark"]
        else:
            if fontcolor in colors:
                fontcolor_ = colors[fontcolor]
            elif fontcolor.startswith("#") and len(fontcolor) == 7:
                try:
                    ImageColor.getrgb(fontcolor)
                except ValueError:
                    raise ConfigurationError(
                        "interface", "textcolor", "Invalid color name/code"
                    )
                else:
                    fontcolor_ = fontcolor
            else:
                raise ConfigurationError(
                    "interface", "textcolor", "Invalid color name/code"
                )

        return ImageColor.getrgb(color_), ImageColor.getrgb(fontcolor_)

    def setcolorfunc(self, objname: str, obj, func: str, params):
        self.setcolorfn[objname] = {}
        self.setcolorfn[objname]["obj"] = obj
        self.setcolorfn[objname]["fn"] = func
        self.setcolorfn[objname]["params"] = params

    def setfontcfunc(self, objname: str, obj, func: str, params):
        self.setfontfn[objname] = {}
        self.setfontfn[objname]["obj"] = obj
        self.setfontfn[objname]["fn"] = func
        self.setfontfn[objname]["params"] = params

    def configure(self, widget):
        """Configures a wxPython widget."""
        widget.SetFont(self._get_font())
        color, fontcolor = self._get_color()

        for item in self.setfontfn:
            if self.setfontfn[item]["obj"] == widget:
                fn = getattr(self.setfontfn[item]["obj"], self.setfontfn[item]["fn"])
                if not self.setfontfn[item]["params"]:
                    fn(fontcolor)
                else:
                    fn(self.setfontfn[item]["params"], fontcolor)

        for item in self.setcolorfn:
            if self.setcolorfn[item]["obj"] == widget:
                fn = getattr(self.setcolorfn[item]["obj"], self.setcolorfn[item]["fn"])
                if not self.setcolorfn[item]["params"]:
                    fn(color)
                else:
                    fn(self.setcolorfn[item]["params"], color)
