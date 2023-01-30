## Requirements
```
python 3.8+ with pip and its development codes
gettext (optional)
meson and ninja (optional)
Microsoft Visual C++ (Windows)
GTK3 development files + pkgconfig and C/C++ compilers (Linux)
```

## Notes
* We assume that you have cloned this project repository and on the cloned folder.
* You can use my builder script on [makerelease.](makerelease)

## Steps
1. Install dependencies first, always:
> On Linux use pip3 instead of the pip command below.
```bash
$ pip install attrdict3
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

Or just use pip (still need build & wheel installed):
```bash
$ pip install .
```

b. Using meson
```bash
$ pip install meson ninja
$ meson build # Use --prefix=<dir> to change the installation location
$ ninja -C build
$ ninja -C build install # On Linux sudo may required
```

4. Run
a. Don't install using meson
```bash
$ python3 -m textworker
```

b. Install using meson
```bash
$ me.lebao3105.textworker
```

On Windows:
```cmd
REM Default install
> C:\bin\me.lebao3105.textworker
REM Custom install prefix
> <install prefix>\bin\me.lebao3105.textworker
```