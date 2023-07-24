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

    return msgbox.askyesno(_(f"{filepath} not found - create it?"))


def start_app(argv: list[str]):
    root = mainwindow.MainWindow()
    n = len(argv)

    if n > 0:
        for i in range(1, n):
            if not (
                os.path.exists(argv[i]) and os.path.isdir(argv[i])
            ) and __filenotfound(argv[i]):
                open(argv[i], "w")

            if i >= 2:
                root.add_tab()

            root.notebook.fileops.LoadFile(argv[i])

    root.mainloop()
