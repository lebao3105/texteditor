import pathlib
import pygubu
import texteditor
from tkinter import Toplevel
from tkinter.ttk import *
from texteditor.backend import get_config

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "about.ui"


class AboutDialog(Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.grab_release()
        self.wm_title(_("About this app"))
        self.geometry("516x356")
        # self.resizable(False, False)

        builder = pygubu.Builder(_)

        # Call both the project folder and
        # the current folder (which contains this file)
        builder.add_resource_path(PROJECT_PATH)
        # print(texteditor.currdir)
        builder.add_resource_path(texteditor.currdir)

        # Load the UI layout
        builder.add_from_file(PROJECT_UI)

        # Get objects
        self.appname = builder.get_object("appname", self)
        self.version = builder.get_object("version", self)
        self.mainfm = builder.get_object("mainfm", self)
        button1 = builder.get_object("button1", self)
        button2 = builder.get_object("button2", self)
        button3 = builder.get_object("button3", self)

        self.version.configure(text=_("Version {}".format(texteditor.version)))

        for item in [
            self.appname,
            self.version,
            self.mainfm,
            button1,
            button2,
            button3,
        ]:
            get_config.GetConfig(item, "config")

        builder.connect_callbacks(self)

    def run(self):
        self.mainloop()

    def quit(self, event=None):
        return self.destroy()

    # Page switching
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

        for item in [labelfm, leftbtn, rightbtn]:
            get_config.GetConfig(item, "config")

        labelfm.pack(expand=True, fill="both")
        newfm.pack(expand=True, fill="both")
        bottomfm.pack(fill="x")
        leftbtn.pack(side="left")
        rightbtn.pack(side="right")

        return labelfm, bottomfm

    def goback(self, *args):
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
                """\
        Texteditor is a small, flexible, and cross-platform text editor. It
        comes with a basic but customizable user interface, and a Command Window
        which allows you to execute some commands.
        """
            )
        )

    def call_license(self, event=None):
        labelfm = self.build_new_page()[0]
        labelfm.config(
            text="""\
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <https://www.gnu.org/licenses/>."""
        )

    def call_devs(self, event=None):
        labelfm = self.build_new_page()[0]
        labelfm.config(
            text="""\
        Le Bao Nguyen for the app code, logo and Vietnamese translation."""
        )
