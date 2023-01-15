import datetime
import inspect
import os
import sys
import textworker.backend
import textworker.tabs as tabs
import traceback
import wx

textworker.backend.require_version("1.6a", ">=")

__dir = os.environ["USERPROFILE"] if sys.platform == "win32" else os.environ["HOME"]
if sys.platform == "win32":
    logfile_ = __dir + "\\.logs\\texteditor.log"
else:
    logfile_ = __dir + "/.logs/texteditor.log"


class Logger:
    format_date = "%m-%d-%Y"  # Month day year
    format_time = "%H:%M:%S"  # Hour min sec
    log_file = logfile_

    def __init__(self, fmt_date=None, fmt_time=None, logfile:str|None=None):
        """Logging unit of texteditor.
        :param fmt_date=None : Date format
        :param fmt_time=None : Time format
        :param logfile=None : Log file

        If logfile is not specified, logger will use texteditor's
        default log path.
        """
        if fmt_date is not None:
            self.format_date = fmt_date
        if fmt_time is not None:
            self.format_time = fmt_time
        if logfile is not None:
            self.log_file = logfile

        self.obj = inspect.getmodule(inspect.stack()[1][0]).__name__
        self.logs = []
        self.islogwindopen: bool = False

        if not os.path.isfile(self.log_file):
            try:
                open(self.log_file, mode="w")
            except:
                self.usable = False
                self.throwerr(
                    "Error occured: (open log file)",
                    showdialog=True
                )
            else:
                self.usable = True
        else:
            self.usable = True

    def printtext(self, title, msg=None, traceback=None):
        """Create a log message with time+date, write it to the log file
        and show it to the console."""
        ## Date time
        now = datetime.datetime.now()
        date = now.strftime(self.format_date)
        time = now.strftime(self.format_time)
        ## Message
        message = title
        if msg is not None or "":
            message += " - {}".format(msg)
        if traceback is not None or "":
            message += "\n{}".format(traceback)
        ## Craft things together
        default = "%s %s %s ~" % (date, time, str(self.obj))
        full = default + " %s" % message
        if self.usable == True:
            with open(self.log_file, mode="a") as f:
                f.write(full)
        self.logs.append(full)
        print(full)

    def throwerr(self, title, noexp: bool = False, msg=None, showdialog: bool = False):
        """Throws an exception message with its traceback and a custom message."""
        if noexp is True:
            traceback_msg = ""
        else:
            traceback_msg = traceback.format_exception(*sys.exc_info())
        if showdialog is True:
            wx.MessageDialog(
                None, message=msg, caption=title, style=wx.OK | wx.ICON_ERROR
            ).ShowModal()
        return self.printtext(title, msg if msg is not None else "", traceback_msg)

    def throwinf(self, title, msg=None, showdialog: bool = False):
        if showdialog is True:
            wx.MessageDialog(
                None, message=msg, caption=title, style=wx.OK | wx.ICON_INFORMATION
            ).ShowModal()
        return self.printtext(title, msg if msg is not None else "")

    def throwwarn(self, title, msg=None, showdialog: bool = False):
        if showdialog is True:
            wx.MessageDialog(
                None, message=msg, caption=title, style=wx.OK | wx.ICON_WARNING
            ).ShowModal()
        return self.printtext(title, msg if msg is not None else "")

    def logwindow(self, evt=None):
        def onwindowclose(evt):
            self.islogwindopen = False
            logwind.fm.Destroy()

        if self.islogwindopen == True:
            return

        logwind = LogsWindow(self.logs)
        logwind.fm.Bind(wx.EVT_CLOSE, onwindowclose)

        logwind.Show()
        self.islogwindopen = True


class LogsWindow:
    def __init__(self, logs: list[str], parent=None):
        """Logs window - use wx.Frame
        :param logs (list) : All logs
        :param parent=None : Parent of the frame

        Objects:
        * fm : Main frame
        * label1, label2 : Message text
        * text : Log object

        Press F5 to refresh the log window (not tested.)
        """

        self._curridx: int = 0
        self._istexthere: bool = False
        self.logs = logs

        self.fm = wx.Frame(parent, title="Logs")

        panel = wx.Panel(self.fm, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.label1 = wx.StaticText(
            panel, wx.ID_ANY, "No new message collected.", style=wx.TE_READONLY
        )
        self.label1.SetFont(
            wx.Font(
                14,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                0,
                "",
            )
        )
        sizer.Add(self.label1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 52, wx.EXPAND)

        self.label2 = wx.StaticText(
            panel, wx.ID_ANY, "Press F5 to refresh.", style=wx.TE_READONLY
        )
        self.label2.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                1,
                "",
            )
        )
        sizer.Add(self.label2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0, wx.EXPAND)

        self.text = tabs.TextWidget(
            panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.EXPAND
        )
        self.text.Hide()

        panel.SetSizerAndFit(sizer)
        self.fm.Bind(wx.EVT_CHAR_HOOK, self.onkeypressed)
        self.refresh()

        self.fm.Layout()

    def onkeypressed(self, evt):
        key = evt.GetKeyCode()
        if key == wx.WXK_F5:
            self.refresh()
        else:
            evt.Skip()

    def refresh(self):
        if self._istexthere == False and self.logs:
            self.text.Show()
            for i in range(self._curridx, len(self.logs)):
                self.text.AppendText(self.logs[i] + "\n")
            self._curridx = len(self.logs)
            self._istexthere = True
        else:
            self.text.Hide()
            self.label1.SetLabelText("No new message collected.")
            self.label2.SetLabelText("Press F5 to refresh.")
            self._istexthere = False

    def Show(self, show: bool = True):
        """Show the window."""
        return self.fm.Show(show)
