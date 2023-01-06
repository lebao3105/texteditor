## Texteditor
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<div align="center">
    <img src="texteditor/icons/texteditor.png">
    <img src="texteditor/icons/texteditor.Devel.png">
</div>

Texteditor is a text editor written in Python using Tkinter interface.

Documents are available on https://lebao3105.gitbook.io/texteditor_doc.

## Features
* Tabs support
* Fast
* Dark mode + Text colors support
* Configuration file support
* Autosave
* Command window where you can run external commands (except Console apps which require your inputs)

> Note: This project also available on GitLab ([link here.](https://gitlab.com/lebao3105/texteditor_tk))

## Running
You need Python 3.8+ with Tkinter & pip installed.

The fastest way is to install texteditor from Pypi Test repo:
```
pip install -i https://test.pypi.org/simple/ texteditor
```

Or you can clone the source code.

If needed, let this app speak your language. Use meson and ninja - which are installable via pip should work:
```
$ pip install meson ninja
$ meson build
$ ninja -C build me.lebao3105.texteditor-pot
$ ninja -C build me.lebao3105.texteditor-update-po
$ # Update your translation
$ ninja -C build me.lebao3105.texteditor-gmo
$ cp -r build/po/* po/
```

Once you're done, run:
```
python3 -m texteditor
```

To make executable files (on Windows only), read the instruction from [makerelease](makerelease/).

## Screenshots
![image](https://user-images.githubusercontent.com/77564176/206902963-b65f0c3c-efa4-438c-8f9b-1d98fa4faae1.png)
<div align="center">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/166142583-5fe685a1-21a4-44e1-8088-73ca27e0b04a.png">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/166142604-791a81ca-4f4c-47db-b037-b5525c7cf313.png">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/169689858-a131cd42-1d6d-4d2a-976d-7daef4fab5ac.png">
</div>
