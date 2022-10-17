import pathlib
import pygubu
from tkinter import *
from texteditor.miscs import get_config

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "about.ui"


class AboutDialog:
    def __init__(self, master=None, translator=None):
        self.builder = builder = pygubu.Builder(translator)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)

        self.mainwindow = builder.get_object("aboutdlg", master)
        label1 = builder.get_object("label1", master)
        label2 = builder.get_object("label2", master)
        label3 = builder.get_object("label3", master)
        btn_ok = builder.get_object("btn_ok", master)

        get_config.GetConfig(label1, "config")
        get_config.GetConfig(label2, "config")
        get_config.GetConfig(label3, "config")
        get_config.GetConfig(btn_ok, "config")

        builder.connect_callbacks(master)

    def run(self):
        self.mainwindow.mainloop()

    def quit(self, event=None):
        self.mainwindow.destroy()
