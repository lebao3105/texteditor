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


class AutoSave(XMLBuilder):
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

    enabled = global_settings.get_setting("editor", "autosave")
    shown = False

    Function: Callable
    Function_args: Any

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
        self.Configure(self.timealiases[choice])

    def Configure(self, time: str in timealiases):
        self.thread = threading.Thread(target=self._Run(time), daemon=True)
        self.thread.start()
        return

    def _Run(self, time: str):
        wx.CallLater(int(time) * 1000, self.Function, self.Function_args)

    def ConfigWindow(self):
        self.Dialog.ShowModal()
        self.shown = True
