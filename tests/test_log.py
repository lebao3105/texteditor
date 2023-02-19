import pytest
from texteditor.backend import logger, textwidget

log = logger.Logger(logfile="tests/test.log")

@pytest.mark.skip(reason='this is not a function to test')
def checklog(msg: str):
    with open("tests/test.log", "r") as f:
        assert f.read().find(msg) != -1, "Log not written?"


def test_throwinf():
    msg = log.throwinf("Infomation", "This is an example infomation.")
    return checklog(msg)


def test_logwindow():
    textw = textwidget.TextWidget(
        parent=None,
        useMenu=True,
        useScrollbars=False,
        enableStatusBar=True,
        unRedo=True,
    )
    wind = logger.LoggerWithStatusbar(textw, True)
    # wind.statusbar.mainloop()

    msg = wind.throwerr("Error", "An error occured!")

    assert wind.statusbar.logs.index(msg)
    return checklog(msg)
