import wx
from ..generic import global_settings, log

# Minutes to seconds
MIN_05 = 30  # 30 secs
MIN_1 = MIN_05 * 2  # 60 secs
MIN_15 = MIN_1 * 15  # 900 secs
MIN_20 = MIN_15 + MIN_1 * 5  # 1200 secs
MIN_30 = MIN_15 * 2  # 1800 secs


class AutoSave:
    cmbitems = [
        "30 seconds",
        "1 minute",
        "2 minutes",
        "5 minutes",
        "10 minutes",
        "15 minutes",
        "20 minutes",
        "30 minutes",
    ]

    timealiases = [
        MIN_05,
        MIN_1,
        MIN_1 * 2,
        MIN_1 * 5,
        MIN_1 * 10,
        MIN_15,
        MIN_20,
        MIN_30,
    ]

    enabled = global_settings.get_setting("extensions.autosave", "enable")
    shown = False

    def __init__(self, savefn, parent):
        self.savefn = savefn
        self.parent = parent

        self.timer = wx.Timer(parent)
        if self.enabled in global_settings.cfg.yes_value or [True]:
            self.timer.Start(
                self.get(global_settings.cfg.getkey("extensions.autosave", "time"))
                * 1000
            )
            parent.Bind(wx.EVT_TIMER, lambda evt: self.savefn(), self.timer)
            # savefn()

    def askwind(self):
        def getvalue(evt):
            nonlocal check_btn, cmb
            if check_btn.GetValue() == True:
                if self.enabled in global_settings.cfg.no_value or [False]:
                    global_settings.cfg.set("extensions.autosave", "enable", "yes")
                self.saveconfig(cmb.GetValue())

            self.savefn()
            self.timer.Start(self.get(cmb.GetValue()) * 1000)
            self.parent.Bind(wx.EVT_TIMER, lambda evt: self.savefn(), self.timer)

        if self.shown == True:
            self.fm.Show()
            return

        fm = wx.Frame(None, title=_("Autosave config"))
        panel = wx.Panel(fm)
        box = wx.BoxSizer(wx.VERTICAL)
        cmb = wx.ComboBox(
            panel, choices=self.cmbitems, style=wx.CB_READONLY | wx.CB_DROPDOWN
        )
        check_btn = wx.CheckBox(panel, label=_("Save this value"))
        btn = wx.Button(panel, label=_("Start"))
        btn.Bind(wx.EVT_BUTTON, getvalue)

        box.Add(cmb, 0, wx.ALIGN_CENTER)
        box.Add(check_btn, 0, wx.ALIGN_CENTER)
        box.Add(btn, 0, wx.ALIGN_CENTER)
        panel.SetSizer(box)

        for widget in [fm, panel, cmb, check_btn, btn]:
            global_settings.cfg.configure(widget)

        fm.Show()
        self.shown = True
        self.fm = fm

    def get(self, value: str):
        if len(self.cmbitems) != len(self.timealiases):
            raise Exception
        else:
            try:
                return self.timealiases[self.cmbitems.index(value)]
            except ValueError:
                return self.timealiases[self.timealiases.index(int(value))]

    def saveconfig(self, value: str) -> bool:
        newvalue = str(self.get(value))
        return global_settings.set_setting("extensions.autosave", "time", newvalue)
