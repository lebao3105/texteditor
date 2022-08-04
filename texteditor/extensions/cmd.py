import os, sys, subprocess
from signal import SIGTERM
from tkinter import *
from threading import Thread
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from miscs import get_config

class cmd(Text):

    def __init__(self, master):
        super().__init__(master)
        self._ = master._
        #self.configure(fg='white', bg='black')
        self.bind('<Return>', self.checkcmds)
        self.pack(expand=True, fill="both")
        self.warning()
        self.parent = master

    def checkcmds(self, *args):
        command = self.get(1.0, END).split('\n')[-2]
        append = self.insert

        if command == 'exit':
            try:
                os.killpg(self.result.pid, SIGTERM)
            except ProcessLookupError:
                pass
            print('Closed Console Window.')
            self.master.destroy() # Destroy the Toplevel widget

        elif command == 'clear':
            self.delete(1.0, END)
            self.mark_set("insert", "%d.%d" % (1.0, 1.0))

        elif command == 'help':
            append('end', "\n")
            append('end', self._("Available commands:\n"))
            append('end', self._("exit: Close this box\n"))
            append('end', self._("help: Show this message\n"))
            append('end', self._("clear: Clear this box\n"))
            append('end', self._("term: Open terminal (not this one) - don't run this if you are running this application from console!\n"))
            append('end', self._("Running CONSOLE application which requires user input is not recommended yet.\n"))
            append('end', self._("You won't get anything.\n"))

        elif command == 'term':
            append('end', '\n')
            append('end', self._("This will open console defined by defconsole value in configuration file. The application will be temporarity unusable!"))
            os.system(get_config.getvalue('cmd', 'defconsole'))

        else:
            rec_thread = Thread(target = lambda: self.runcommand(command))
            rec_thread.start()

    def runcommand(self, cmd : str):
        self.result = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = self.result.communicate()
        self.insert('end', output)
        self.insert('end', error)
        self.result.wait()

class CommandPrompt(Toplevel):

    def __init__(self, master, event=None):
        super().__init__(master)
        self._ = master._
        self.title("Command Window")
        cmd(self)