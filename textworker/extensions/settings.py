import json
import os
import requests

import wx
import wx.html2
import wx.lib.agw.cubecolourdialog
import wx.xrc

from libtextworker.general import CraftItems
from libtextworker.interface.manager import AUTOCOLOR, ColorManager
from libtextworker.interface.wx.miscs import localizePy

# from markdown2 import markdown

from . import _
from .. import __version__, branch
from ..generic import *

preferences = localizePy(CraftItems(UIRC_DIR, "preferences.py"), "from textworker import _")

class SettingsDialog(preferences.StDialog):
    """
    A WIP settings page for text worker.
    """

    AUTOUPDATE: bool = global_settings["base"]["autoupdate"] in global_settings.yes_values
    NB_LOC: str = global_settings['extensions.textwkr.multiview']['notebook_location']

    AUTOCOLOR_CHANGE: bool = clrCall["color"]["auto"] in clrCall.yes_values
    CURRTHEME: str = global_settings["config-paths.ui"]["theme"]


    def __init__(this, parent: wx.Window):
        preferences.StDialog.__init__(this, parent)

        # General page
        this.m_checkBox1.SetValue(this.AUTOUPDATE)
        this.m_choice2.SetStringSelection(this.NB_LOC.capitalize())

        this.Bind(wx.EVT_CHECKBOX,
                  lambda evt: global_settings.set_and_update(
                        "base", "autoupdate", this.m_checkBox1.IsChecked()
                  ),
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
            except Exception as e:
                text = e

            wb = wx.html2.WebView.New(new)
            # wb.SetPage(markdown(text), "")
            wb.SetPage(text, "")
            new.ShowModal()

        this.Bind(wx.EVT_BUTTON, showchangelog, this.m_button4)

        this.Bind(wx.EVT_CHOICE, lambda evt: global_settings.set_and_update(
                    "extensions.textwkr.multiview",
                    "notebook_location",
                    this.m_choice2.GetStringSelection().lower()
                  ),
                  this.m_choice2)

        # Colors page
        colors = {_("Dark"): 1, _("Light"): 2} # Corresponding to the XRC file

        this.m_radioBox1.SetSelection(0 if this.AUTOCOLOR_CHANGE
                                        else colors[_(clrCall.getkey("color", "background").capitalize())])
        

        this.Bind(wx.EVT_RADIOBOX, lambda evt: this.apply_color(this.m_radioBox1.GetStringSelection()), this.m_radioBox1)

        for i in os.listdir(THEMES_DIR):
            this.m_choice3.Append(i.removesuffix(".ini"))

        def setTheme(evt):
            global_settings.set_and_update("config-paths.ui", "theme", this.m_choice3.GetStringSelection().lower())
            wx.MessageBox(_("Restart the application to get the effect"), _("Completed"), parent=this)

        this.m_choice3.SetStringSelection(this.CURRTHEME)
        this.Bind(wx.EVT_CHOICE, setTheme, this.m_choice3)

        def target_type() -> str:
            if AUTOCOLOR and (this.m_radioBox1.GetSelection() == 0) and this.m_checkBox71.IsChecked(): import darkdetect; return f"-{darkdetect.theme()}"
            elif this.m_checkBox71.IsChecked(): return "-" + {1: "dark", 2: "light"}.get(this.m_radioBox1.GetSelection())
            else: return ""

        def getandsetcolor(kind: str):
            result = this.ShowAndSetColourIfAbleTo()
            if result:
                clrCall.set_and_update("color", kind + target_type(), result)

        this.m_button5.Bind(wx.EVT_BUTTON, lambda evt: getandsetcolor("background"))
        this.m_button6.Bind(wx.EVT_BUTTON, lambda evt: getandsetcolor("foreground"))

        def newtheme(evt):
            if not this.m_textCtrl1.GetLabelText():
                wx.MessageBox(_("Error while setting a new theme: Name required."),
                              style=wx.ICON_ERROR | wx.OK)
            else:
                new = this.m_textCtrl1.GetLabel()
                global clrCall
                clrCall = ColorManager(customfilepath=CraftItems(THEMES_DIR, new + ".ini"))
                this.m_choice3.Append(new)
                this.m_choice3.SetStringSelection(new)
                # wx.MessageBox(_("Not implemented yet."))

        this.Bind(wx.EVT_BUTTON, newtheme, this.m_button31)

        # this.m_fontPicker1 with EVT_FONTPICKER_CHANGED event
        this.m_fontPicker1.SetSelectedFont(clrCall.GetFont())

        # Editors page

        indentationTypes = ["tabs", "spaces"]

        this.m_choice1.SetSelection(indentationTypes.index(editorCfg.getkey("indentation", "type").lower()))
        this.m_comboBox1.SetValue(editorCfg.getkey("indentation", "size"))
        this.m_checkBox3.SetValue(editorCfg.getkey("indentation", "backspace_unindents"))
        this.m_checkBox6.SetValue(editorCfg.getkey("indentation", "show_guide"))
        this.m_checkBox4.SetValue(editorCfg.getkey("editor", "view_whitespaces"))
        this.m_checkBox5.SetValue(editorCfg.getkey("editor", "viewEOL"))
        this.m_checkBox7.SetValue(editorCfg.getkey("editor", "line_count"))

        for item in os.listdir(EDITOR_DIR):
            this.m_choice31.Append(item)

        this.Bind(wx.EVT_CHOICE,
                  lambda evt: editorCfg.set_and_update(
                      "indentation", "type", indentationTypes[this.m_choice1.GetSelection()]
                  ),
                  this.m_choice1)

        this.Bind(wx.EVT_TEXT,
                  lambda evt: editorCfg.set_and_update("indentation", "size", evt.GetString()),
                  this.m_comboBox1)

        # Lazy bind
        # Because checkbox numbers are not correctly listed,
        # so we have this
        editorSettings = {3: "backspace_unindents",
                          4: "view_whitespaces",
                          5: "view_EOL",
                          6: "show_guide",
                          7: "line_count"}
        
        for i in range(3, 8):
            checkbox = getattr(this, f"m_checkBox{str(i)}")
            this.Bind(wx.EVT_COMBOBOX,
                      lambda evt: editorCfg.set_and_update(
                          "indentation" if i in [3, 6] else "editor",
                          editorSettings[i], checkbox.IsChecked()
                      ),
                      checkbox)
        
        clrCall.configure(this)
        clrCall.autocolor_run(this)

    def check_updates(this, evt):
        import importlib.util

        spec = importlib.util.spec_from_file_location("updater", f"{DATA_PATH}/updater.py")
        updater = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(updater)
        updater.currver = __version__
        result = updater.parse_json(CONFIGS_PATH)

        match result:
            case None:
                return wx.MessageBox(_("The program is up-to-date"), parent=this)
        
            case "invalid_json":
                return wx.MessageBox(_("Invalid response received"), parent=this)

            case _:
                if isinstance(result, tuple):
                    # TODO: If packaging is still a problem, redirect the user to the release page.
                    if wx.MessageBox(_(f"Your editor is outdated: new {result[0]} from branch {branch}.\n"
                                       f"Get via: {result[2]}" if result[2] else ""),
                                     _("Update available"), wx.YES_NO, this) == wx.YES:
                        new = wx.Frame(this)
                        text = wx.html2.WebView.New(new)
                        # text.SetPage(markdown(result[1]), f"{result[0]} changelog")
                        text.SetPage(result[1], f"{result[0]} changelog")
                        text.Show()
                        new.Show()
            
        clrCall.configure(this)

    def apply_color(this, string):
        if string != _("Automatic"):
            clrCall.set_and_update("color", "background", string.lower())
            clrCall.set_and_update("color", "auto", "no")
        else:
            clrCall.set_and_update("color", "background", "light")
            clrCall.set_and_update("color", "auto", "yes")

    def ShowAndSetColourIfAbleTo(this) -> str | None:
        dlg = wx.lib.agw.cubecolourdialog.CubeColourDialog(this)
        clrCall.configure(dlg)
        clrCall.autocolor_run(dlg)

        if dlg.ShowModal() == wx.ID_OK:
            colourdata = dlg.GetColourData()
            return colourdata.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        
        return None