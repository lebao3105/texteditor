import wx
import wx.xrc

from threading import Thread
from typing import Callable

from .. import _
from ..generic import global_settings
from . import autosave_generated


# Configs
enabled = global_settings['editor.autosave']["enable"]
time = global_settings['editor.autosave']["time"]
if not int(time):
    time = 30

TOGGLE: bool = enabled in global_settings.yes_values


class AutoSaveConfig(autosave_generated.AutoSaveDialog):
    timealiases = {
        _("30 seconds"): 30,
        _("1 minute"): 60,
        _("2 minutes"): 120,
        _("5 minutes"): 300,
        _("10 minutes"): 600,
        _("15 minutes"): 900,
        _("20 minutes"): 1200,
        _("30 minutes"): 1800,
    }
    enabled = enabled
    shown = False

    def __init__(this, Parent: wx.Window):

        def onDlgClose(evt):
            this.shown = False
            evt.Skip()

        autosave_generated.AutoSaveDialog.__init__(this, Parent)

        for item in this.timealiases.keys():
            this.Cmb.Append(item)

        this.Cmb.Bind(wx.EVT_COMBOBOX, this.OnChoiceSelected)
        this.Cmb.Bind(wx.EVT_TEXT_ENTER, this.OnChoiceSelected)
        this.Bind(wx.EVT_CLOSE, onDlgClose)

    def OnChoiceSelected(this, evt):
        choice = this.Cmb.GetValue()
        if choice:
            global_settings["editor"]["autosave"]["time"] = this.timealiases[choice]

    def ConfigWindow(this):
        this.ShowModal()
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
        this.Timer = wx.CallLater(
            int(this.CurrDelay) * 1000, this.Function, **this.Function_args
        )
        Thread(target=this.Toggle,
               args=(((not TOGGLE) and this.Timer.IsRunning())
                     or
                     not this.Timer.IsRunning(),)
        ).start()

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
        if (not TOGGLE) and this.Timer.IsRunning():
            this.Stop()
        elif not this.Timer.IsRunning():
            this.Start()
