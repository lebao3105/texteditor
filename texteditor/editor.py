from .extensions.autosave import AutoSave, AutoSaveConfig
from libtextworker.interface.tk.editor import TextWidget

class Editor(TextWidget, AutoSave, AutoSaveConfig):
    FileLoaded: str
    
    def SaveFile(self, path: str):
        return open(path, "w").write(self.get(1.0, "end"))
    
    def LoadFile(self, path: str):
        return self.insert(1.0, open(path, "r").read())
    
    # AutoSaveConfig
    def do_the_task(self):
        choice = self.builder.get_variable("selected_time").get()
        self.Start(self.timealiases[choice])

    def ShowWind(self):
        self.checkbtn.forget()
        return super().ShowWind()