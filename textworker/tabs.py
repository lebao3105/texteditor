import textworker
import wx
import wx.stc
from textworker.backend import file_operations, get_config
from .extensions import autosave


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
        self.autosv = autosave.AutoSave()
        self.autosv.parent = self.Parent
        self.autosv.savefn = lambda: self.text_editor.fileops.savefile_()

        if tabname is None:
            _tabname = _("New file")
        else:
            _tabname = tabname

        self.AddPage(self.text_editor, _tabname, select=True)

        textw = self.text_editor
        textworker.cfg.setcolorfunc(
            "textw", textw, "StyleSetBackground", wx.stc.STC_STYLE_DEFAULT
        )
        textworker.cfg.setfontcfunc(
            "textw", textw, "StyleSetForeground", wx.stc.STC_STYLE_DEFAULT
        )
        textworker.cfg.configure(textw)

        self.SetTitle("Textworker - %s" % _tabname)

    def SetTitle(self, title=""):
        return self.Parent.SetTitle(title)

    def OnPageChanged(self, evt=None):
        tabname = self.GetPageText(self.GetSelection())
        if self.setstatus is True:
            self.Parent.SetStatusText(tabname)
        self.SetTitle("Textworker - %s" % tabname)

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
                _("Close the current (open) tab"),
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

    def __init__(self, id, line_number: bool = True, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.stc.STC_STYLE_DEFAULT
        super().__init__(id, **kwds)
        if self.rcmenu == True:
            self.Bind(wx.EVT_RIGHT_DOWN, self.OpenMenu)

        if line_number == True:
            self.EnableLineCount(True)
        else:
            self.EnableLineCount(False)

        cfg = get_config.GetConfig(get_config.cfg, get_config.file)
        bg, fg = cfg._get_color()
        bg = "#" + "%02x%02x%02x" % bg
        fg = "#" + "%02x%02x%02x" % fg
        self.StyleSetSpec(0, "fore:{},back:{}".format(fg, bg))
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, "fore:{},back:{}".format(fg, bg))

        self.Bind(wx.stc.EVT_STC_MODIFIED, self.OnKeyPress)

    def EnableLineCount(self, set:bool):
        if set == True:
            self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
            self.SetMarginMask(1, 0)
            self.SetMarginWidth(1, 20)
        else:
            self.SetMarginWidth(1, 0)

    def OnKeyPress(self, evt):
        if evt:
            pos = evt.GetPosition()
            length = evt.GetLength()
        else:
            pos = 0
            length = self.GetLength()
        self.StartStyling(pos)
        self.SetStyling(length, 0)
        evt.Skip()

    if rcmenu == True:

        def OpenMenu(self, event):
            pt = event.GetPosition()
            self.RightClickMenu(pt)

        def RightClickMenu(self, pt):
            menu = wx.Menu()
            cut = menu.Append(wx.ID_CUT)
            copy = menu.Append(wx.ID_COPY)
            paste = menu.Append(wx.ID_PASTE)
            menu.AppendSeparator()

            undo = menu.Append(wx.ID_UNDO)
            redo = menu.Append(wx.ID_REDO)
            delete = menu.Append(wx.ID_DELETE)
            selectall = menu.Append(wx.ID_SELECTALL)

            commands = {
                cut: lambda evt: self.Cut(),
                copy: lambda evt: self.Copy(),
                paste: lambda evt: self.Paste(),
                undo: lambda evt: self.Undo(),
                redo: lambda evt: self.Redo(),
                delete: lambda evt: self.DeleteBack(),
                selectall: lambda evt: self.SelectAll(),
            }

            cut.Enable(self.CanCut())
            copy.Enable(self.CanCopy())
            paste.Enable(self.CanPaste())
            undo.Enable(self.CanUndo())
            redo.Enable(self.CanRedo())

            for item in [delete, selectall]:
                if self.GetValue() != "":
                    item.Enable(True)
                else:
                    item.Enable(False)

            for item in commands:
                self.Bind(wx.EVT_MENU, commands[item], item)

            self.PopupMenu(menu, pt)
            menu.Destroy()

    else:

        def OpenMenu(self, event):
            raise NotImplementedError

        def RightClickMenu(self, pt):
            raise NotImplementedError
