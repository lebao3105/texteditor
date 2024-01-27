import json
import os
import requests
import wx
import wx.html2
import wx.xrc

from libtextworker.general import CraftItems
from libtextworker.interface import stock_ui_configs
from libtextworker.interface.manager import hextorgb, AUTOCOLOR, ColorManager

from markdown2 import markdown

from . import _
from .. import __version__, branch
from ..generic import (
    CONFIGS_PATH,
    UIRC_DIR,
    clrCall,
    global_settings,
    DATA_PATH,
    editorCfg,
    THEMES_DIR,
    EDITOR_DIR
)

content: str
backup: str
replaced: bool

def initialize_work():
    global content, backup, replaced
    content = open(CraftItems(UIRC_DIR, "preferences.py"), "r").read()
    replaced = content.startswith("from textworker import _")
    if not replaced: backup = content

def localize(forced: bool = False):
    import re
    global content, replaced, backup
    if replaced and not forced: return

    content = "from textworker import _\n" + backup # Add gettext import

    # Made with the help of, yeah, AI. (cuz I'm bad at regex)
    # I have modified it myself for the most perfect pattern.
    # All strings in wxFormBuilder generated Python code are unicode type:
    # u"<content>"
    # Pattern with start with u. Then 4 regex groups:
    # One for the first double quote (")
    # One for the string content (. for every character except \n, + for >=1 match, ? to catch as much as posible)
    # The matching quote (")
    # The final look for space (just one space) OR a comma (,) but NOT include it to the catch result.
    # One draw back is that numberic only strings are include, but can be skipped below.
    pattern = r'u(")(.+?)(")(?=[\s,])'
    matches = re.findall(pattern, content)
    for match in matches:
        # The match result will be a list of
        # ('"', '<string>', '"') tuples.
        # Skip number-only strings.
        try: int(match[1])
        except: pass
        else: continue
        localized = f'_(u"{match[1]}")'
        content = content.replace(f"u{match[0]}{match[1]}{match[2]}", localized)

    open(CraftItems(UIRC_DIR, "preferences.py"), "w").write(content)
    replaced = True


def trytoimport():
    try:
        from ..ui import preferences as prefs
        return prefs
    except:
        return wx.MessageBox("An error occured calling the dialog code. "
                             "Please report back to the developer.\n"
                             "Also send the log when this message shows.",
                             style=wx.OK_DEFAULT | wx.ICON_ERROR)
initialize_work()
localize()
preferences = trytoimport()

