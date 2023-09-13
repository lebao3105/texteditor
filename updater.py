import configparser
import logging
import packaging.version as version
import requests

GITHUB_LINK = "https://github.com/lebao3105/texteditor"
RAW = "https://raw.githubusercontent.com/lebao3105/texteditor"
RELEASES = GITHUB_LINK + "/releases/tag/"

currver: str
logger = logging.Logger("textworker-updater")
currappbranch: str

_handler = logging.StreamHandler()
_formatter = logging.Formatter('[%(asctime)s] [%(name)s %(levelname)s] %(message)s')
_handler.setFormatter(_formatter)
logger.addHandler(_handler)

def parse_json(inipath: str):
    """
    Try to get and parse version.json from texteditor's data branch.
    If the file is not a valid json, will return "invalid_json" response.
    If the file cannot be reached, will return request.get.status_code.
    """

    r = requests.get(RAW + "/data/version.json")
    if not r.text:
        return r.status_code

    if not r.json(): return "invalid_json"

    parser = configparser.ConfigParser()
    parser.read(inipath, "utf-8")

    try:
        branch = parser["base"]["branch"]
    except KeyError:
        logger.info("No app versioning setting found. Will assume that we'll go stable.")
        branch = "stable"
    finally:
        global currappbranch
        if version.Version(currver) < version.Version ("1.6"): # Tkinter
            currappbranch = "tk"
        else:
            currappbranch = "wx"
    
    try:
        target_branch = r.json()[branch]
    except:
        logging.warning("""Invalid branch name on settings.ini? Or version.json?
                        Whatever the updater must be stopped.
                        """
        )
        return "invalid_json (No such branch %s found in version.json)" % branch
    else:
        if version.Version(branch) < version.Version(target_branch["version"]):
            return target_branch["version"], branch, target_branch["changelog"]
        elif version.Version(branch) == version.Version(target_branch["version"]):
            return # Up to date

# def install(version: str):
#     r = requests.get()