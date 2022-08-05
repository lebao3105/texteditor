import os, sys, subprocess
from signal import SIGTERM
from threading import Thread
from tkinter import *
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from miscs import get_config

class cmd(ScrolledText):

    def __init__(self, master):
        super().__init__(master)
        self._ = master._
        self.parent = master
        self.configure(fg='white', bg='black', insertbackground='white', undo=False)
        self.bind('<Return>', self.checkcmds)
        self.bind('<Button-3><ButtonRelease-3>', lambda event: self.rightclickmenu(event))
        self.pack(expand=True, fill="both")

    def checkcmds(self, *args):
        command = self.get(1.0, END).split('\n')[-2]
        append = self.insert

        if command == 'exit':
            try:
                # os.killpg doesn't work on Windows (python in my PC returns no attribute error)
                # Try to use os.kill instead..
                if sys.platform == "win32":
                    self.result.kill()
                else:
                    os.killpg(self.result.pid, SIGTERM)
            except ProcessLookupError:
                pass
            print('Closed Console Window.')
            self.parent.destroy() # Destroy the Toplevel widget

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
            cmd = get_config.getvalue('cmd', 'defconsole')
            if cmd == ("bash" or "xonsh" or "zsh"):
                showerror(title="Error", message="This application cannot run shell, use terminal emulator instead.\nProgram: "+cmd)
            elif cmd == ("cmd" or "powershell"):
                Thread(target = lambda: self.runcommand("start "+cmd)).start()

        else:
            rec_thread = Thread(target = lambda: self.runcommand(command))
            rec_thread.start()

    def runcommand(self, cmd : str):
        self.result = subprocess.Popen(cmd, shell=True,# preexec_fn=os.setsid,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = self.result.communicate()
        self.insert('end', output)
        self.insert('end', error)
        self.result.wait()

    def rightclickmenu(self, event=None):
        self.readonlybtn = BooleanVar()
        self.readonlybtn.set(False)
        try:
            menu = Menu(self, tearoff=0)
            menu.add_command(label=self._("Copy"), accelerator="Ctrl+C", command=lambda: self.event_generate("<Control-c>"))
            menu.add_command(label=self._("Paste"), accelerator="Ctrl+V", command=lambda: self.event_generate("<Control-v>"))
            menu.add_command(label=self._("Cut"), accelerator="Ctrl+X", command=lambda: self.event_generate("<Control-x>"))
            menu.add_checkbutton(label=self._("Read only"), command=self.readonlymode, variable=self.readonlybtn)
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_current()
        
    def readonlymode(self, event=None):
        if self.readonlybtn.get() == True:
            self.configure(state='disabled')
            self.readonlybtn.set(False)
        else:
            self.configure(state='normal')
            self.readonlybtn.set(True)

class CommandPrompt(Toplevel):

    def __init__(self, master, event=None):
        super().__init__(master)
        self._ = master._
        self.title("Command Window")
        cmd(self)