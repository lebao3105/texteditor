from libtextworker.interface.tk.editor import TextWidget

from .extensions.autosave import AutoSave, AutoSaveConfig


class Editor(TextWidget, AutoSave):
    FileLoaded: str

    def __init__(self, *args, **kwds):
        TextWidget.__init__(self, *args, **kwds)
        self.autosv = AutoSaveConfig(self)
        self.autosv.do_the_task = self.do_the_task

    def SaveFile(self, path: str):
        return open(path, "w").write(self.get(1.0, "end"))

    def LoadFile(self, path: str):
        return self.insert(1.0, open(path, "r").read())

    # AutoSaveConfig
    def do_the_task(self):
        choice = self.autosv.builder.get_variable("selected_time").get()
        self.Start(self.autosv.timealiases[choice])

    def ShowWind(self):
        self.autosv.checkbtn.forget()
        return self.autosv.ShowWind()
