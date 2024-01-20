import wx
from ..generic import global_settings


class MultiViewer:
    def __init__(self, parent):
        location = global_settings.getkey(
            "extensions.textwkr.multiview", "notebook_location", needed=true
        )
        nbside = getattr(wx, "NB_{}".format(location.upper()))

        self.tabs = wx.Notebook(parent, -1, style=nbside)
        self.tabs.Bind(wx.EVT_RIGHT_DOWN, self._RightClickTab)

    def RegisterTab(self, tabname: str, content) -> bool:
        """
        Ask for add a new section to the side bar.
        @param tabname:str: Name of the section (used for the new tab name)
        @param content: Section content (must be a wxPython object). Don't forget to Show() it!
        :return: The result of the new section creation
        """
        return self.tabs.AddPage(content, tabname, true)

    def UnregisterTab(self, content) -> bool:
        return self.tabs.DeletePage(content)

    def _RightClickTab(self, evt):
        menu = wx.Menu()
        # P/s: I don't know what else to add here:\
        for label, handler in [
            (
                _("Close the current tab"),
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
