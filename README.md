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
        <image src="https://github.com/lebao3105/texteditor/actions/workflows/wheel.yml/badge.svg" align="right"/>
    </a>
</p>

<br clear="both">

## For Tkinter builds

Releases from 1.5a0 and their source code will be placed in a new repository: lebao3105/texteditor-tk.

This was made in order to make the updater for both 2 types of app works easier.

So that: the `main` branch will place the latest (trunk) code (again).

Texteditor-tk is still available in TestPypi, even for the 1.5 release.

## Features

* Tabs split/rearrangement
* Access to your files without opening File Explorer
* ~~Run some tasks with Command Window~~
* Customizable interface
* Open history
* ~~Partial Git support (1.6a3+)~~
* Auto save

See all app releases [here.](https://github.com/lebao3105/texteditor/releases)

You can get wheels from [GitHub Actions](https://github.com/lebao3105/texteditor/actions).

## Setup

Requires Python 3. Version 3.10+ maybe ideal.

Install all dependencies shown in [requirements.txt](requirements.txt)

Additional dependencies may required for wxPython:

* Linux: ```libgtk-3-dev``` and ```libsdl2-dev``` plus C++ compiler (g++). That's basic for now - you may need more

* macOS: You don't need to worry if you're on a recent macOS on a x86_64 Intel Mac, else you may need to have a build.

* Windows: Microsoft Visual C++

Installable directly from Pypi as the ```textworker``` package.

Run:

```bash
$ python3 -m textworker [args]
```

For any additional arguments, please use ```-h``` / ```--help``` to show them.

If you want to use the source code: Clone the source code, install dependencies as shown in pyproject.toml, run module `textworker` as a normal Python module.

Install from source: ```pip install -e .``` or ```python3 builder.py install```

## Contributing

Feel free to do that!

As the code is hosted on GitHub, that means you use GitHub to report issues, share ideas, or make your own work and do a PR.

Before reporting issues:

- Check for all steps you've done to run textworker.

- Try running in Terminal/Command Prompt to capture everything

- Check for all the issues, including closed ones.

- Check for open PRs.

Look at [CONTRIBUTING](./CONTRIBUTING) for more stuff.