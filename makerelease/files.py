import sys
from os.path import isfile, dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from texteditor.miscs import constant

# These are __init__.py files in the source code.
# Without they we can't import any file(s)
initfiles = [
    "pages/__init__.py",
    "miscs/__init__.py",
    "__init__.py"
]

for i in range(len(initfiles)):
    if not isfile(initfiles[i]):
        raise Exception("File not found: "+initfiles[i])

# Icon
if constant.STATE == "DEV":
	icon = "../data/org.lebao3105.texteditor.Devel.png"
else:
	icon = "../data/org.lebao3105.texteditor.png"