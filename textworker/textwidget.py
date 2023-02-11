import wx.stc
from .generic import global_settings


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

        bg, fg = global_settings.cfg._get_color()
        bg = "#" + "%02x%02x%02x" % bg
        fg = "#" + "%02x%02x%02x" % fg
        self.StyleSetSpec(0, "fore:{},back:{}".format(fg, bg))
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, "fore:{},back:{}".format(fg, bg))

        self.Bind(wx.stc.EVT_STC_MODIFIED, self.OnKeyPress)

    def EnableLineCount(self, set: bool):
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
            menu.AppendSeparator()
            readonly = menu.Append(wx.ID_ANY, _("Read only"))

            commands = {
                cut: lambda evt: self.Cut(),
                copy: lambda evt: self.Copy(),
                paste: lambda evt: self.Paste(),
                undo: lambda evt: self.Undo(),
                redo: lambda evt: self.Redo(),
                delete: lambda evt: self.DeleteBack(),
                selectall: lambda evt: self.SelectAll(),
                readonly: lambda evt: self.SetEditable(not self.IsEditable()),
            }

            cut.Enable(self.CanCut())
            copy.Enable(self.CanCopy())
            paste.Enable(self.CanPaste())
            undo.Enable(self.CanUndo())
            redo.Enable(self.CanRedo())
            readonly.Enable(True)

            menu.Check(readonly, False)

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
