import os
import sys
import textworker
import traceback
import wx

from textworker import _
from textworker.splash import splash
from textworker.icons import icon
from textworker.generic import logger, ready
from wx.lib.agw.advancedsplash import AdvancedSplash, AS_TIMEOUT, AS_CENTER_ON_SCREEN

ignore_not_exists: bool = False
create_new: bool = False


def start_app(files: list[str], directory: list[str], showsplash: bool):

    def _file_not_found(filename):
        if ignore_not_exists: return wx.ID_CANCEL
        
        if create_new: return wx.ID_YES
        
        return wx.MessageBox(_("Cannot find file name %s - create it?") % filename,
                             _("File not found"), wx.YES_NO | wx.ICON_INFORMATION, fm)

    if files: logger.info("Passed files: ", " ".join(files))

    ready()

    textworker.ICON = icon.GetIcon()
    from .ui.mainwindow import MainFrame


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
                nb.OpenFile(files[i])

    for path in directory: fm.OpenDir(None, path)

    if sys.platform == "win32":
        import ctypes

        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    else:
        is_admin = (os.getuid() == 0)

    if is_admin:
        wx.MessageBox(_("You are running this program as root.\n"
                                   "You must be responsible for your changes."),
                      style=wx.OK | wx.ICON_WARNING,
                      parent=fm)
    del is_admin

    exchook = sys.excepthook
    def handleexc(exc_type, value, traceb):
        trace_back = traceback.extract_tb(traceb)

        dlg = wx.Dialog(None, title=_("Exception caught"),
                        style=wx.DEFAULT_DIALOG_STYLE)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(dlg, -1,
                              _("An error occured and textworker caught it:\n"
                                f"Exception type: {exc_type.__name__}\n"
                                f"Exception message: {value}\n")),
                0, wx.ALIGN_CENTER | wx.TOP, 10)
        
        boxInfo = wx.ListCtrl(dlg, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        boxInfo.InsertColumn(0, _("File"))
        boxInfo.InsertColumn(1, _("Line"))
        boxInfo.InsertColumn(2, _("Function"))
        boxInfo.InsertColumn(3, _("Called code"))
        
        for x in range(len(trace_back)):
            data = trace_back[x]
            boxInfo.InsertItem(x, os.path.basename(data[0]))
            boxInfo.SetItem(x, 1, str(data[1]))
            boxInfo.SetItem(x, 2, str(data[2]))
            boxInfo.SetItem(x, 3, str(data[3]))

        for i in range(0, 4): boxInfo.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

        box.Add(boxInfo, 1, wx.EXPAND | wx.ALL, 5)

        from textworker.generic import clrCall
        clrCall.configure(dlg)
        clrCall.autocolor_run(dlg)
        
        # logger.exception(f"Exception occured (type {exc_type}): {value}\n{trace_back}")

        dlg.SetSizer(box)
        box.Fit(dlg)
        dlg.Show()
        
        exchook(exc_type, value, traceb)

    sys.excepthook = handleexc

    # https://stackoverflow.com/a/27872625
    if sys.platform == "win32":
        import ctypes

        myappid = "me.lebao3105.textworker"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    fm = MainFrame()
    fm.SetIcon(textworker.ICON)

    if showsplash:
        AdvancedSplash(fm, bitmap=splash.GetBitmap(), timeout=5000,
                       agwStyle=AS_TIMEOUT | AS_CENTER_ON_SCREEN)
        wx.CallLater(5000, fm.Show).Start()
    else:
        fm.Show()
