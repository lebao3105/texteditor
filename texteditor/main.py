import os, sys
from tkinter import messagebox as msgbox
from . import mainwindow


# Startup functions
def __filenotfound(filepath):
    return msgbox.askyesno(
        _("File not found"), _("Cannot find the file %s - create it?" % str(filepath))
    )


def start_app(argv=None):
    argv = sys.argv[1:]
    root = mainwindow.MainWindow()
    n = len(argv)

    if n > 0:
        if os.path.isfile(argv[1]):
            root.notebook.fileops.openfile(argv[1])
        else:
            if __filenotfound(argv[1]):
                f = open(argv[1], mode="w")
                root.notebook.fileops.openfile(argv[1])
                del f

        for i in range(2, n):
            if os.path.isfile(argv[i]):
                root.add_tab()
                root.notebook.fileops.openfile(argv[i])
            elif __filenotfound(argv[i]):
                f = open(argv[i], mode="w")
                root.add_tab()
                root.notebook.fileops.openfile(argv[i])
                del f
    else:
        pass

    root.mainloop()
