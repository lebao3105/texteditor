import os
import signal
import subprocess
import texteditor
import threading

from tkinter import END, BooleanVar, Toplevel, messagebox
from texteditor.backend import get_config, textwidget

arr = []


class cmd(textwidget.TextWidget):
    useUnRedo = True
    useWrap = True

    def __init__(self, master, _=None, **kw):
        super().__init__(master, _=_, **kw)
        self.parent = master
        self.bind("<Return>", self.checkcmds)

        self.readonlybtn = BooleanVar()
        self.readonlybtn.set(False)
        self.addMenucheckbtn(
            label=self._("Read only"), fn=self.readonlymode, variable=self.readonlybtn
        )
        self.configure(foreground="white", background="black", insertbackground="white")
        self.statusbar.righttext.configure(text="")
        self.statusbar.writeleftmessage(os.getcwd())

    def checkcmds(self, *args):
        command = self.get(1.0, END).split("\n")[-2]
        append = self.insert

        if command == "exit":
            try:
                for pids in arr:
                    os.kill(pids, signal.SIGTERM)
            except ProcessLookupError:
                pass
            print("Closed Console Window.")
            self.parent.destroy()  # Destroy the Toplevel widget

        elif command == "clear":
            self.delete(1.0, END)

        elif command == "help":
            append("end", "\n")
            append("end", self._("Available commands:\n"))
            append("end", self._("exit: Close this box\n"))
            append("end", self._("help: Show this message\n"))
            append("end", self._("clear: Clear this box\n"))
            append(
                "end",
                self._(
                    "term: Open terminal (not this one) - don't run this if you are running this application from console!\n"
                ),
            )
            append(
                "end",
                self._(
                    "Running CONSOLE application which requires user input is not recommended yet.\n"
                ),
            )
            append("end", self._("You won't get anything.\n"))

        elif command == "term":
            append("end", "\n")
            append(
                "end",
                self._(
                    "This will open console defined by defconsole value in configuration file. Please don't run any shell!"
                ),
            )
            cmd = get_config.GetConfig.getvalue("cmd", "defconsole")

            if cmd == ("bash" or "xonsh" or "zsh" or "fish" or "sh"):
                messagebox.showerror(
                    title="Error",
                    message="This application cannot run shell, use terminal emulator instead.\nProgram: "
                    + cmd,
                )
            elif cmd == ("cmd" or "powershell" or "pwsh"):
                threading.Thread(target=lambda: self.runcommand("start " + cmd)).start()
            else:
                threading.Thread(target=lambda: self.runcommand(cmd)).start()
        elif command.startswith("cd "):
            try:
                os.chdir(command.removeprefix("cd "))
            except OSError:
                append("end", self._("No such a directory like that"))
            else:
                self.statusbar.writeleftmessage(os.getcwd())
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
    def __init__(self, master, _=None, event=None):
        super().__init__(master)
        self.geometry("600x400")
        self.title("Commander")
        console = cmd(
            self,
            _=_,
            undo=False,
        )
        console.pack(expand=True, fill="both")
