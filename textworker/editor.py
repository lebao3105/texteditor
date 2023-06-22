import wx
import wx.xrc

from libtextworker.interface.wx.editor import StyledTextControl

from .extensions.autosave import AutoSave, AutoSaveConfig
from .generic import _editor_config_load


class Editor(StyledTextControl, AutoSave, AutoSaveConfig):
    
    FileLoaded: str = _("New file")
    
    def __init__(
            self,
            parent: wx.Window,
            id = wx.ID_ANY,
            pos: wx.Point = wx.DefaultPosition,
            size: wx.Size = wx.DefaultSize,
            style = 0,
            name: str = ""
        ):
        self.Function = self.SaveFile
        self.Function_args = {"filename": self.FileLoaded}

        StyledTextControl.__init__(self, parent, id, pos, size, style, name)
        AutoSave.__init__(self)
        AutoSaveConfig.__init__(self, self)
        
        self.EditorInit(_editor_config_load)


    def ConfigWindow(self):
        wx.xrc.XRCCTRL(self.Dialog, "m_checkBox1", "wxCheckBox").Hide()
        super().ConfigWindow()

    def OnChoiceSelected(self, evt):
        value = self.Cmb.GetValue()
        if value:
            self.Start(self.timealiases[value])