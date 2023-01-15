## Requirements
```
python 3.8+ with pip
gettext (optional)
meson and ninja (optional)
```

## Notes
* We assume that you have cloned this project repository and on the cloned folder.
* You can use my builder script on [makerelease.](makerelease)

## Steps
1. Install dependencies first, always:
```bash
$ pip install -r requirements.txt
```

2. (Optional) Generate translation
```bash
$ meson build
$ ninja -C build me.lebao3105.textworker-pot
$ # If you don't see any file that have your language translation,
$ # please add your language code into po/LINGUAS or run the command
$ # below and duplicate any generated .po file and rename it
$ # your language code!
$ ninja -C build me.lebao3105.textworker-update-po
$ # Update your translation...
$ # Now compile all translations
$ ninja -C build me.lebao3105.textworker-gmo
$ cp -r build/po/* po/
```

3. Install!

a. Using build module
```bash
$ pip install build wheel
$ rm -rf dist build # Remove generated files, if have
$ python3 -m build
$ pip install dist/<file name>.whl --force-reinstall
```

(Or just run pip (still need build & wheel installed):
```bash
$ pip install .
```
)

b. Using meson (only use this on Linux)
```bash
$ pip install meson ninja
$ meson build --prefix=/usr
$ ninja -C build
$ sudo ninja -C build install
```