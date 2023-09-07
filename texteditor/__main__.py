import getopt
import os
import sys
import typing

commands: dict[str, list[typing.Callable, str]] = {}

def register_command(cmd: typing.Callable, help: str):
    global commands
    commands[cmd.__code__.co_name] = [cmd, help]

def help():
    print("All available options:")
    for command in commands:
        print(f"--{command}\t\t{commands[command][1]}")
    exit(0)
    

def version():
    from texteditor import __version__
    print(__version__)
    exit(0)

def editorcfg(path_: str):
    if not os.path.isdir(path_): raise NotADirectoryError(path_)
    import libtextworker
    libtextworker.EDITOR_DIR = path_

def themesdir(path_: str):
    if not os.path.isdir(path_): raise NotADirectoryError(path_)
    import libtextworker
    libtextworker.THEMES_DIR = path_

def libtewdir(path_: str):
    if not os.path.isdir(path_): raise NotADirectoryError(path_)
    sys.path.insert(0, path_)
    try:
        import libtextworker
    except ImportError as e: raise e
    else:
        if not libtextworker.__path__  == path_ + "/libtextworker" : raise ImportError("Can't find libtextworker in the specified path", path=path_)

def appdatadir(path_: str):
    if not os.path.isdir(path_): raise NotADirectoryError(path_)
    from texteditor.extensions import generic
    generic.DATA_PATH = path_

register_command(editorcfg, "Custom editor settings folder path (should be placed after --libtewdir if used)")
register_command(themesdir, "Custom application themes folder path (should be placed after --libtewdir if used)")
register_command(libtewdir, "Custom libtextworker path (usually used for testers) - can use PYTHONPATH instead")
register_command(appdatadir, "Custom textworker Git-cloned data branch path (for testers)")
register_command(help, "Show this help and exit")
register_command(version, "Show the app version")

def invalid_option(): help(); exit(-1)

def getoptions():
    opts = [
        "editorcfg=",
        "themesdir=",
        "help",
        "version",
        "libtewdir=",
        "appdatadir="
    ]

    options, args = getopt.getopt(
        sys.argv[1:],
        "",
        opts
    )
    for option, follow in options:
        for it in opts:
            if option == f'--{it.removesuffix("=")}':
                target = commands.get(option.removeprefix("--"))[0]
                if target.__code__.co_argcount == 0:
                    target()
                else:
                    target(follow)
    
    return args

def main():
    files = getoptions()
    from .extensions import generic
    generic.ready()
    from . import main
    main.start_app(files)

if __name__ == "__main__":
    sys.exit(main())