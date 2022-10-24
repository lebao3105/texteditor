import pathlib
import pygubu
import texteditor
from tkinter import *
from texteditor.miscs import get_config

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "about.ui"


class AboutDialog(Toplevel):
    def __init__(self, master, translator=None):
        super().__init__(master=master)
        builder = pygubu.Builder(translator)

        # Call both the project folder and
        # the current folder (which contains this file)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_resource_path(texteditor.currdir)
        # Load the UI layout
        builder.add_from_file(PROJECT_UI)

        label1 = builder.get_object("label1", self)
        label2 = builder.get_object("label2", self)
        label3 = builder.get_object("label3", self)
        btn_ok = builder.get_object("btn_ok", self)

        get_config.GetConfig(label1, "config")
        get_config.GetConfig(label2, "config")
        get_config.GetConfig(label3, "config")
        get_config.GetConfig(btn_ok, "config")

        label1.configure(font=(label1["font"], 17))
        builder.connect_callbacks(self)

    def run(self):
        self.mainloop()

    def quit(self, event=None):
        self.destroy()
