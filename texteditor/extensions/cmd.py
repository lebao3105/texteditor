import os
import sys
from tkinter import *
import subprocess
from tkinter.messagebox import showwarning
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from miscs import get_config

class cmd(Text):

    def __init__(self, master):
        super().__init__(master)
        self._ = master._
        self.configure(fg='white', bg='black')
        self.bind('<Return>', self.runcommand)
        self.pack(expand=True, fill="both")
        self.warning()
        master.commandprompt = self

    """
    Run a command.
    Outputs will be redirected to the widget.
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
            append('end', "\n")
            append('end', self._("Available commands:\n"))
            append('end', self._("exit: Close this box\n"))
            append('end', self._("help: Show this message\n"))
            append('end', self._("clear: Clear this box\n"))
            append('end', self._("term: Open terminal (not this one) - don't run this if you are running this application from console!\n"))
            append('end', self._("Running application which requires user input is not recommended yet.\n"))
        elif command == 'term':
            append('end', self._("This will open console defined by defconsole value in configuration file. The application will be temporarity unusable!"))
            os.system(get_config.getvalue('cmd', 'defconsole'))
        else:
            command_splited = command.split(' ')
            result = subprocess.run(command_splited, shell=True,
                        stderr=subprocess.STDOUT, stdout=subprocess.PIPE, env=os.environ)
            output = result.stdout
            append('end', '\n')
            append('end', output)

    def warning(self):
        showwarning(
            title=self._('Warning'),
            message=self._("""This is a working feature - use some commands will make the application unusable. Run help to get more notes and available commands!""")
        )

class CommandPrompt(Toplevel):

    def __init__(self, master, event=None):
        super().__init__(master)
        self._ = master._
        self.title("Command Prompt - Tkinter")
        cmd(self)