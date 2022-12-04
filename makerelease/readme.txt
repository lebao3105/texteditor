1. Making .exe file
Just copy files.py and setupwin.py to ../texteditor, install py2exe via pip.
Make sure that you're in ../texteditor, run:
$ py setupwin.py py2exe
The output will be in build folder.

2. Using meson (and ninja)
> This is not completed yet. The project will be installed to C:\Lib\site-packages by the default.
Install meson and ninja via pip. Also install gettext.
Run:
$ meson build
$ ninja -C build me.lebao3105.texteditor-pot
$ ninja -C build me.lebao3105.texteditor-update-po
$ ninja -C build me.lebao3105.texteditor-gmo
$ ninja -C build install
Copy this:

(Windows)
import sys
sys.path.insert(1, 'C:\Lib\site-packages\texteditor')
import texteditor
texteditor.start_app()

(Linux)
---

to runtextd.py (or something else you want) - save to somewhere safe.
Try to run it.