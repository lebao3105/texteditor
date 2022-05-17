from distutils.core import setup
import py2exe
import os

if not os.path.isfile("pages/__init__.py") or not os.path.isfile("miscs/__init__.py") or not os.path.isfile("__init__.py"):
	raise Exception("Needed files not found!")

setup(windows=['main.py'])
