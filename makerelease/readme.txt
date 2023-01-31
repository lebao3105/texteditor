## Makerelease
Making releases for texteditor.

1. Using meson (and ninja)
Install meson and ninja via pip. Also install gettext if needed.
Run:
$ meson build
$ # Skip THREE next commands if you don't use gettext
$ ninja -C build me.lebao3105.texteditor-pot
$ ninja -C build me.lebao3105.texteditor-update-po
$ ninja -C build me.lebao3105.texteditor-gmo
$ # Install
$ ninja -C build install

Run:
$ me.lebao3105.texteditor

2. Using build script (builder.py)
Use help flag to see the usage of the script. Note that this is not completed yet, but good enough to use.

3. Using pyinstaller
$ pyinstaller --noconfirm --onedir --windowed --icon "<project path>/texteditor/icons/texteditor.Devel.png" --name "texteditor" --clean --add-data "<project path>/texteditor/icons/texteditor.Devel.png;." --add-data "<project path>/texteditor/icons/texteditor.png;."  --add-data "<project path>/po;po/" "<project path>/texteditor/__main__.py"
