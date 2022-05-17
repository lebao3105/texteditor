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
```

If you see error ```/bin/bash^M: bad interpreter: No such file or directory``` (usually heppends in bash shell), do:
```
for i in $(ls -d po/*/); do
    msgfmt ${i%%/}/LC_MESSAGES/base -o ${i%%/}/LC_MESSAGES/base.mo
done
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