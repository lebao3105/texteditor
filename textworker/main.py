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
    root.SetExitOnFrameDelete(True)

    if argc > 0:
        nb = fm.notebook
        if os.path.isfile(argv[1]):
            nb.fileops.openfile(argv[1])
        else:
            if _file_not_found(argv[1]) == wx.ID_YES:
                f = open(argv[1], mode="w")
                nb.fileops.openfile(argv[1])
                del f

        for i in range(2, argc + 1):

            if os.path.isfile(argv[i]):
                nb.AddTab()
                nb.fileops.openfile(argv[i])
            else:
                if _file_not_found(argv[i]) == wx.ID_YES:
                    nb.AddTab()
                    f = open(argv[i], "w")
                    nb.fileops.openfile(argv[i])
                    del f
                    
    fm.Show()
    root.MainLoop()
