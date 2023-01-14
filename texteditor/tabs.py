import wx
import wx.stc
from texteditor.backend import file_operations, get_config


class Tabber(wx.Notebook):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.NB_TOP
        wx.Notebook.__init__(self, *args, **kwds)

        self.setstatus: bool = False

        self.AddTab()
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClicked)

    def AddTab(self, evt=None, tabname=None):
        """Add a new tab.
        If tabname is not specified, use texteditor's new tab label."""

        self.text_editor = TextWidget(self, style=wx.TE_MULTILINE | wx.EXPAND)
        self.text_editor.fileops = file_operations.FileOperations(
            self.text_editor, self, self.AddTab, self.SetTitle, self.Parent
        )
        if tabname is None:
            _tabname = _("New file")
        else:
            _tabname = tabname
        
        self.AddPage(self.text_editor, _tabname, select=True)
        self.SetTitle(_("Texteditor - %s") % _tabname)

    def SetTitle(self, evt=None, title=None):
        return self.Parent.SetTitle(title)

    def OnPageChanged(self, evt=None):
        tabname = self.GetPageText(self.GetSelection())
        if self.setstatus is True:
            self.Parent.SetStatusText(tabname)
        self.SetTitle(_("Texteditor - %s") % tabname)

    def CloneTab(self, evt=None):
        tabname = self.GetPageText(self.GetSelection())
        content = self.text_editor.GetValue()
        self.AddTab(tabname=tabname)
        self.text_editor.AppendText(content)

    def CloseTab(self, evt=None):
        if self.GetPageCount() == 0:
            self.Parent.Destroy()
        else:
            self.RemovePage(self.GetSelection())

    def OnRightClicked(self, evt):
        menu = wx.Menu()
        for id, label, handler in [
            (wx.ID_ANY, _("New Tab\tCtrl-N"), lambda evt: self.AddTab()),
            (
                wx.ID_ANY,
                _("Close the current open tab"),
                lambda evt: self.CloseTab(),
            ),
            (wx.ID_ANY, _("Clone this tab"), lambda evt: self.CloneTab()),
        ]:
            item = menu.Append(id, label)
            menu.Bind(wx.EVT_MENU, handler, item)
        self.PopupMenu(menu)
        menu.Destroy()


class TextWidget(wx.stc.StyledTextCtrl):
    rcmenu: bool = True

    def __init__(self, id=wx.ID_ANY, line_number: bool = True, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.stc.STC_STYLE_DEFAULT
        super().__init__(id, **kwds)
        if self.rcmenu == True:
            self.Bind(wx.EVT_RIGHT_DOWN, self.OpenMenu)

        if line_number == True:
            self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
            self.SetMarginMask(1, 0)
            self.SetMarginWidth(1, 20)
        else:
            self.SetMarginWidth(1, 0)

        cfg = get_config.GetConfig(get_config.cfg, get_config.file)
        bg, fg = cfg._get_color()
        bg = "#" + "%02x%02x%02x" % bg
        fg = "#" + "%02x%02x%02x" % fg
        self.StyleSetSpec(0, "fore:{},back:{}".format(fg, bg))

        self.Bind(wx.stc.EVT_STC_MODIFIED, self.OnKeyPress)

    def OnKeyPress(self, evt):
        if evt:
            pos = evt.GetPosition()
            length = evt.GetLength()
        else:
            pos = 0
            length = self.GetLength()
        self.StartStyling(pos)
        self.SetStyling(length, 0)

    if rcmenu == True:

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

    else:

        def OpenMenu(self, event):
            raise NotImplementedError

        def RightClickMenu(self, event, pt, enable):
            raise NotImplementedError
