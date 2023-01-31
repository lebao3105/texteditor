import inspect
import packaging.version

__version__ = "1.4.1"


def require_version(version: str, ctype):
    """Requires texteditor version for an object.

    Supported comparison types (ctype):\n
    >=, ==, =<, >, <
    :raises Exception if the app version is not satisfied required version
    :raises ValueError if ctype uses a invalid comparison type
    """

    def raise_err():
        nonlocal caller, currver, reqver
        raise Exception(
            "Object {} is not available for this app version ({}), it requires texteditor {} {}".format(
                caller, __version__, ctype, version
            )
        )

    currver = packaging.version.parse(__version__)
    reqver = packaging.version.parse(version)
    caller = inspect.getmodule(inspect.stack()[1][0]).__name__
    if ctype == ">=" or ">":
        if reqver > currver:
            raise_err()
    elif ctype == "==":
        if reqver != currver:
            raise_err()
    elif ctype == "=<" or "<":
        if reqver < currver:
            raise_err()
    else:
        raise ValueError("Unknown comparison type.")


def is_development_build():
    return packaging.version.parse(__version__).is_devrelease