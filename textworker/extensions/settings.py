import wx
import wx.xrc

from libtextworker.general import CraftItems
from libtextworker.interface.wx.miscs import XMLBuilder
from ..generic import UIRC_DIR, clrcall, _editor_config_load, global_settings

class SettingsDialog(XMLBuilder):
    """
    A WIP, useful textworker settings dialog with lots of things inside lol.
    We're all waiting for new features;)
    """
    
    """
    ~~Here are our configs per-page~~ (not this time)
    All changes will only be applied on the "Apply" button click event
    This should be optional.
    """

    def __init__(self, Parent: wx.Window):
        XMLBuilder.__init__(self, Parent, CraftItems(UIRC_DIR, "preferences.xrc"), _)

        # Here is our get-n-bind time
        # Top-level widgets first
        self.dlg: wx.Dialog = self.loadObject("StDialog", "wxDialog")
        StdDlgButtons: wx.StdDialogButtonSizer = self.loadObject("m_sdbSizer1", "wxStdDialogButtonSizer")
        
        # General page

        # self.dlg.Bind(
        #     wx.EVT_CHECKBOX
        #     wx.xrc.XRCCTRL(self.dlg, "m_checkBox1")
        # )

        # Bottom bar
        # We just need to bind the apply button
        self.dlg.Bind(
            wx.EVT_BUTTON, self.Apply,
            StdDlgButtons.GetChildren()[1]
        )
    
    def Apply(self, evt):
        evt.Skip()
        
