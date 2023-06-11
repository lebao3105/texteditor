import pathlib
import pygubu
import texteditor

from tkinter import Toplevel
from tkinter.ttk import *

from ..extensions.generic import clrcall
from libtextworker.general import CraftItems, GetCurrentDir, __file__ as libpath

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "about.ui"


class AboutDialog(Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.grab_release()
        self.wm_title(_("About this app"))
        self.geometry("300x400")
        # self.resizable(False, False)

        builder = pygubu.Builder(_)

        # Call both the project folder and
        # the current folder (which contains this file)
        builder.add_resource_path(PROJECT_PATH)
        builder.add_resource_path(texteditor.currdir)

        # Load the UI layout
        builder.add_from_file(PROJECT_UI)

        # Get objects
        self.appname = builder.get_object("appname", self)
        self.version = builder.get_object("version", self)
        self.mainfm = builder.get_object("mainfm", self)

        self.version.configure(text=_("Version {}".format(texteditor.__version__)))

        clrcall.configure(self.mainfm, True)

        builder.connect_callbacks(self)

    def run(self):
        self.mainloop()

    def quit(self, event=None):
        return self.destroy()

    # Page switching functions
    def build_new_page(self):
        for item in self.mainfm.winfo_children():
            item.forget()
        self.appname.forget()
        self.version.forget()
        self.mainfm.forget()

        newfm = Frame(self)
        labelfm = Label(newfm)
        bottomfm = Frame(self)
        leftbtn = Button(
            bottomfm, text=_("Go back"), command=lambda: self.goback(newfm, bottomfm)
        )
        rightbtn = Button(bottomfm, text=_("Close"), command=lambda: self.quit())

        labelfm.pack(expand=True, fill="both")
        newfm.pack(expand=True, fill="both")
        bottomfm.pack(fill="x")
        leftbtn.pack(side="left")
        rightbtn.pack(side="right")

        self.geometry("500x350")
        return labelfm, bottomfm

    def goback(self, *args):
        self.geometry("300x400")
        for widget in args:
            widget.forget()
            for children in widget.winfo_children():
                children.forget()
        self.appname.pack(pady="0 20", side="top")
        self.version.pack(pady="0 20", side="top")
        self.mainfm.pack(expand=True, fill="both")

        for child in self.mainfm.winfo_children():
            child.pack(expand=True, fill="x", side="top")

    def call_des(self, event=None):
        labelfm = self.build_new_page()[0]
        labelfm.config(
            text=_(
                """Texteditor is a small, flexible, and cross-platform text editor. It
        comes with a basic but customizable user interface, and a Command Window
        which allows you to execute some commands.
        """
            )
        )

    def call_license(self, event=None):
        labelfm = self.build_new_page()[0]
        labelfm.config(
            text=open(
                CraftItems(GetCurrentDir(libpath), "licenses", "GPL3_short.txt"), "r"
            ).read()
        )

    def call_devs(self, event=None):
        labelfm = self.build_new_page()[0]
        labelfm.config(
            text="""\
        Le Bao Nguyen for the app code, logo and Vietnamese translation."""
        )
