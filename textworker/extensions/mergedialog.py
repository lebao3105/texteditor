import wx
from ..generic import clrcall, moves, global_settings

class MergeDialog(wx.Dialog):
    """
    Settings merge dialog.
    """

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.SetTitle(_("This needs your attention"))

        mainBoxer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainBoxer)

        header = wx.StaticText(self, label=_("Merges ahead"))
        text = wx.StaticText(self,
                             label=_(
                                "The settings system has been changed recently and you need to merge them."
                                "Look for the changes below."
                                "All changes are required."
                                )
                            )
        listctrl = wx.ListCtrl(self, style=wx.LC_AUTOARRANGE | wx.LC_REPORT)
        listctrl.InsertColumn(0, _("Setting (section->option)"))
        listctrl.InsertColumn(1, _("New setting (section->option)"))
        listctrl.InsertColumn(2, _("Moved to file..."))
        start = wx.Button(self, label=_("Start"))
        self.Bind(wx.EVT_BUTTON, lambda evt: global_settings.move(moves), start)

        for oldpath in moves:
            listctrl.InsertItem(0, oldpath)
            listctrl.SetItem(0, 1, moves[oldpath]["newpath"])
            if "file" in moves[oldpath]:
                listctrl.SetItem(0, 2, moves[oldpath]["file"])
            else:
                listctrl.SetItem(0, 2, "Unchanged")

        mainBoxer.Add(header, 0, wx.ALL, 5)
        mainBoxer.Add(text, 0, wx.ALL, 5)
        mainBoxer.Add(listctrl, 0, wx.ALL, 5)
        mainBoxer.Add(start, 0, wx.ALL|wx.RIGHT, 5)

        clrcall.configure(self, True)
        header.SetFont(wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))