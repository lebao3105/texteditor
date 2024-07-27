from textworker.ui.about import AboutDialog
from wx import App

def test_about():
    app = App()
    dlg = AboutDialog(None)
    dlg.ShowModal()
    app.MainLoop()