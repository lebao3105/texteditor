import wx
from texteditor.backend import file_operations


class Tabber(wx.Notebook):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.NB_TOP
        wx.Notebook.__init__(self, *args, **kwds)

        self.AddTab()
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

    def AddTab(self, evt=None, tabname=None):
        """Add a new tab. If tabname is not specified, use texteditor's new tab label."""
        self.text_editor = TextWidget(self, -1, value="", style=wx.TE_MULTILINE)
        self.text_editor.fileops = file_operations.FileOperations(
            self.text_editor, self, self.AddTab, self.Parent
        )
        if tabname is None:
            _tabname = _("New file")
        else:
            _tabname = tabname
        self.AddPage(self.text_editor, _tabname)
        self.SetSelection(self.text_editor)
        self.OnPageChanged()
        return

    def OnPageChanged(self, evt=None):
        tabname = self.GetPageText(self.GetSelection())
        self.Parent.SetStatusText(tabname)
        self.Parent.SetTitle(_("Texteditor - %s") % tabname)


class TextWidget(wx.TextCtrl):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OpenMenu)

    def OpenMenu(self, event):
        pt = event.GetPosition()
        self.RightClickMenu(event, pt, True)

    def RightClickMenu(self, event, pt, enable):
        menu = wx.Menu()
        cut = menu.Append(wx.ID_CUT, _("Cut\tCtrl-X"))
        copy = menu.Append(wx.ID_COPY, _("Copy\tCtrl-C"))
        paste = menu.Append(wx.ID_PASTE, _("Paste\tCtrl-V"))
        menu.AppendSeparator()
        undo = menu.Append(wx.ID_UNDO, _("Undo\tCtrl-Z"))
        delete = menu.Append(wx.ID_REDO, _("Redo\tCtrl-Y"))
        selectall = menu.Append(wx.ID_SELECTALL, _("Select All\tCtrl-A"))

        undo.Enable(False)
        cut.Enable(False)
        copy.Enable(False)

        if enable:
            paste.Enable(True)
        else:
            paste.Enable(False)
        delete.Enable(False)
        selectall.Enable(False)

        self.PopupMenu(menu, pt)
        menu.Destroy()
