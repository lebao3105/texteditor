import pathlib
import pygubu
import texteditor
from tkinter import *
from texteditor.miscs import get_config

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "about.ui"


class AboutDialog:
    def __init__(self, master=None, translator=None):
        builder = pygubu.Builder(translator)

        # Call both the project folder and
        # the current folder (which contains this file)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_resource_path(texteditor.currdir)
        # Load the UI layout
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

        label1.configure(font=(label1["font"], 17))
        builder.connect_callbacks(master)

    def run(self):
        self.mainwindow.mainloop()

    def quit(self, event=None):
        self.mainwindow.destroy()
