import os.path
import sys
import wx

ignore_not_exists: bool = False
create_new: bool = False

def _file_not_found(filename):
    if ignore_not_exists:
        return wx.ID_CANCEL
    if create_new == True:
        return wx.ID_YES
    return wx.MessageDialog(
        None,
        message=_("Cannot find file name %s - create it?") % filename,
        caption=_("File not found"),
        style=wx.YES_NO | wx.ICON_INFORMATION,
    ).ShowModal()


def start_app(files: list[str]):
    app = wx.App()

    from .mainwindow import MainFrame
    fm = MainFrame(None)

    if len(files) >= 1:
        nb = fm.notebook
        if os.path.isfile(files[0]):
            nb.text_editor.LoadFile(files[0])
        else:
            if _file_not_found(files[0]) == wx.ID_YES:
                open(files[0], "w")
                nb.text_editor.LoadFile(files[0])
        
        for i in range(1, len(files)):
            if os.path.isfile(files[i]):
                nb.AddTab()
                nb.text_editor.LoadFile(files[i])
            else:
                if _file_not_found(files[i]) == wx.ID_YES:
                    nb.AddTab()
                    open(files[i], "w")
                    nb.text_editor.LoadFile(files[i])

    app.SetTopWindow(fm)
    fm.Show()
    app.MainLoop()
