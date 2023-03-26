import threading
import wx
import wx.xrc

from typing import Any, Callable
from libtextworker.general import GetCurrentDir
from ..generic import global_settings, XMLBuilder

# Minutes to seconds
MIN_05 = 30  # 30 secs
MIN_1 = MIN_05 * 2  # 60 secs
MIN_15 = MIN_1 * 15  # 900 secs
MIN_20 = MIN_15 + MIN_1 * 5  # 1200 secs
MIN_30 = MIN_15 * 2  # 1800 secs

# Configs
enabled = global_settings.get_setting(
    "editor", "autosave", noraiseexp=True, restore=True
)
if not enabled:
    enabled = global_settings.get_setting("extensions.autosave", "enable", noraiseexp=True, resotre=False)

time = global_settings.get_setting(
    "editor", "autosave_time", noraiseexp=True, restore=True
)
if not int(time):
    time = global_settings.get_setting("extensions.autosave", "time", noraiseexp=True, restore=False)
    if not int(time):
        time = MIN_05

class AutoSaveConfig(XMLBuilder):
    timealiases = {
        "30 seconds": MIN_05,
        "1 minute": MIN_1,
        "2 minutes": MIN_1 * 2,
        "5 minutes": MIN_1 * 5,
        "10 minutes": MIN_1 * 10,
        "15 minutes": MIN_15,
        "20 minutes": MIN_20,
        "30 minutes": MIN_30,
    }
    enabled = enabled
    shown = False

    def __init__(self, Parent):
        super().__init__(
            Parent, str(GetCurrentDir(__file__, True) / ".." / "ui" / "autosave.xrc"), _
        )

        self.Dialog = self.loadObject("AutoSaveDialog", "wxDialog")
        self.Cmb = wx.xrc.XRCCTRL(self.Dialog, "m_comboBox1")
        self.ChkBox = wx.xrc.XRCCTRL(self.Dialog, "m_checkBox1")

        for item in self.timealiases.keys():
            self.Cmb.Append(item)

        self.Cmb.Bind(wx.EVT_COMBOBOX, self.OnChoiceSelected)
        self.Cmb.Bind(wx.EVT_TEXT_ENTER, self.OnChoiceSelected)

    def OnChoiceSelected(self, evt):
        choice = self.Cmb.GetValue()
        if self.ChkBox.GetValue():
            global_settings.set_setting(
                "editor", "autosave_time", self.timealiases[choice]
            )

    def ConfigWindow(self):
        def onDlgClose(evt):
            self.shown = False
            evt.Skip()

        self.Dialog.ShowModal()
        self.Dialog.Bind(wx.EVT_CLOSE, onDlgClose)
        self.shown = True

class AutoSave:
    """
    Auto-save support for wxPython editors.
    """
    Function: Callable
    Function_args: Any

    def __init__(self, editor):
        """
        Constructor of the class.
        @param editor: wxPython editable editor
        """
        self.cfg = AutoSaveConfig(editor.Parent)

        if enabled in global_settings.cfg.no_values or [False]:
            return
        else:
            pass
    
    def Start(self, time: str=time):
        return wx.CallAfter(int(time) * 1000, self.Function, **self.Function_args)
    
    def Config(self, evt=None):
        return self.cfg.ConfigWindow()