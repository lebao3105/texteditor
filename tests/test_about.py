from textworker.extensions import AboutDialog
from wx import App

def test_about():
    app = App()
    dlg = AboutDialog(None)
    dlg.Customize()
    dlg.ShowModal()
    app.MainLoop()