import os
import shutil
import subprocess
import sys
import miscs

# Options
ALL_ARGS = ["build", "install", "help", "checkreq"]
## Checkreq
CHECKREQ_FLAG = True
CHECKREQ_NOT_IN_FLAG = True  # Don't use checkreq as a argument
FOUND_NREQ = False  # Found not-solved dependency
## Build
BUILD_FLAG = True
MESON_FLAG = False

pycmd = sys.executable

print(miscs.headertext("texteditor Python package build script"))

# Checking functions
def checkreq():
    global FOUND_NREQ
    global CHECKREQ_NOT_IN_FLAG

    print(miscs.boldtext("Checking for requirements..."))
    print(
        miscs.warntext(
            "Version of all requirements are not here now - use latest version for sure."
        )
    )
    print("Use help flag to see all requirements.")

    # Python version
    if sys.version_info.major < 3 or sys.version_info.minor < 8:
        print(miscs.failtext("Python version 3.8 or higher is required."))
        exit(1)

    # Build system
    if BUILD_FLAG is True:
        try:
            import build
        except ImportError:
            print(miscs.failtext("'Build' module not found"))
            FOUND_NREQ = True
        else:
            del build

    if MESON_FLAG is True:

        if shutil.which("meson") is None:
            print(miscs.failtext("Meson program not found"))
        try:
            import mesonbuild
        except ImportError:
            print(miscs.failtext("'Meson' module not found"))
            FOUND_NREQ = True
        else:
            del mesonbuild

    if CHECKREQ_NOT_IN_FLAG is True:
        if FOUND_NREQ is True:
            print(
                miscs.boldtext(
                    "Some requirements did not meet the build requirement. Exiting."
                )
            )
            exit(1)
        else:
            build_()


def checkflag(arg: str):
    global MESON_FLAG
    global BUILD_FLAG
    global CHECKREQ_FLAG
    global CHECKREQ_NOT_IN_FLAG

    if arg == "--use-meson":
        MESON_FLAG = True
        BUILD_FLAG = False
    if arg == "--no-checkreq":
        CHECKREQ_FLAG = False

    if arg == "--help" or "help":
        help()
    if arg == "checkreq":
        CHECKREQ_NOT_IN_FLAG = False
        checkreq()
    if arg == "build":
        build_(noexit=False)
    elif arg == "install":
        install_()


def help():
    print(miscs.boldtext("All posible arguments:"))
    print("build : Build the program")
    print("install : Install the program")
    print("help : Show this box then exit")
    print("checkreq : Check for build requirements")
    print(miscs.boldtext("Flags:"))
    print("--use-meson : Build/install using meson and ninja")
    print("--no-checkreq : Tell us not to check for requirements")
    print(miscs.boldtext("Build requirements: (use the latest version for be sure)"))
    print("python version 3.8+")
    print("meson (and ninja) : Installable via pip")
    print(
        "build : Install it via pip - you don't need both build and meson are installed together."
    )
    print("gettext (optional) : To generate translations")
    print("tkinter : GUI Framework")
    print("darkdetect, packaging, pygubu, configparser, sv_ttk : Install via pip")
    exit()


def build_(noexit: bool = True):
    os.chdir("..")
    clean_()
    print(miscs.boldtext("Starting the build...Check the output below."))
    if BUILD_FLAG is True:
        command = pycmd + " -m build"
        pass
    if MESON_FLAG is True:
        command = "meson build --reconfigure"
        pass
    run_command(command)
    os.chdir("makerelease")
    if noexit == False:
        exit()


def install_():
    build_()
    os.chdir("..")
    print(miscs.boldtext("Starting the project installation...Check the output below."))
    if BUILD_FLAG is True:
        import re

        dir = "dist"
        regex = re.compile("(.*whl$)")
        for root, dirs, files in os.walk(dir):
            for file in files:
                print(file)
                if regex.match(file):
                    pass
                else:
                    print(
                        miscs.failtext(
                            "Unable to find required files for the installation."
                        )
                    )
                    print(miscs.failtext("Exiting..."))
                    exit(1)
        command = pycmd + " -m pip install {}/{} --force-reinstall".format(dir, file)
        pass
    if MESON_FLAG is True:
        command = "ninja -C build install"
        pass
    run_command(command)
    os.chdir("makerelease")
    exit()


def clean_():
    try:
        os.rmdir("build")
        os.rmdir("dist")
    except:
        return


def run_command(command: str):
    result = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    out, err = result.communicate()
    print(out)
    print(miscs.boldtext("Errors if have: "), err)
    result.wait()


def main():
    args = sys.argv[1:]
    argc = len(args)

    argtouse = [
        "--use-meson",
        "--no-checkreq",
        "--help",
        "help",
        "checkreq",
        "build",
        "install",
    ]
    argused = args
    cbargs = []
    cbargs += argtouse, argused

    if argc > 0:
        seen = set([x for x in cbargs if cbargs.count(x) > 1])
        for item in seen:
            checkflag(item)


if __name__ == "__main__":
    main()
