import os.path
import sys
import wx

from . import mainwindow

# Start
def _file_not_found(filename):
    return wx.MessageDialog(
        None,
        message=_("Cannot find file name %s - create it?") % filename,
        caption=_("File not found"),
        style=wx.YES_NO | wx.ICON_INFORMATION,
    ).ShowModal()


def start_app():
    """Start the application."""
    argv = sys.argv
    argc = len(argv) - 1

    root = wx.App(0)
    fm = mainwindow.MainFrame(None)
    root.SetTopWindow(fm)

    if argc > 0:
        textw = fm.notebook.text_editor
        if os.path.isfile(argv[1]):
            textw.fileops.openfile(argv[1])
        else:
            if _file_not_found(argv[1]) == wx.ID_YES:
                f = open(argv[1], mode="w")
                textw.fileops.openfile(argv[1])
                del f

        for i in range(2, argc + 1):

            if os.path.isfile(argv[i]):
                root.frame.notebook.AddTab()
                textw.fileops.openfile(argv[i])
            else:
                if _file_not_found(argv[i]) == wx.ID_YES:
                    root.frame.notebook.AddTab()
                    textw.fileops.openfile(argv[i])
                    del f
    fm.Show()
    root.MainLoop()
