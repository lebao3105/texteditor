import os
import sys
import traceback
import wx

import textworker
import textworker.icon
from textworker.generic import logger, ready

ignore_not_exists: bool = False
create_new: bool = False


def _file_not_found(filename):
    if ignore_not_exists:
        return wx.ID_CANCEL
    if create_new == True:
        return wx.ID_YES
    return wx.MessageDialog(
        None,
        message=textworker._("Cannot find file name %s - create it?") % filename,
        caption=textworker._("File not found"),
        style=wx.YES_NO | wx.ICON_INFORMATION,
    ).ShowModal()


def start_app(files: list[str], directory: list[str]):
    app = wx.App(0)
    app.SetAppName("textworker")

    textworker.ICON = getattr(textworker.icon, textworker.branch).GetIcon()
    if files: logger.info("Passed files: ", " ".join(files))
    
    ready()
    
    from .mainwindow import MainFrame

    fm = MainFrame()

    if len(files) >= 1:
        nb = fm.notebook

        for i in range(0, len(files)):
            if i >= 1:
                nb.AddTab(tabname=files[i])

            if not os.path.isfile(files[i]):
                if _file_not_found(files[i]) != wx.ID_YES:
                    nb.DeletePage(nb.GetSelection())
                    continue

            try:
                open(files[i], "r")
            except Exception as e:
                logger.warning(str(e))
                nb.DeletePage(nb.GetSelection())
                raise e
            else:
                nb.fileops.OpenFile(files[i])

    for path in directory: fm.OpenDir(None, path)

    if sys.platform == "win32":
        import ctypes

        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    else:
        is_admin = os.getuid() == 0

    if is_admin:
        wx.MessageBox(textworker._("You are running this program as root.\n"
                                   "You must be responsible for your changes."),
                      style=wx.OK | wx.ICON_WARNING,
                      parent=fm.mainFrame)

    app.SetTopWindow(fm.mainFrame)
    
    exchook = sys.excepthook

    def handleexc(exc_type, value, traceb):
        trace_back = traceback.extract_tb(traceb)

        dlg = wx.Dialog(fm.mainFrame, title=textworker._("Exception caught"),
                        style=wx.DEFAULT_DIALOG_STYLE)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(dlg, -1,
                              textworker._("An error occured and textworker caught it:\n"
                                                 f"Exception type: {exc_type.__name__}\n"
                                                 f"Exception message: {value}\n")),
                0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        boxInfo = wx.ListCtrl(dlg, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        boxInfo.InsertColumn(0, textworker._("File"))
        boxInfo.InsertColumn(1, textworker._("Line"))
        boxInfo.InsertColumn(2, textworker._("Function"))
        boxInfo.InsertColumn(3, textworker._("Called code"))
        
        for x in range(len(trace_back)):
            data = trace_back[x]
            boxInfo.InsertItem(x, os.path.basename(data[0]))
            boxInfo.SetItem(x, 1, str(data[1]))
            boxInfo.SetItem(x, 2, str(data[2]))
            boxInfo.SetItem(x, 3, str(data[3]))

        for i in range(0, 4): boxInfo.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

        box.Add(boxInfo, 1, wx.EXPAND | wx.ALL, 5)

        from textworker.generic import clrCall
        clrCall.configure(dlg, True)
        
        # logger.exception(f"Exception occured (type {exc_type}): {value}\n{trace_back}")
        exchook(exc_type, value, traceb)

        dlg.SetSizer(box)
        box.Fit(dlg)
        dlg.Show()

    sys.excepthook = handleexc

    fm.Show()
    app.MainLoop()
