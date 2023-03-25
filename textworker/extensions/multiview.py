import wx

from ..generic import global_settings


class MultiViewer(wx.Frame):
    def __init__(self, *args, **kw):
        kw["style"] = kw.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(*args, **kw)

        location = global_settings.cfg.getkey(
            "extensions.multiview", "notebook_location", needed=True
        )
        if location == "bottom":
            nbside = wx.NB_BOTTOM
        elif location == "left":
            nbside = wx.NB_LEFT
        elif location == "right":
            nbside = wx.NB_RIGHT
        elif location == "default" or "top":
            nbside = wx.NB_DEFAULT | wx.NB_TOP

        self.tabs = wx.Notebook(self, -1, style=nbside)
        self.tabs.Bind(wx.EVT_RIGHT_DOWN, self._RightClickTab)

    def RegisterTab(self, tabname: str, content) -> bool:
        """
        Ask for add a new section to the side bar.
        @param tabname:str: Name of the section (used for the new tab name)
        @param content: Section content (must be a wxPython object). Don't forget to Show() it!
        :return: The result of the new section creation
        """
        return self.tabs.AddPage(content, tabname, True)

    def UnregisterTab(self, content) -> bool:
        return self.tabs.DeletePage(content)

    def _RightClickTab(self, evt):
        menu = wx.Menu()
        # Note: I don't know what else to add to here:\
        for label, handler in [
            (
                _("Close the current (open) tab"),
                lambda evt: self.UnregisterTab(self.tabs.GetCurrentPage()),
            ),
            (
                _("Disable this (open) tab"),
                lambda evt: self.tabs.GetCurrentPage().Disable(),
            ),
            (_("Close the side bar"), lambda evt: self.Close()),
        ]:
            item = menu.Append(wx.ID_ANY, label)
            menu.Bind(wx.EVT_MENU, handler, item)
        self.tabs.PopupMenu(menu, evt.GetPosition())
        menu.Destroy()
