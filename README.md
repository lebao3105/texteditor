## Texteditor
[![Code style: black][codestyle]](https://github.com/psf/black)

<div align="center">
    <img src="texteditor/icons/texteditor.png">
    <img src="texteditor/icons/texteditor.Devel.png">
</div>

Texteditor is a text editor written in Python using Tkinter interface.

Read documents online: https://lebao3105.gitbook.io/texteditor_doc.

## Features
* Tabs support
* Fast
* Dark mode + Text colors support
* Configuration file support
* Autosave
* Command window where you can run external commands (except Console apps which require your inputs)

> This project is mirrored to [GitLab.](https://gitlab.com/lebao3105/texteditor_tk)

## Running
Before continue, make sure that you have Python 3.8 or higher installed with pip and Tkinter. If you use wxPython version, you don't need Tkinter, but you need wxPython installed via pip.

Read [this file][buildmd] for the full instructions.

## Future of this program
* 1.5 **may be** the final version of texteditor (now is textworker) uses Tkinter interface. This release will come with a lot of code fixes and cleans. I hope there are also features defined in [TODO](TODO) too.
* 1.6 is the first version to use wxPython - and it is published to Pypi as the "textworker" package.
* Important changes implemented on any branch will be ported to each other.

## Screenshots
![image][img]
![image2][img2]

[buildmd]: BuildAndRun.md
[codestyle]: https://img.shields.io/badge/code%20style-black-000000.svg
[img]: https://user-images.githubusercontent.com/77564176/206902963-b65f0c3c-efa4-438c-8f9b-1d98fa4faae1.png
[img2]: https://user-images.githubusercontent.com/77564176/166142583-5fe685a1-21a4-44e1-8088-73ca27e0b04a.png