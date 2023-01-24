import os
import subprocess
import wx

from ..tabs import *
from ..backend import get_config, logger

cfg = get_config.GetConfig(get_config.cfg, get_config.file, default_section="interface")


class CommandWidget(TextWidget):
    """
    A terminal widget for wxPython.
    But it doesn't embed any shell to it like wx.py.shell, this is just a text widget with a prompt
    that the user can enter command on it and get the result.
    """

    def __init__(self, id, **kwds):
        super().__init__(id, line_number=False, **kwds)
        self.shell = Shell(self)
        self.shell.showprompt(True)

        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPress2)

    def RightClickMenu(self, pt):
        menu = wx.Menu()
        copy = menu.Append(wx.ID_COPY)
        paste = menu.Append(wx.ID_PASTE)

        copy.Enable(self.CanCopy())
        paste.Enable(self.CanPaste())

        self.Bind(wx.EVT_MENU, self.Copy, copy)
        self.Bind(wx.EVT_MENU, self.Paste, paste)

    def OnKeyPress2(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            if self.GetCurrentLine() == self.GetLineCount() - 1:
                line = self.GetLine(self.GetLineCount() - 1)
                self.shell.getcommand(line)
        elif evt.GetKeyCode() == wx.WXK_LEFT:
            if self.GetCurrentLine() == self.GetLineCount() - 1:
                currpos = self.PositionToXY(self.GetInsertionPoint())
                if currpos != (len(self.shell.prompt), self.GetCurrentLine()):
                    evt.Skip()
        else:
            evt.Skip()


class Tabb(Tabber):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    def AddTab(self, evt=None, tabname: str = ""):
        """
        Create a new Terminal tab.
        Will use "Terminal" for the tab label if tabname is not specified.
        """
        textw = CommandWidget(self)
        textw.shell.statusobj = self.Parent
        textw.shell.root = self.Parent
        self.Parent.SetStatusText(os.getcwd())

        cfg.setcolorfunc("textw", textw, "StyleSetBackground", wx.stc.STC_STYLE_DEFAULT)
        cfg.setfontcfunc("textw", textw, "StyleSetForeground", wx.stc.STC_STYLE_DEFAULT)
        cfg.configure(textw)

        if tabname == "":
            newtabname = "Terminal"
        else:
            newtabname = tabname

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
    * help : Show this box
    * runterm : Start a terminal emulator, defined in textworker's configuration file

    You can use [command] && [command] (...) to run multiple commands (but not at the same time).

    Please don't do anything to the shell prompt ('your username' + 'Shell>')!
    After you run a command, scroll down and place the mouse cursor to the next of the last prompt.
    """

    prompt = "{} Shell> ".format(os.getlogin())
    intro = "Enter a command to start." "\nThis cant send input to any program.\n"
    aliases: dict = {}
    exitcode: int = 0
    statusobj = None
    root = None  # Frame, Panel...
    runterm = get_config.defconsole

    def __init__(self, parent, statusobj=None):
        self.parent = parent
        if statusobj != None:
            self.statusobj = statusobj
        if self.statusobj != None:
            self.statusobj.SetStatusText(os.getcwd())

    def showprompt(self, intro=False):
        if intro == True:
            self.parent.AppendText(self.intro)
        self.parent.AppendText("\n")
        self.parent.AppendText(self.prompt)

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

        elif cmd.startswith("exit"):
            if self.root != None:
                self.root.Close()
            else:
                title = "Missing root variable for CommandWindow"
                msg = "Please close the command window by any other way."
                logger.Logger().throwerr(title=title, msg=msg, showdialog=True)

        elif cmd.startswith("alias "):
            args = cmd.removeprefix("alias ").split(" ")
            self.aliases[args[1]] = args[2]
            self.exitcode = 0

        elif cmd.startswith("alias --system "):  # Use the system alias command
            self.runcommand("alias {}".format(cmd.removeprefix("alias --system ")))

        elif cmd.startswith("runterm"):
            self.runcommand(self.runterm)

        elif cmd.startswith("help"):
            self.parent.AppendText(self.__doc__)
            self.exitcode = 0

        else:
            self.runcommand(cmd)

        self.finalize_run()

    def runcommand(self, input: str):
        if input in self.aliases:
            input = self.aliases[input]
        result = subprocess.Popen(
            input, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True
        )
        out, err = result.communicate()
        self.parent.AppendText("\n")
        self.parent.AppendText(out)
        self.parent.AppendText(err)
        self.exitcode = result.returncode
        # self.SelectNone() # This will break SetInsertionPoint

    def finalize_run(self):
        if hasattr(self, "statusobj") and self.statusobj != None:
            self.statusobj.SetStatusText(
                "Command exited with code {}".format(self.exitcode), 1
            )

        self.showprompt()
        self.parent.SetInsertionPoint(
            self.parent.XYToPosition(len(self.prompt), self.parent.GetLineCount())
        )
