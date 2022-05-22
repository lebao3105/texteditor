## Text-editor
<div align="center">
    <img src="data/org.lebao3105.texteditor.svg">
</div>

A graphical text editor for Windows, macOS, Linux, BSD, and other operating systems.
![image](https://user-images.githubusercontent.com/77564176/166142583-5fe685a1-21a4-44e1-8088-73ca27e0b04a.png)

## Features
* Tabs support
* Lightweight
* [Initial] Dark mode + Text colors support
* [Initial] Configuration file support
* [Initial] Installation on Linux/BSD + Windows .exe file making
* [Working] Normal features for a text editor

## Running
Always generate .mo files first:
```
./upd_trans.sh -upd
# If you see wrong text, do:
./upd_trans.sh -tep # Generate new .pot file
# Translate the application by opening <language code>/LC_MESSAGES
# /base.po, save it then:
./upd_trans.sh -upd
```

If you see error ```/bin/bash^M: bad interpreter: No such file or directory``` (usually heppends in bash shell), do:
```
# Generate .mo files
for i in $(ls -d po/*/); do
    msgfmt ${i%%/}/LC_MESSAGES/base -o ${i%%/}/LC_MESSAGES/base.mo
done

# Wrong text in the program
xgettext -d base -o po/base.pot src/{main,tabs}.py src/pages/*.py
for i in $(ls -d po/*/); do
    msgmerge -U ${i%%/}/LC*/base.po po/base.pot
done

# Edit .po file in <your language code>/LC_MESSAGES folder, then
# re-generate .mo files
```

Now run:
```
python src/main.py
```

or:
```
python3 src/main.py
```

> **Warning:** If you want to run main.py from src folder, it's not recommended. Always run the program from the root folder, while we don't have a good fix for that.

> **On Windows:** To make .exe file, do:
```
pip install py2exe
cd src
python setup.py py2exe
.\dist\main.exe
```

You will need python 3.8+ with tkinter installed to use this program.

## Screenshots
![image](https://user-images.githubusercontent.com/77564176/166142604-791a81ca-4f4c-47db-b037-b5525c7cf313.png)
![image](https://user-images.githubusercontent.com/77564176/169689858-a131cd42-1d6d-4d2a-976d-7daef4fab5ac.png)
