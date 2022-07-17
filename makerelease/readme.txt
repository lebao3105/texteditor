## This folder contains scripts to build executable files (.exe and .AppImage).

Make .exe on Windows:
- pip install py2exe
- py setupwin.py py2exe
When done, run dist\main.exe.

Make AppImage on Linux: Just run makeappimage.sh - output will be in this directory.
Parameters:
- build : Build AppImage
- clean : Clean outputs