## Texteditor
<div align="center">
    <img src="texteditor/icons/texteditor.png">
    <img src="texteditor/icons/texteditor.Devel.png">
</div>

Texteditor is a text editor written in Python using Tkinter interface.

![image](https://user-images.githubusercontent.com/77564176/166142583-5fe685a1-21a4-44e1-8088-73ca27e0b04a.png)

## Features
* Tabs support
* Fast
* Dark mode + Text colors support
* [Working] Configuration file support
* [New] Autosave
* Able to make Windows executable file (.exe)
* Command window where you can run external commands (except Console apps which require you inputs)

> Note: This project also available on GitLab with this [link](https://gitlab.com/lebao3105/texteditor_tk)

## Running
You need Python 3.8+ with Tkinter & pip installed.

Install texteditor from Pypi Test repo first:
```
pip install -i https://test.pypi.org/simple/ texteditor
```

Then run:
```
python3 -m texteditor
```

Start from version 1.3-dev1, you can use ```texteditor``` directly.

## Running from source
If needed, let this app speak your language. On Linux, use [```upd_trans.sh```](upd_trans.sh) should work:
```
./upd_trans.sh -upd
# If you see wrong text, do:
./upd_trans.sh -tep # Generate new .pot file
# Translate the application by editing <language code>/LC_MESSAGES/base.po, then save it:
./upd_trans.sh -upd
```

On Windows, find pygettext & msgfmt from your Python installation folder. Then use them:
```
REM Generate .pot + .po files
pygettext.py -d base -o po/base.pot <every file on texteditor/>
REM Copy .pot file to your_language_code/LC_MESSAGES/ then rename it to base.po
REM edit your .po files, then generate .mo files. This use 
REM for all available languages here.
msgfmt.py po/<language code>/LC_MESSAGES/base -o po/<language code>/LC_MESSAGES/base.mo
```

Once done, run ```python3 -m texteditor```.

To make executable files, read instructions in [makerelease](makerelease/).

## Screenshots
<div align="center">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/166142604-791a81ca-4f4c-47db-b037-b5525c7cf313.png">
    <img id="image" src="https://user-images.githubusercontent.com/77564176/169689858-a131cd42-1d6d-4d2a-976d-7daef4fab5ac.png">
    <img id="image" src="image.png">
</div>

## UI on Linux
It's ugly here... If you don't like this, try to find some ttk theme on the internet, download it to somewhere safe.

Then add the following code (just an example) to texteditor/mainwindow.py:

> Add codes before ```self.place_widgets()``` line!
```
style = ttk.Style(self)
self.tk.call('source', '{tcl file location}')
style.theme_use('{theme name}')
```

Or use the instructions from the theme's author.
