import wx
import wx.stc

from .generic import global_settings
from libtextworker.interface.wx import editor

class TextWidget(editor.StyledTextControl):
    rcmenu: bool = True

    def __init__(self, line_number: bool = True, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.stc.STC_STYLE_DEFAULT
        super().__init__(line_number, **kwds)
        dt = DNDTarget(self)
        self.SetDropTarget(dt)

        if self.rcmenu == True:
            self.Bind(wx.EVT_RIGHT_DOWN, self.OpenMenu)

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
            # menu.AppendSeparator()
            # readonly = wx.MenuItem(menu, wx.ID_ANY, _("Read only"), kind=wx.ITEM_CHECK)
            # menu.Append(readonly)

            commands = {
                cut: lambda evt: self.Cut(),
                copy: lambda evt: self.Copy(),
                paste: lambda evt: self.Paste(),
                undo: lambda evt: self.Undo(),
                redo: lambda evt: self.Redo(),
                delete: lambda evt: self.DeleteBack(),
                selectall: lambda evt: self.SelectAll(),
                # readonly: lambda evt: self.SetEditable(not self.IsEditable()),
            }

            cut.Enable(self.CanCut())
            copy.Enable(self.CanCopy())
            paste.Enable(self.CanPaste())
            undo.Enable(self.CanUndo())
            redo.Enable(self.CanRedo())
            # readonly.Enable(True)

            # readonly.Check(False)

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

class DNDTarget(wx.FileDropTarget, wx.TextDropTarget):
    
    def __init__(self, textctrl):
        super().__init__()
        self.Target = textctrl
    
    def OnDropText(self, x, y, data):
        self.Target.WriteText(data)
        return True
    
    def OnDragOver(self, x, y, defResult):
        return wx.DragCopy
    
    def OnDropFiles(self, x, y, filenames):
        if len(filenames) > 0:
            self.Target.LoadFile(filenames)
        return True