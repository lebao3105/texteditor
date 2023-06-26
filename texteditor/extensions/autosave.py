from tkinter import Toplevel, messagebox as msb, Misc
from .generic import global_settings, clrcall
from libtextworker.general import logger, CraftItems, GetCurrentDir
from pygubu.builder import Builder
from threading import Thread

# Minutes to seconds
MIN_05 = 30  # 30 secs
MIN_1 = MIN_05 * 2  # 60 secs
MIN_15 = MIN_1 * 15  # 900 secs
MIN_20 = MIN_15 + MIN_1 * 5  # 1200 secs
MIN_30 = MIN_15 * 2  # 1800 secs

enabled = global_settings.getkey("editor.autosave", "enable", False, True)
time = global_settings.getkey("editor.autosave", "time", False, True)

if not enabled in global_settings.yes_values:
    enabled = False

if not int(time):
    time = 30

TOGGLE: bool = bool(enabled)

class AutoSave:
    Editor: Misc
    CurrDelay: int = time

    def Start(self, time_: int = time):
        self.CurrDelay = time_
        if not enabled:
            return
        self.TaskId = self.Editor.after(int(time_) * 1000, lambda: self.SaveFunc())
    
    def Stop(self):
        self.Editor.after_cancel(self.TaskId)
        self.__delattr__("TaskId")

    def CheckToggle(self):
        if not TOGGLE and hasattr(self, "TaskId") == True:
            self.Stop()
        elif not hasattr(self, "TaskId"):
            self.Start()

    def Toggle(self, on: bool):
        if on:
            self.Start()
        else:
            self.Stop()

    def __init__(self):
        Thread(target=self.CheckToggle, daemon=True).start()

class AutoSaveConfig(Toplevel):
    """
    Autosave window.
    """
    timealiases = {
        "30 seconds": 30,
        "1 minute": 60,
        "2 minutes": 120,
        "5 minutes": 300,
        "10 minutes": 600,
        "15 minutes": 900,
        "20 minutes": 1200,
        "30 minutes": 1800
    }

    def __init__(self, parent: Misc):
        super().__init__(master=parent)
        self.grab_release()
        self.resizable(False, False)

        self.builder = Builder(_)
        self.builder.add_from_file(CraftItems(GetCurrentDir(__file__), "../views", "autosave.ui"))

        self.dialog = self.builder.get_object("dialog1", self)
        self.combobox = self.builder.get_object("combobox1", self.dialog)
        self.checkbtn = self.builder.get_object("checkbutton1", self.dialog)
        self.combobox["values"] = [item for item in self.timealiases]
        self.combobox["state"] = "readonly"

        clrcall.configure(self.dialog, True)
        self.builder.connect_callbacks(self)
    
    def do_the_task(self):
        choice = self.builder.get_variable("selected_time").get()
        do_save = self.builder.get_variable("save").get()
        if choice:
            global_settings.set(
                "editor.autosave",
                self.timealiases[choice]
            )
            if do_save:
                global_settings.update()
    
    def ShowWind(self):
        self.dialog.mainloop()
