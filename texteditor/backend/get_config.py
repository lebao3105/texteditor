import configparser
import darkdetect
import os
import packaging.version
import pathlib
import sys
import sv_ttk
import threading

from tkinter import TclError, font, messagebox
from texteditor.backend import (
    constants,
    logger,
    require_version,
    __version__,
    is_development_build,
)

require_version("1.4a", ">=")
# backend.require_version("1.6a", "<") # Why the heck require_version stops at ctype == ">=" or ">" ?


# The location of the configuration file
# In older versions, it is stored in <home folder>/.config/texteditor
# In 1.4, there are 2 files for branch stable and dev - config(_dev).ini.
# and it can be overwriten by other version - especially wip/wx builds.
# Now I store the configs under a subfolder for specific versions (NOT builds yet).
if sys.platform == "win32":
    dird = os.environ["USERPROFILE"] + "\\.config\\texteditor\\"
    defconsole = "cmd"
else:
    dird = os.environ["HOME"] + "/.config/texteditor/"
    defconsole = os.environ["TERM"]


def createdir(dirname):
    if not os.path.exists(dirname):
        return os.mkdir(dirname)
    else:
        return "break"


createdir(dird.removesuffix("texteditor"))
createdir(dird)

appver = packaging.version.parse(__version__)
createdir(dird + appver.base_version)

# Not all configs on dev builds are complete.
file = dird + appver.base_version
if is_development_build():
    file = str(pathlib.Path(file) / "configs_dev.ini")
else:
    file = str(pathlib.Path(file) / "configs.ini")

# print(file)

# --- #

# Init.
log = logger.GenericLogs()

cfg = {
    "global": {
        "color": "light",
        "sub_color": "default",
        "autocolor": "yes",
        "font": "default",
        "font_size": "12",
    },
    "cmd": {"defconsole": defconsole, "isenabled": "yes"},
    "filemgr": {"autosave": "yes", "autosave-time": "120"},
}

# --- #


