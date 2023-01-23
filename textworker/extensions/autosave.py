import wx
from ..backend import logger, get_config

# Minutes to seconds
MIN_05 = 30  # 30 secs
MIN_1 = MIN_05 * 2  # 60 secs
MIN_15 = MIN_1 * 15  # 900 secs
MIN_20 = MIN_15 + MIN_1 * 5  # 1200 secs
MIN_30 = MIN_15 * 2  # 1800 secs

cfg = get_config.GetConfig(get_config.cfg, get_config.file, default_section="interface")
log = logger.Logger()


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

    savefn = object
    usable = cfg.getkey("extensions.autosave", "enable")
    forced = False
    parent = object
    shown = False

    def askwind(self):
        def getvalue(evt):
            nonlocal check_btn, cmb, timer
            if check_btn.GetValue() == True:
                self.saveconfig(cmb.GetValue())
            self.start()
            timer.Start(self.get(cmb.GetValue()) * 1000)
            self.parent.Bind(wx.EVT_TIMER, lambda evt: self.savefn(), timer)

        if self.shown == True:
            self.fm.Show()
            return

        fm = wx.Frame(None, title="Autosave config")
        timer = wx.Timer(fm)
        panel = wx.Panel(fm)
        box = wx.BoxSizer(wx.VERTICAL)
        cmb = wx.ComboBox(
            panel, choices=self.cmbitems, style=wx.CB_READONLY | wx.CB_DROPDOWN
        )
        check_btn = wx.CheckBox(panel, label="Save this value")
        btn = wx.Button(panel, label="Start")
        btn.Bind(wx.EVT_BUTTON, getvalue)

        box.Add(cmb, 0, wx.ALIGN_CENTER)
        box.Add(check_btn, 0, wx.ALIGN_CENTER)
        box.Add(btn, 0, wx.ALIGN_CENTER)
        panel.SetSizer(box)

        for widget in [fm, panel, cmb, check_btn, btn]:
            cfg.configure(widget)

        fm.Show()
        self.shown = True
        self.fm = fm

    def get(self, value: str):
        if len(self.cmbitems) != len(self.timealiases):
            raise Exception
        else:
            seen = set()
            for item in self.cmbitems and self.timealiases:
                if item in seen:
                    log.throwwarn(
                        title="AutoSave - code bug",
                        msg="Found duplicate item in AutoSave.cmbitems and/or AutoSave.timealiases. Please fix it. AutoSave will stop working now.",
                    )
                    self.usable = False
                    return
                else:
                    seen.add(item)
            return self.timealiases[self.cmbitems.index(value)]

    def check_state(self) -> bool:
        if (self.forced == True) or (self.usable == "yes" or True):
            self.usable = True
        elif (self.usable == "no" or False) and (self.forced == False):
            log.throwerr(
                msg="""
                AutoSave called when it's turned off in the configuration file and the developer not forced to turn it on temporary.
                Please tell the devloper to set AutoSave.forced to True to use the auto-saving document feature.
                """
            )
            self.usable = False
        return self.usable

    def start(self):
        if self.check_state() == True:
            self.savefn()
        else:
            return

    def saveconfig(self, value: str) -> bool:
        newvalue = str(self.get(value))
        return cfg.set("extensions.autosave", "time", newvalue)
