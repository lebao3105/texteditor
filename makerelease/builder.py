import os
import shutil
import subprocess
import sys
import miscs

## Options
ALL_ARGS = ["build", "install", "help", "checkreq"]
## Checkreq
CHECKREQ_FLAG = True
CHECKREQ_NOT_IN_FLAG = True  # Don't use checkreq as a argument
FOUND_NREQ = False  # Found not-solved dependency
## Build
BUILD_FLAG = True
MESON_FLAG = False

if sys.platform == "win32":
    pycmd = "python"
else:
    pycmd = "python3"

print(miscs.headertext("texteditor Python package build script"))

# Checking functions
def checkreq():
    global FOUND_NREQ
    print(miscs.boldtext("Checking for requirements..."))
    print(
        miscs.warntext(
            "Version of all requirements are not here now - use latest version for sure."
        )
    )
    print("Use help flag to see all requirements.")

    # Python version
    if sys.version_info.major < 3 or sys.version_info.minor < 8:
        raise Exception("Python 3.8+ is required")

    # Build system
    if BUILD_FLAG is True:
        try:
            import build
        except ImportError:
            print(miscs.failtext("'Build' module not found"))
            FOUND_NREQ = True
    if MESON_FLAG is True:
        if shutil.which("meson") is None:
            print(miscs.failtext("Meson program not found"))
            FOUND_NREQ = True

    if CHECKREQ_NOT_IN_FLAG is True:
        if FOUND_NREQ is True:
            print(
                miscs.boldtext(
                    "Some requirements did not meet the build requirement. Exiting."
                )
            )
            exit(1)
    miscs.oktext("Check requirements task completed.")


def checkflag(arg: str):
    global CHECKREQ_NOT_IN_FLAG
    global MESON_FLAG
    global BUILD_FLAG
    global CHECKREQ_FLAG
    if arg == "--use-meson":
        MESON_FLAG = True
        BUILD_FLAG = False
    if arg == "--no-checkreq":
        CHECKREQ_FLAG = False

    if arg == "help":
        help()
    if arg == "checkreq":
        CHECKREQ_NOT_IN_FLAG = False
        checkreq()
    if arg == "build":
        build_()
    elif arg == "install":
        install_()
    exit()


def help():
    print(miscs.boldtext("All posible arguments:"))
    print("build : Build the program")
    print("install : Install the program")
    print("help : Show this box then exit")
    print("checkreq : Check for build requirements")
    print(miscs.boldtext("Flags:"))
    print("--use-meson : Build/install using meson and ninja")
    print("--no-checkreq : Tell us not to check for requirements")
    print(miscs.boldtext("Build requirements: (use the latest version for sure)"))
    print("Python 3.8 or higher,")
    print("Build systems:")
    print("* meson and ninja - To make a system-wide installation. Texteditor will NOT be found by pip.")
    print("* build : Build wheel files - which are often used for pip releases.")
    print("(You dont need all of them, depend on your need.)")
    print("Dependencies:")
    print("* wxPython : GUI. Visit extras.wxpython.org for wheels (install its dependencies yourself)")
    print("*nothing more*")
    exit()


def build_():
    os.chdir("..")
    print(miscs.boldtext("Starting the build...Check the output below."))
    if BUILD_FLAG is True:
        command = pycmd + " -m build"
        pass
    if MESON_FLAG is True:
        command = "meson build --reconfigure"
        pass
    result = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out = result.stdout.readline()
    err = result.stderr.readline()
    print(out.strip())
    print(miscs.boldtext("Errors if have: "), err.strip())
    result.wait()
    os.chdir("makerelease")
    exit()


def install_():
    os.chdir("..")
    print(miscs.boldtext("Starting the project installation...Check the output below."))
    if BUILD_FLAG is True:
        command = pycmd + " -m pip install dists/*.whl --force-reinstall"
        pass
    if MESON_FLAG is True:
        command = "ninja -C build install"
        pass
    result = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out = result.stdout.readline()
    err = result.stderr.readline()
    print(out.strip())
    print(miscs.boldtext("Errors if have: "), err.strip())
    result.wait()
    os.chdir("makerelease")
    exit()


def main():
    args = sys.argv
    argc = len(args)
    if argc > 0:
        for i in range(1, argc):
            checkflag(args[i])
    elif argc == 0:
        help()


if __name__ == "__main__":
    main()
