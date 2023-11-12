import configparser
import json
import logging
import sys
import packaging.version as version
import requests

GITHUB_LINK = "https://api.github.com/repos/lebao3105/texteditor"
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

    parser = configparser.ConfigParser()
    parser.read(inipath, "utf-8")

    # Get the current app type & branch
    try:
        branch = parser["base"]["branch"]
    except KeyError:
        logger.info("No app versioning setting found. Will go stable.")
        branch = "latest"
    finally:
        global currappbranch, currver
        if version.parse(currver) < version.parse("1.6"): # Tkinter
            currappbranch = "tk"
        else:
            currappbranch = "wx"
        branch += f"-{currappbranch}"
    
    # Get the latest release
    r = requests.get(GITHUB_LINK + "/releases")
    all = json.loads(r.text)

    latest = all[0]
    tag = latest["tag_name"].removeprefix("v")

    # TODO
    for i in range(latest["assets"]):
        if latest["assets"][i]["name"].startswith(f"textworker-{latest}-{sys.platform}"):
            get = latest["assets"][i]["browser_download_url"]

    if version.parse(tag) > version.parse(currver):
        return tag, latest["body"], get


# def install(version: str):
#     r = requests.get()