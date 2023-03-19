import datetime
import inspect
import os
import os.path
import sys
import texteditor
import texteditor.backend
import tkinter.ttk as ttk
import traceback
from texteditor.backend import textwidget

texteditor.backend.require_version("1.4b0", ">=")


class Logger(object):
    format_date = "%m-%d-%Y"  # Month day year
    format_time = "%H:%M:%S"  # Hour min sec

    if sys.platform == "win32":
        __dir = os.environ["USERPROFILE"]
        logfile = __dir + "\\.logs\\texteditor.log"
    else:
        __dir = os.environ["HOME"]
        logfile = __dir + "/.logs/texteditor.log"

    def __init__(self, fmt_date=None, fmt_time=None, logfile=None):
        """
        A basic logger class.
        :param fmt_date=None : Date format (default is %m-%d-%Y)
        :param fmt_time=None : Time format (default is %H:%M:%S)
        :param logfile=None : File to log to (default is texteditor's one)
        """
        if fmt_date is not None:
            self.format_date = fmt_date
        if fmt_time is not None:
            self.format_time = fmt_time
        if logfile is not None:
            self.logfile = logfile

        try:
            open(self.logfile, mode="a")
        except OSError:
            self.usable = False
            self.throwerr(
                "Error occured: (open log file)", "Please contact the developer."
            )
        else:
            # Don't write test log to files (temporary?)
            self.usable = True

    def printtext(self, title, msg=None, traceback=None) -> str:
        self.obj = inspect.getmodule(inspect.stack()[1][0]).__name__
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
            with open(self.logfile, mode="a") as f:
                f.write("\n")
                f.write(full)
        print(full)
        return full

    def throwerr(self, title, noexp: bool = False, msg=None):
        """Throws an exception message with its traceback and a custom message."""
        if noexp is True:
            traceback_msg = ""
        else:
            traceback_msg = traceback.format_exc()
        return self.printtext(title, msg if msg is not None else "", traceback_msg)

    def throwinf(self, title, msg=None):
        return self.printtext(title, msg if msg is not None else "")

    def throwwarn(self, title, msg=None):
        return self.printtext(title, msg if msg is not None else "")


class GenericLogs(Logger):
    """
    A class built on top of the Logger class, but this has
    some extra functions to specific errors.
    """

    def FileIOError(self, msg: str):
        """
        :param msg (str): Error message

        Throws an File I/O exception.
        """
        return self.throwerr("File I/O Error", msg=msg)

    def ConfigurationError(self, msg: str):
        """
        :param msg (str): Error message

        Throws an configuration file parser error.
        """
        return self.throwerr("Configuration Error", msg=msg)

    def GUIError(self, title: str, msg: str):
        """
        :param msg (str): Error message

        Throws an error occured from GUI app.
        """
        return self.throwerr("GUI App error", msg=msg)


