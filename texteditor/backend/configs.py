import configparser
import os
from libtextworker import EDITOR_DIR, THEMES_DIR
from ..extensions.generic import global_settings, CONFIGS_PATH
from tkinter.messagebox import showinfo, showerror
from tkinter.simpledialog import askstring

changelog: str = _("No additional infomation here.")

# Sections
old_configs = ["global", "cmd", "filemgr", "extensions.autosave", "extensions.cmd"]

current = [
    "interface",
    "interface.tabs",
    "editor",
    # "extensions.multiview",
    "fun",
]

# Configs to move
moves = {
    "global.color": "color.background",
    "global.sub_color": "color.textcolor",
    "global.autocolor": "color.autocolor",
    "global.font": "font.family",
    "global.font_size": "font.size",
    "filemgr.autosave": "editor.autosave",
    "filemgr.autosave-time": "editor.autosave_time",
}


def update_theme():
    if os.path.isfile(THEMES_DIR + "default.ini"):
        name = askstring(
            _("Theme configuration"),
            _(
                "Enter a name for your theme configuration. It will be saved under ~/.config/textworker/themes/<theme>.ini."
            ),
        )
        target = THEMES_DIR + name + ".ini"
        if os.path.isfile(target):
            showerror(_("Error"), _(f"A theme named '{name}' already exists."))
            return False
        move_configs("global", "color", CONFIGS_PATH, target)


def move_configs(section, targetsection, oldfile, target):
    # Old file
    oldobj = configparser.ConfigParser()
    oldobj.read(oldfile)

    # New file
    newobj = configparser.ConfigParser()

    # Move configs
    for item in moves:
        if not item.startswith(section):
            break
        value = oldobj.get(section, item.removeprefix(section))
        newobj.set(section, moves[item].removeprefix(targetsection), value)
    with open(target, "w") as f:
        newobj.write(f)


usercfgs = global_settings.cfg.sections()
if old_configs in usercfgs:
    showinfo(
        _("Changed configuration system"),
        _(
            "The texteditor's configuration system has been changed recently and yours needs to be fixed. Not all configs will be deleted."
        ),
    )
    update_theme()
