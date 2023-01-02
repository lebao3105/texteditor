import glob
from distutils.core import setup
from setuptools import find_packages
import miscs
import sys

if sys.platform != "win32":
    raise Exception("Please use this file on Windows.")

try:
    import py2exe
except ImportError:
    import os
    print("Py2exe not found, installing it from pip...")
    os.system("pip install py2exe")

setup(
    windows=[{"script": "__main__.py"}],
    options={
        "py2exe": {
            "optimize": 2,
            "includes": [
                "os",
                "pathlib",
                "wxpython",
            ],
            "bundle_files": 1,
        }
    },
    data_files=[("icons", glob.glob(r"icons/*.png"))],
    packages=find_packages(),
)
