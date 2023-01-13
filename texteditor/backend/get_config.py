import configparser
import os
import os.path
import pathlib
import platform
import texteditor.backend
import wx
from . import constants

texteditor.backend.require_version(1.6, "alpha")

# Configuration file
if platform.system() == "Windows":
    file = os.environ["USERPROFILE"] + "\\.config\\texteditor_configs.ini"
    defconsole = "cmd"
else:
    file = os.environ["HOME"] + "/.config/texteditor_configs.ini"
    defconsole = "xterm"

file = pathlib.Path(file)

if texteditor.backend.is_devlopment_build():
    file = (
        str(file).removesuffix("texteditor_configs.ini")
        / "texteditor"
        / "configs_dev.ini"
    )
    # file = pathlib.Path(file)

# Default configs
cfg = {}

cfg["interface"] = {"color": "light", "autocolor": "no", "textcolor": "default"}

cfg["interface.font"] = {
    "style": "normal",
    "weight": "normal",
    "family": "default",
    "size": "normal",
}

cfg["cmd"] = {"enable": "yes", "console": defconsole}

cfg["autosave"] = {"enable": "no", "time": "120"}


class GetConfig(configparser.ConfigParser):
    yes_value = "yes"
    no_value = "no"
    returnbool = True
    aliases: dict

    def __init__(self, config: dict, file: str, *args):
        """Customized configuration parser.
        :param config : Default configurations, used to reset the file or do some comparisions
        :param file : Configuration file
        :param *args : To pass to configparser.ConfigParser (base class)

        When initialized, GetConfig will load all default configs (config param) and store it in
        a dictionary for further actions (backup/restore file)"""
        super().__init__(self, *args)
        self.cfg = {}
        for key in config:
            self[key] = config[key]
            self.cfg[key] = config[key]
        self.readf(file)
        self.file = file

    def readf(self, file, encoding: str = None):
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

    def reset(self, evt=None):
        try:
            os.remove(self.file)
        except:
            raise Exception("Unable to reset configuration file!")
        else:
            for key in self.cfg:
                self[key] = self.cfg[key]
            with open(self.file, mode="w") as f:
                self.write(f)

    def getkey(self, section, option):
        value = self.get(section, option)
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

    def configure(self, widget):
        """Configures a wxPython widget."""
        return widget.SetFont(self._get_font())
