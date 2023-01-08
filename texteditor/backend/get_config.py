import configparser
import os
import platform
import texteditor.backend
import traceback
import wx
from . import logger, constants

texteditor.backend.require_version("1.6a", ">=")

# Configuration file
if platform.system() == "Windows":
    file = os.environ["USERPROFILE"] + "\\.config\\texteditor_configs.ini"
    backup = os.environ["USERPROFILE"] + "\\.config\\texteditor_bck.ini"
    defconsole = "cmd"
else:
    file = os.environ["HOME"] + "/.config/texteditor_configs.ini"
    backup = os.environ["HOME"] + "/.config/texteditor_bck.ini"
    defconsole = "xterm"

# Default configs
cfg = {}

cfg["font"] = {
    "style": "normal",
    "weight": "normal",
    "family": "default",
    "size": "normal",
}

cfg["cmd"] = {"enable": "yes", "console": defconsole}


class GetConfig(configparser.ConfigParser):
    yes_value = "yes"
    no_value = "no"
    returnbool = True
    aliases: dict

    def __init__(self, config: dict, file: str, *args):
        """Customized configuration parser.
        :param config : Default configurations, used to reset the file or do some comparisions
        :param file : Configuration file
        :param *args : To pass to configparser.ConfigParser"""
        super().__init__(self, *args)
        self.cfg = {}
        for key in config:
            self.cfg[key] = config[key]
        self.read(file)
        self.file = file

    def getkey(self, section, option):
        value = self[section][option]
        if value == self.yes_value:
            if self.returnbool == True:
                return True
        elif value == self.no_value:
            if self.returnbool == True:
                return False
        elif value in self.aliases:
            return self.aliases[value]
        else:
            return value

    def aliasyesno(self, yesvalue, novalue, enable: bool = True):
        """Use a custom yes/no value, for example:
        There is an option under [section], and GetConfig will return\
        True if the options is 'yes', False if the options is 'no'.
        You can change 'yes' and 'no' value for your use.
        If you dont want the parser return a boolean, set enable to false."""
        self.yes_value = yesvalue
        self.no_value = novalue
        self.returnbool = enable
        return

    def alias(self, value, value2):
        self.aliases[value] = value2

    def reset(self, evt=None):
        try:
            os.remove(self.file)
        except:
            raise Exception(
                "Unable to reset configuration file - {}".format(traceback.format_exc())
            )
        else:
            for key in self.cfg:
                self[key] = self.cfg[key]
            with open(self.file, mode="w") as f:
                self.write(f)

    def _get_font(self):
        family = self.get("font", "family")
        size = self.get("font", "size")
        weight = self.get("font", "weight")
        style = self.get("font", "style")

        weight_ = constants.FONTWT[weight]
        style_ = constants.FONTST[style]

        if family == "default":
            family = ""

        if int(size):
            size_ = int(size)
        else:
            size_ = constants.FONTSZ[size]

        return wx.Font(size_, wx.FONTFAMILY_DEFAULT, style_, weight_, 0, family)
