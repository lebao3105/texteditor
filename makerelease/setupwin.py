from glob import glob
import py2exe
from distutils.core import setup
from setuptools import find_packages
import files

setup(
	windows = [{
		"script": "__main__.py",
		"icon_resource": [(1, files.icon)]
	}],
    options = {
		  'py2exe': {
			  'optimize': 2,
			  'includes': ['os', 'configparser'],
			  'bundle_files': 1
			}
	},
	data_files=[('icons', glob(r'icons/texteditor.Devel.png'))],
	packages=find_packages()
)