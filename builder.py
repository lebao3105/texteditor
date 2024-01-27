import argparse
import os
import glob
import shutil
import sys

from textworker import __version__

print("Textworker version", __version__)
parser = argparse.ArgumentParser(
    description = "Help setting up textworker easier",
    usage = "'install' to install the project, 'build' to build, "
            "'maketrans' to create translations (gettext required), "
            "'genicons' to generate app icons.")

parser.add_argument(
    "action", nargs="*", help="Action to run"
)

opts = parser.parse_args()

def make_trans():
    msgfmt = shutil.which("msgfmt")
    gettext = shutil.which("xgettext")
    msgmerge = shutil.which("msgmerge")
    wxrc = shutil.which("pywxrc")

    print("Going to use the following tools:")
    print(f"* xgettext : {gettext}")
    print(f"* msgmerge {msgmerge}")
    print(f"* msgfmt {msgfmt}")
    print(f"* pywxrc {wxrc}")
    print("---------------------------------------")

    for line in open("po/WXRCFILES", "r").read().split("\n"):
        source = line.split(" ")[0]
        out = line.split(" ")[1]
        os.system(
            f'"{wxrc}" {source} -g -o {out}'
        )
    
    os.system(
        f'"{gettext}"'
        + ' --copyright-holder="Le Bao Nguyen <bao12345yocoo@gmail.com>"'
        + f" --package-version={__version__}"
        + " -C --language=python"
        + " -f po/POTFILES"
        " -d textworker -o po/textworker.pot"
    )
    
    for line in open("po/LINGUAS", "r").read().split():
        target = f"po/{line}.po"
        os.system(
            '"{}"'.format(msgmerge)
            + " {} po/textworker.pot".format(target)
            + " -o {}".format(target)
        )
        os.mkdir("po/{}".format(line))
        os.mkdir("po/{}/LC_MESSAGES".format(line))
        os.system(
            '"{}"'.format(msgfmt)
            + " -D po "
            + target.removeprefix("po/")
            + " -o po/{}/LC_MESSAGES/{}.mo".format(line, line)
        )

    print("---------------------------------------")


def install():
    make_trans()
    makeicons()
    return os.system(f'"{sys.executable}" -m pip install -e .')


def build():
    make_trans()
    makeicons()
    os.system(f'"{sys.executable}" -m pip install poetry')
    return os.system(f'"{sys.executable}" -m poetry build')

def makeicons():
    img2py = shutil.which("img2py")
    if os.path.isfile("textworker/icon.py"): os.remove("textworker/icon.py")
    os.system(f"{img2py} -n dev textworker/data/icons/me.lebao3105.textworker.Devel.svg textworker/icon.py")
    os.system(f"{img2py} -a -n stable textworker/data/icons/me.lebao3105.textworker.svg textworker/icon.py")

def clean():
    try:
        # po directory
        dirs = glob.glob("po/*/LC_MESSAGES")
        for path in dirs:
            shutil.rmtree(path)
        for line in open("po/LINGUAS", "r").read().split():
            shutil.rmtree("po/{}".format(line))
        # textworker
        # shutil.rmtree("textworker/po")
        # py build outputs
        for path in glob.glob("*.egg-info"):
            shutil.rmtree(path)
        shutil.rmtree("dist")
    except FileNotFoundError:
        pass

clean()
if "maketrans" in opts.action:
    make_trans()
elif "build" in opts.action:
    build()
elif "install" in opts.action:
    install()
elif "genicons" in opts.action:
    makeicons()
else:
    parser.error("No (valid) argument provided")
