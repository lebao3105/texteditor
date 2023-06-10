import logging
import os
import shutil
import subprocess
import wx
import wx.xrc

from libtextworker.general import CraftItems

logger = logging.getLogger("textworker")


class GitSupport:
    IsGitRepo: bool = False
    HasSubModules: bool = False  # TODO

    GitPath = shutil.which("git")

    Remote = []
    Branch = {}  # {current, list}
    Changes: dict[str, str] = {}  # {path, type}

    def InitGit(self):
        if not self.GitPath:
            logger.exception("textworker.extensions.gitsp[INIT]: Git not found")
            return False
        else:
            gitver = str(subprocess.check_output([self.GitPath, "version"]))
            logger.debug("Using " + gitver + " from " + os.path.dirname(self.GitPath))
            return True

    def InitFolder(self, path: str):
        if not os.path.isdir(path):
            raise Exception(
                "textworker.extensions.gitsp[INIT]: Folder not found: " + path
            )

        if not os.path.isdir(CraftItems(path, ".git")):
            logger.debug(
                "textworker.extensions.gitsp: Not a git repo (or any of the parent directories) - .git not found anywhere"
            )
            return None

        status = str(
            subprocess.check_output([self.GitPath, "status", "-z"], encoding="utf-8")
        )

        self.IsGitRepo = True

        # Repo status

        ## 'git status -z' output format:

        ## M <modified files> ?? <untracked> D <deleted files> T <file type changed> A <added>
        ## R <renamed files> C <copied - if status.renames git config is set to "copies">
        ## U <updated but unmerged>

        ## Thanks to GitHub for suggestting me the '-s' parameter:)
        ## Mostly taken from: https://git-scm.com/docs/git-status

        ## P/s: The code below looks good:v
        status = status.replace("M ", "<M>")
        status = status.replace("D ", "<D>")
        status = status.replace("?? ", "<N>")
        status = status.replace("T ", "<T>")
        status = status.replace("A ", "<A>")
        status = status.replace("R ", "<R>")
        status = status.replace("C ", "<C>")
        status = status.replace("U ", "<U>")

        self.Refresh()  # Clean

        for item in status.split():
            for string in ["A", "C", "D", "M", "N", "R", "T"]:
                if item.startswith(f"<{string}>"):
                    self.Changes[item.removeprefix(f"<{string}>")] = string

        # Repo branch & remote
        self.Branch["current"] = str(
            subprocess.check_output([self.GitPath, "branch"])
        ).removeprefix("* ")
        self.Branch["list"] = str(
            subprocess.check_output([self.GitPath, "branch", "-r"])
        )

        self.Remote = str(subprocess.check_output([self.GitPath, "remote"]))

    def Refresh(self):
        self.Branch = {}
        self.Modified = self.New = self.Remote = []


class GitSupportGUI(GitSupport):
    currdir: str = ""

    def __init__(self, Parent):
        self.Panel = wx.Panel(Parent)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.Blank = wx.StaticText(self.Panel, label="No git repository found.")
        self.Blank.Wrap(-1)

        self.Blank.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD,
                False,
                "Arial",
            )
        )

        bSizer1.Add(self.Blank, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.NewRepoBtn = wx.Button(self.Panel, label="Create a new git repository")

        self.NewRepoBtn.SetDefault()
        bSizer1.Add(self.NewRepoBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.RepoPath = wx.StaticText(self.Panel, label="Git repo path:")
        self.RepoPath.Wrap(-1)

        self.RepoPath.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "Arial",
            )
        )

        bSizer1.Add(self.RepoPath, 0, wx.ALL, 5)

        self.Header1 = wx.StaticText(self.Panel, label="Existing file changes")
        self.Header1.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "Arial",
            )
        )
        self.Header1.Wrap(-1)

        bSizer1.Add(self.Header1, 0, wx.ALL, 5)

        self.EditedList = wx.ListCtrl(
            self.Panel, style=wx.LC_AUTOARRANGE | wx.LC_REPORT
        )
        self.EditedList.InsertColumn(0, "File")
        self.EditedList.InsertColumn(1, "Type", width=200)
        bSizer1.Add(self.EditedList, 0, wx.ALL, 5)

        self.Panel.SetSizer(bSizer1)
        self.Panel.Layout()

        for string in ["RepoPath", "Header1", "EditedList"]:
            getattr(self, string).Hide()

        if not self.InitGit():
            self.Blank.SetLabel(_("Git not found - install it to use this plugin."))
            self.NewRepoBtn.Hide()

        self.NewRepoBtn.Bind(wx.EVT_BUTTON, self.NewRepo)

        bSizer1.Layout()
        self.Panel.Layout()
        self.Panel.Centre()

    def NewRepo(self, evt=None) -> int | None:
        target = self.currdir
        if not os.path.isdir(self.currdir):
            target = wx.DirSelector(_("Open a folder to start"))
        if not target:
            return None
        self.currdir = target
        status = subprocess.call([self.GitPath, "init"], cwd=self.currdir)
        self.InitFolder(self.currdir)
        return status

    def InitFolder(self, path: str):
        self.currdir = path
        super().InitFolder(path)

        for string in ["RepoPath", "Header1", "EditedList"]:
            getattr(self, string).Show()

        self.RepoPath.SetLabel("Git repo path: " + os.path.realpath(self.currdir))

        # print(self.Changes)
        for file in self.Changes:
            self.EditedList.InsertItem(0, file)
            self.EditedList.SetItem(0, 1, self.Changes[file])
            self.EditedList.SetItem(
                list(self.Changes).index(file), 1, self.Changes[file]
            )

        self.Blank.Hide()
        self.NewRepoBtn.Hide()

        self.Panel.Refresh()
