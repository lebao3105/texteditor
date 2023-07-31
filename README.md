<div style="float: left;">
    <img src="https://raw.githubusercontent.com/lebao3105/texteditor/data/icons/me.lebao3105.textworker.svg">
    <img src="https://raw.githubusercontent.com/lebao3105/texteditor/data/icons/me.lebao3105.textworker.Devel.svg">
</div>

<p align="right">
    <h1 align="right">
        <strong>Textworker</strong>
    </h1>
    <h3 align="right">
    A simple and cross-platform Python text editor.
    </h3>
    <a href="https://github.com/psf/black">
        <image src="https://img.shields.io/badge/code%20style-black-000000.svg" align="right"/>
    </a>
    <a href="https://github.com/lebao3105/texteditor/actions/workflows/wheel.yml">
        <image src="https://github.com/lebao3105/texteditor/actions/workflows/wheel.yml/badge.svg?branch=data" align="right"/>
    </a>
</p>

<br clear="both">

## Features
* Tabs split/rearrangement
* Access to your files without opening File Explorer
* Run some tasks with Command Window
* Customizable interface
* Partial Git support (1.6a3+)
* Auto save

See all app releases [here.](https://github.com/lebao3105/texteditor/releases)

You can get wheels from [GitHub actions](https://github.com/lebao3105/texteditor/actions).

## Build and install
Requires Python 3.8+.

Additional dependencies may required:
* Linux: ```libgtk-3-dev``` and ```libsdl2-dev``` plus C++ compiler (g++). That's basic for now - you may need more
* macOS: You don't need to worry if you're on a recent macOS on a x86_64 Intel mac, else you may need to have a build. ```XCode Command-line tools``` may not enough.
* Windows: Microsoft Visual C++

Installable directly from Pypi as the ```textworker``` package.

Run:
```bash
$ python3 -m textworker [args]
```

For any additional arguments, please use ```-h``` / ```--help``` to show them.

If you want to use the source code:

```bash
$ git clone https://github.com/lebao3105/texteditor.git -b wip/wx # Or you can use gitlab instead
$ cd texteditor
$ git submodule update --init --recursive
$ pip install attrdict3
$ pip install cairosvg # If you want, for app icon support
$ pip install ./libtextworker[autocolor,configparser,wx] # autocolor is optional, even you have dark mode.
```

Install from source: ```pip install -e .```
