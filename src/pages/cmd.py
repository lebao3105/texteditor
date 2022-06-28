import subprocess
from tkinter import *
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from miscs import init

class CommandPrompt(Text):

    def __init__(self, master):
        super().__init__(master)
        self._ = master._
        self.bind('<Return>', self.runcommand)
        self.pack(expand=True, fill="both")
        master.commandprompt = self
    
    """
    Run a command.
    We might can change some variables (e.g default shell...)
    """
    def runcommand(self, *args):
        command = self.get(1.0, END).split('\n')[-2]
        append = self.insert
        if command == 'exit':
            self.destroy()
        elif command== 'clear':
            self.delete(1.0, END)
            self.mark_set("insert", "0.0")
        elif command == 'help':
            append('end', self._("Available commands:"))
            append('end', self._("exit: Close this box"))
            append('end', self._("help: Show this message"))
            append('end', self._("clear: Clear this box"))
            append('end', self._("Running pre installed shells (Bash, Cmd, Zsh...) is blocked."))
            append('end', self._("You can change defshell variable to force this window run commands under that."))
        else:
            append('end', f'\n{subprocess.getoutput(command)}')
            


        

