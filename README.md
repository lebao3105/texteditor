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
    <!-- <a href="https://gitlab.com/textworker/textworker_py/actions/workflows/wheel.yml">
        <image src="https://gitlab.com/textworker/texteditor/actions/workflows/wheel.yml/badge.svg" align="right"/>
    </a> -->
</p>

<br clear="both">

> Tkinter version has been moved to [texteditor-tk](https://gitlab.com/textworker/legacy_python/textworker-tkinter).

> Future releases will be placed in TestPypi.

## Features

* Tabs split/rearrangement
* Access to your files without opening File Explorer
* ~~Run some tasks with Command Window~~
* Customizable interface
* Open history
* ~~Partial Git support (1.6a3+)~~
* Auto save

See all app releases [here.](https://gitlab.com/textworker/legacy_python/textworker/releases)

## Setup

Requires Python 3.10 or later.

Install all dependencies shown in [requirements.txt](requirements.txt)

Additional dependencies may required for wxPython:

* All: Install `attrdict3` from Pypi first

* Linux: ```libgtk-3-dev``` and ```libsdl2-dev``` plus C++ compiler (g++). That's basic for now - you may need more

* macOS: You don't need to worry if you're on a recent macOS on a x86_64 Intel Mac, else you may need to have a build.

* Windows: Microsoft Visual C++

Wheels for some Linux distributions (and their based-ons): https://extras.wxpython.org/wxPython4/extras/linux/gtk3/

Installable directly from Pypi as the ```textworker``` package.

Run this project like every Python projects else. Use `-h` / `--help` to see all available options.

There is a Makefile in this project. Run `make targets` to see all availale targets.

## Contributing

We welcome people to make forks, make issues, and submit patches, features (request) as well!

Before reporting issues:

- Check for all steps you've done to run textworker.

- Try running in Terminal/Command Prompt to capture everything

- Check for all the issues, including closed ones.

- Check for open PRs.

Look at [CONTRIBUTING](./CONTRIBUTING) for more stuff.