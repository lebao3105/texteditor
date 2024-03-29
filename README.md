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
    <a href="https://github.com/lebao3105/texteditor/actions/workflows/wheel.yml">
        <image src="https://github.com/lebao3105/texteditor/actions/workflows/wheel.yml/badge.svg" align="right"/>
    </a>
</p>

<br clear="both">

> Tkinter version has been moved to [texteditor-tk](https://github.com/lebao3105/texteditor-tk). Its future release will still be placed in TestPypi.

> This is the last Python version of the project. When version 1.6 comes out and have all fixes + new things as much as possible, the development will be temporary stopped (as I am the only one here) for C++ and build systems + templates preparation, then a fresh write will begin.
> Happy summer!

> All textworker projects have been moved to [GitLab](https://gitlab.com/textworker). This is the last commit on this GitHub repo.

## Features

* Tabs split/rearrangement
* Access to your files without opening File Explorer
* ~~Run some tasks with Command Window~~
* Customizable interface, right on the native UI
* Open history
* ~~Partial Git support (1.6a3+)~~
* Auto save

See all app releases [here.](https://github.com/lebao3105/texteditor/releases)

You can get wheels from [GitHub Actions](https://github.com/lebao3105/texteditor/actions).

## Setup

Requires Python 3.10 or later.

Install all dependencies shown in [requirements.txt](requirements.txt)

Additional dependencies may required for wxPython:

* All: Install `attrdict3` from Pypi first BEFORE RUNNING `pip install wxpython`

* Linux: ```libgtk-3-dev``` and ```libsdl2-dev``` plus C++ compiler (g++). That's basic for now - you may need more

* macOS: You don't need to worry if you're on a recent macOS on a x86_64 Intel Mac, else you may need to have a build.

* Windows: Microsoft Visual C++

Wheels for some Linux distributions (and their based-ons): https://extras.wxpython.org/wxPython4/extras/linux/gtk3/

Installable directly from Pypi as the ```textworker``` package.

Run this project like every Python projects else. Use `-h` / `--help` to see all available options.

There is a Makefile in this project. Run `make targets` to see all availale targets.

## Contributing

Feel free to do that!

As the code is hosted on GitHub, that means you use GitHub to report issues, share ideas, or make your own work and do a PR.

Before reporting issues:

- Check for all steps you've done to run textworker.

- Try running in Terminal/Command Prompt to capture everything

- Check for all the issues, including closed ones.

- Check for open PRs.

Look at [CONTRIBUTING](./CONTRIBUTING) for more stuff.
