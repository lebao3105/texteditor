import wx
from .. import _
from ..generic import clrCall, moves


class MergeDialog(wx.Dialog):
    """
    Settings merge dialog.
    """

    def __init__(this, *args, **kwds):
        wx.Dialog.__init__(this, *args, **kwds)
        this.SetTitle(_("This needs your attention"))

        mainBoxer = wx.BoxSizer(wx.VERTICAL)
        this.SetSizer(mainBoxer)

        header = wx.StaticText(this, label=_("Merges ahead"))
        text = wx.StaticText(
            this,
            label=_(
                "The settings system has been changed recently and automatically merged into your settings."
                "Look for the changes below."
                "All changes are required. You just need to review what are they:)"
            ),
        )
        listctrl = wx.ListCtrl(this, style=wx.LC_AUTOARRANGE | wx.LC_REPORT)
        listctrl.InsertColumn(0, _("Setting (section->option)"))
        listctrl.InsertColumn(1, _("New setting (section->option)"))
        listctrl.InsertColumn(2, _("Moved to file..."))

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

        clrCall.configure(this, true)
        header.SetFont(
            wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        )
