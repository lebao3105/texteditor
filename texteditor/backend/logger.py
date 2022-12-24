import datetime
import os
import sys
import traceback


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
