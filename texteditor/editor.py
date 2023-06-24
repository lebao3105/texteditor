from .extensions.autosave import AutoSave, AutoSaveConfig
from libtextworker.interface.tk.editor import TextWidget

class Editor(TextWidget, AutoSave, AutoSaveConfig):
    FileLoaded: str
    
    def SaveFile(self, path: str):
        return open(path, "w").write(self.get(1.0, "end"))
    
    def ShowWind(self):
        self.checkbtn.forget()
        return super().ShowWind()