# Initialize for this application
# Including language, and configures.
import gettext
from . import get_config
import os

def initialize(self, part):
    if part == 1:
        # Initialize the language
        if os.path.isdir("po"):
            gettext.bindtextdomain('base', 'po')
            gettext.textdomain('base')
            self._ = gettext.gettext
            """
            en = gettext.translation('base', localedir='po', languages=['en'])
            en.install()
            """
        else:
            raise Exception("Could not find the language directory!")
    elif part == 2:
        # Initialize the configures
        get_config.set_windows_color(self)
