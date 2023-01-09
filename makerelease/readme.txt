## Makerelease
Making releases for texteditor.

1. Using meson (and ninja)
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

2. Using build script (builder.py)
Use help flag to see the usage of the script. Note that this is not completed yet, but good enough to use.

3. Using py2exe
Because of the deprecation of py2exe's setup.py method, you can't use this method now. At least until I can use py2exe.freeze or pyinstaller...