import wx
import wx.xrc
import wx.stc

from libtextworker.interface.wx.editor import StyledTextControl

from .extensions.autosave import AutoSave, AutoSaveConfig
from .generic import clrCall, editorCfg


class Editor(StyledTextControl, AutoSave, AutoSaveConfig):
    FileLoaded: str = ""

    def __init__(
        self,
        parent: wx.Window,
        id=wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style=0,
        name: str = "",
    ):
        self.Function = self.SaveFile
        self.Function_args = {"filename": self.FileLoaded}

        StyledTextControl.__init__(self, parent, id, pos, size, style, name)
        AutoSave.__init__(self)
        AutoSaveConfig.__init__(self, self)

        self.cfg = editorCfg

        # self.EditorInit() content :smile:
        self.LineNumbers()
        self.DNDSupport()
        self.IndentationSet()

        if self.cfg.getkey("menu", "enabled") in self.cfg.yes_values:
            self.Bind(wx.EVT_RIGHT_DOWN, self.MenuPopup)

        self.SetWrapMode(self.cfg.getkey("editor", "wordwrap") in self.cfg.yes_values)

        # font = self.StyleGetFont(wx.stc.STC_STYLE_DEFAULT)
        # font.SetFaceName("Consolas")
        # self.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, font)
        clrCall.configure(self)

    # AutoSaveConfig
    def ConfigWindow(self):
        wx.xrc.XRCCTRL(self.Dialog, "m_checkBox1", "wxCheckBox").Hide()
        super().ConfigWindow()

    def OnChoiceSelected(self, evt):
        value = self.Cmb.GetValue()
        if value:
            self.Start(self.timealiases[value])
