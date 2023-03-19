import getpass
import os
import subprocess
import threading
import wx
import wx.stc

from ..tabs import Tabber

from libtextworker.interface.wx.editor import StyledTextControl

class CommandWidget(StyledTextControl):
    """
    A terminal widget for wxPython.
    But it doesn't embed any shell to it like wx.py.shell, this is just a text widget with a prompt
    that the user can enter command in it and get the result.
    """

    def __init__(self, id=wx.ID_ANY, **kw):
        super().__init__(id, **kw)
        self.shell = Shell(self)
        self.shell.showprompt(True)

        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPress2)

    def RightClickMenu(self, pt):
        menu = wx.Menu()
        copy = menu.Append(wx.ID_COPY)
        paste = menu.Append(wx.ID_PASTE)
        readonly = menu.AppendCheckItem(wx.ID_ANY, _("Read only"))

        copy.Enable(self.CanCopy())
        paste.Enable(self.CanPaste())

        menu.Check(readonly.GetId(), False)

        self.Bind(wx.EVT_MENU, self.Copy, copy)
        self.Bind(wx.EVT_MENU, self.Paste, paste)
        self.Bind(wx.EVT_MENU, self.SetEditable(not self.IsEditable()), readonly)

        self.PopupMenu(menu, pt)
        menu.Destroy()

    def OnKeyPress2(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            if self.GetCurrentLine() == self.GetLineCount() - 1:
                line = self.GetLine(self.GetLineCount() - 1)
                self.shell.getcommand(line)
        elif evt.GetKeyCode() == wx.WXK_UP or wx.WXK_DOWN:
            if self.GetCurrentLine() != self.GetLineCount() - 1:
                evt.Skip()
        # elif evt.GetKeyCode() == wx.WXK_LEFT:
        #     if self.GetCurrentLine() == self.GetLineCount():
        #         currpos = self.PositionToXY(self.GetInsertionPoint())
        #         if currpos != (self.GetCurrentLine() +- 1, len(self.shell.prompt)):
        #             evt.Skip()
        evt.Skip()


class Tabb(Tabber):

    def AddTab(self, evt=None, tabname: str = ""):
        """
        Create a new Terminal tab.
        Will use "Terminal" for the tab label if tabname is not specified.
        """
        textw = CommandWidget(parent=self, style=wx.TE_MULTILINE)
        textw.shell.statusobj = self.Parent
        textw.shell.root = self.Parent
        self.Parent.SetStatusText(os.getcwd())

        if tabname == "":
            newtabname = "Terminal"
        else:
            newtabname = tabname

        timer = wx.Timer(self)
        timer.Start()
        self.Bind(
            wx.EVT_TIMER,
            lambda evt: self.SetPageText(self.GetSelection(), os.getcwd()),
            timer,
        )

        self.AddPage(textw, newtabname, select=True)
        self.text_editor = textw

    def OnPageChanged(self, evt=None):
        tabname = self.GetPageText(self.GetSelection())
        if self.setstatus is True:
            self.Parent.SetStatusText(tabname)
        self.SetTitle(tabname)


class Shell:
    """
    This is 'shell' for wxPython, used to run commands then get their outputs and errors (if have) and show them to a text widget.
    How to use (for developers):
    * Set statusobj (optional, should be set from the first class call, on __init__) to any object that can use SetStatusText function to use its status bar.
      The status bar must have 2 entries+.
    * Set parent to a wxPython text widget (StyledTextCtrl, TextCtrl) (on __init__)
    * Set prompt (optional) to any string you want. That's the prompt for the shell (e.g {username} {dir}$ in bash) - should not use os.getcwd()
      or anything else about directories except you override the finalize_run function.
    * Set intro (optional) to any thing you want.
    * Set root (must have for the exit command) to a top-level window (wx.Frame).
    * Override the runterm variable to a terminal emulator (optional, if you don't use this far away textworker)
    Please note that this 'shell' can not send any input from the user, or in the code, to any program. This can't run other shells like bash, or cmd.
    Keep warning everyone about this.

    Available commands:
    * alias [--system] item1=item2... : Set aliases - use --system flag to run the system's command
    * cd [directory] : Change the current directory
    * clear (or cls) : Clear the window
    * help : Show this box
    * runterm : Start a terminal emulator, defined in textworker's configuration file

    You can use [command] && [command] (...) to run multiple commands (but not at the same time).

    Please don't do anything to the shell prompt ('your username' + 'Shell>')!
    After you run a command, scroll down and place the mouse cursor to the next of the last prompt.
    """

    prompt = "(User: {}) Shell> ".format(getpass.getuser())
    intro = "Enter a command to start." "\nThis cant send input to any program.\n"
    aliases: dict = {}
    exitcode: int = 0
    statusobj = None
    root = None  # Frame, Panel...
    runterm = "xterm"

    def __init__(self, parent, statusobj=None):
        self.parent = parent
        if statusobj != None:
            self.statusobj = statusobj
        if self.statusobj != None:
            self.statusobj.SetStatusText(os.getcwd())

    def showprompt(self, intro: bool = False, godown: bool = True):
        if intro == True:
            self.parent.AddText(self.intro)
        if godown == True:
            self.parent.AddText("\n")
        self.parent.AddText(self.prompt)

    def getcommand(self, input: str):
        cmd = input.removeprefix(self.prompt)

        if "&&" in cmd:
            for i in range(len(cmd.split("&&"))):
                self.getcommand(cmd.split("&&")[i])

        if cmd.startswith("cd "):
            try:
                os.chdir(cmd.removeprefix("cd "))
            except OSError:
                self.parent.AppendText(
                    "\nDirectory not found/not a directory or invalid syntax: %s"
                    % cmd.removeprefix("cd ")
                )
                self.exitcode = 1
            else:
                if hasattr(self, "statusobj") and self.statusobj != None:
                    self.statusobj.SetStatusText(os.getcwd())
                self.exitcode = 0

        elif cmd.startswith("clear"):
            self.parent.ClearAll()
            self.showprompt(godown=False)

        elif cmd.startswith("cls"):
            self.parent.ClearAll()
            self.showprompt(godown=False)

        elif cmd.startswith("exit"):
            if self.root != None:
                self.root.Close()
            else:
                title = _("Missing root variable for CommandWindow")
                msg = _("Please close the command window by any other way.")
                logger.Logger().throwerr(title=title, msg=msg, showdialog=True)

        elif cmd.startswith("alias "):
            args = cmd.removeprefix("alias ").split()
            self.aliases[args[1]] = args[2]
            self.showprompt()

        elif cmd.startswith("alias --system "):  # Use the system alias command
            threading.Thread(
                target=lambda: self.runcommand(
                    "alias {}".format(cmd.removeprefix("alias --system "))
                ),
                daemon=True,
            ).start()

        elif cmd.startswith("runterm"):
            threading.Thread(
                target=lambda: self.runcommand(self.runterm), daemon=True
            ).start()

        elif cmd.startswith("help"):
            self.parent.AddText(self.__doc__)
            self.exitcode = 0
            self.showprompt()

        # Issue: https://github.com/lebao3105/texteditor/issues/3
        # Solution from the main branch...
        else:
            threading.Thread(target=lambda: self.runcommand(cmd), daemon=True).start()

    def runcommand(self, input: str):
        if input in self.aliases:
            input = self.aliases[input]

        result = subprocess.Popen(
            input,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True,
        )
        self.parent.AddText("\n")

        for item in result.communicate():
            # https://stackoverflow.com/questions/606191/
            self.parent.AddText(item.decode("utf-8"))

        result.wait()
        self.exitcode = result.returncode
        self.finalize_run()

    def finalize_run(self):
        if hasattr(self, "statusobj") and self.statusobj != None:
            self.statusobj.SetStatusText(
                _("Command exited with code {}".format(self.exitcode)), 1
            )

        self.showprompt()
