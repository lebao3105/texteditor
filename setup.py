from distutils.core import setup
import py2exe

setup(console=['src/main.py'],
	options={
	        "py2exe":{
	            "optimize": 2,
	            "includes": [
	                "src/pages/__init__.py", "src/pages/about.py", "src/pages/helpme.py",
	                "src/miscs/__init__.py", "src/miscs/init.py", "src/miscs/get_config.py",
	                "src/miscs/constants.py", "src/miscs/file_operations.py"
	            ]
	        }
	})
