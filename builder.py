import argparse
import os
import glob
import shutil
import sys

from textworker import __version__

print("Textworker version: ", __version__)
parser = argparse.ArgumentParser(
    description="Help setting up textworker easier",
    usage="'install' for install the project, 'build' to build, 'maketrans' to create translations (gettext required).\nThat's all.",
)
parser.add_argument(
    "--install-req",
    "-r",
    const="False",
    nargs="?",
    choices=["True", "False"],
    help="Install requirements",
)
parser.add_argument(
    "action", nargs="*", help="Action to run (install, build, maketrans)"
)

opts = parser.parse_args()
if opts.install_req:
    os.system('"{}" -m pip install -r requirements.txt'.format(sys.executable))


def make_trans():
    msgfmt = shutil.which("msgfmt")
    gettext = shutil.which("xgettext")
    msgmerge = shutil.which("msgmerge")
    wxrc = shutil.which("wxrc")

    print("Going to use the following tools:")
    print(f"* xgettext : {gettext}")
    print(f"* msgmerge {msgmerge}")
    print(f"* msgfmt {msgfmt}")
    print(f"* wxrc {wxrc}")
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

    # Pyinstaller should handle this
    # (by my passed parameter)
    # if os.path.isdir("textworker/po"):
    #    shutil.rmtree("textworker/po")
    # shutil.copytree("po", "textworker/po")

    print("---------------------------------------")


def install():
    make_trans()
    return os.system(f'"{sys.executable}" -m pip install -e .')


def build():
    make_trans()
    os.system(f'"{sys.executable}" -m pip install poetry')
    return os.system(f'"{sys.executable}" -m poetry build')

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


if "maketrans" in opts.action:
    make_trans()
elif "build" in opts.action:
    build()
elif "install" in opts.action:
    install()
elif "clean" in opts.action:
    clean()
else:
    parser.error("No (valid) argument provided")
