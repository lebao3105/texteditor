from . import constants
import os
import configparser
import platform

if platform.system() == "Linux":
    dir = os.environ['HOME'] + "/.config/"
elif platform.system() == "Windows":
    dir = os.environ['USERPROFILE'] + "\\.config\\"

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
                configfile.write("width = "+str(constants.DEFAULT_OTHERS_WIGHT)+"\n")
                configfile.write("height = "+str(constants.DEFAULT_OTHERS_WIGHT)+"\n")
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

# At least we make this independently frin set_window_color(self).
def change_text_color(self):
    check_exists()
    with open(dir + "config.ini", "r") as configfile:
        parser = configparser.ConfigParser()
        parser.read_file(configfile)
        if parser.get("global", "color") == "dark":
            item = constants.DARK_BG
        else:
            item = constants.LIGHT_BG

        if parser.get("global", "sub_color") == "default":
            return True
        elif parser.get("global", "sub_color") == "Green":
            self.configure(fg=constants.GREEN_TEXT, bg=item)
        elif parser.get("global", "sub_color") == "Blue":
            self.configure(fg=constants.BLUE_TEXT, bg=item)
        elif parser.get("global", "sub_color") == "Red":
            self.configure(fg=constants.RED_TEXT, bg=item)
        else:
            return False

def set_windows_color(self):
    check_exists()

    with open(dir + "config.ini", "r") as configfile:
        config = configparser.ConfigParser()
        config.read_file(configfile)
        if config["global"]["color"] == "dark":
            change_color(self, 'dark')
        elif config["global"]["color"] == "light":
            change_color(self, 'light')
        
    if check_if_its_a_window(self) == "Toplevel":
        self.geometry(config["other_windows"]["width"] + "x" + config["other_windows"]["height"])
        self.resizable(False, False)
        self.grab_set()

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
    if hasattr(self, "configure"):
        self.configure(bg=item)
    else:
        self.config(bg=item)
    
    if check_if_its_a_window(self) == "Text":
        self.configure(bg=item, fg=sub_item)

# Use for the setup window only
def change_config(self):
    check_exists()
    with open(dir + "config.ini", "r") as configfile:
        config = configparser.ConfigParser()
        config.read_file(configfile)
        config.set("other_windows", "sub_color", self)
        