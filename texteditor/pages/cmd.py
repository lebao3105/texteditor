import os
import sys
from tkinter import *
import subprocess
from tkinter.messagebox import showinfo, showwarning
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from miscs import get_config

class CommandPrompt(Text):

    def __init__(self, master):
        super().__init__(master)
        self._ = master._
        self.bind('<Return>', self.runcommand(self))
        self.pack(expand=True, fill="both")
        self.warning()
        master.commandprompt = self

    """
    Run a command.
    All output will be redirected to the widget.
    TODO: auto detect arguments + allow to use xterm (maybe in v1.1?)
    """
    def runcommand(self):
        command = self.get(1.0, END).split('\n')[-2]
        append = self.insert
        append('end', '\n')
        
        # Do stuff
        if command == 'exit':
            self.destroy()
            
        elif command== 'clear':
            self.delete(1.0, END)
            
        elif command == 'help':
            append('end', self._("Available commands:\n"))
            append('end', self._("exit: Close this box\n"))
            append('end', self._("help: Show this message\n"))
            append('end', self._("clear: Clear this box\n"))
            append('end', self._("term: Open terminal (not this one) - don't run this if you are running this application from console!"))
            append('end', self._("Running application which requires user input is not recommended yet.\n"))
            
        elif command == 'term':
            append('end', self._("This will open console defined by defconsole value in configuration file. The application will be temporarity unusable!"))
            try:
                os.system(get_config.getvalue('cmd', 'defconsole'))
            except:
                raise Exception('Program not found?')
                
        else:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            out = p.stdout.read()
            append('end', '\n')
            try:
                append('end', out)
            except:
                raise Exception('Unable to print output.')

    def warning(self):
        showwarning(
            title='Warning',
            message="""This is a working feature - use some commands will make the application unusable. Run help to get more notes and available commands!"""
        )

