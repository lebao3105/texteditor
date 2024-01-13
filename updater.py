import configparser
import json
import logging
import multiprocessing
import os
import sys
import packaging.version as version
import requests

GITHUB_LINK = "https://api.github.com/repos/lebao3105/texteditor"
RELEASES = GITHUB_LINK + "/releases/tag/"

currver: str
logger = logging.Logger("textworker-updater")
currappbranch: str

_formatter = logging.Formatter('[%(asctime)s] [%(name)s %(levelname)s] %(message)s')

_fhandler = logging.FileHandler(os.path.expanduser("~/.logs/textworker-updater.log"))
_fhandler.setFormatter(_formatter)

_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)

logger.addHandler(_fhandler)
logger.addHandler(_handler)

def parse_json(inipath: str):
    """
    Try to get and parse version.json from texteditor's data branch.
    If the file is not a valid json, will return "invalid_json" response.
    If the file cannot be reached, will return request.get.status_code.
    """
    logger.info("Starting the updater...")

    parser = configparser.ConfigParser()
    parser.read(inipath, "utf-8")

    # Get the current app type & branch
    branch = os.path.basename(inipath).removesuffix(".ini").removeprefix("configs")
    branch = "latest" + branch # If empty then just 'latest' = stable branch
    branch = branch.replace("_", "-") # For dev branch
    
    global currappbranch, currver
    logger.info("Current app version: %s", currver)

    if version.parse(currver) > version.parse("1.5"): # Tkinter
        currappbranch = "wx"
    else:
        currappbranch = "tk"
        global GITHUB_LINK
        GITHUB_LINK += "-tk" # Separate repo for Tkinter version

    branch += f"-{currappbranch}"
    logger.info("Target branch: %s", branch)
    
    # Get the latest release
    r = requests.get(GITHUB_LINK + "/releases")
    try:
        all = json.loads(r.text) # Output should be a list
    except Exception as e:
        logger.error("Unable to parse update metadata: ", e)
        return "invalid_json"

    # Find the correct release
    for i in range(0, len(all)):
        if not all[i]["draft"]: # No draft release
            latest = all[i]
            # Err...
            if (all[i]["prerelease"] and branch.startswith("latest-dev")): break # Dev
            elif (all[i]["prerelease"] is False and branch == f"latest-{currappbranch}"): break # Stable

    tag = latest["tag_name"].removeprefix("v")
    logger.info("Target app version: %s", tag)

    # Find the file to download
    if len(latest["assets"]) == 0: get = "" # No premade builds available
    else:
        for i in range(0, len(latest["assets"])):
            if latest["assets"][i]["name"].startswith(f"textworker-{tag}-{sys.platform}"):
                get = latest["assets"][i]["browser_download_url"]
                break

    if version.parse(tag) > version.parse(currver):
        return tag, latest["body"], get