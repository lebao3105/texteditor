import glob
import py2exe
from distutils.core import setup
from setuptools import find_packages
import files

setup(
    windows=[{"script": "__main__.py"}],
    options={
        "py2exe": {"optimize": 2, "includes": ["os", "configparser"], "bundle_files": 1}
    },
    data_files=[("icons", glob.glob(r"icons/*.png"))],
    packages=find_packages(),
)
