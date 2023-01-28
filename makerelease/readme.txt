1. Making .exe file
Install pyinstaller, then run (thanks Auto Py to exe!):
$ pyinstaller --noconfirm --onedir --windowed --icon "<project path>/textworker/icons/textworker.Devel.png" --name "Textworker" --clean --add-data "<project path>/textworker/icons/textworker.Devel.png;." --add-data "<project path>/textworker/icons/textworker.png;."  "<project path>/textworker/__main__.py"

2. Using meson (and ninja)
> The project will be installed to C:\bin and C:\share by the default on Windows.
Install meson and ninja via pip (in Linux install from the distro's repo). Also install gettext.
Run:
$ meson build
$ ninja -C build me.lebao3105.texteditor-pot
$ ninja -C build me.lebao3105.texteditor-update-po
$ ninja -C build me.lebao3105.texteditor-gmo
$ ninja -C build install

to runtextd.py (or something else you want) - save to somewhere safe.
Try to run it.

3. Using build script (builder.py)
Use help flag to see the usage of the script. Note that this is not completed yet.