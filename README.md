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
Install all requirements (configparser + pillow) before continue.

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

> **On Windows:** To make .exe file, do:
```
pip install py2exe
cd src
python setup.py py2exe
.\dist\main.exe
```

## Screenshots
<div align="center">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/166142604-791a81ca-4f4c-47db-b037-b5525c7cf313.png">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/169689858-a131cd42-1d6d-4d2a-976d-7daef4fab5ac.png">
</div>

## Note
* Text editor's UI works best on... Windows, not Linux! I see there are problems that I can't use Pillow on Linux - this will prevent us from seeing the icon in About.
* Basic things (copy, paste, cut) are not implemented yet.
* Code in this project may be too complex.
* Some part of the project is based on dh7qc's [text editor](https://github.com/dh7qc/Python-Text-Editor/).
