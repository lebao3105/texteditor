from os.path import isfile

# These are __init__.py files in the source code.
# Without they we can't import any file(s)
initfiles = [
    "extensions/__init__.py",
    "backend/__init__.py",
    "views/__init__.py",
    "__init__.py",
]

for i in range(len(initfiles)):
    if not isfile("../texteditor/" + initfiles[i]):
        raise Exception("File not found: " + "../texteditor/" + initfiles[i])


class bcolors:
    HEADER = "\033[95m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def headertext(text: str):
    return bcolors.HEADER + text


def oktext(text: str):
    return bcolors.OKGREEN + text


def warntext(text: str):
    return bcolors.WARNING + text


def failtext(text: str):
    return bcolors.FAIL + text


def boldtext(text: str):
    return bcolors.BOLD + text


def utext(text: str):
    return bcolors.UNDERLINE + text
