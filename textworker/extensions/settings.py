import json
import os
import requests
import wx
import wx.html2
import wx.xrc

from libtextworker.general import CraftItems
from libtextworker.get_config import GetConfig
from libtextworker.interface import stock_ui_configs
from libtextworker.interface.manager import hextorgb
from libtextworker.interface.wx.miscs import XMLBuilder

from markdown2 import markdown

from ..generic import (
    CONFIGS_PATH,
    UIRC_DIR,
    clrCall,
    global_settings,
    DATA_PATH,
    editorCfg,
    THEMES_DIR,
)
from .. import __version__


class SettingsDialog(XMLBuilder):
    """
    A WIP, useful textworker settings dialog with lots of things inside lol.
    We're all waiting for new features;)
    """

    """
    Here are our configs per-page
    All changes will only be applied on the "Apply" button click event
    This should be optional.
    """

    AUTOUPDATE: bool = global_settings.getkey("base", "autoupdate", True, True, True)
    NB_LOC: str = global_settings.getkey(
        "extensions.textwkr.multiview", "notebook_location", True, True, True
    )

    def __init__(self, Parent: wx.Window):
        XMLBuilder.__init__(self, Parent, CraftItems(UIRC_DIR, "preferences.xrc"), _)

        # Here is our get-n-bind
        # Note: all objects will be named by their name in wxFormBuilder
        # Top-level widgets first
        self.dlg: wx.Dialog = self.Res.LoadDialog(Parent, "StDialog")
        nb: wx.Notebook = self.dlg.GetChildren()[0]

        # Get all pages
        page1 = nb.GetPage(0)
        page2 = nb.GetPage(1)
        page3 = nb.GetPage(2)

        # The most stupid way to work with XRC lmao
        # But I can't make wxFB to generate python code because,
        # you know: multiple language. Would be fine if I know
        # how to use the re module.

        # General page
        m_checkbox1: wx.CheckBox = page1.GetChildren()[0].GetChildren()[0]
        m_button3 = page1.GetChildren()[0].GetChildren()[1]
        m_button4 = page1.GetChildren()[0].GetChildren()[2]
        m_choice2: wx.Choice = page1.GetChildren()[1].GetChildren()[1]

        m_checkbox1.SetValue(
            global_settings.getkey("base", "autoupdate") in global_settings.yes_values
        )

        m_choice2.SetStringSelection(
            global_settings.getkey(
                "extensions.textwkr.multiview", "notebook_location"
            ).capitalize()
        )

        self.dlg.Bind(
            wx.EVT_CHECKBOX,
            lambda evt: global_settings.set(
                "base", "autoupdate", m_checkbox1.IsChecked()
            ),
            m_checkbox1,
        )

        self.dlg.Bind(wx.EVT_BUTTON, self.check_updates, m_button3)

        def showchangelog(evt):
            new = wx.Dialog(self.dlg)
            try:
                text = json.loads(
                    requests.get(
                        f"https://api.github.com/repos/lebao3105/texteditor/releases/v{__version__}"
                    ).text
                )["body"]
            except:
                text = _("No changelog/unable to get.")

            wb = wx.html2.WebView.New(new)
            wb.SetPage(markdown(text), "")
            new.ShowModal()

        self.dlg.Bind(wx.EVT_BUTTON, showchangelog, m_button4)

        self.dlg.Bind(
            wx.EVT_CHOICE,
            lambda evt: global_settings.set(
                "extensions.textwkr.multiview",
                "notebook_location",
                m_choice2.GetStringSelection().lower(),
            ),
            m_choice2,
        )

        # Colors page
        m_radioBox1: wx.RadioBox = page2.GetChildren()[0]
        m_colourPicker1: wx.ColourPickerCtrl = page2.GetChildren()[1].GetChildren()[1]
        m_colourPicker2: wx.ColourPickerCtrl = page2.GetChildren()[1].GetChildren()[3]
        m_choice3: wx.Choice = page2.GetChildren()[2].GetChildren()[1]
        m_textCtrl1: wx.TextCtrl = page2.GetChildren()[2].GetChildren()[3]
        m_button31: wx.TextCtrl = page2.GetChildren()[2].GetChildren()[4]

        colors = { # Correspondint to the XRC file
            _("Dark"): 1, _("Light"): 2
        }
        m_radioBox1.SetSelection(
            0
            if clrCall.getkey("color", "auto") is true
            else colors[_(clrCall.getkey("color", "background").capitalize())]
        )

        m_colourPicker1.SetColour(wx.Colour(*hextorgb(clrCall.GetColor()[0])))
        m_colourPicker2.SetColour(wx.Colour(*hextorgb(clrCall.GetColor()[1])))

        self.dlg.Bind(
            wx.EVT_RADIOBOX,
            lambda evt: self.apply_color(m_radioBox1.GetStringSelection()),
            m_radioBox1,
        )

        for i in os.listdir(THEMES_DIR):
            m_choice3.Append(i.removesuffix(".ini"))

        m_choice3.SetStringSelection(global_settings.getkey("config-paths.ui", "theme"))

        # Needs some changes
        # self.dlg.Bind(wx.EVT_COLOURPICKER_CHANGED,
        #               lambda evt: )

        # self.dlg.Bind(wx.EVT_COLOURPICKER_CHANGED,
        #               lambda evt: global_settings.set())

        def newtheme(evt):
            if not m_textCtrl1.GetLabelText():
                wx.MessageBox(
                    _("Error while setting a new theme: Name required."),
                    style=wx.ICON_ERROR | wx.OK,
                )
            else:
                # new = m_textCtrl1.GetLabel()
                # scheme = m_radioBox1.GetStringSelection().lower()
                # cfg = GetConfig(stock_ui_configs, CraftItems(THEMES_DIR, f"{new}.ini"))

                # cfg.set_and_update("color", "background", scheme)
                # cfg.set_and_update("color", "foreground", m_colourPicker1.GetTextCtrl().GetLabelText())
                # global_settings.set_and_update("config-paths.ui", "theme", new)
                # m_choice3.Append(new)
                # m_choice3.SetStringSelection(new)
                wx.MessageBox(_("Not implemented yet."))

        self.dlg.Bind(wx.EVT_BUTTON, newtheme, m_button31)

        # Editors page
        m_choice1: wx.Choice = page3.GetChildren()[0].GetChildren()[1]
        m_comboBox1: wx.ComboBox = page3.GetChildren()[0].GetChildren()[3]
        m_checkBox3: wx.CheckBox = page3.GetChildren()[0].GetChildren()[5]
        m_checkBox6: wx.CheckBox = page3.GetChildren()[0].GetChildren()[7]
        m_checkBox4: wx.CheckBox = page3.GetChildren()[1].GetChildren()[1]
        m_checkBox5: wx.CheckBox = page3.GetChildren()[1].GetChildren()[3]
        m_checkBox7: wx.CheckBox = page3.GetChildren()[1].GetChildren()[5]

        indentationTypes = ["tabs", "spaces"]

        m_choice1.SetSelection(
            indentationTypes.index(editorCfg.getkey("indentation", "type"))
        )
        m_comboBox1.SetValue(editorCfg.getkey("indentation", "size"))
        m_checkBox3.SetValue(editorCfg.getkey("indentation", "backspace_unindents"))
        m_checkBox6.SetValue(editorCfg.getkey("indentation", "show_guide"))
        m_checkBox4.SetValue(editorCfg.getkey("editor", "view_whitespaces"))
        m_checkBox5.SetValue(editorCfg.getkey("editor", "viewEOL"))
        m_checkBox7.SetValue(editorCfg.getkey("editor", "line_count"))

        self.dlg.Bind(
            wx.EVT_CHOICE,
            lambda evt: editorCfg.set_and_update(
                "indentation", "type", indentationTypes[m_choice1.GetSelection()]
            ),
            m_choice1,
        )

        self.dlg.Bind(
            wx.EVT_TEXT,
            lambda evt: editorCfg.set_and_update(
                "indentation", "size", evt.GetString()
            ),
            m_comboBox1,
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
            checkbox = locals()[f"m_checkBox{str(i)}"]
            self.dlg.Bind(
                wx.EVT_COMBOBOX,
                lambda evt: editorCfg.set_and_update(
                    "indentation" if i in [3, 6] else "editor",
                    editorSettings[i],
                    checkbox.IsChecked(),
                ),
                checkbox,
            )

        # WE.REALLY.NEED.TO.IMPLEMENT.A.NEW.PREFERENCES.LIBRARY

    def check_updates(self, evt):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "updater", f"{DATA_PATH}/updater.py"
        )
        updater = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(updater)
        updater.currver = __version__
        result = updater.parse_json(CONFIGS_PATH)

        if result is None:
            return wx.MessageBox(_("The program is up-to-date"), parent=self.dlg)
        elif result == "invalid_json":
            return wx.MessageBox(
                _(
                    "Invalid response received: Maybe an internet problem, or my data is invalid."
                ),
                parent=self.dlg,
            )
        elif result.startswith("invalid_json: "):
            return wx.MessageBox(result.split(" ")[1], parent=self.dlg)
        elif isinstance(result, tuple):
            if result[1] == "github":  # Go to GitHub releases
                rl = _(f"Changelog: {updater.RELEASES}{result[0]}")
            else:
                rl = ""
            wx.MessageBox(
                _(f"Update available: {result[0]} from branch {result[2]}." f"{rl}"),
                parent=self.dlg,
            )

    def apply_color(self, string):
        if string != _("Automatic"):
            clrCall.set("color", "background", string.lower())
            clrCall.set("color", "auto", "no")
        else:
            clrCall.set("color", "background", "light")
            clrCall.set("color", "auto", "yes")
