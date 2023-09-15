import os
import requests
import wx
import wx.xrc

from libtextworker.general import CraftItems
from libtextworker.interface.wx.miscs import XMLBuilder, BindEvents
from ..generic import CONFIGS_PATH, UIRC_DIR, clrcall, _editor_config_load, global_settings, DATA_PATH
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
    NB_LOC: str = global_settings.getkey("extensions.textwkr.multiview", "notebook_location", True, True, True)

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
        m_checkbox1 = page1.GetChildren()[0].GetChildren()[0]
        m_button3 = page1.GetChildren()[0].GetChildren()[1]
        m_choice2 = page1.GetChildren()[1].GetChildren()[1]

        self.dlg.Bind(
            wx.EVT_CHECKBOX,
            lambda evt: global_settings.set("base", "autoupdate", m_checkbox1.IsChecked()),
            m_checkbox1
        )

        self.dlg.Bind(
            wx.EVT_BUTTON,
            self.check_updates,
            m_button3
        )

        # Bottom bar
        # We just need to bind the apply button
        self.dlg.Bind(wx.EVT_BUTTON,
            self.Apply, self.dlg.GetChildren()[2]
        )
    
    def Apply(self, evt):
        evt.Skip()
        
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
            return wx.MessageBox(
                _("The program is up-to-date"),
                parent=self.dlg
            )
        elif result == "invalid_json":
            return wx.MessageBox(
                _("Invalid response received: Maybe an internet problem, or my data is invalid."),
                parent=self.dlg
            )
        elif result.startswith("invalid_json: "):
            return wx.MessageBox(
                result.split(" ")[1],
                parent=self.dlg
            )
        elif isinstance(result, tuple):
            if result[1] == "github": # Go to GitHub releases
                rl = _(f"Changelog: {updater.RELEASES}{result[0]}")
            else:
                rl = ""
            wx.MessageBox(
                _(f"Update available: {result[0]} from branch {result[2]}."
                  f"{rl}"
                ),
                parent=self.dlg
            )