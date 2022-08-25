from . import constants
import os
import configparser
import platform

if platform.system() == "Windows":
    dir = os.environ['USERPROFILE'] + "\\.config\\texteditor_configs.ini"
    defconsole = 'cmd'
else:
    dir = os.environ['HOME'] + "/.config/texteditor_configs.ini"
    defconsole = 'xterm'

cfg = configparser.ConfigParser()
cfg.read(dir)

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

def _file():
    if not os.path.isfile(dir):
        with open(dir, 'w') as f:
            cfg.write(f)

_file()

def find_widget(self):
    arr = ['Tk', 'Frame', 'TopLevel']

    if self.winfo_class() == "Label" or self.winfo_class() == "Button" or self.winfo_class() == "Text":
        return "Text"
    for item in arr:
        if self.winfo_class() == item:
            return item
        else:
            return False

# At least we made this independent from set_window_color(self).
def change_text_color(self):
    """Get text color defined in global->sub_color.
    Supported colors:
    default: default color
    Green: green color
    Blue: blue color
    Red: red color
    If check_dark_mode return(s) False, any other color then default won't be applied."""
    if cfg.get("global", "color") == "dark":
        item = constants.DARK_BG
    else:
        item = constants.LIGHT_BG

    if cfg.get("global", "sub_color") == "default":
        return True
    elif cfg.get("global", "sub_color") == "Green":
        if check_dark_mode(self, item):
            self.configure(fg=constants.GREEN_TEXT, bg=item)
    elif cfg.get("global", "sub_color") == "Blue":
        if check_dark_mode(self, item):
            self.configure(fg=constants.BLUE_TEXT, bg=item)
    elif cfg.get("global", "sub_color") == "Red":
        if check_dark_mode(self, item):
            self.configure(fg=constants.RED_TEXT, bg=item)
    else:
        return False

# Check if we are in dark mode which allows us 
# to change the text color
def check_dark_mode(self, color):
    if color == constants.DARK_BG:
        self.configure(fg=constants.LIGHT_TEXT)
        return True
    else:
        return False

def set_window_color(self):
    if cfg.get("global","color") == "dark":
        change_color(self, 'dark')
    elif cfg.get("global","color") == "light":
        change_color(self, 'light')
    
    # For TopLevel windows
    if find_widget(self) == "Toplevel":
        self.geometry(cfg.get("other_windows","width") + "x" + cfg.get("other_windows","height"))
        #self.resizable(False, False)
        #self.grab_set()

# Don't make functions too complicated
def change_color(self, color):
    # Check for the selected theme
    if color == "dark":
        item = constants.DARK_BG
        sub_item = constants.LIGHT_BG
    else:
        item = constants.LIGHT_BG
        sub_item = constants.DARK_BG

    # Then set it
    self.configure(bg=sub_item, fg=item)

# Get a value...
def getvalue(section:str, name:str):
    if not section in cfg:
        raise "Section not found "+section
    else:
        return cfg.get(section, name)        
