## Texteditor
[![Code style: black][codestyle]](https://github.com/psf/black)

<!-- <div align="center">
    <img src="texteditor/icons/texteditor.png">
    <img src="texteditor/icons/texteditor.Devel.png">
</div> -->

Texteditor is a text editor written in Python using Tkinter interface.

Read documents online: https://lebao3105.gitbook.io/texteditor_doc

Read the app API online: https://lebao3105.github.io/libtextworker

## Features
* Tabs support
* Fast
* Dark mode + Text colors support
* Configuration file support
* Auto save documents
* Command window where you can run external commands (except Console apps which require your inputs)

> This project is available on [GitLab.](https://gitlab.com/lebao3105/texteditor_tk)

## Running
Make sure you have Python 3.8 or higher with pip and Tkinter (not from Pypi), installed.

Cairosvg is used for generating app icon (.png) from .svg file, and it's optional.

Install dependencies: ```pip install ./libtextworker[tkinter]```

Run: ```python3 -m texteditor [args]```

Install: ```pip install -e .```

## Screenshots
![image][img]

[buildmd]: BuildAndRun.md
[codestyle]: https://img.shields.io/badge/code%20style-black-000000.svg
[img]: https://user-images.githubusercontent.com/77564176/206902963-b65f0c3c-efa4-438c-8f9b-1d98fa4faae1.png
