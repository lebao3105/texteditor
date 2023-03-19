import inspect
import packaging.version

__version__ = "1.5.a0"
TEST: bool = False


def require_version(version: str, ctype: str):
    """Requires texteditor version for an object.

    Supported comparison types (ctype):\n
    >=, ==, =<, >, <
    :raises Exception if the app version is not satisfied required version
    :raises ValueError if ctype uses a invalid comparison type
    :returns True if the check succeed
    """

    def raise_err():
        nonlocal caller, currver, reqver
        raise Exception(
            "Object {} is not available for this app version ({}), it requires texteditor {} {}".format(
                caller, __version__, ctype, version
            )
        )

    # print(ctype)
    currver = packaging.version.parse(__version__).base_version
    reqver = packaging.version.parse(version).base_version
    # print(currver, reqver)
    caller = inspect.getmodule(inspect.stack()[1][0]).__name__
    if ctype == ">=" or ">":
        if reqver > currver:
            raise_err()
        else:
            return True
    elif ctype == "==":
        if reqver != currver:
            raise_err()
        else:
            return True
    elif ctype == "=<" or "<":
        if reqver < currver:
            raise_err()
        else:
            return True
    else:
        raise ValueError("Unknown comparison type.")


def is_development_build():
    return packaging.version.parse(__version__).is_devrelease
