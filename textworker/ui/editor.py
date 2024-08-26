import wx
import wx.xrc
import wx.stc

from libtextworker.interface.wx.editor import StyledTextControl

from .autosave import AutoSave, AutoSaveConfig
from ..generic import editorCfg


class Editor(StyledTextControl, AutoSave):

    def __init__(this, *args, **kwds):
        this.Function = this.SaveFile
        this.Function_args = {"filename": this.FileLoaded}

        StyledTextControl.__init__(this, *args, **kwds)
        AutoSave.__init__(this)

        this.asDlg = AutoSaveConfig(this)
        this.asDlg.OnChoiceSelected = this.OnChoiceSelected

        this.cfg = editorCfg

        # this.EditorInit() content :smile:
        this.LineNumbers()
        this.DNDSupport()
        this.IndentationSet()

        if this.cfg.Get("menu", "enabled") in this.cfg.yes_values:
            this.Bind(wx.EVT_RIGHT_DOWN, this.MenuPopup)

        this.SetWrapMode(this.cfg.Get("editor", "wordwrap") in this.cfg.yes_values)

    # AutoSaveConfig
    def ASConfig(this):
        this.asDlg.ChkBox.Hide()
        this.asDlg.ConfigWindow(this)

    def OnChoiceSelected(this, evt):
        value = this.asDlg.Cmb.GetValue()
        if value:
            this.Start(this.asDlg.timealiases[value])
