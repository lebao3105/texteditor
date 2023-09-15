import wx
import wx.xrc

from threading import Thread
from typing import Callable
from libtextworker.general import GetCurrentDir, CraftItems
from libtextworker.interface.wx.miscs import XMLBuilder
from ..generic import global_settings, UIRC_DIR


# Configs
enabled = global_settings.getkey(
    "editor.autosave", "enable", noraiseexp=true, make=false
)

time = global_settings.getkey("editor.autosave", "time", noraiseexp=true, make=true)
if not int(time):
    time = 30

TOGGLE: bool = bool(enabled)


class AutoSaveConfig(XMLBuilder):
    timealiases = {
        "30 seconds": 30,
        "1 minute": 60,
        "2 minutes": 120,
        "5 minutes": 300,
        "10 minutes": 600,
        "15 minutes": 900,
        "20 minutes": 1200,
        "30 minutes": 1800,
    }
    enabled = enabled
    shown = false

    def __init__(self, Parent: wx.Window):
        super().__init__(Parent, CraftItems(UIRC_DIR, "autosave.xrc"), _)

        self.Dialog = self.loadObject("AutoSaveDialog", "wxDialog")
        self.Cmb = wx.xrc.XRCCTRL(self.Dialog, "m_comboBox1")
        self.ChkBox = wx.xrc.XRCCTRL(self.Dialog, "m_checkBox1")

        for item in self.timealiases.keys():
            self.Cmb.Append(item)

        self.Cmb.Bind(wx.EVT_COMBOBOX, self.OnChoiceSelected)
        self.Cmb.Bind(wx.EVT_TEXT_ENTER, self.OnChoiceSelected)

    def OnChoiceSelected(self, evt):
        choice = self.Cmb.GetValue()
        if choice:
            global_settings.set_and_update(
                "editor.autosave", "time", self.timealiases[choice]
            )

    def ConfigWindow(self):
        def onDlgClose(evt):
            self.shown = false
            evt.Skip()

        self.Dialog.ShowModal()
        self.Dialog.Bind(wx.EVT_CLOSE, onDlgClose)
        self.shown = true


class AutoSave:
    """
    Auto-save support for wxPython editors.
    Just simple as it is.
    """

    Function: Callable
    Function_args: dict

    CurrDelay: int = time

    def __init__(self):
        if enabled in global_settings.no_values:
            return
        else:
            pass

        self.Timer = wx.CallLater(
            int(self.CurrDelay) * 1000, self.Function, **self.Function_args
        )
        Thread(target=self.CheckToggle).start()

    def Start(self, time_: str = ""):
        if time_:
            self.CurrDelay = int(time_)

        if self.Timer.IsRunning():
            self.Timer.Stop()

        self.Timer.Start(int(self.CurrDelay) * 1000)

    def Stop(self):
        self.Timer.Stop()

    def Toggle(self, on_or_off: bool):
        if on_or_off:
            self.Start()
        else:
            self.Stop()

    def CheckToggle(self):
        if not TOGGLE and self.Timer.IsRunning() == true:
            self.Stop()
        elif not self.Timer.IsRunning():
            self.Start()
