## Text-editor
<div align="center">
    <img src="data/org.lebao3105.texteditor.svg">
    <img src="data/org.lebao3105.texteditor.Devel.svg">
</div>

A graphical text editor.
![image](https://user-images.githubusercontent.com/77564176/166142583-5fe685a1-21a4-44e1-8088-73ca27e0b04a.png)

## Features
* Tabs support
* Lightweight
* [Initial] Dark mode + Text colors support
* [Initial] Configuration file support
* [Initial] Installation on Linux (deb-based distros) + Windows .exe file making (completed)

## Running
Install configparser package before continue.

This project needs python3 + Tcl/Tkinter and pip installed. Also install PIL package with pip.

Always generate .mo files first:
> **On Windows:** To do this, find for msgfmt, msgmerge and xgettext from the Python installation folder.

```
./upd_trans.sh -upd
# If you see wrong text, do:
./upd_trans.sh -tep # Generate new .pot file
# Translate the application by opening <language code>/LC_MESSAGES
# /base.po, save it then:
./upd_trans.sh -upd
```

> **On Windows,** use:
```
REM Generate .pot + .po files
pygettext.py -d base -o po/base.pot src/main.py src/tabs.py src/pages/about.py src/pages/helpme.py
REM Copy .pot file to your_language_code/LC_MESSAGES/ then rename it to base.po
REM edit your .po files, then generate .mo files. This use 
REM for all available languages here.
msgfmt.py po/vi/LC_MESSAGES/base -o po/vi/LC_MESSAGES/base.mo
msgfmt.py po/en/LC_MESSAGES/base -o po/en/LC_MESSAGES/base.mo
```

If you see error ```/bin/bash^M: bad interpreter: No such file or directory``` (sometimes in bash), just run all commands created in if..elif block:
* $1 == "-tep": Create new .pot file
* $1 == "-upd": Generate .mo files (after you run use -tep & edited needed things)

Now just run [src/main.py](src/main.py).

To make executable files, read instructions in [makerelease](makerelease/).

## Screenshots
<div align="center">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/166142604-791a81ca-4f4c-47db-b037-b5525c7cf313.png">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/169689858-a131cd42-1d6d-4d2a-976d-7daef4fab5ac.png">
</div>

## Notes
* Text editor's UI works best on... Windows, not Linux! Tkinter GUI on Linux is ugly - and tabs dragging may not work.
* Code in this project may be too complex.
* Only a simple part of the project is based on dh7qc's [text editor](https://github.com/dh7qc/Python-Text-Editor/).
* Don't use Open System Shell if you want to use commands that require your input - the program will be broken with that!
* The project is also available on GitLab under the same user & repository name.
