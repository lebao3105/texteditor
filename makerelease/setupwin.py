import py2exe
from distutils.core import setup
import files

setup(
	windows = [{
		"script": "main.py",
		"icon_resource": [(1, files.icon)]
	}],
    options = {
		  'py2exe': {
			  'optimize': 2,
			  'includes': ['os.path', 'configparser']
			}
	}
)