class GetConfig(configparser.ConfigParser):
    def __init__(self, cfgs: dict[str, str], filepath: str, **kwds):
        """
        Changes Tkinter/TTK widget configurations from a configuration file.
        :param cfgs (dict): Default configurations
        :param filepath (str): File path
        :param default_section (str): Default section on the configuration file (default is the first child of cfgs)
        :param **kwds (dict): Other options - they will be passed to configparser.ConfigParser.
        """
        kwds["default_section"] = kwds.get("default_section", list(cfgs.keys())[0])

        self.backup = {}
        self.backup2 = {}
        print('here')
        super().__init__(**kwds)

        for key in cfgs:
            self.backup[key] = cfgs[key]
            # self[key] = cfgs[key]

        self.readf(filepath)
        self.filepath = filepath
            
    def readf(self, file, encoding: str | None = None):
        print('reached there')
        if os.path.isfile(file):
            self.read(file, encoding)
        else:
            print('here too')
            with open(file, mode="w") as f:
                self.write(f)
                print('good!')
                self.read(file, encoding)
                print('omg!')
            del f

    def backupvalue(self, values: dict):
        for key in values:
            self.backup2[key] = self[key]

    def reset(self, restore_backup: bool = False):
        try:
            os.remove(self.filepath)
        except OSError:
            log.ConfigurationError(_("Unable to delete the configuration file"))
        else:
            self.read_dict(self.backup)
            if restore_backup:
                if not self.backup2:
                    log.throwwarn(
                        _("Configuration warning"),
                        _("Backed-up user options not found"),
                    )
                else:
                    for key in self.backup2:
                        self[key] = self.backup2[key]

            with open(self.filepath, "w") as f:
                self.write(f)
                log.throwinf(_("Success"), _("Restored all configurations."))

    def checkclass(self, widget):
        wind = ["Tk", "Frame", "TopLevel"]
        text = ["Label", "Text"]
        ttk_widgets = ["TCombobox", "Button"]

        # Combine 3 arrays together
        for it in text:
            wind.append(it)
        for it2 in ttk_widgets:
            wind.append(it2)

        class_name = type(widget).__name__
        if class_name in (wind or cfg.sections()):
            return class_name
        else:
            return False

    def getvalue(self, section: str, name: str):
        if not section in self.sections():
            return log.ConfigurationError("Section %s not found" % section)
        elif not self[section][name]:
            return log.ConfigurationError("Option [%s->%s] not found" % section, name)
        else:
            return self.get(section, name)

    def change_config(self, section: str, option: str, value: str | int):
        self.set(section, option, str(value))
        with open(file, "w") as filed:
            try:
                self.write(filed)
            except:
                log.ConfigurationError(
                    "Unable to write new configuration! (make %s->%s use %s)" % section,
                    option,
                    value,
                )
                return False
            finally:
                log.throwinf("Changed texteditor configuration.")
                return True

    @property
    def checkfont(self):
        return self._checkfont()

    @checkfont.setter
    def checkfont(self, func):
        self._checkfont = func

    def _checkfont(self):
        # Get values
        font_type = self.getvalue("global", "font")
        font_size = self.getvalue("global", "font_size")

        if not int(font_size):
            messagebox.showwarning(
                _("Warning"),
                _(
                    "Wrong font size defined on the configuration file - the program will use font size 14."
                ),
            )
            font_size = "14"
        elif int(font_size) <= 11:
            messagebox.showwarning(
                _("Warning"),
                _("The defined font size is smaller (or equal) than 10."),
            )

        font_families = font.families()
        if font_type == "default":
            font_type = "Consolas"
        else:
            if font_type not in font_families:
                if (
                    not isshown
                ):  # To prevent the application from showing the message box after open a new tab
                    messagebox.showwarning(
                        message=_("Wrong font type in the configuration file.")
                    )
                    isshown = True
                font_type = "Consolas"

        return font_type, font_size

    @property
    def get_color(self):
        return self._get_color()

    @get_color.setter
    def get_color(self, func):
        self._get_color = func

    def _get_color(self):
        """
        Get UI color.
        * background color: [global][color]
        * font color: [global][sub_color]
        * autocolor: [global][autocolor]
        :return tuple[str, str, bool] : (background color, font color, autocolor mode)
        """
        color = self.getvalue("global", "color")
        fontcolor = self.getvalue("global", "sub_color")
        autocolor = self.getvalue("global", "autocolor")
        colormode_auto: bool = False

        colors = {"light": constants.LIGHT_BG, "dark": constants.DARK_BG}

        fontcolors = {"green": constants.GREEN_TEXT, "red": constants.RED_TEXT}

        reserve_colors = {"light": constants.DARK_BG, "dark": constants.LIGHT_BG}

        # Default colors will be based on the system color
        colors["default"] = colors[darkdetect.theme().lower()]
        fontcolors["default"] = reserve_colors[darkdetect.theme().lower()]

        if autocolor == "yes":
            colormode_auto = True
        else:
            colormode_auto = False

        # ConfigParser, in somehow called our properties and raise KeyError while
        # The configs are not parsed. That's why we have this.
        # Also for some case the values really does not exist.
        if color and fontcolor and colormode_auto:
            return colors[color], fontcolors[fontcolor], colormode_auto
        else:
            return colors["default"], fontcolors["default"], False

    def configure(self, widget, childs_too: bool = False):
        """
        Configures (a) (Themed-) Tkinter widget.
        TODO: AutoColor.
        :param widget : Target widget to theme it
        :param childs_too (bool=False) : Is this function can also apply configs to the widget's
            childrens? Default to False to avoid TCLError, which occurs on invalid configuration v.v..
        """

        def _configure(target):
            classname = self.checkclass(target)
            font_type, font_size = self._checkfont()
            color, fontcolor, automode = self._get_color()

            if classname not in ["Tk", "Frame", "TopLevel", "Button"]:
                if font_type and font_size != None:
                    target.configure(font=(font_type, int(font_size)))
                if automode == True:
                    threading.Thread(
                        target=darkdetect.listener,
                        args=lambda output: _configure(target),
                        daemon=True,
                    ).start()
                sv_ttk.set_theme(darkdetect.theme().lower())
                try:
                    target.configure(fg=fontcolor)
                    target.configure(bg=color)
                except TclError:
                    target.configure(foreground=fontcolor)
                    target.configure(background=color)

        if childs_too == True:
            for child in widget.winfo_children():
                _configure(child)
        _configure(widget)
