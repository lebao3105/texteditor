from . import constant
import os
import configparser
import platform

if platform.system() == "Windows":
<<<<<<< HEAD
    dir = os.environ['USERPROFILE'] + "\\.config\\"
    defconsole = 'cmd'
else:
    dir = os.environ['HOME'] + "/.config/"
    defconsole = 'xterm'

def check_exists():
    if os.path.isdir(dir):
        if os.path.isfile(dir + "config.ini"):
            return True
        else:
            with open(dir + "config.ini", "w") as configfile:
                configfile.write("[global]\n")
                configfile.write("color = light\n")
                configfile.write("sub_color = default\n")
                configfile.write("font = default\n\n")
                configfile.write("[other_windows]\n")
                configfile.write("width = "+str(constant.DEFAULT_OTHERS_WIGHT)+"\n")
                configfile.write("height = "+str(constant.DEFAULT_OTHERS_WIGHT)+"\n\n")
                configfile.write("[cmd]\n")
                configfile.write("defconsole = "+defconsole)
    else:
        test = os.mkdir(dir)
        if not test:
            raise Exception("Could not create the configure directory!")

def check_if_its_a_window(self):
    if self.winfo_class() == "Tk":
        return "Tk"
    elif self.winfo_class() == "Toplevel":
        return "Toplevel"
    elif self.winfo_class() == "Frame":
        return "Frame"
    elif self.winfo_class() == "Label" or self.winfo_class() == "Button" or self.winfo_class() == "Text":
        return "Text"
    else:
        return False

# At least we made this independently from set_window_color(self).
def change_text_color(self):
    check_exists()
    with open(dir + "config.ini", "r") as configfile:
        parser = configparser.ConfigParser()
        parser.read_file(configfile)
        if parser.get("global", "color") == "dark":
            item = constant.DARK_BG
        else:
            item = constant.LIGHT_BG

        if parser.get("global", "sub_color") == "default":
            return True
        elif parser.get("global", "sub_color") == "Green":
            if check_dark_mode(self, item):
                self.configure(fg=constant.GREEN_TEXT, bg=item)
        elif parser.get("global", "sub_color") == "Blue":
            if check_dark_mode(self, item):
                self.configure(fg=constant.BLUE_TEXT, bg=item)
        elif parser.get("global", "sub_color") == "Red":
            if check_dark_mode(self, item):
                self.configure(fg=constant.RED_TEXT, bg=item)
        else:
            return False

=======
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
    # TODO: They should be different
    'width': str(constant.DEFAULT_OTHERS_WIGHT),
    'height': str(constant.DEFAULT_OTHERS_WIGHT)
}

cfg['cmd'] = {
    'defconsole': defconsole,
    'isenabled': 'yes'
}

if not os.path.isfile(dir):
    with open(dir, 'w') as f:
        cfg.write(f)

def find_widget(self):
    arr = [
        'Tk', 'Frame', 'TopLevel'
    ]

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
        item = constant.DARK_BG
    else:
        item = constant.LIGHT_BG

    if cfg.get("global", "sub_color") == "default":
        return True
    elif cfg.get("global", "sub_color") == "Green":
        if check_dark_mode(self, item):
            self.configure(fg=constant.GREEN_TEXT, bg=item)
    elif cfg.get("global", "sub_color") == "Blue":
        if check_dark_mode(self, item):
            self.configure(fg=constant.BLUE_TEXT, bg=item)
    elif cfg.get("global", "sub_color") == "Red":
        if check_dark_mode(self, item):
            self.configure(fg=constant.RED_TEXT, bg=item)
    else:
        return False

>>>>>>> b35a36977b88c3114d7f544fec4c57ce48b0658f
# Check if we are in dark mode which allows us 
# to change the text color
def check_dark_mode(self, color):
    if color == constant.DARK_BG:
        self.configure(fg=constant.LIGHT_TEXT)
        return True
    else:
        return False

def set_window_color(self):
<<<<<<< HEAD
    check_exists()

    with open(dir + "config.ini", "r") as configfile:
        config = configparser.ConfigParser()
        config.read_file(configfile)
        if config["global"]["color"] == "dark":
            change_color(self, 'dark')
        elif config["global"]["color"] == "light":
            change_color(self, 'light')
    
    # For TopLevel windows
    if check_if_its_a_window(self) == "Toplevel":
        self.geometry(config["other_windows"]["width"] + "x" + config["other_windows"]["height"])
=======
    if cfg["global"]["color"] == "dark":
        change_color(self, 'dark')
    elif cfg["global"]["color"] == "light":
        change_color(self, 'light')
    
    # For TopLevel windows
    if find_widget(self) == "Toplevel":
        self.geometry(cfg["other_windows"]["width"] + "x" + cfg["other_windows"]["height"])
>>>>>>> b35a36977b88c3114d7f544fec4c57ce48b0658f
        self.resizable(False, False)
        self.grab_set()

# Don't make functions too complicated
def change_color(self, color):

    # Check for the selected theme
    if color == "dark":
        item = constant.DARK_BG
        sub_item = constant.LIGHT_BG
    else:
        item = constant.LIGHT_BG
        sub_item = constant.DARK_BG

    # Then set it
    if hasattr(self, "configure"):
        self.configure(bg=item)
    else:
        self.config(bg=item)
    
<<<<<<< HEAD
    if check_if_its_a_window(self) == "Text":
        self.configure(bg=item, fg=sub_item)

# Get a value...
def getvalue(section, name):
    check_exists()
    with open(dir + "config.ini") as f:
        config = configparser.ConfigParser()
        config.read(f)
        try:
            return config[section][name]
        except:
            return defconsole
        
=======
    if find_widget(self) == "Text":
        self.configure(bg=item, fg=sub_item)

# Get a value...
def getvalue(section:str, name:str):
    if not section in cfg:
        raise "Section not found "+section
    else:
        return cfg.get(section, name)        
>>>>>>> b35a36977b88c3114d7f544fec4c57ce48b0658f
