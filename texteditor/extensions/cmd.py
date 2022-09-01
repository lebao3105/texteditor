import os, sys, subprocess, threading
from signal import SIGTERM
import gettext

from tkinter import BooleanVar, END, messagebox, Toplevel

from texteditor.miscs import get_config, textwidget

_ = gettext.gettext
arr = []


class cmd(textwidget.TextWidget):
    useUnRedo = True
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

    def checkcmds(self, *args):
        command = self.get(1.0, END).split("\n")[-2]
        append = self.insert

        if command == "exit":
            try:
                # TODO: Manage processes
                if sys.platform == "win32":
                    self.result.kill()
                else:
                    for pids in arr:
                        os.killpg(pids, SIGTERM)
            except ProcessLookupError:
                pass
            print("Closed Console Window.")
            self.parent.destroy()  # Destroy the Toplevel widget

        elif command == "clear":
            self.delete(1.0, END)

        elif command == "help":
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

        elif command == "term":
            append("end", "\n")
            append(
                "end",
                _(
                    "This will open console defined by defconsole value in configuration file. Please don't run any shell!"
                ),
            )
            cmd = get_config.getvalue("cmd", "defconsole")

            if cmd == ("bash" or "xonsh" or "zsh" or "sh"):
                messagebox.showerror(
                    title="Error",
                    message="This application cannot run shell, use terminal emulator instead.\nProgram: "
                    + cmd,
                )
            elif cmd == ("cmd" or "powershell"):
                threading.Thread(target=lambda: self.runcommand("start " + cmd)).start()
            else:
                threading.Thread(target=lambda: self.runcommand(cmd)).start()

        else:
            rec_thread = threading.Thread(target=lambda: self.runcommand(command))
            rec_thread.start()

    def runcommand(self, cmd: str):
        self.result = subprocess.Popen(
            cmd,
            shell=True,  # preexec_fn=os.setsid,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, error = self.result.communicate()
        arr.append(self.result.pid)
        self.insert("end", output)
        self.insert("end", error)
        self.result.wait()

    def readonlymode(self, event=None):
        if self.readonlybtn.get() == True:
            self.configure(state="disabled")
        else:
            self.configure(state="normal")


class CommandPrompt(Toplevel):
    def __init__(self, master, event=None):
        super().__init__(master)
        self.geometry("600x400")
        self.title(_("Command Window"))
        console = cmd(
            self,
            foreground="white",
            background="black",
            insertbackground="white",
            undo=False,
        )
        console.pack(expand=True, fill="both")
