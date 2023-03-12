import pathlib
import wx
import wx.xrc
from ..generic import global_settings, XMLBuilder

# Minutes to seconds
MIN_05 = 30  # 30 secs
MIN_1 = MIN_05 * 2  # 60 secs
MIN_15 = MIN_1 * 15  # 900 secs
MIN_20 = MIN_15 + MIN_1 * 5  # 1200 secs
MIN_30 = MIN_15 * 2  # 1800 secs


class AutoSave(XMLBuilder):

    cmbitems = [
        "30 seconds",
        "1 minute",
        "2 minutes",
        "5 minutes",
        "10 minutes",
        "15 minutes",
        "20 minutes",
        "30 minutes",
    ]

    timealiases = [
        MIN_05,
        MIN_1,
        MIN_1 * 2,
        MIN_1 * 5,
        MIN_1 * 10,
        MIN_15,
        MIN_20,
        MIN_30,
    ]

    enabled = global_settings.get_setting("editor", "autosave")
    shown = False

    def __init__(self, Parent):
        super().__init__(Parent, str(pathlib.Path(__file__).parent / ".." / "ui" / "autosave.xrc"), _)
    
    def ConfigWindow(self):
        self.Dialog = self.loadObject("AutoSaveDialog", "wxDialog")
        self.Cmb = wx.xrc.XRCCTRL(self.Dialog, "m_comboBox1")

        self.Dialog.ShowModal()
        self.shown = True
    
    @property
    def Function(self):
        return self._Function
    
    @Function.setter
    def Function(self, fn):
        self._Function = fn
    
    @Function.deleter
    def Function(self, fn):
        self._Function = None
