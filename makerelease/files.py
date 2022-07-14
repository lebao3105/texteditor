import sys
from os.path import isfile, dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from src.miscs import constants

# These are __init__.py files in the source code.
# Without they we can't import any file(s)
initfiles = [
    "src/pages/__init__.py",
    "src/miscs/__init__.py",
    "src/__init__.py"
]

for i in range(len(initfiles)):
    if not isfile(initfiles[i]):
        raise Exception("File not found: "+initfiles[i])

# Icon
if constants.STATE == "DEV":
	icon = "data/org.lebao3105.texteditor.Devel.png"
else:
	icon = "data/org.lebao3105.texteditor.png"