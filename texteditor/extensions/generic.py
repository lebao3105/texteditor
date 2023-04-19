import logging
import os

# from libtextworker.general import logging_configs
from libtextworker import THEMES_DIR
from libtextworker.get_config import GetConfig
from libtextworker.interface.tk import ColorManager, default_configs
from libtextworker.versioning import is_development_version

__all__ = ["CONFIGS_PATH", "Setter", "log", "global_settings"]

CONFIGS_PATH = os.path.expanduser(
    "~/.config/textworker/configs{}.ini".format(
        "_dev" if is_development_version("1.5a0") else ""  # Temporary
    )
)
configs = {
    "interface": {"theme": "default", "path": "themes"},
    "interface.tabs": {"middle_close": "no", "close_on_no_tab": "no"},
    "editor": {
        "autosave": "yes",
        "autosave_time": "120",
    },
    # "extensions.multiview": {
    #     "notebook_location": "bottom"
    # },
    "fun": {"empty_page_on_last_tab_close": "yes"},
    "cmd": {"enable": "yes", "term": "xterm"},
}


class Setter:
    cfg = GetConfig(configs, CONFIGS_PATH)

    def __init__(self):
        # Additional setup for themes
        themename = self.call("interface", "theme")
        themepath = THEMES_DIR + f"{themename}.ini"

        self.clrmgr = ColorManager(default_configs, themepath)
        pass

    # GetConfig shortcuts
    def call(self, section, option):
        return self.cfg.getkey(section, option)

    def set(self, section, option, value):
        self.cfg.set(section, option, value)
        self.cfg.update()


log = logging.getLogger("textworker")
global_settings = Setter()
