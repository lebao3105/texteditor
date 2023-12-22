import os
import pygubu
import texteditor
import webbrowser

from libtextworker.general import ResetEveryConfig, logger
from libtextworker.interface.tk.dirctrl import DirCtrl, DC_HIDEROOT

from tkinter.filedialog import askdirectory
from tkinter import Menu, PhotoImage, TclError, Tk, Toplevel
from tkinter import messagebox as msgbox
from typing import Literal, NoReturn

from .extensions.generic import CONFIGS_PATH
from .extensions.generic import clrcall, global_settings
from .extensions import autosave, finding
from .tabs import TabsViewer
from .views import about

try:
    from cairosvg import svg2png
except ImportError:
    CAIRO_AVAILABLE = False
else:
    CAIRO_AVAILABLE = True


logger.UseGUIToolKit("tk")


class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("810x610")

        # Set the application icon
        if os.path.isfile(texteditor.icon) and CAIRO_AVAILABLE:
            svg2png(open(texteditor.icon, "r").read(), write_to="./icon.png")
            try:
                self.wm_iconphoto(False, PhotoImage(file="./icon.png"))
            except TclError as e:
                logger.exception("Unable to set application icon: ", e)

        # Build the UI
        self.builder = pygubu.Builder(_)
        self.builder.add_from_file(texteditor.currdir / "views" / "menubar.ui")

        self.notebook = TabsViewer(self, do_place=True)
        self.autosv = autosave.AutoSaveConfig(self)

        self.GetColor()
        self.LoadMenu()
        self.BindEvents()

        # BooleanVar_s
        self.wrapbtn = self.builder.get_variable("wrapbtn")
        self.autosave_local = self.builder.get_variable("autosave_local")
        self.autosave_global = self.builder.get_variable("autosave_global")

        if (
            global_settings.getkey("editor.autosave", "enable")
            in global_settings.yes_values
        ):
            self.autosave_global.set(True)
            self.autosave_local.set(True)

    def LoadMenu(self):
        # Configure some required menu items callback
        self.callbacks = {
            "aboutdlg": lambda: about.About().ShowDialog(self),
            "add_tab": lambda: self.add_tab(),
            "autosv_local": lambda: self.autosv_config("local", "switch"),
            "autosv_global": lambda: self.autosv_config("global", "switch"),
            "autosv_localcfg": lambda: self.autosv_config("local"),
            "autosv_globalcfg": lambda: self.autosv_config("global"),
            "change_color": lambda: self.change_color(),
            "destroy": lambda: self.destroy(),
            "gofind": lambda: finding.Finder(self, "find"),
            "goreplace": lambda: finding.Finder(self, ""),
            "opencfg": lambda: self.opencfg(),
            "open_doc": lambda: webbrowser.open(
                "https://lebao3105.gitbook.io/texteditor_doc"
            ),
            "openfile": lambda: self.notebook.fileops.OpenFileDialog(),
            "openfolder": lambda: self.openfolder(),
            "savefile": lambda: self.notebook.fileops.SaveFileEvent(),
            "savefileas": lambda: self.notebook.fileops.SaveAs(),
            "resetcfg": lambda: self.resetcfg(),
            "toggle_wrap": lambda: self.toggle_wrap(),
        }

        menu = Menu(self)
        self.config(menu=menu)

        for menu_, name in [
            ("menu1", _("File")),
            ("menu2", _("Edit")),
            ("menu3", _("Config")),
            ("menu4", _("Help")),
        ]:
            setattr(self, menu_, self.builder.get_object(menu_, self))
            menu.add_cascade(menu=getattr(self, menu_), label=name)

        self.builder.connect_callbacks(self.callbacks)

    def BindEvents(self):
        bindcfg = self.bind
        bindcfg("<Control-n>", lambda event: self.add_tab(self))
        bindcfg("<Control-f>", lambda event: finding.Finder(self, "find"))
        bindcfg("<Control-r>", lambda event: finding.Finder(self, ""))
        bindcfg("<Control-Shift-S>", lambda event: self.notebook.fileops.SaveAs())
        bindcfg("<Control-s>", self.notebook.fileops.SaveFileEvent)
        bindcfg("<Control-o>", self.notebook.fileops.OpenFileDialog)
        bindcfg(
            "<Control-w>",
            lambda event: self.notebook.fileops.GetEditorFromCurrTab().wrapmode(),
        )

    # Menu bar callbacks
    def resetcfg(self, event=None) -> NoReturn:
        if msgbox.askyesno(
            _("Warning"),
            _("This will reset ALL configurations you have ever made. Continue?"),
        ):
            ResetEveryConfig()

    def opencfg(self, event=None):
        self.add_tab()
        self.notebook.fileops.LoadFile(CONFIGS_PATH)

    def GetColor(self):
        if clrcall.getkey("color", "background") == "dark":
            self.lb = "light"
        else:
            self.lb = "dark"
        clrcall.recursive_configure = True
        clrcall.autocolor_run(self)

    def change_color(self, event=None):
        if self.autocolor.get() is True:
            if not msgbox.askyesno(
                _("Warning"),
                _(
                    """\
                Changing the application color requires the autocolor function to be turned off.
                Don't worry, this change is only for this session.
                """
                ),
            ):
                return
        clrcall.set("color", "background", self.lb)
        clrcall.set("color", "autocolor", "no")
        self.GetColor()

    def add_tab(self, event=None):
        return self.notebook.add_tab(idx="default")

    def toggle_wrap(self, event=None):
        toggle = self.wrapbtn.get()
        self.notebook.fileops.GetEditorFromCurrTab().configure(wrap="word" if toggle else "none")

    def autosv_config(
        self, type: Literal["global", "local"], type2: Literal["switch"] | None = None
    ):
        if type == "global":
            if type2 == "switch":
                msgbox.showinfo(message=_("This is applied only for this session."))
                autosave.TOGGLE = self.autosave_global.get()
            else:
                self.autosv.ShowWind()
        else:
            if type2 == "switch":
                self.notebook.fileops.GetEditorFromCurrTab().Toggle(
                    self.autosave_local.get()
                )
            else:
                self.notebook.fileops.GetEditorFromCurrTab().ShowWind()

    def openfolder(self):
        new = Toplevel(self)
        path = askdirectory(
            initialdir=os.path.expanduser("~/"), mustexist=True,
            parent=self, title=_("Open a directory")
        )
        control = DirCtrl(new, w_styles=DC_HIDEROOT)
        control.SetFolder(path)
        control.Frame.pack(expand=True, fill="both")
        new.wm_title(path)
        new.mainloop()