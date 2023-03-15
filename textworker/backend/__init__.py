import inspect
import os
import packaging.version

__version__ = "1.6a2"

def require_version(version: str):
    """
    Requires texteditor version for an object (minium version).
    :raises Exception: If the required version is unavailable for the current app version.
    """
    currver = parse_version(__version__)
    reqver = parse_version(version)
    caller = inspect.getmodule(inspect.stack()[1][0]).__name__

    if not currver >= reqver:
        raise Exception(
            "Object {} is not available for this app version ({}), it requires texteditor >= {}".format(
                caller, __version__, version
            )
        )
    else:
        return True

def require_exact_version(version: str):
    """
    Requires a texteditor version, exactly.
    :raises Exception: If the app version not met the required check.
    """
    currver = parse_version(__version__)
    reqver = parse_version(version)
    caller = inspect.getmodule(inspect.stack()[1][0]).__name__

    if not currver == reqver:
        raise Exception(
            "Object {} is not available for this app version ({}), it requires texteditor >= {}".format(
                caller, __version__, version
            )
        )
    else:
        return True

def require_lower_version(version: str):
    """
    Requires a texteditor version (lower than required).
    :raises Exception: If the app version not met the required check.
    """
    currver = parse_version(__version__)
    reqver = parse_version(version)
    caller = inspect.getmodule(inspect.stack()[1][0]).__name__

    if not currver < reqver:
        raise Exception(
            "Object {} is not available for this app version ({}), it requires texteditor >= {}".format(
                caller, __version__, version
            )
        )
    else:
        return True

def parse_version(version: str):
    return packaging.version.parse(version)

def is_development_build():
    return packaging.version.parse(__version__).is_prerelease

# Config file path, default configs moved to /generic
configpath = os.path.expanduser("~/.config/textworker/configs{}.ini".format("" if not is_development_build() else "_dev"))
