from glob import glob
from wx.tools import img2py
import getopt
import os
import sys

__doc__ = "embedimgs [action] [value]\n" \
          "Embed generated PNG images into specific textworker parts.\n" \
          "[action]:\n" \
          "-d = Set application universal data path (data branch on Git repository) for splash screens and app icons\n" \
          "-h = Show this message\n" \
          "-t = Target (icons/assets/splash)" \
          "-a = Same as -d (but not that universal as this is used only on wx version) but for app assets"

dataPath = os.path.dirname(__file__) + "/textworker/data/"
assetsPath = os.path.dirname(__file__) + "/data/"

def remove_if_exists(path: str):
    if os.path.exists(path): os.remove(path)

def append_import_first(path: str):
    with open(path, "x") as f:
        f.write("from wx.lib.embeddedimage import PyEmbeddedImage\n\n")

def update_icons():
    remove_if_exists("textworker/icons.py")
    iconsPath = dataPath + "icons/"
    append_import_first("textworker/icons.py")
    for img in glob(pathname="*.png", root_dir=iconsPath):
        img2py.img2py(iconsPath + img, "textworker/icon.py", True,
                      imgName=img.removesuffix(".png"))

def update_assets():
    remove_if_exists("textworker/assets.py")
    append_import_first("textworker/assets.py")
    for asset in glob(pathname="*.png", root_dir=assetsPath):
        img2py.img2py(assetsPath + asset, "textworker/assets.py", True,
                      imgName=asset.removesuffix(".png"))

def update_splash():
    remove_if_exists("textworker/splash.py")
    append_import_first("textworker/splash.py")
    splashPath = dataPath + "splash/"
    for splash in glob(pathname="*.png", root_dir=splashPath):
        img2py.img2py(splashPath + splash, "textworker/splash.py", True,
                      imgName=splash.removesuffix(".png"))

if __name__ == '__main__':
    try:
        opts, fileArgs = getopt.getopt(sys.argv[1:], "d:a:t:h")
    except getopt.GetoptError as e:
        print(__doc__)
        raise e
    
    for opt, val in opts:
        match opt:
            case "-h": print(__doc__); exit(0)
            case "-d": dataPath = val
            case "-a": assetsPath = val
            case "-t":
                match val:
                    case "icons": update_icons()
                    case "assets": update_assets()
                    case "splash": update_splash()
                    case _: raise Exception("Unknown target: must be icons/assets/splash")
                exit(0)