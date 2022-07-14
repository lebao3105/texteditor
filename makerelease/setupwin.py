import py2exe
from setuptools import setup # test
import files

setup(
	windows = [{
		"script": "src/main.py",
		"icon_resource": [(1, files.icon)]
	}],
    options = {
		  'py2exe': {
			  'optimize': 2
			}
	}
)