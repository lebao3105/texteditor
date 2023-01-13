import texteditor
import tkinter.messagebox as msb
from tkinter import BooleanVar, Label, StringVar, Toplevel
from tkinter.ttk import Button, Checkbutton, Combobox

from ..backend import get_config, logger

# Minutes to seconds
MIN_05 = 30  # 30 secs
MIN_1 = MIN_05 * 2  # 60 secs
MIN_15 = MIN_1 * 15  # 900 secs
MIN_20 = MIN_15 + MIN_1 * 5  # 1200 secs
MIN_30 = MIN_15 * 2  # 1800 secs

log = logger.Logger("texteditor.extensions.autosave")

texteditor.backend.require_version("1.6a", "<")

class AutoSave:
    """Contructs the autosaving files function on texteditor.\n
    Configurations:
    * forceEnable : bool : Force enable this
    * useTime : float : Force auto save after a time

    Functions:
    * openpopup : Make a popup window which asks the user to change the auto save time.
    It will modify useTime!
    * start : Start the timing loop
    """

    forceEnable: bool = False
    useTime: float = float(get_config.GetConfig.getvalue("filemgr", "autosave-time"))

    def __init__(self, master, savefile_fn):
        self.autosave = get_config.GetConfig.getvalue("filemgr", "autosave")
        self.__check()
        self.parent = master
        self.savecommand = savefile_fn

    def __check(self):
        if self.forceEnable == False:
            if self.autosave == "yes":
                self.__converter(self.useTime)
                pass
            else:
                return "break"

    def openpopup(self):
        askwin = Toplevel(self.parent)
        self.askwin = askwin
        # askwin.geometry("400x230")
        askwin.title(_("Autosave configuration"))
        askwin.resizable(False, False)

        selected_time = StringVar()
        updatest = BooleanVar()

        label = Label(
            askwin,
            text=_(
                "Select autosave time (minutes)\nAutosave function will be launched after a time."
            ),
        )
        label2 = Label(
            askwin,
            text=_("Please note that Autosave only saves the current selected tab."),
        )
        cb = Combobox(askwin, textvariable=selected_time)
        cb["values"] = [0.5, 1, 2, 5, 10, 15, 20, 30]
        cb["state"] = "readonly"
        if self.useTime in cb["values"]:
            cb.current(self.__converter(self.useTime))

        checkbtn = Checkbutton(
            askwin,
            text=_("Save this value"),
            variable=updatest,
            onvalue=True,
            offvalue=False,
        )
        okbtn = Button(
            askwin,
            text="OK",
            command=lambda: self.__okbtn_clicked(selected_time, updatest),
        )
        cancelbtn = Button(askwin, text=_("Cancel"), command=lambda: askwin.destroy())

        label.pack(fill="x")
        cb.pack(fill="x", padx=15, pady=15)
        checkbtn.pack(fill="x")
        okbtn.pack(padx=30)
        cancelbtn.pack(padx=40)
        label2.pack(fill="x")

        get_config.GetConfig(askwin, "config")
        get_config.GetConfig(label, "config")
        get_config.GetConfig(label2, "config")
        get_config.GetConfig(cb, "config")

    def __converter(self, time: float):
        switch = {
            0.5: MIN_05,
            1: MIN_1,
            2: MIN_1 * 2,
            5: MIN_1 * 5,
            10: MIN_1 * 10,
            15: MIN_15,
            20: MIN_20,
            30: MIN_30,
        }
        return switch.get(time)

    def __okbtn_clicked(self, selected_time, up_st, event=None):
        tm = selected_time.get()
        st = up_st.get()
        timetouse = self.__converter(float(tm))

        # This depends on the __converter function.
        # No problem if you don't rewrite it.
        if not isinstance(timetouse, int):
            log.throwerr(_("Wrong autosave time specified."), noexp=True)
            return
        else:
            self.config(timetouse)

        if st is True:
            get_config.GetConfig.change_config(
                "filemgr", "autosave-time", str(self.useTime)
            )
        self.askwin.destroy()
        self.start()

    def config(self, useTime, event=None):
        print("Trying to use autosave time: ", useTime)
        self.useTime = float(useTime)
        self.__check()

    def start(self):
        result = msb.askquestion(message="Do you want to start autosave loop now?")
        if result != "yes":
            return
        else:
            try:
                self.parent.after(
                    int(self.useTime * 1000),  # Tk().after() uses miliseconds
                    lambda: self.savecommand(),
                )
            except:
                return
