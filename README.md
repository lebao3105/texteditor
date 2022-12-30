## Texteditor
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple and cross-platform Python text editor.
(This is an initial port of texteditor to use wxPython - not all features are implemented.)

<div align="center">
    <img src="texteditor/icons/texteditor.png">
    <img src="texteditor/icons/texteditor.Devel.png">
</div>

## Setup
> Note: Please uninstall older version of texteditor first, if you have installed it
This project requires Python >=3.8 with only wxPython installed (for this time). To generate wheel files you also need ```build``` installed.

Let's get started:

Want to setup translations? Use meson and ninja - which are installable via pip should work:
```
$ pip install meson ninja
$ meson build
$ ninja -C build me.lebao3105.texteditor-pot
$ ninja -C build me.lebao3105.texteditor-update-po
$ # Update your language translation
$ ninja -C build me.lebao3105.texteditor-gmo
$ cp -r build/po/* po/
```
Run the app:
* If you just want to try out this application without installing, ```python3 -m texteditor``` is what you want.
* If you want to install, do ```python3 -m build``` (delete dist folder first if there is) then ```pip3 install dist/<filename>.whl```. Run the app with ```texteditor```.