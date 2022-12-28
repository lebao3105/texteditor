import datetime
import os
import sys
import texteditor
import traceback
from tkinter import ttk
from texteditor.backend import get_config, textwidget


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

    def throwerr(self, title, noexp:bool=None, msg=None):
        """Throws an exception message with its traceback and a custom message."""
        if noexp is True:
            traceback_msg = ""
        else:
            traceback_msg = traceback.format_exc()
        return self.printtext(
            title, msg if msg is not None else "", traceback_msg
        )

    def throwinf(self, title, msg=None):
        return self.printtext(title, msg if msg is not None else "")

    def throwwarn(self, title, msg=None):
        return self.printtext(title, msg if msg is not None else "")


class StatusBar(ttk.Frame):
    def __init__(self, parent, _=None, **kwargs):
        super().__init__(master=parent, **kwargs)

        if _ is None:
            self._ = texteditor._
        else:
            self._ = _

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

        get_config.GetConfig.configure(self)
        get_config.GetConfig.configure(self.lefttext)
        get_config.GetConfig.configure(self.righttext)

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
            3500,
            lambda: self.lefttext.config(text=self._("New message(s) collected.")),
        )

    def get_messages(self):
        curridx : int = 0
        isplaced : bool

        def refresh(replace:bool=None, event=None):
            nonlocal curridx
            nonlocal isplaced

            # This needs a fix
            if not self.logs:
                label = ttk.Label(mss, text=self._("No new message here."))
                label2 = ttk.Label(mss, text=self._("You always can refresh by just press F5."), cursor="hand2")
                label.config(font=(label["font"], 14))
                mss.bind("<F5>", lambda event: refresh(replace=True))

                get_config.GetConfig(label, "config")
                get_config.GetConfig(label2, "config")

                alllogs.forget()
                yscroll.forget()
                label.pack(pady="0 30")
                label2.pack(pady="0 30")
                isplaced = False
            
            if replace == True and isplaced == False:
                mss.bind("<F5>", lambda event: refresh())
                label.forget()
                label2.forget()
                yscroll.pack(side="right", fill="y")
                alllogs.pack(expand=True, fill='both')
                isplaced = True

            alllogs.config(state='normal')
            for i in range(curridx, len(self.logs)):
                alllogs.insert('end', self.logs[i]+"\n")
            curridx = len(self.logs)

            alllogs.config(state='disabled')

        def on_close():
            self.islogwindowopen = False
            mss.destroy()
            return # That's it

        import tkinter as tk
        
        if self.islogwindowopen is True:
            return

        mss = tk.Toplevel(self)
        alllogs = textwidget.TextWidget(mss, _=self._, useMenu=True, addWrap=True)
        yscroll = ttk.Scrollbar(mss, orient='vertical', command=alllogs.yview)

        mss.bind("<F5>", lambda event: refresh())
        alllogs.config(state="disabled")
        alllogs.RMenu.delete(2)
        alllogs.RMenu.add_command(
            label=self._("Refresh"),
            command=lambda: refresh(),
            accelerator="F5"
        )

        yscroll.pack(side="right", fill='y')
        alllogs.pack(expand=True, fill='both')
        refresh()

        mss.wm_title(self._("Logs"))
        mss.protocol("WM_DELETE_WINDOW", on_close)
        mss.mainloop()
        self.islogwindowopen = True