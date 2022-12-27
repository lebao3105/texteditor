import datetime
import gettext
import os
import sys
import traceback
import tkinter.ttk as ttk
from texteditor.backend import get_config


class Logger:
    format_date = "%m-%d-%Y"  # Month day year
    format_time = "%H:%M:%S"  # Hour min sec
    __dir = os.environ["USERPROFILE"] if sys.platform == "win32" else os.environ["HOME"]
    if sys.platform == "win32":
        logfile = __dir + "\\.logs\\texteditor.log"
    else:
        logfile = __dir + "/.logs/texteditor.log"

    def __init__(self, obj: str, fmt_date=None, fmt_time=None, logfile=None):
        if fmt_date is not None:
            self.format_date = fmt_date
        if fmt_time is not None:
            self.format_time = fmt_time
        if logfile is not None:
            self.logfile = logfile
        self.obj = obj

        try:
            open(self.logfile, mode="w")
        except Exception:
            self.usable = False
            self.throwerr(
                "Error occured: (open log file)", "Please contact the developer."
            )
        else:
            self.usable = True

    def printtext(self, title, msg=None, traceback=None):
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
            with open(self.logfile, mode="w") as f:
                f.write(full)
        print(full)

    def throwerr(self, title, msg=None):
        """Throws an exception message with its traceback and a custom message."""
        return self.printtext(
            title, msg if msg is not None else "", traceback.format_exc()
        )

    def throwinf(self, title, msg=None):
        return self.printtext(title, msg if msg is not None else "")

    def throwwarn(self, title, msg=None):
        return self.printtext(title, msg if msg is not None else "")


class StatusBar(ttk.Frame):
    def __init__(self, parent, _=None, bindsignal: bool = None, **kwargs):
        super().__init__(master=parent, **kwargs)

        if _ is None:
            self._ = gettext.gettext
        else:
            self._ = _

        self.lefttext = ttk.Label(self, cursor="hand2")
        self.righttext = ttk.Label(self)
        self.lefttext.configure(state="readonly")
        self.righttext.configure(state="readonly")

        if bindsignal is True:
            self.righttext.bind("<KeyRelease>", self.keypress)
        self.lefttext.bind("<Button-1>", lambda e: self.get_messages())

        self.lefttext.pack(side="left")
        self.righttext.pack(side="right")

        get_config.GetConfig.configure(self)
        get_config.GetConfig.configure(self.lefttext)
        get_config.GetConfig.configure(self.righttext)

        self.textw = parent
        self.logs = []
        self.keypress()
        self.writeleftmessage(self._("No new message."), nowrite=True)

        self.pack(side="bottom", fill="x")  # TODO: Place it outside the text editor

    def keypress(self, event=None):
        row, col = self.textw.index("insert").split(".")
        self.righttext.config(text=self._("Line %s : Col %s") % (str(row), str(col)))

    def writeleftmessage(self, message: str, nowrite: bool = None, event=None):
        self.lefttext.config(text=message)
        if nowrite is True:
            return
        now = datetime.datetime.now()
        date = now.strftime(Logger.format_date)
        time = now.strftime(Logger.format_time)
        self.logs.append("{} {} - {}".format(date, time, message))
        self.after(
            1500,
            self.writeleftmessage(self._("New message(s) collected."), nowrite=True),
        )

    def get_messages(self):
        import tkinter as tk

        mss = tk.Toplevel(self)
        alllogs = tk.Text(mss)

        for i in self.logs:
            alllogs.insert(1.0, i)

        mss.wm_title("Logs")
        alllogs.config(state="disabled")
        alllogs.pack()
        mss.mainloop()
