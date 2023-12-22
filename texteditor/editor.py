from hashlib import md5
from libtextworker.interface.tk.editor import TextWidget
from .extensions.autosave import AutoSave, AutoSaveConfig


class Editor(TextWidget, AutoSave):

    def __init__(self, *args, **kwds):
        TextWidget.__init__(self, *args, **kwds)
        self.autosv = AutoSaveConfig(self)
        self.autosv.do_the_task = self.do_the_task

    # AutoSaveConfig
    def do_the_task(self):
        choice = self.autosv.builder.get_variable("selected_time").get()
        self.Start(self.autosv.timealiases[choice])

    def ShowWind(self):
        self.autosv.checkbtn.forget()
        return self.autosv.ShowWind()
