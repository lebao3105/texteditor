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

## Install dependencies
```bash
$ pip install attrdict3
$ pip install configparser darkdetect pillow packaging wxpython # This will take minutes!
```

## Run (and install)
### With pip (to install textworker)
```bash
$ pip install textworker
```

### With git (run from source)
1. Clone the source code:
```bash
$ git clone https://github.com/lebao3105/texteditor.git -b wip/wx textworker
$ cd textworker
$ git submodule update --init --recursive --remote
```
2. Make translation (optional, gettext and meson required):
```bash
$ meson build # --prefix=<dir> # Use this to set the install prefix
$ ninja -C build me.lebao3105.textworker-pot # Use for translators, to get new & untranslated strings
$ ninja -C build me.lebao3105.textworker-update-po
$ ninja -C build me.lebao3105.textworker-gmo
```

Run:
```bash
$ python -m textworker [file]
```

With pip installation you can use:
```bash
$ textworker [file]
```

If you use meson (run ```ninja -C build install``` to install), run:
```bash
$ <install_prefix>/bin/me.lebao3105.textworker [file]
```