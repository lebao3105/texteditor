import os
from tkinter import messagebox as msgbox
from . import mainwindow

ignore_not_exists: bool = False
create_new: bool = True


# Startup functions
def __filenotfound(filepath):
    if ignore_not_exists:
        return False
    if create_new:
        return True
    return msgbox.askyesno(
        _("File not found"), _("Cannot find %s - create it?" % str(filepath))
    )


def start_app(argv: list[str]):
    root = mainwindow.MainWindow()
    n = len(argv)

    if n > 0:
        if os.path.isfile(argv[1]):
            root.notebook.fileops.LoadFile(argv[1])
        else:
            if __filenotfound(argv[1]):
                f = open(argv[1], mode="w")
                root.notebook.fileops.LoadFile(argv[1])
                del f

        for i in range(2, n):
            if os.path.isfile(argv[i]):
                root.add_tab()
                root.notebook.fileops.LoadFile(argv[i])
            elif __filenotfound(argv[i]):
                f = open(argv[i], mode="w")
                root.add_tab()
                root.notebook.fileops.LoadFile(argv[i])
                del f
    else:
        pass

    root.mainloop()
