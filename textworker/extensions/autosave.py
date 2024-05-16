import wx
import wx.xrc

from threading import Thread
from typing import Callable
from libtextworker.general import CraftItems
from libtextworker.interface.wx.miscs import XMLBuilder

from .. import _
from ..generic import global_settings, UIRC_DIR


# Configs
enabled = eval(global_settings['editor']['autosave'])["enable"]
time = eval(global_settings['editor']['autosave'])["time"]
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
    shown = False

    def __init__(this, Parent: wx.Window):
        XMLBuilder.__init__(this, Parent, CraftItems(UIRC_DIR, "autosave.xrc"), _)

        this.Dialog = this.loadObject("AutoSaveDialog", "wxDialog")
        this.Cmb = wx.xrc.XRCCTRL(this.Dialog, "m_comboBox1")
        this.ChkBox = wx.xrc.XRCCTRL(this.Dialog, "m_checkBox1")

        for item in this.timealiases.keys():
            this.Cmb.Append(item)

        this.Cmb.Bind(wx.EVT_COMBOBOX, this.OnChoiceSelected)
        this.Cmb.Bind(wx.EVT_TEXT_ENTER, this.OnChoiceSelected)

    def OnChoiceSelected(this, evt):
        choice = this.Cmb.GetValue()
        if choice:
            global_settings["editor"]["autosave"]["time"] = this.timealiases[choice]

    def ConfigWindow(this):
        def onDlgClose(evt):
            this.shown = False
            evt.Skip()

        this.Dialog.ShowModal()
        this.Dialog.Bind(wx.EVT_CLOSE, onDlgClose)
        this.shown = True


class AutoSave:
    """
    Auto-save support for wxPython editors.
    Just simple as it is.
    """

    Function: Callable
    Function_args: dict

    CurrDelay: int = time

    def __init__(this):
        if enabled in global_settings.no_values:
            return

        this.Timer = wx.CallLater(
            int(this.CurrDelay) * 1000, this.Function, **this.Function_args
        )
        Thread(target=this.CheckToggle).start()

    def Start(this, time_: str = ""):
        if time_:
            this.CurrDelay = int(time_)

        if this.Timer.IsRunning():
            this.Timer.Stop()

        this.Timer.Start(int(this.CurrDelay) * 1000)

    def Stop(this):
        this.Timer.Stop()

    def Toggle(this, on_or_off: bool):
        if on_or_off:
            this.Start()
        else:
            this.Stop()

    def CheckToggle(this):
        if not TOGGLE and this.Timer.IsRunning():
            this.Stop()
        elif not this.Timer.IsRunning():
            this.Start()