class SettingsDialog(preferences.StDialog):
    """
    A WIP settings page for text worker.
    """

    AUTOUPDATE: bool = global_settings.getkey("base", "autoupdate", True, True, True) in global_settings.yes_values
    NB_LOC: str = global_settings.getkey("extensions.textwkr.multiview", "notebook_location", True, True, True)

    AUTOCOLOR_CHANGE: bool = clrCall.getkey("color", "auto", True, True, True) in clrCall.yes_values
    CURRTHEME: str = global_settings.getkey("config-paths.ui", "theme", True, True, True)


    def __init__(this, parent: wx.Window):
        preferences.StDialog.__init__(this, parent)

        # General page
        this.m_checkBox1.SetValue(this.AUTOUPDATE)
        this.m_choice2.SetStringSelection(this.NB_LOC.capitalize())

        this.Bind(wx.EVT_CHECKBOX,
                  lambda evt: global_settings.set("base", "autoupdate", this.m_checkBox1.IsChecked()),
                  this.m_checkBox1)

        this.Bind(wx.EVT_BUTTON, this.check_updates, this.m_button3)

        def showchangelog(evt):
            new = wx.Dialog(this)
            try:
                text = json.loads(
                    requests.get(
                        f"https://api.github.com/repos/lebao3105/texteditor/releases/v{__version__}"
                    ).text
                )["body"]
            except: # TODO: Check exception message
                text = _("No changelog/unable to get.")

            wb = wx.html2.WebView.New(new)
            wb.SetPage(markdown(text), "")
            new.ShowModal()

        this.Bind(wx.EVT_BUTTON, showchangelog, this.m_button4)

        this.Bind(
            wx.EVT_CHOICE,
            lambda evt: global_settings.set(
                "extensions.textwkr.multiview",
                "notebook_location",
                this.m_choice2.GetStringSelection().lower(),
            ),
            this.m_choice2,
        )

        # Colors page
        colors = { # Corresponding to the XRC file
            _("Dark"): 1, _("Light"): 2
        }

        this.m_radioBox1.SetSelection(
            0
            if this.AUTOCOLOR_CHANGE
            else colors[_(clrCall.getkey("color", "background").capitalize())]
        )

        this.m_colourPicker1.SetColour(wx.Colour(*hextorgb(clrCall.GetColor()[0])))
        this.m_colourPicker2.SetColour(wx.Colour(*hextorgb(clrCall.GetColor()[1])))

        this.Bind(
            wx.EVT_RADIOBOX,
            lambda evt: this.apply_color(this.m_radioBox1.GetStringSelection()),
            this.m_radioBox1,
        )

        for i in os.listdir(THEMES_DIR):
            this.m_choice3.Append(i.removesuffix(".ini"))

        this.m_choice3.SetStringSelection(this.CURRTHEME)

        def target_type():
            if AUTOCOLOR and this.m_radioBox1.GetSelection() == 0 and this.m_checkBox71.IsChecked(): import darkdetect; return f"-{darkdetect.theme()}"
            elif this.m_checkBox71.IsChecked(): return "-" + {1: "dark", 2: "light"}.get(this.m_radioBox1.GetSelection())
            else: return ""

        this.Bind(wx.EVT_COLOURPICKER_CHANGED,
                      lambda evt: clrCall.set_and_update("color", "background" + target_type(), 
                                                         this.m_colourPicker1.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)),
                      this.m_colourPicker1)

        this.Bind(wx.EVT_COLOURPICKER_CHANGED,
                      lambda evt: clrCall.set_and_update("color", "foreground" + target_type(), 
                                                         this.m_colourPicker2.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)),
                      this.m_colourPicker2)

        def newtheme(evt):
            if not this.m_textCtrl1.GetLabelText():
                wx.MessageBox(
                    _("Error while setting a new theme: Name required."),
                    style=wx.ICON_ERROR | wx.OK,
                )
            else:
                new = this.m_textCtrl1.GetLabel()
                global clrCall
                clrCall = ColorManager(customfilepath=CraftItems(THEMES_DIR, new + ".ini"))
                this.m_choice3.Append(new)
                this.m_choice3.SetStringSelection(new)
                wx.MessageBox(_("Not implemented yet."))

        this.Bind(wx.EVT_BUTTON, newtheme, this.m_button31)

        # Editors page

        indentationTypes = ["tabs", "spaces"]

        this.m_choice1.SetSelection(
            indentationTypes.index(editorCfg.getkey("indentation", "type"))
        )
        this.m_comboBox1.SetValue(editorCfg.getkey("indentation", "size"))
        this.m_checkBox3.SetValue(editorCfg.getkey("indentation", "backspace_unindents"))
        this.m_checkBox6.SetValue(editorCfg.getkey("indentation", "show_guide"))
        this.m_checkBox4.SetValue(editorCfg.getkey("editor", "view_whitespaces"))
        this.m_checkBox5.SetValue(editorCfg.getkey("editor", "viewEOL"))
        this.m_checkBox7.SetValue(editorCfg.getkey("editor", "line_count"))

        for item in os.listdir(EDITOR_DIR):
            this.m_choice31.Append(item)

        this.Bind(
            wx.EVT_CHOICE,
            lambda evt: editorCfg.set_and_update(
                "indentation", "type", indentationTypes[this.m_choice1.GetSelection()]
            ),
            this.m_choice1,
        )

        this.Bind(
            wx.EVT_TEXT,
            lambda evt: editorCfg.set_and_update(
                "indentation", "size", evt.GetString()
            ),
            this.m_comboBox1,
        )

        # Lazy bind
        # Because checkbox numbers are not correctly listed,
        # so we have these
        editorSettings = {
            3: "backspace_unindents",
            6: "show_guide",
            4: "view_whitespaces",
            5: "view_EOL",
            7: "line_count",
        }
        for i in range(3, 8):
            checkbox = getattr(this, f"m_checkBox{str(i)}")
            this.Bind(
                wx.EVT_COMBOBOX,
                lambda evt: editorCfg.set_and_update(
                    "indentation" if i in [3, 6] else "editor",
                    editorSettings[i],
                    checkbox.IsChecked(),
                ),
                checkbox,
            )

    def check_updates(this, evt):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "updater", f"{DATA_PATH}/updater.py"
        )
        updater = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(updater)
        updater.currver = __version__
        result = updater.parse_json(CONFIGS_PATH)

        if result is None:
            return wx.MessageBox(_("The program is up-to-date"), parent=this)
        elif result == "invalid_json":
            return wx.MessageBox(
                _(
                    "Invalid response received: Maybe an internet problem, or my data is invalid."
                ),
                parent=this,
            )
        elif isinstance(result, tuple):
            if wx.MessageBox(
                message = _(f"Update available: {result[0]} from branch {branch}.\n" +
                            (f"Get via: {result[2]}" if result[2] else "")),
                parent=this,
                style=wx.YES_NO
            ) == wx.YES:
                
                new = wx.Frame(this)
                text = wx.html2.WebView.New(new)
                text.SetPage(markdown(result[1]), f"{result[0]} changelogs")
                text.Show()
                new.Show()

                # if result[2]: updater.install(result[2])
                # else: wx.MessageBox(_("No downloadable files yet - this means you"
                #                       "need to either wait or install from source code."))
            
            clrCall.configure(this)

    def apply_color(this, string):
        if string != _("Automatic"):
            clrCall.set("color", "background", string.lower())
            clrCall.set("color", "auto", "no")
        else:
            clrCall.set("color", "background", "light")
            clrCall.set("color", "auto", "yes")
