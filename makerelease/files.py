import sys
from os.path import isfile, dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))
from texteditor.miscs import constants

# These are __init__.py files in the source code.
# Without they we can't import any file(s)
initfiles = ["extensions/__init__.py", "miscs/__init__.py", "__init__.py"]

for i in range(len(initfiles)):
    if not isfile(initfiles[i]):
        raise Exception("File not found: " + initfiles[i])

# Icon
if constants.STATE == "DEV":
    icon = "icons/texteditor.Devel.png"
elif constants.STATE == "STABLE":
    icon = "icons/texteditor.png"
else:
    print("Warning: Wrong application branch (STABLE/DEV) in miscs.constants module")
    icon = None
