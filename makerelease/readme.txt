## This folder contains scripts to build executable files (.exe and .AppImage).

To make exe file on Windows, copy setupwin.py and files.py to ..\texteditor, "cd" to it, then:
- pip install py2exe
- py setupwin.py py2exe
When done, run dist\main.exe.

Make AppImage on Linux: Just run makeappimage.sh - output will be in this directory.
Parameters:
- build : Build AppImage
- clean : Clean outputs