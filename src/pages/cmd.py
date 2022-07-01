import subprocess
from tkinter import *
from sys import platform
from tkinter.messagebox import showinfo

class CommandPrompt(Text):

    def __init__(self, master):
        super().__init__(master)
        self._ = master._
        self.bind('<Return>', self.runcommand)
        self.pack(expand=True, fill="both")
        master.commandprompt = self

    """
    Run a command.
    All output will be redirected to the widget.
    TODO: auto detect arguments + allow to use xterm (maybe in v1.1?)
    """
    def runcommand(self, *args):
        command = self.get(1.0, END).split('\n')[-2]
        append = self.insert

        if command == 'exit':
            self.destroy()
        elif command== 'clear':
            self.delete(1.0, END)
            self.mark_set("insert", "-1.-1")
        elif command == 'help':
            append('end', self._("Available commands:\n"))
            append('end', self._("exit: Close this box\n"))
            append('end', self._("help: Show this message\n"))
            append('end', self._("clear: Clear this box\n"))
            append('end', self._("Running pre installed shells (Bash, Cmd, Zsh...) is blocked. But you can use xterm instead.\n"))
        else:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            out = p.communicate()
            append('end', '\n')
            append('end', out)



