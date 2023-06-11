import os
import subprocess
import threading

from tkinter import END, BooleanVar, TclError, Toplevel, messagebox
from .generic import global_settings

from libtextworker.interface.tk.editor import TextWidget


class cmd(TextWidget):
    useWrap = True

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.parent = master
        self.bind("<Return>", self.checkcmds)

        self.readonlybtn = BooleanVar()
        self.readonlybtn.set(False)
        self.addMenucheckbtn(
            label=_("Read only"), fn=self.readonlymode, variable=self.readonlybtn
        )
        self.configure(foreground="white", background="black", insertbackground="white")
        self.statusbar.righttext.configure(text="")
        self.statusbar.writeleftmessage(os.getcwd(), nowrite=True)

    def checkcmds(self, *args):
        command = self.get(1.0, END).split("\n")[-2]
        append = self.insert

        if command.startswith("exit"):
            # print("Closed Console Window.")
            self.parent.destroy()  # Destroy the Toplevel widget

        elif command.startswith("clear"):
            self.delete(1.0, END)

        elif command.startswith("help"):
            append("end", "\n")
            append("end", _("Available commands:\n"))
            append("end", _("exit: Close this box\n"))
            append("end", _("help: Show this message\n"))
            append("end", _("clear: Clear this box\n"))
            append(
                "end",
                _(
                    "term: Open terminal (not this one) - don't run this if you are running this application from console!\n"
                ),
            )
            append(
                "end",
                _(
                    "Running CONSOLE application which requires user input is not recommended yet.\n"
                ),
            )
            append("end", _("You won't get anything.\n"))

        elif command.startswith("term"):
            append("end", "\n")
            append(
                "end",
                _(
                    "This will open console defined by defconsole value in configuration file. Please don't run any shell!"
                ),
            )
            cmd = global_settings.call("cmd", "defconsole")

            threading.Thread(target=lambda: self.runcommand(cmd, noout=True)).start()

        elif command.startswith("cd "):
            try:
                os.chdir(command.removeprefix("cd "))
            except OSError:
                append("end", _("No such a directory like that"))
            else:
                self.statusbar.writeleftmessage(os.getcwd())
        else:
            rec_thread = threading.Thread(target=lambda: self.runcommand(command))
            rec_thread.start()

    def runcommand(self, cmd: str, noout: bool = None):
        self.result = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, error = self.result.communicate()
        try:
            self.insert("end", output)
            self.insert("end", error)
        except TclError:
            if not noout:
                messagebox.showerror(
                    _("Error"),
                    _(
                        "Cannot return the command result to the terminal : TCLError occured!"
                    ),
                )
            return
        self.result.wait()

    def readonlymode(self, event=None):
        if self.readonlybtn.get() == True:
            self.configure(state="disabled")
        else:
            self.configure(state="normal")


def showcmd(parent, evt=None):
    toplv = Toplevel(parent)
    toplv.geometry("600x400")
    toplv.title(_("Command Prompt"))
    cmd(toplv, undo=False).pack(expand=True, fill="both")
