import configparser
import os
import platform
import threading
from tkinter import TclError, font, messagebox

import darkdetect
import sv_ttk

from . import constants

if platform.system() == "Windows":
    file = os.environ["USERPROFILE"] + "\\.config\\texteditor_configs.ini"
    backup = os.environ["USERPROFILE"] + "\\.config\\texteditor_bck.ini"
    defconsole = "cmd"
else:
    file = os.environ["HOME"] + "/.config/texteditor_configs.ini"
    backup = os.environ["HOME"] + "/.config/texteditor_bck.ini"
    defconsole = "xterm"

cfg = configparser.ConfigParser()

# Default variables.
# We must use cfg.get() to get the current variable's value.
cfg["global"] = {
    "color": "light",
    "sub_color": "default",
    "autocolor": "yes",
    "font": "default",
    "font_size": "12",
}

# An old configuration
cfg["popups"] = {
    # TODO/NOTE: They should be different
    "width": str(constants.DEFAULT_OTHERS_WIGHT),
    "height": str(constants.DEFAULT_OTHERS_WIGHT),
}

cfg["cmd"] = {"defconsole": defconsole, "isenabled": "yes"}

# New: Auto-save files
cfg["filemgr"] = {"autosave": "yes", "autosave-time": "150"}  # in seconds

cfg["versioning"] = {"version": "1.4", "branch": "dev"}

# File write/backup
with open(backup, "w") as f2:
    cfg.write(f2)
with open(backup, "r") as f:
    bck = f.read()

if not os.path.isfile(file):
    try:
        with open(file, "w") as f:
            cfg.write(f)
    except:
        raise Exception("Unable to write configuration file!")

cfg.read(file)

bg = cfg.get("global", "color")
fg = cfg.get("global", "sub_color")

autocolormode = False

# OK, so this class only able to change some configuration? Can we use more?
class GetConfig:
    """Changes Tkinter/TTK widget configuration from the configuration file."""

    def __init__(self, parent=None, action: str = None):
        """parent: Widget to use\n
        action:str=None: |\n
        --> config : Configure the widget\n
        --> reset : Reset the configuration file\n
        If you use config, you must include parent also."""
        super().__init__()
        if parent == None or "":
            if action == "reset":
                self.reset()

        if action != None or "":
            if action == "config":
                GetConfig.configure(parent)
            elif action == "reset":
                GetConfig.reset()

    @staticmethod
    def reset():
        if not bck:
            print(
                "Error: Unable to reset configuration file: Backed up default variables not found"
            )
            return False
        try:
            os.remove(file)
            with open(file, "w") as f:
                f.write(bck)
        except OSError as e:
            messagebox.showerror(
                "Error occured while writing contents to the file", str(e)
            )
            return
        finally:
            print("Completed resetting texteditor configuration file.")
            return True

    @staticmethod
    def checkclass(widget):
        wind = ["Tk", "Frame", "TopLevel"]
        text = ["Label", "Text"]
        ttk_widgets = ["TCombobox", "Button"]

        # Combine 3 arrays together
        for it in text:
            wind.append(it)
        for it2 in ttk_widgets:
            wind.append(it2)

        class_name = widget.winfo_class()
        if class_name in (wind or cfg.sections()):
            return class_name
        else:
            return False

    @staticmethod
    def configure(widget):
        """Configures the selected widget.
        This function is used for texteditor with
        _checkfont, so please make your own function."""
        classname = GetConfig.checkclass(widget)
        colormger = AutoColor(widget)
        if classname is not False:
            if classname not in ["Tk", "Frame", "TopLevel", "Button"]:
                font_type, font_size = GetConfig._checkfont(GetConfig)
                if font_type and font_size is not None:
                    widget.configure(font=(font_type, int(font_size)))
            colormger.changecolor()

    @staticmethod
    def change_config(section: str, option: str, value: str | int, event=None):
        cfg.set(section, option, str(value))
        try:
            with open(file, "w") as filed:
                cfg.write(filed)
        except:
            print("Unable to write new configuration!")
            print(
                "Detail: make section %s->option %s to use value %s"
                % (section, option, value)
            )
            return False
        finally:
            print("Changed texteditor configuration.")
            return True

    def _checkfont(self):
        # Get values
        font_type = self.getvalue("global", "font")
        font_size = self.getvalue("global", "font_size")

        if not int(font_size):
            messagebox.showwarning(
                "Warning",
                "Wrong font size defined on the configuration file - the program will use font size 14.",
            )
            font_size = "14"
        elif int(font_size) <= 11:
            messagebox.showwarning(
                "Warning", "The defined font size is smaller (or equal) than 10."
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
                        message="Wrong font type in the configuration file."
                    )
                    isshown = True
                font_type = "Consolas"

        return font_type, font_size

    @staticmethod
    def getvalue(section: str, name: str):
        if not section in cfg.sections():
            raise Exception("Section %s not found" % section)
        elif not cfg[section][name]:
            raise Exception("%s->%s not found" % section, name)
        else:
            return cfg.get(section, name)


class AutoColor:
    """The color manager for texteditor."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.autocolor = GetConfig.getvalue("global", "autocolor")
        self.start = autocolormode
        self.bg = GetConfig.getvalue("global", "color")
        self.fg = GetConfig.getvalue("global", "sub_color")
        self.colors = {"light": str(constants.DARK_BG), "dark": str(constants.LIGHT_BG)}
        if self.bg == "default":
            self.bg = "light"
        if self.fg == "default":
            self.fg = "dark"

    def startasync(self):
        if self.start is True:
            # Automatically changes the theme if
            # the system theme is CHANGED
            self.t = threading.Thread(target=darkdetect.listener, args=(self.setcolor,))
            self.t.daemon = True
            self.t.start()
            self.setcolor(darkdetect.theme())
            return
        else:
            self.start = True

    def stopasync(self):
        if hasattr(self, "t"):
            del self.t

    def changecolor(self):
        if self.start is True:
            self.startasync()
            # return
        else:
            self.setcolor()

    def setcolor(self, color: str = None):
        fg = self.__checkcolor(str(darkdetect.theme()).lower())
        if color is not None:
            sv_ttk.set_theme(color.lower())
        else:
            if self.autocolor == "yes":
                sv_ttk.set_theme(str(darkdetect.theme()).lower())
            else:
                theme = self.bg
                fg = self.colors[self.fg]
                sv_ttk.set_theme(theme)

        # Set the foreground
        try:
            self.parent.configure(fg=fg)
        except TclError:
            self.parent.configure(foreground=fg)

    def __checkcolor(self, bg):
        if bg == "dark":
            if fg == "default":
                fg2 = constants.LIGHT_BG
            elif fg == "Green":
                fg2 = constants.GREEN_TEXT
            elif fg == "Red":
                fg2 = constants.RED_TEXT
            else:
                fg2 = constants.LIGHT_BG
        else:
            fg2 = constants.DARK_BG
        return fg2
