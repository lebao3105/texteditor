import gettext
import sys, os
from os.path import isfile

import texteditor.mainwindow
import texteditor.tabs
from texteditor.miscs import file_operations, constants

gettext.bindtextdomain("base", "po")
gettext.textdomain("base")
texteditor._ = gettext.gettext

currdir = os.path.dirname(os.path.abspath(__file__))

if constants.STATE == "DEV":
    texteditor.icon = currdir + "/icons/texteditor.Devel.png"
elif constants.STATE == "STABLE":
    texteditor.icon = currdir + "/icons/texteditor.png"
else:
    print("Warning: Wrong application branch (STABLE/DEV) in miscs.constants module")
    texteditor.icon = None


def start_app(argv: sys.argv = None):
    if not argv:  # For __main__
        argv = sys.argv
    root = texteditor.mainwindow.MainWindow()
    n = len(argv)
    if n - 1 > 0:
        if isfile(argv[1]):
            file_operations.openfilename(root, argv[1])
        for i in range(2, n):
            if isfile(argv[i]):
                texteditor.tabs.add_tab(root)
                file_operations.openfilename(root, argv[i])
    else:
        pass

    root.mainloop()


if __name__ == "__main__":
    start_app(sys.argv)
