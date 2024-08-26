import wx
from .. import _
from ..generic import global_settings, clrCall


class MultiViewer:
    def __init__(this, parent):
        location = global_settings.Get(
            "extensions.textwkr.multiview", "notebook_location", needed=True
        )
        nbside = getattr(wx, f"NB_{location.upper()}")

        this.tabs = wx.Notebook(parent, -1, style=nbside)
        this.tabs.Bind(wx.EVT_RIGHT_DOWN, this._RightClickTab)
        clrCall.configure(this.tabs)

    def RegisterTab(this, tabname: str, content) -> bool:
        """
        Ask for add a new section to the side bar.
        @param tabname:str: Name of the section (used for the new tab name)
        @param content: Section content (must be a wxPython object). Don't forget to Show() it!
        @return The result of the new section creation
        """
        clrCall.configure(content)
        return this.tabs.AddPage(content, tabname, True)

    def UnregisterTab(this, content) -> bool:
        return this.tabs.DeletePage(content)

    def _RightClickTab(this, evt):
        menu = wx.Menu()
        for label, handler in [
            (
                _("Close the current tab"),
                lambda evt: this.UnregisterTab(this.tabs.GetCurrentPage()),
            ),
            (
                _("Disable this (open) tab"),
                lambda evt: this.tabs.GetCurrentPage().Disable(),
            ),
            (
                _("Close the side bar"),
                lambda evt: this.tabs.Close()
            )
        ]:
            item = menu.Append(wx.ID_ANY, label)
            menu.Bind(wx.EVT_MENU, handler, item)
        this.tabs.PopupMenu(menu, evt.GetPosition())
        menu.Destroy()
