import os
import wx

from . import _
from .generic import global_settings
from hashlib import md5

searchdir = global_settings.getkey("editor", "searchdir", noraiseexp=true, make=true)
if not os.path.isdir(searchdir):
    searchdir = os.path.expanduser("~/Documents")


class FileOperations:
    Tabber: wx.Window

    file_dialog = wx.FileDialog(nil, defaultDir=searchdir)
    message = wx.MessageDialog(nil, "")

    def __init__(this, Tabber: wx.Window):
        this.Tabber = Tabber

    def AskToOpen(this, evt=nil):
        this.file_dialog.SetName(_("Open a file"))
        result = this.file_dialog.ShowModal()
        if result == wx.ID_OK:
            this.OpenFile(this.file_dialog.GetPath())

    def AskToSave(this, evt=nil):
        this.file_dialog.SetName(_("Save this to..."))
        result = this.file_dialog.ShowModal()

        if result == wx.ID_OK:
            this.Tabber.GetCurrentPage().SaveFile(this.file_dialog.GetPath())

    def SaveFileEvent(this, evt=nil):
        tablabel = this.Tabber.GetPageText(this.Tabber.GetSelection())
        if not os.path.isfile(tablabel):
            return this.AskToSave()
        else:
            return this.SaveFile(tablabel)

    def OpenFile(this, path: str):
        if this.Tabber.GetCurrentPage().IsModified:
            this.Tabber.AddTab()

        this.Tabber.GetCurrentPage().LoadFile(path) # Load the content
        this.Tabber.GetCurrentPage().FileLoaded = path

        this.Tabber.SetPageText(this.Tabber.GetSelection(), path) # Set tab title
        wx.GetTopLevelParent(this.Tabber).SetTitle(path) # Set the window title

    def SaveFile(this, path: str):
        return this.Tabber.GetCurrentPage().SaveFile(path)

    def OnEditorDestroy(this, evt):
        curreditor = evt.GetWindow()
        path = curreditor.FileLoaded if curreditor.FileLoaded else "this new file"

        if curreditor.IsModified:
            ask = wx.MessageBox(_(f"Save {path}? It has unsaved changes."),
                                _("Not saved"), wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT)
            
            if ask == wx.YES:
                if curreditor.FileLoaded != path: this.AskToSave()
                else: this.SaveFile(path)

            elif ask == wx.CANCEL:
                return

        evt.Skip()
    
    def OnEditorModify(this, evt: wx.KeyEvent):
        editor = evt.GetEventObject()

        editor.Hash = md5(editor.GetText().encode("utf-8"))
        if editor.FileLoaded:
            if not this.Tabber.GetPageText(this.Tabber.GetPageIndex(editor)).endswith(" *"):
                # print(this.Tabber.GetPageIndex(editor))
                this.Tabber.SetPageText(this.Tabber.GetPageIndex(editor), editor.FileLoaded + " *")

        evt.Skip()