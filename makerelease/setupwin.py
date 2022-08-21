import py2exe
from setuptools import setup, find_packages
import files

setup(
	windows = [{
		"script": "__main__.py",
		"icon_resource": [(1, files.icon)]
	}],
    options = {
		  'py2exe': {
			  'optimize': 2,
			  'includes': ['os', 'configparser']
			}
	},
	packages=find_packages()
)
