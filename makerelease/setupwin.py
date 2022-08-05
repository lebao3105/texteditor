<<<<<<< HEAD
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
			  'includes': ['os', 'configparser']
			}
	}
)
=======
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
			  'includes': ['os', 'configparser']
			}
	}
)
>>>>>>> b35a36977b88c3114d7f544fec4c57ce48b0658f
