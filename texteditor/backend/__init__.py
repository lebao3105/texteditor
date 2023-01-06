import inspect

__version__ = "1.6.0alpha"


def get_version():
    """
    Returns the app version with branch.\n
    Branches are 'alpha', 'dev', 'beta', 'rc' (not used)\n
    Version will be released as a float number with format
        major.minor.patch
    """
    if not __version__:
        print(
            "Attribute __version__ not found! Are you running an old texteditor version?"
        )
        return
    else:
        for branch in ["alpha", "dev", "beta", "rc"]:
            for i in range(0, 9):
                suffix = ".{}{}".format(str(i), branch)
                if __version__.endswith(suffix):
                    return float(__version__.removesuffix(suffix)), i, branch
                else:
                    return float(__version__), "unknown", "unknown"


def require_version(version: float, branch):
    """
    Requires texteditor version for an object.
    (required version >= app version)
    :param version : Required app version
    :param patch : App patch
    :param branch : Required app branch ('alpha', 'dev', 'beta', 'rc')
    (note: comparison between branches is not completed yet. If you don't
    need to use any branch above, simply pass branch to ''.)
    """
    version_ = get_version()[0]
    branch_ = get_version()[2]
    caller = inspect.getmodule(inspect.stack()[1][0]).__name__
    err_msg = """\
    The following object {} requires texteditor version \
    {} but it cannot, because this is texteditor {}.
    """.format(
        caller, "".join([str(version), branch]), __version__
    )
    if branch != branch_ and branch_ != "unknown":
        print(err_msg)
    if version_ < float(version):
        print(err_msg)
    return
