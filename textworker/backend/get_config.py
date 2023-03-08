import configparser
import threading
import darkdetect
import os
import os.path
import platform
import wx

from PIL import ImageColor
from . import constants, is_development_build

__all__ = [
    'defconsole',
    'file',
    'ConfigurationError',
    'GetConfig'
]

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
    "autosave_time": "120",
    "searchdir": ""
}

## Extensions
cfg["extensions.cmd"] = {"enable": "yes", "console": defconsole}
# cfg["extensions.autosave"] = {"enable": "no", "time": "120"}
cfg["extensions.multiview"] = {"notebook_location": "bottom"}


class ConfigurationError(Exception):
    def __init__(
        self, section: str = "", option: str = "", msg: str = "", *args: object
    ):
        prefix = "Error in the configuration file: "
        if not msg:
            msg = "*UNKNOW ERROR*"
        else:
            msg = "[{}->{}] : {}".format(
                section,
                "(None)" if option == "" else option,
                "No Message" if msg == "" else msg,
            )
        full = prefix + msg
        super().__init__(full, *args)


class GetConfig(configparser.ConfigParser):
    # Values
    yes_values: list = []
    no_values: list = []

    returnbool: bool = True
    aliases = {}
    detailedlogs: bool = True
    backups = {}

    # Functions
    setfontfn = {}
    setcolorfn = {}
    threads = []

    # "Protected" properties
    _yes_values = ["yes", "True"]
    _no_values = ["no", "False"]

    def __init__(self, config: dict, file: str, **kwds):
        """Customized configuration parser.
        :param config : Default configurations, used to reset the file or do some comparisions
        :param file : Configuration file
        :param default_section : Default section
        :param **kwds : To pass to configparser.ConfigParser (base class)

        When initialized, GetConfig loads all default configs (from config param) and store it in
        a dictionary for further actions (backup/restore file).

        How to use:
        * Just call it once for your project, pass everything needed to the contrucstor and do things
        your self!
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

    def reset(self, restore: bool = False) -> bool:
        try:
            os.remove(self.__file)
        except:
            return False
        else:
            for key in self.cfg:
                self[key] = self.cfg[key]

            if restore and self.backups:
                for key in self.backups:
                    self[key] = self.backups[key]

            with open(self.__file, mode="w") as f:
                self.write(f)
            return True

    # Options
    def backup(self, keys: dict, direct_to_keys: bool = False) -> dict:
        """
        Backs up user data, specified by the keys parameter (dictionary).
        Returns the successfully *updated* dictionary (if direct_to_keys param is True),
        or the self-made dict.
        """
        for key in keys:
            for subelm in keys[key]:
                if direct_to_keys == True:
                    keys[key][subelm] = self[key][subelm]
                    return keys
                else:
                    self.backups[key][subelm] = self[key][subelm]
                    return self.backups

    def getkey(self, section, option, needed: bool = False, restore: bool = False, noraiseexp: bool = False) -> str|bool:
        """
        Try to get the value of an option under the spectified section.

        If the option does not exist and needed parameter is set to True,
        GetConfig will add that option automatically with the value based on
        its previously initialized configs. If restore parameter is set to True,
        GetConfig will use the backed up option, if possible.

        If you don't want to see exceptions raised and just need False (when something went wrong),
        set noraiseexp to True.

        Otherwise it will check for the value's alias, then return the value.
        """
        if not section in self.sections():
            if needed == True:
                self.add_section(section)
            else:
                if noraiseexp != True:
                    raise ConfigurationError(section, msg="Section not found: %s" % section)
                else:
                    return False

        if not option in self[section]:
            if needed == True:
                if restore == True:
                    self.set(
                        section,
                        option,
                        self.backups[section][option]
                        if option in self.backups[section]
                        else self.cfg[section][option],
                    )
                else:
                    self.set(section, option, self[section][option])
            else:
                if noraiseexp != True:
                    raise ConfigurationError(
                        section, option, "Option not found: %s" % option
                    )
                else:
                    return False

        if needed == True:
            self.write(open(self.__file, "w"))

        value = self.get(section, option)

        # if self.returnbool == True:
        #     if value in self.yes_values or self._yes_values:
        #         return True
        #     elif value in self.no_values or self._no_values:
        #         return False
        # else:
        #     return value if value not in self.aliases else self.aliases[value]
        return value if value not in self.aliases else self.aliases[value]

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
    @property
    def GetFont(self):
        return self._get_font()

    @GetFont.setter
    def GetFont(self, func):
        self._get_font = func

    @GetFont.deleter
    def GetFont(self):
        self._get_font = print("Deleted object: GetConfig.GetFont/_get_font")

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

    @property
    def GetColor(self):
        return self._get_color()

    @GetColor.setter
    def GetColor(self, func):
        self._get_color = func

    @GetColor.deleter
    def GetColor(self):
        self._get_color = print("Deleted object: GetConfig.GetColor/_get_color")

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

        ##
        resv = {"light": "dark", "dark": "light"}

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
                fontcolor_ = colors[resv[color]]
            else:
                fontcolor_ = colors[resv[_get_sys_mode()]]
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

    def setcolorfunc(self, objname: str, func, params: dict):
        """
        Set wxPython widgets background color function.
        :param objname (str): Object name (for easier access)
        :param func (function): Function to set the background color (no arg)
        :param params (dict): Parameters to pass to func
        """
        self.setcolorfn[objname] = {"fn": func, "params": params}

    def setfontcfunc(self, objname: str, func, params: dict):
        """
        Set wxPython widgets background color function.
        :param objname (str): Object name (for easier access)
        :param func (function): Function to set the background color (no arg)
        :param params (dict): Parameters to pass to func
        """
        self.setfontfn[objname] = {"fn": func, "params": params}

    def configure(self, widget):
        """Configures a wxPython widget."""
        if not widget:
            print("Widget died, skip configuring.")
            return

        widget.SetFont(self._get_font())
        color, fontcolor = self._get_color()

        for item in self.setfontfn:
            fn = self.setfontfn[item]["fn"]
            if not self.setfontfn[item]["params"]:
                fn(fontcolor)
            else:
                fn(self.setfontfn[item]["params"], fontcolor)

        for item in self.setcolorfn:
            fn = self.setcolorfn[item]["fn"]
            if not self.setcolorfn[item]["params"]:
                fn(color)
            else:
                fn(self.setcolorfn[item]["params"], color)

        autocolor = self.getkey("interface", "autocolor")
        if autocolor == True and widget in self.threads:
            if not self.threads[widget].is_alive():
                self.threads[widget] = threading.Thread(
                    args=self.configure(widget), daemon=True
                )
                self.threads[widget].start()
