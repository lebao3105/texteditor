## Makerelease
Making releases for texteditor.

1. Using meson (and ninja)
Install meson and ninja via pip. Also install gettext if needed.
Run:
$ meson build
$ # Skip TWO next commands if you don't use gettext
$ ninja -C build me.lebao3105.texteditor-pot
$ ninja -C build me.lebao3105.texteditor-update-po
$ #
$ ninja -C build me.lebao3105.texteditor-gmo
$ ninja -C build install

Run:
$ me.lebao3105.texteditor

2. Using build script (builder.py)
Use help flag to see the usage of the script. Note that this is not completed yet, but good enough to use.

3. Using py2exe
Because of the deprecation of py2exe's setup.py method, you can't use this method now. At least until I can use py2exe.freeze or pyinstaller...