from . import constant
import os
import configparser
import platform

if platform.system() == "Windows":
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
                configfile.write("defconsole = "+defconsole+"\n")
                configfile.write("isenabled = no")
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

# Check if we are in dark mode which allows us 
# to change the text color
def check_dark_mode(self, color):
    if color == constant.DARK_BG:
        self.configure(fg=constant.LIGHT_TEXT)
        return True
    else:
        return False

def set_window_color(self):
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
    
    if check_if_its_a_window(self) == "Text":
        self.configure(bg=item, fg=sub_item)

# Get a value...
def getvalue(section:str, name:str):
    check_exists()
    with open(dir + "config.ini") as f:
        config = configparser.ConfigParser()
        config.read(f)
        return config[section][name]
        