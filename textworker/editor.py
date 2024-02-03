import wx
import wx.xrc
import wx.stc

from libtextworker.interface.wx.editor import StyledTextControl

from .extensions.autosave import AutoSave, AutoSaveConfig
from .generic import editorCfg


class Editor(StyledTextControl, AutoSave, AutoSaveConfig):

    def __init__(
        this,
        parent: wx.Window,
        id=wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style=0,
        name: str = "",
    ):
        this.Function = this.SaveFile
        this.Function_args = {"filename": this.FileLoaded}

        StyledTextControl.__init__(this, parent, id, pos, size, style, name)
        AutoSave.__init__(this)
        AutoSaveConfig.__init__(this, this)

        this.cfg = editorCfg

        # this.EditorInit() content :smile:
        this.LineNumbers()
        this.DNDSupport()
        this.IndentationSet()

        if this.cfg.getkey("menu", "enabled") in this.cfg.yes_values:
            this.Bind(wx.EVT_RIGHT_DOWN, this.MenuPopup)

        this.SetWrapMode(this.cfg.getkey("editor", "wordwrap") in this.cfg.yes_values)

    # AutoSaveConfig
    def ConfigWindow(this):
        wx.xrc.XRCCTRL(this.Dialog, "m_checkBox1", "wxCheckBox").Hide()
        AutoSaveConfig.ConfigWindow(this)

    def OnChoiceSelected(this, evt):
        value = this.Cmb.GetValue()
        if value:
            this.Start(this.timealiases[value])
