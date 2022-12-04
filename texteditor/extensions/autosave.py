import gettext
import tkinter.messagebox as msb
from tkinter import BooleanVar, Label, StringVar, Toplevel
from tkinter.ttk import Button, Checkbutton, Combobox

from ..backend import file_operations, get_config

# Minutes to seconds
MIN_05 = 30  # 30 secs
MIN_1 = MIN_05 * 2  # 60 secs
MIN_15 = MIN_1 * 15  # 900 secs
MIN_20 = MIN_15 + MIN_1 * 5  # 1200 secs
MIN_30 = MIN_15 * 2  # 1800 secs


class AutoSave:
    """Contructs the autosaving files function on texteditor.\n
    Only save the current opening tab.\n
    Configurations:\n
    forceEnable : bool : Force enable this\n
    useTime : float : Force auto save after a time\n
    Function:\n
    openpopup : Make a popup window which asks the user to change the auto save time.
    It will modify useTime!\n
    start : Start the timing loop
    """

    forceEnable: bool = False
    useTime: float = float(get_config.GetConfig.getvalue("filemgr", "autosave-time"))

    def __init__(self, master, _=None):
        super().__init__()
        if _ is None:
            self._ = gettext.gettext
        else:
            self._ = _
        self.autosave = get_config.GetConfig.getvalue("filemgr", "autosave")
        self.savetime = get_config.GetConfig.getvalue("filemgr", "autosave-time")
        self._do_check()
        self.parent = master

    def _do_check(self):
        if self.forceEnable == False:
            if self.autosave == "yes":
                pass
            else:
                print("Error: Autosave is disabled on user configuration file")

        if (self.useTime or float(self.savetime)) > MIN_30:  # 30 minutes
            print("Error: Auto save time is higher than 30 minutes")

        if (self.useTime or float(self.savetime)) < MIN_05:  # 30 secs
            print("Error: Auto save time is smaller than 30 seconds!")

    def openpopup(self):
        # Note: I want to use auto save to all tabs (aka files open in texteditor)
        # but now I only can do this to opening tab only.
        askwin = Toplevel(self.parent)
        self.askwin = askwin
        askwin.geometry("400x230")
        askwin.title("Autosave configuration")
        askwin.resizable(False, False)

        selected_time = StringVar()
        updatest = BooleanVar()

        label = Label(
            askwin,
            text="Select autosave time (minutes)\nAutosave function will be launched after a time.",
        )
        label2 = Label(
            askwin,
            text="Please note that this feature only affect the current opening tab.",
        )
        cb = Combobox(askwin, textvariable=selected_time)
        cb["values"] = [0.5, 1, 2, 5, 10, 15, 20, 30]
        cb["state"] = "readonly"

        checkbtn = Checkbutton(
            askwin,
            text="Save this value",
            variable=updatest,
            onvalue=True,
            offvalue=False,
        )
        okbtn = Button(
            askwin,
            text="OK",
            command=lambda: self.okbtn_clicked(selected_time, updatest),
        )
        cancelbtn = Button(askwin, text="Cancel", command=lambda: askwin.destroy())

        label.pack(fill="x")
        cb.pack(fill="x", padx=15, pady=15)
        checkbtn.pack(fill="x")
        okbtn.pack(padx=30)
        cancelbtn.pack(padx=40)
        label2.pack(fill="x")

        # The new get_config isn't available for TopLevel now
        get_config.GetConfig.configure(askwin)

        get_config.GetConfig(label, "config")
        get_config.GetConfig(label2, "config")
        get_config.GetConfig(cb, "config")

    def okbtn_clicked(self, selected_time, up_st, event=None):
        tm = selected_time.get()
        st = up_st.get()
        if tm == 0.5:
            self.config(MIN_05)
        elif tm == 1:
            self.config(MIN_1)
        elif tm == 2:
            self.config(MIN_1 * 2)
        elif tm == 5:
            self.config(MIN_1 * 5)
        elif tm == 10:
            self.config(MIN_1 * 10)
        elif tm == 15:
            self.config(MIN_15)
        elif tm == 20:
            self.config(MIN_20)
        elif tm == 30:
            self.config(MIN_30)
        else:
            return
        if st is True:
            get_config.GetConfig.change_config(
                "filemgr", "autosave-time", str(self.useTime)
            )
        self.askwin.destroy()
        self.start()

    def config(self, useTime, event=None):
        print("Trying to use autosave time: ", useTime)
        self.useTime = float(useTime)
        self._do_check()

    def start(self):
        result = msb.askquestion(message="Do you want to start autosave loop now?")
        if result != "yes":
            return
        else:
            try:
                self.parent.after(
                    int(self.useTime * 1000),  # Tk().after() uses miliseconds
                    lambda: file_operations.save_file(self.parent),
                )
            except:
                return
