## Textworker
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build releases (wheel) (wx version)](https://github.com/lebao3105/texteditor/actions/workflows/wheel.yml/badge.svg?branch=data)](https://github.com/lebao3105/texteditor/actions/workflows/wheel.yml)

A simple and cross-platform Python text editor.

> Note: This is a port of texteditor/textworker to use wxPython. Features, mostly are different to the Tkinter one and are not fully completed.

Stuffs you can do with this editor:
* VSCode-like tabs split - re-arrangement & side bar
* Access to your files without opening File Explorer
* Run some tasks with Command Window
* Customizable interface
* New since 1.6a3: Git support!
* Auto save! (for the current tab in this time) (currently disabled)

<div align="center">
    <img src="textworker/data/icons/me.lebao3105.textworker.Devel.svg">
    <img src="textworker/data/icons/me.lebao3105.textworker.svg">
</div>

See all app releases [here.](https://github.com/lebao3105/texteditor/releases) You can get wheels from [GitHub actions](https://github.com/lebao3105/texteditor/actions).

## Build and install
Requires Python 3.8+.

Additional dependencies may required:
* Linux: ```libgtk-3-dev``` and ```libsdl2-dev``` plus C++ compiler (g++)
* Windows: Microsoft Visual C++

Installable directly from Pypi as the ```textworker``` package.

Run:
```bash
$ python3 -m textworker [args]
```

If you want to use the source code:
```bash
$ git clone https://github.com/lebao3105/texteditor.git -b wip/wx # Or you can use gitlab instead
$ cd texteditor
$ git submodule update --init --recursive
$ pip install attrdict3
$ pip install cairosvg # If you want, for app icon support
$ pip install -r requirements.txt
```

Install from source: ```pip install -e .```
