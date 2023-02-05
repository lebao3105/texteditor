import json
import sys
import wx

from .backend import get_config, logger

class Error(Exception):
    def __init__(self, objname:str, title:str, msg:str, *args:object):
        fullmsg = "Object {} error: ({}) {}".format(objname, title, msg)
        log.throwerr(title, True, msg)
        super().__init__(fullmsg, *args)

class AppSettings(object):
    
    def __init__(self,
                 cfg:dict=get_config.cfg,
                 file:str=get_config.file,
                 default_section:str=(item[0] for item, item2 in get_config.cfg.items()),
                 **kwds
    ):
        self.cfg = get_config.GetConfig(
            cfg,
            file,
            default_section=default_section,
            **kwds
        )
    
    def get_setting(self, sectionname, option, needed:bool=False):
        return self.cfg.getkey(sectionname, option, needed)
    
    def set_setting(self, section, option, value):
        return self.cfg.set(section, option, value)
    
    def register_section(self, section_name, options: dict):
        """Register a new section on the configuration file."""
        self.cfg.add_section(section_name)
        self.cfg[section_name] = options
    
    def unregister_section(self, section_name):
        """Unregister a section on the configuration file."""
        return self.cfg.remove_section(section_name)

class MenuBar(wx.MenuBar):

    def SetParent(self, parent):
        self.parent = parent
        return
    
    def AddMenu(self, name, items:list):
        """Add a new menu entry.
        Menu items use the following format:
        ```
        [   # Must be a list
            (id, label, helptext, handler, None),
            ...
            (id, label, helptext, handler, wx.ITEM_CHECK), # Add check item
            (id, label, helptext, handler, wx.ITEM_RADIO) # Add radio item
            (None, None, None, None, None) # Add separator
        ]
        ```
        Sub-menus are not supported.
        Don't forget to set the parent of the menubar first! (SetParent function)
        Returns the generated menu.
        """
        target_menu = wx.Menu()
    
        for id, label, helptext, handler, kind in items:
            if id == None:
                target_menu.AppendSeparator()
            else:
                if kind == None:
                    kind = wx.ITEM_NORMAL
                if label == None:
                    label = ""
                if helptext == None:
                    helptext = ""
                item = target_menu.Append(id, label, helptext, kind)
                self.parent.Bind(wx.EVT_MENU, handler, item)
        self.Append(target_menu, name)
        return target_menu

global_settings = AppSettings()
log = logger.Logger()