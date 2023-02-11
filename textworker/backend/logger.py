import datetime
import inspect
import os
import sys
import textworker.backend
import textworker.textwidget as textwidget
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

    def __init__(self, fmt_date=None, fmt_time=None, logfile: str | None = None):
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

        if not os.path.isfile(self.log_file):
            try:
                open(self.log_file, mode="w")
            except:
                self.usable = False
                self.throwerr("Error occured: (open log file)", showdialog=True)
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
        if msg != None or "":
            message += " - {}".format(msg)
        if traceback != None or "":
            message += "\n{}".format(traceback)
        ## Craft things together
        default = "%s %s %s ~" % (date, time, str(self.obj))
        full = default + " %s" % message
        if self.usable == True:
            with open(self.log_file, mode="a") as f:
                f.write("\n" + full)
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