class StatusBar(ttk.Frame):
    def __init__(self, parent, pack: bool = False, **kwargs):
        super().__init__(master=parent, **kwargs)

        self.textw = parent
        self.logs = []
        self.islogwindowopen = False

        self.lefttext = ttk.Label(self, cursor="hand2")
        self.righttext = ttk.Label(self)
        self.lefttext.configure(state="readonly")
        self.righttext.configure(state="readonly")

        self.righttext.bind("<KeyRelease>", self.keypress)
        self.lefttext.bind("<Button-1>", lambda e: self.get_messages())

        self.lefttext.pack(side="left")
        self.righttext.pack(side="right")

        # get_config.GetConfig.configure(self)
        # get_config.GetConfig.configure(self.lefttext)
        # get_config.GetConfig.configure(self.righttext)

        self.keypress()
        self.writeleftmessage(_("No new message."), nowrite=True)

        if pack == True:
            self.pack(side="bottom", fill="x")  # TODO: Place it outside the text editor

    def keypress(self, event=None):
        row, col = self.textw.index("insert").split(".")
        self.righttext.config(text=_("Line %s : Col %s") % (str(row), str(col)))

    def writeleftmessage(self, message: str, nowrite: bool = None, event=None):
        self.lefttext.config(text=message)
        if nowrite is True:
            return
        now = datetime.datetime.now()
        date = now.strftime(Logger.format_date)
        time = now.strftime(Logger.format_time)
        self.logs.append("{} {} - {}".format(date, time, message))
        self.after(
            3500,
            lambda: self.lefttext.config(text=_("New message(s) collected.")),
        )

    def get_messages(self):
        curridx: int = 0
        isplaced: bool

        def refresh(replace: bool = None, event=None):
            nonlocal curridx
            nonlocal isplaced

            label1 = ttk.Label(mss, text=_("No new message here."))
            label2 = ttk.Label(mss, text=_("You always can refresh by press F5 key."))

            # This needs a fix
            if not self.logs:
                label1.config(font=(label1["font"], 14))
                mss.bind("<F5>", lambda event: refresh(replace=True))

                # get_config.GetConfig(label1, "config")
                # get_config.GetConfig(label2, "config")

                alllogs.forget()
                yscroll.forget()
                label1.pack(pady="0 30")
                label2.pack(pady="0 30")
                isplaced = False

            if replace == True and isplaced == False:
                mss.bind("<F5>", lambda event: refresh())
                label1.config(text=_("All logs"))
                yscroll.pack(side="right", fill="y")
                alllogs.pack(expand=True, fill="both")
                isplaced = True

            alllogs.config(state="normal")
            for i in range(curridx, len(self.logs)):
                alllogs.insert("end", self.logs[i] + "\n")
            curridx = len(self.logs)

            alllogs.config(state="disabled")

        def on_close():
            self.islogwindowopen = False
            mss.destroy()
            return  # That's it

        import tkinter as tk

        if self.islogwindowopen is True:
            return

        mss = tk.Toplevel(self)
        alllogs = textwidget.TextWidget(mss, useMenu=True, unRedo=False)
        yscroll = ttk.Scrollbar(mss, orient="vertical", command=alllogs.yview)

        mss.bind("<F5>", lambda event: refresh())
        alllogs.config(state="disabled")
        alllogs.RMenu.delete(2)
        alllogs.RMenu.add_command(
            label=_("Refresh"), command=lambda: refresh(), accelerator="F5"
        )

        yscroll.pack(side="right", fill="y")
        alllogs.pack(expand=True, fill="both")
        refresh()

        mss.wm_title(_("Logs"))
        mss.protocol("WM_DELETE_WINDOW", on_close)
        mss.mainloop()
        self.islogwindowopen = True


class LoggerWithStatusbar(Logger):
    def __init__(self, parent, showlog: bool = False, pack: bool = False, **kwargs):
        """Parameters:
        * parent: Parent of the statusbar or the statusbar itself
            (texteditor.backend.logger.StatusBar)
        * showlog (boolean): Whetever to show the message to the statusbar
            (default is False, anyway this class will append messages to
            StatusBar.logs)
        * pack (boolean): Pack the StatusBar (ignore this if you use Grid or parent is a StatusBar)
        * **kwargs: Configurations for the base Logger class"""
        super().__init__(**kwargs)
        self.showlog = showlog
        if isinstance(parent, StatusBar):
            self.statusbar = parent
        else:
            self.statusbar = StatusBar(parent, pack)

    def throwerr(self, title, noexp: bool = False, msg=""):
        msg = super().throwerr(title, noexp, msg)
        if self.showlog is True:
            self.statusbar.writeleftmessage(title)
        self.statusbar.logs.append(msg)
        return msg

    def throwinf(self, title, msg=""):
        msg = super().throwinf(title, msg)
        if self.showlog is True:
            self.statusbar.writeleftmessage(title)
        self.statusbar.logs.append(msg)
        return msg

    def throwwarn(self, title, msg=""):
        msg = super().throwwarn(title, msg)
        if self.showlog is True:
            self.statusbar.writeleftmessage(title)
        self.statusbar.logs.append(msg)
        return msg
