## Requirements
* Python 3.8+
* Pip3 (comes with Python)
* Tkinter (if you don't use wip/wx branch)
* wxPython (if you use wip/wx branch, install wxPython's requirements also)
* Packages specified in [requirements.txt](requirements.txt) via pip
* Gettext (optional) to generate translations
* Meson and ninja (installable via pip) (optional) to install the project
* Build (install via pip) (optional) to build and install the project (after the installation pip will recognize texteditor as a Python package)

## Notes
* We assume that you have cloned this project repository and on the cloned folder.
* To make portable version of this app (Windows only), please go to [makerelease](makerelease) folder.

## Steps
1. Install dependencies first, always:
```sh
$ pip install -r requirements.txt
```

2. (Optional) Generate translation
```sh
$ meson build
$ ninja -C build me.lebao3105.texteditor-pot
$ # If you don't see any file that have your language translation,
$ # please add your language code into po/LINGUAS or run the command
$ # below and duplicate any generated .po file and rename it
$ # your language code!
$ ninja -C build me.lebao3105.texteditor-update-po
$ # Update your translation...
$ # Now compile all translations
$ ninja -C build me.lebao3105.texteditor-gmo
$ cp -r build/po/* po/
```

3. Install!

a. Using build module
```sh
$ pip install build wheel
$ rm -rf dist build # Remove generated files, if have
$ python3 -m build
$ pip install dist/<file name>.whl --force-reinstall
```

b. Using meson
```sh
$ pip install meson ninja
$ meson build --prefix=/usr
$ ninja -C build
$ sudo ninja -C build install
$ me.lebao3105.texteditor # Run
```
