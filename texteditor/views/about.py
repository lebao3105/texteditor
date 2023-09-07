import platform
import sys
from tkinter import Misc, TclVersion, TkVersion, Toplevel
from tkinter.ttk import Button, Frame, Label, Notebook

from libtextworker.general import CraftItems
from libtextworker.interface.tk.about import AboutDialog
from libtextworker.interface.tk.editor import StyledTextControl

from libtextworker import LICENSES
from libtextworker import __version__ as libver
from texteditor import __version__ as appver
from texteditor.extensions.generic import clrcall


class About(AboutDialog):
    ProjectName = "textworker"
    ProjectVersion = appver
    ProjectSite = (
        "https://github.com/lebao3105/texteditor "
        "and https://gitlab.com/lebao3105/texteditor (mirror)"
    )

    ProjectDescription = _(
        "A text editor in Python, with customizable and easy-to-use user interface."
        "Read documents online: https://lebao3105.gitbook.io/texteditor_doc"
    )

    ProjectLicense = (
        "(C) Le Bao Nguyen 2022-2023\n"
        "By using this application, you agree to texteditor license below:\n\n"
        f'{open(CraftItems(LICENSES, "GPL3_full.txt"), "r").read()}'
    )

    ProjectBuilds: str = (
        f"Libtextworker {libver}\n"
        f"Tk {TkVersion}\n"
        f"Tcl {TclVersion}\n"
        f"Operating system: {platform.system()} version {platform.version()}\n"
        f"Python {sys.version}"
    )

    Developers = "Le Bao Nguyen (@lebao3105)"
    Translators = Testers = Developers  # Looks sad btw

    def ShowDialog(self, master: Misc | None = None):
        dlg = Toplevel(master)
        dlg.wm_title(_("About this project"))
        dlg.geometry("350x485")

        project_infos = _(
            "About this project\n"
            f"{self.ProjectName} version {self.ProjectVersion}\n"
            f"Description: {self.ProjectDescription}\n"
            f"Project website: {self.ProjectSite}"
        )

        project_credits = _(
            "This software is made possible by:\n" f"Developers:\n\t{self.Developers}"
        )

        if self.ArtMakers:
            project_credits += _(f"\nArtists:\n\t{self.ArtMakers}")

        if self.Testers:
            project_credits += _(f"\nTesters:\n\t{self.Testers}")

        if self.Translators:
            project_credits += _(f"\nTranslators:\n\t{self.Translators}")

        nb = Notebook(dlg)
        nb.pack(fill="both", expand=True)

        # Make tabs
        credits_te = StyledTextControl(dlg, state="disabled", wrap="word")
        license_te = StyledTextControl(dlg, state="disabled", wrap="word")
        license_te.insert(1.0, self.ProjectLicense)
        credits_te.insert(1.0, project_credits)
        license_te.pack(expand=True, fill="both")
        credits_te.pack(expand=True, fill="both")

        nb.add(Label(dlg, text=project_infos), text=_("This software"))
        nb.add(credits_te._frame, text=_("Contributors"))
        nb.add(license_te._frame, text=_("License"))
        nb.add(Label(dlg, text=self.ProjectBuilds), text=_("System specifications"))

        # The bottom bar
        bottomfm = Frame(dlg)
        quitbtn = Button(bottomfm, text="OK", default="active")
        quitbtn.bind("<Button-1>", lambda evt: (dlg.destroy()))
        quitbtn.pack(side="right")
        bottomfm.pack(fill="x", side="bottom")

        clrcall.configure(dlg, True)
        # clrcall.autocolor_run(dlg)

        dlg.mainloop()
