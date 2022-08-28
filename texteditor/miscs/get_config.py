from . import constants
import os
import configparser
import platform

if platform.system() == "Windows":
    file = os.environ['USERPROFILE'] + "\\.config\\texteditor_configs.ini"
    defconsole = 'cmd'
else:
    file = os.environ['HOME'] + "/.config/texteditor_configs.ini"
    defconsole = 'xterm'

cfg = configparser.ConfigParser()

# Default variables.
# We must use cfg.get() to get the current variable's value.
cfg['global'] = {
    'color': 'light',
    'sub_color': 'default',
    'font': 'default'
}

cfg['popups'] = {
    # TODO/NOTE: They should be different
    'width': str(constants.DEFAULT_OTHERS_WIGHT),
    'height': str(constants.DEFAULT_OTHERS_WIGHT)
}

cfg['cmd'] = {
    'defconsole': defconsole,
    'isenabled': 'yes',
    'writelog': 'no'
}

# New: Auto-save files
cfg['filemgr'] = {
    'autosave': 'yes',
    'autosave-time' : '5' # in minutes
}

if not os.path.isfile(file):
    try:
        with open(file, 'w') as f:
            cfg.write(f)
    finally:
        with open(file, 'r') as f: # Open the file again
            backup = f.read()
        pass

cfg.read(file)

bg = cfg.get('global', 'color')
fg = cfg.get('global', 'sub_color')

class GetConfig:
    """Changes a Tkinter/TTK widget configuration."""

    def __init__(self, parent=None, action:str=None):
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
                self.configure(parent)
            elif action == "reset":
                self.reset()
    
    @staticmethod
    def reset():
        if not backup:
            print("Error: Unable to reset configuration file: Backed up default variables not found")
            return False
        try:
            os.remove(file)
            with open(file, 'w') as f:
                f.write(backup)
        finally:
            print("Completed resetting texteditor configuration file.")
            return True

    @staticmethod
    def checkclass(widget):
        wind = ['Tk', 'Frame']
        text = ['Label', 'Text']
        ttk_widgets = ['TCombobox']
        
        # Combine 3 arrays together
        for it in text:
            wind.append(it)
        for it2 in ttk_widgets:
            wind.append(it2)

        class_name = widget.winfo_class()
        if class_name in wind and cfg.sections():
            return class_name
        else:
            return False
    
    @staticmethod
    def configure(widget):
        class_name = GetConfig.checkclass(widget)
        if class_name:
            fg2 = GetConfig._checkcolor(GetConfig, widget)
            if fg2 != constants.LIGHT_BG:
                try:
                    return widget.configure(fg=fg2, bg=constants.DARK_BG)
                except:
                    return widget.configure(foreground=fg2, background=constants.DARK_BG)
    
    def _checkcolor(self, widget):
        if bg == "dark":
            if fg == "default":
                fg2 = constants.LIGHT_BG
            elif fg == "Green":
                fg2 = constants.GREEN_TEXT
            elif fg == "Red":
                fg2 = constants.RED_TEXT
            # Test
            elif fg == "Pink":
                fg2 = constants.PINK_TEXT
            elif fg == "Yellow":
                fg2 = constants.YELLOW_TEXT
            else:
                fg2 = constants.LIGHT_BG
        else:
            fg2 = constants.LIGHT_BG
        return fg2
    
    @staticmethod
    def getvalue(section:str, name:str):
        if not section in cfg.sections():
            raise Exception ("Section not found "+section)
        else:
            return cfg.get(section, name)