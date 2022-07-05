from distutils.core import setup
import py2exe
import os
import miscs.constants

if not os.path.isfile("pages/__init__.py") or not os.path.isfile("miscs/__init__.py") or not os.path.isfile("__init__.py"):
	raise Exception("Needed files not found!")

if miscs.constants.APPSTATE == "STABLE":
	icon = '../data/org.lebao3105.texteditor.png'
else:
	icon = '../data/org.lebao3105.texteditor.Devel.png'

setup(windows = [{
		"script" : 'main.py',
		"icon_resources": [(1, icon)]
	}],
    options = { 'py2exe': { 'optimize': 2 } }
)
