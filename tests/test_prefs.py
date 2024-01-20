from textworker.extensions.settings import SettingsDialog
from wx import App, MessageBox, EVT_CLOSE

def test_prefs():
    def OnClose(evt):
        nonlocal app
        evt.Skip()
        app.ExitMainLoop()

    app = App()
    MessageBox(
        "Everything you make will be applied",
        "Warning"
    )
    prefs = SettingsDialog(None)
    prefs.dlg.Show()
    prefs.dlg.Bind(EVT_CLOSE, OnClose)
    app.MainLoop()