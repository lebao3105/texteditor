import os
import sys
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
        message=_("Cannot find file name %s - create it?") % filename,
        caption=_("File not found"),
        style=wx.YES_NO | wx.ICON_INFORMATION,
    ).ShowModal()


def start_app(files: list[str], directory: str | None = None):
    app = wx.App(0)
    app.SetAppName("textworker")

    textworker.ICON = getattr(textworker.icon, textworker.branch).GetIcon()
    if files:
        logger.info("Passed files: ", " ".join(files))
    
    ready()
    
    from .mainwindow import MainFrame

    fm = MainFrame()

    if len(files) >= 1:
        nb = fm.notebook
        for i in range(0, len(files)):
            if i >= 1:
                nb.AddTab(tabname=files[i])

            if not os.path.exists(files[i]):
                if _file_not_found(files[i]) != wx.ID_YES:
                    nb.DeletePage(nb.GetSelection())
                    break

            try:
                open(files[i], "r")
            except Exception as e:
                logger.warning(e)
                nb.DeletePage(nb.GetSelection())
            else:
                nb.fileops.OpenFile(files[i])

    # Needs a fix
    # if directory != None:
    #     directory = os.path.realpath(os.path.curdir + "/" + directory)
    #     print(directory)
    #     if os.path.exists(directory) and os.path.isdir(directory):
    #         fm.OpenDir(None, directory)
    #     else:
    #         logger.warning(f"{directory} does not exist as a directory. Skipping.")

    if sys.platform == "win32":
        import ctypes

        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    else:
        is_admin = os.getuid() == 0

    if is_admin:
        wx.MessageBox(
            _(
                "You are running this program as root.\n"
                "You must be responsible for your changes."
            ),
            style=wx.OK | wx.ICON_WARNING,
            parent=fm.mainFrame,
        )

    app.SetTopWindow(fm.mainFrame)
    try:
        fm.Show()
        app.MainLoop()
    except Exception as e:
        wx.MessageBox(e, _("An error occured"),
                      wx.OK_DEFAULT | wx.ICON_ERROR, fm)
        raise e
