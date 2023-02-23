import io
import pathlib
import re
import wx
import wx.xml
import wx.xrc
import wx.adv

from .backend import get_config, logger

currdir = pathlib.Path(__file__).parent


class Error(Exception):
    def __init__(self, objname: str, title: str, msg: str, *args: object):
        fullmsg = "Object {} error: ({}) {}".format(objname, title, msg)
        log.throwerr(title, True, msg)
        super().__init__(fullmsg, *args)


class AppSettings(object):
    def __init__(
        self,
        cfg: dict = get_config.cfg,
        file: str = get_config.file,
        default_section: str = (item[0] for item, item2 in get_config.cfg.items()),
        **kwds,
    ):
        self.cfg = get_config.GetConfig(
            cfg, file, default_section=default_section, **kwds
        )
        self.file = file

    def get_setting(self, sectionname, option, needed: bool = False):
        return self.cfg.getkey(sectionname, option, needed)

    def set_setting(self, section, option, value):
        self.cfg.set(section, option, value)
        with open(self.file, "w") as f:
            self.cfg.write(f)

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

    def AddMenu(self, name, items: list):
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


def txtLocalize(match_obj):
    return _(match_obj.group(1))


class SettingsWindow:
    def __init__(self, parent):
        # Setup translation
        # Cre: https://wiki.wxpython.org/XRCAndI18N
        file = str(currdir / "ui" / "preferences.xrc")
        with open(file, encoding="utf8") as f:
            xrc_data = f.read()

        xrc_data = re.sub("_\(['\"](.*?)['\"]\)", txtLocalize, xrc_data)
        xrc_data = xrc_data.encode("utf8")

        # Call out the resource file, with translated strings
        xmlload = wx.xml.XmlDocument(io.BytesIO(xrc_data))
        self.Res = wx.xrc.XmlResource()
        self.Res.LoadDocument(xmlload)

        # Load initial items
        self.Frame = self.Res.LoadObject(parent, "Preferences", "wxWizard")
        self.Page1 = wx.xrc.XRCCTRL(self.Frame, "WelcomeScreen")
        self.Frame.SetPageSize((595, 424))

        # Images
        self.Img1 = wx.xrc.XRCCTRL(self.Frame, "m_bitmap1")
        self.Img2 = wx.xrc.XRCCTRL(self.Frame, "m_bitmap2")
        self.Img3 = wx.xrc.XRCCTRL(self.Frame, "m_bitmap3")

        self.Img1.SetBitmap(wx.Icon(str(currdir / "images" / "terminal.png")))
        self.Img2.SetBitmap(wx.Icon(str(currdir / "images" / "logs.png")))
        self.Img3.SetBitmap(wx.Icon(str(currdir / "images" / "configs.png")))

        # Font
        self.Font = wx.xrc.XRCCTRL(self.Frame, "m_fontPicker1")
        self.Font.SetSelectedFont(global_settings.cfg._get_font())
        self.TextPreview = wx.xrc.XRCCTRL(self.Frame, "m_staticText6")
        global_settings.cfg.configure(self.TextPreview)

        # Color choices
        self.FontColorChoices = wx.xrc.XRCCTRL(self.Frame, "m_choice1")
        self.ColorPicker = wx.xrc.XRCCTRL(self.Frame, "m_colourPicker1")
        self.AppTheme = wx.xrc.XRCCTRL(self.Frame, "m_choice2")

        # Bind events
        self.Font.Bind(wx.EVT_FONTPICKER_CHANGED, self.SelectFont)
        self.FontColorChoices.Bind(wx.EVT_CHOICE, self.SetFontColor)
        self.ColorPicker.Bind(
            wx.EVT_COLOURPICKER_CHANGED,
            lambda evt: (
                global_settings.set_setting(
                    "interface",
                    "textcolor",
                    evt.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
                )
            ),
        )
        self.AppTheme.Bind(wx.EVT_CHOICE, self.SetTheme)

    def SelectFont(self, evt):
        selected_font = self.Font.GetSelectedFont()
        selected_color = self.Font.GetSelectedColour()

        style = selected_font.GetStyle()
        family = selected_font.GetFaceName()
        weight = selected_font.GetWeight()

        styles = {
            wx.FONTSTYLE_NORMAL: "normal",
            wx.FONTSTYLE_ITALIC: "italic",
        }

        weights = {
            wx.FONTWEIGHT_LIGHT: "light",
            wx.FONTWEIGHT_NORMAL: "normal",
            wx.FONTWEIGHT_SEMIBOLD: "semibold",
            wx.FONTWEIGHT_BOLD: "bold",
            wx.FONTWEIGHT_EXTRALIGHT: "maxlight",
            wx.FONTWEIGHT_EXTRABOLD: "maxbold",
        }

        global_settings.set_setting(
            "interface", "textcolor", selected_color.GetAsString(wx.C2S_HTML_SYNTAX)
        )
        global_settings.set_setting("interface.font", "weight", weights[weight])
        global_settings.set_setting("interface.font", "style", styles[style])
        global_settings.set_setting("interface.font", "family", family)

        self.TextPreview.SetFont(selected_font)

    def SetFontColor(self, evt):
        selected_item = self.FontColorChoices.GetStringSelection()
        self.ColorPicker.Enable(False)
        if selected_item == _("Default"):
            return global_settings.set_setting("interface", "textcolor", "default")
        elif selected_item == _("Red"):
            return global_settings.set_setting("interface", "textcolor", "red")
        elif selected_item == _("Green"):
            return global_settings.set_setting("interface", "textcolor", "green")
        elif selected_item == _("Custom"):
            self.ColorPicker.Enable()
            return

    def SetTheme(self, evt):
        selected_item = self.AppTheme.GetStringSelection()
        if selected_item == _("Dark"):
            return global_settings.set_setting("interface", "color", "dark")
        elif selected_item == _("Light"):
            return global_settings.set_setting("interface", "color", "light")
        elif selected_item == _("Automatic"):
            return global_settings.set_setting("interface", "autocolor", "yes")

    def Run(self):
        self.Frame.RunWizard(self.Page1)
        self.Frame.Destroy()
